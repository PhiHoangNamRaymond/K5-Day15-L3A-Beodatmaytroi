import { useMemo, useState } from "react";
import { Icon } from "./Icon";
import { shortDate } from "../features/schedule/types";
import type { Changes, Issue, Review, Session } from "../features/schedule/types";

interface Props {
  week: string;
  review?: Review;
  proposal: Changes;
  pending: boolean;
  busy: boolean;
  onOpen: (id: string) => void;
}

type Tone = "ready" | "attention" | "online" | "proposal" | "pending";

interface Block {
  key: string;
  rows: Session[];
  date: string;
  start: number;
  end: number;
  tone: Tone;
  issues: Issue[];
  column: number;
  columns: number;
}

const HOUR = 60; // px per hour
const DAY_NAMES = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"];
const TONE_LABEL: Record<Tone, string> = {
  ready: "Đủ căn cứ",
  attention: "Cần xác minh",
  online: "Online",
  proposal: "Có đề xuất",
  pending: "Chờ rà lại",
};

function minutes(value: string) {
  const [h, m] = value.split(":").map(Number);
  return h * 60 + (m || 0);
}

function addDays(iso: string, days: number) {
  const date = new Date(iso + "T00:00:00");
  date.setDate(date.getDate() + days);
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
}

function rooms(rows: Session[]) {
  return [...new Set(rows.flatMap((row) => row.room.split(/[,;]\s*/)).filter(Boolean))];
}

/** Group parallel-room records of one session, colour by status, and lay out overlaps side by side. */
function buildBlocks(review: Review | undefined, proposal: Changes, pending: boolean): Block[] {
  const groups = new Map<string, Session[]>();
  for (const row of review?.rows ?? []) {
    const list = groups.get(row.group_id) ?? [];
    list.push(row);
    groups.set(row.group_id, list);
  }
  const blocks: Block[] = [...groups.entries()].map(([key, rows]) => {
    const ids = new Set(rows.map((row) => row.id));
    const issues = (review?.issues ?? []).filter((issue) => issue.sessions.some((id) => ids.has(id)));
    const tone: Tone = pending ? "pending"
      : rows.some((row) => proposal[row.id]) ? "proposal"
      : issues.length ? "attention"
      : rows[0].format === "online" ? "online" : "ready";
    return { key, rows, date: rows[0].date, start: minutes(rows[0].start), end: minutes(rows[0].end), tone, issues, column: 0, columns: 1 };
  });
  const byDay = new Map<string, Block[]>();
  for (const block of blocks) byDay.set(block.date, [...(byDay.get(block.date) ?? []), block]);
  for (const list of byDay.values()) {
    list.sort((a, b) => a.start - b.start || b.end - a.end);
    let cluster: Block[] = [];
    let clusterEnd = -1;
    const flush = () => {
      const width = Math.max(1, ...cluster.map((block) => block.column + 1));
      cluster.forEach((block) => { block.columns = width; });
      cluster = [];
    };
    for (const block of list) {
      if (block.start >= clusterEnd) { flush(); clusterEnd = -1; }
      const used = new Set(cluster.filter((other) => other.end > block.start).map((other) => other.column));
      let column = 0;
      while (used.has(column)) column += 1;
      block.column = column;
      cluster.push(block);
      clusterEnd = Math.max(clusterEnd, block.end);
    }
    flush();
  }
  return blocks;
}

export function WeekCalendar({ week, review, proposal, pending, busy, onOpen }: Props) {
  const [selected, setSelected] = useState<string>();
  const blocks = useMemo(() => buildBlocks(review, proposal, pending), [review, proposal, pending]);
  const days = useMemo(() => Array.from({ length: 7 }, (_, index) => addDays(week, index)), [week]);
  const first = Math.min(8 * 60, ...blocks.map((block) => block.start));
  const last = Math.max(18 * 60, ...blocks.map((block) => block.end));
  const startHour = Math.floor(first / 60);
  const endHour = Math.ceil(last / 60);
  const hours = Array.from({ length: endHour - startHour }, (_, index) => startHour + index);
  const active = blocks.find((block) => block.key === selected);
  const counts = blocks.reduce<Record<Tone, number>>((acc, block) => ({ ...acc, [block.tone]: acc[block.tone] + 1 }),
    { ready: 0, attention: 0, online: 0, proposal: 0, pending: 0 });

  return <section className="calendar-card" aria-labelledby="calendar-heading">
    <div className="calendar-head">
      <div>
        <h2 id="calendar-heading">Tuần {shortDate(week)} – {shortDate(addDays(week, 6))}</h2>
        <p>{blocks.length} buổi học · bấm vào một buổi để xem nguồn và cảnh báo</p>
      </div>
      <ul className="calendar-legend" aria-label="Chú thích màu">
        {(Object.keys(TONE_LABEL) as Tone[]).filter((tone) => counts[tone]).map((tone) =>
          <li key={tone}><span className={"legend-dot tone-" + tone} />{TONE_LABEL[tone]} <b>{counts[tone]}</b></li>)}
      </ul>
    </div>
    <div className={active ? "calendar-body with-detail" : "calendar-body"}>
      <div className="calendar-scroll" tabIndex={0} aria-label="Lưới lịch tuần">
        <div className="calendar-grid" style={{ ["--hours" as string]: hours.length, ["--hour" as string]: HOUR + "px" }}>
          <div className="cal-corner" />
          {days.map((day, index) => <div key={day} className={"cal-day-head" + (index >= 5 ? " weekend" : "")}>
            <span>{DAY_NAMES[index]}</span><strong>{day.slice(8, 10)}/{day.slice(5, 7)}</strong>
          </div>)}
          <div className="cal-times">{hours.map((hour) => <span key={hour} style={{ top: (hour - startHour) * HOUR }}>{String(hour).padStart(2, "0")}:00</span>)}</div>
          {days.map((day, index) => <div key={day} className={"cal-day" + (index >= 5 ? " weekend" : "")}>
            {blocks.filter((block) => block.date === day).map((block) => {
              const row = block.rows[0];
              const roomList = rooms(block.rows);
              return <button key={block.key} type="button" disabled={busy}
                className={"cal-event tone-" + block.tone + (block.columns >= 3 ? " compact" : "") + (selected === block.key ? " selected" : "")}
                aria-pressed={selected === block.key}
                title={`${row.class_name} ${row.session} · ${row.start}–${row.end} · ${row.format === "online" ? "Online" : roomList.join(", ") || "Chưa có phòng"} · ${TONE_LABEL[block.tone]}`}
                aria-label={`${row.class_name} ${row.session}, ${row.start}–${row.end}, ${TONE_LABEL[block.tone]}`}
                style={{
                  top: ((block.start - startHour * 60) / 60) * HOUR + 2,
                  height: Math.max(((block.end - block.start) / 60) * HOUR - 4, 28),
                  // Cascade like common calendars: later columns overlap earlier ones instead of shrinking to slivers.
                  left: `calc(${(block.column / block.columns) * 100}% + 3px)`,
                  width: `calc(${Math.min(100 / block.columns * (block.columns > 1 ? 1.7 : 1), 100 - (block.column / block.columns) * 100)}% - 6px)`,
                  zIndex: block.column + 1,
                }}
                onClick={() => setSelected(selected === block.key ? undefined : block.key)}>
                <span className="ev-time">{row.start}–{row.end}</span>
                <span className="ev-title"><b>{row.class_name}</b> <span>{row.session}</span></span>
                <span className="ev-meta">{row.format === "online" ? "Online" : roomList.length > 1 ? roomList.length + " phòng" : roomList[0] || "Chưa có phòng"}</span>
                {block.issues.length > 0 && !pending && <span className="ev-flag" aria-hidden="true">{block.issues.length}</span>}
              </button>;
            })}
          </div>)}
        </div>
      </div>
      {active && <aside className="calendar-detail" aria-label="Chi tiết buổi học">
        <div className="detail-top">
          <span className={"detail-tone tone-" + active.tone}>{TONE_LABEL[active.tone]}</span>
          <button type="button" className="quiet detail-close" aria-label="Đóng chi tiết" onClick={() => setSelected(undefined)}>×</button>
        </div>
        <h3>{active.rows[0].class_name} · {active.rows[0].session}</h3>
        <p className="detail-topic">{active.rows[0].topic}</p>
        <dl>
          <dt><Icon name="clock" />Thời gian</dt><dd>{shortDate(active.date)} · {active.rows[0].start}–{active.rows[0].end}</dd>
          <dt><Icon name="building" />Phòng</dt><dd>{active.rows[0].format === "online" ? "Online" : rooms(active.rows).join(", ") || "Chưa có phòng"}{active.rows[0].room_status === "pending" && <em> · chờ xác nhận</em>}</dd>
          <dt><Icon name="document" />Giảng viên</dt><dd>{[...new Set(active.rows.map((row) => row.teacher).filter(Boolean))].join(", ") || "Chưa chọn"}</dd>
          <dt><Icon name="check" />Lab coach</dt><dd>{[...new Set(active.rows.flatMap((row) => row.coach))].join(", ") || "Chưa phân"}{active.rows[0].key_coaches.length > 0 && <small>Key coach: {active.rows[0].key_coaches.join(", ")}</small>}</dd>
        </dl>
        {!pending && active.issues.length > 0 && <div className="detail-issues">
          <strong><Icon name="alert" />{active.issues.length} điểm cần xử lý</strong>
          <ul>{active.issues.slice(0, 5).map((issue, index) => <li key={index}>{issue.message}</li>)}</ul>
        </div>}
        <details className="source"><summary>Nguồn ({active.rows.reduce((sum, row) => sum + row.sources.length, 0)})</summary>
          <ul>{active.rows.flatMap((row) => row.sources).map((source, index) => <li key={source.ref + index}><strong>{source.kind}</strong><br />{source.ref}</li>)}</ul>
        </details>
        <button type="button" className="primary" disabled={busy} onClick={() => onOpen(active.rows[0].id)}>Chỉnh sửa buổi này</button>
      </aside>}
    </div>
    {!blocks.length && <div className="empty-state"><Icon name="calendar" /><strong>{busy ? "Đang tải lịch giảng dạy…" : "Chưa có buổi học"}</strong></div>}
  </section>;
}
