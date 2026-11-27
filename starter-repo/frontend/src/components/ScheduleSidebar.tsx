import { shortDate } from "../features/schedule/types";
import type { Review } from "../features/schedule/types";
import { useState } from "react";

interface Props {
  view: "changes" | "review";
  review?: Review;
  update: string;
  busy: boolean;
  pending: boolean;
  approved: boolean;
  onUpdate: (id: string) => void;
  onCopy: () => void;
  onSource: (id: string) => void;
}

export function ScheduleSidebar({ view, review, update, busy, pending, approved, onUpdate, onCopy, onSource }: Props) {
  const [expanded, setExpanded] = useState(false);
  const impact = review?.impact;
  const issues = review?.issues ?? [];
  const visibleIssues = expanded ? issues : issues.slice(0, 3);
  const sourceRows = new Map(review?.rows.map((row) => [row.id, row]));
  if (view === "changes") return <section className="panel" aria-labelledby="update-heading">
      <div className="panel-title"><h2 id="update-heading">Cập nhật phòng</h2></div>
      <div className="issues">
        <label className="field"><span className="sr-only">Nguồn cập nhật</span>
          <select id="update" value={update} disabled={busy || !review?.updates.length}
            onChange={(event) => onUpdate(event.target.value)}>
            <option value="">Chọn sự kiện đổi phòng</option>
            {review?.updates.map((item) => <option key={item.id} value={item.id}>{item.label}</option>)}
          </select>
        </label>
        {!impact && !pending && <p>Chọn một sự kiện để xem buổi bị ảnh hưởng và nháp gửi BTC.</p>}
        {impact && !pending && <div id="impact">
          <strong>{impact.old_room ? impact.class_name + " · " + impact.session : "Chưa xác định lớp cần báo lại"}</strong>
          <p>{shortDate(impact.date)} · {impact.start}–{impact.end}</p>
          <p>{impact.old_room ? impact.old_room + " → " + (impact.room || "Chờ phòng thay thế") :
            "Cần bản lịch đã thông báo để đối chiếu."}</p>
          <small>Nguồn {impact.source}</small>
          {impact.old_room && <button className="quiet" onClick={() => onSource(impact.session)}>Mở buổi trong lịch</button>}
        </div>}
        <div id="notice" hidden={!review?.notice || pending}>
          <h3>Nháp thông báo cho BTC</h3>
          <pre id="notice-text">{pending ? "" : review?.notice}</pre>
          <button id="copy" className="secondary" disabled={busy || pending} onClick={onCopy}>Sao chép nháp</button>
        </div>
      </div>
    </section>;
  return <section className="panel" aria-labelledby="alerts-heading">
      <div className="panel-title"><h2 id="alerts-heading">Cảnh báo</h2>
        <span id="issue-count">{!pending && review ? issues.length + " lỗi chặn" : ""}</span></div>
      <div id="issues" className="issues">
        {pending ? <p>Đang chờ kiểm tra bản nháp.</p> :
          issues.length ? visibleIssues.map((issue) => (
            <article key={issue.field + issue.sessions.join("-") + issue.message} className="issue">
              <p>{issue.message}</p>
              {issue.sessions.map((id) => {
                const row = sourceRows.get(id);
                return <button key={id} className="source-link" onClick={() => onSource(id)}>
                  {row ? row.class_name + " · " + id + " · " + row.start + "–" + row.end : id}
                </button>;
              })}
            </article>
          )) : <p>{approved ? "Bản bàn giao đã duyệt." : "Có thể duyệt bản bàn giao."}</p>}
        {!pending && issues.length > 3 && <button className="quiet more-issues" aria-expanded={expanded}
          onClick={() => setExpanded(!expanded)}>
          {expanded ? "Thu gọn cảnh báo" : "Xem thêm " + (issues.length - 3) + " cảnh báo"}
        </button>}
      </div>
    </section>;
}
