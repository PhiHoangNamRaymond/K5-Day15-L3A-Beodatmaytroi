import { shortDate } from "../features/schedule/types";
import type { Review } from "../features/schedule/types";

interface Props {
  review?: Review;
  update: string;
  busy: boolean;
  pending: boolean;
  approved: boolean;
  onUpdate: (id: string) => void;
  onCopy: () => void;
}

function openSource(id: string) {
  const details = document.querySelector<HTMLDetailsElement>("#row-" + id + " details");
  if (!details) return;
  details.open = true;
  details.querySelector("summary")?.focus({ preventScroll: true });
}

export function ScheduleSidebar({ review, update, busy, pending, approved, onUpdate, onCopy }: Props) {
  const impact = review?.impact;
  const issues = review?.issues ?? [];
  const sourceRows = new Map(review?.rows.map((row) => [row.id, row]));
  return <aside className="side">
    <section className="panel" aria-labelledby="update-heading">
      <div className="panel-title"><h2 id="update-heading">Cập nhật phòng</h2></div>
      <div className="issues">
        <label className="field">Nguồn cập nhật
          <select id="update" value={update} disabled={busy || !review?.updates.length}
            onChange={(event) => onUpdate(event.target.value)}>
            <option value="">Lập lịch từ nguồn của tuần</option>
            {review?.updates.map((item) => <option key={item.id} value={item.id}>{item.label}</option>)}
          </select>
        </label>
        {impact && !pending && <div id="impact">
          <strong>{impact.old_room ? impact.class_name + " · " + impact.session : "Chưa xác định lớp cần báo lại"}</strong>
          <p>{shortDate(impact.date)} · {impact.start}–{impact.end}</p>
          <p>{impact.old_room ? impact.old_room + " → " + (impact.room || "Chờ phòng thay thế") :
            "Cần bản lịch đã thông báo để đối chiếu."}</p>
          <small>Nguồn {impact.source}</small>
        </div>}
        <div id="notice" hidden={!review?.notice || pending}>
          <h3>Nháp thông báo cho BTC</h3>
          <pre id="notice-text">{pending ? "" : review?.notice}</pre>
          <button id="copy" className="secondary" disabled={busy || pending} onClick={onCopy}>Sao chép nháp</button>
        </div>
      </div>
    </section>
    <section className="panel" aria-labelledby="alerts-heading">
      <div className="panel-title"><h2 id="alerts-heading">Cảnh báo</h2>
        <span id="issue-count">{!pending && review ? issues.length + " lỗi chặn" : ""}</span></div>
      <div id="issues" className="issues">
        {pending ? <p>Đang chờ kiểm tra bản nháp.</p> :
          issues.length ? issues.map((issue) => (
            <article key={issue.field + issue.sessions.join("-") + issue.message} className="issue">
              <p>{issue.message}</p>
              {issue.sessions.map((id) => {
                const row = sourceRows.get(id);
                return <a key={id} href={"#row-" + id} onClick={() => openSource(id)}>
                  {row ? row.class_name + " · " + id + " · " + row.start + "–" + row.end : id}
                </a>;
              })}
            </article>
          )) : <p>{approved ? "Bản bàn giao đã duyệt." : "Có thể duyệt bản bàn giao."}</p>}
      </div>
    </section>
  </aside>;
}
