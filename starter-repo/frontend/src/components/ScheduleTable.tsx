import { shortDate } from "../features/schedule/types";
import type { Assignment, AssignmentField, Changes, Review, Session } from "../features/schedule/types";

interface Props {
  review?: Review;
  proposal: Changes;
  changes: Changes;
  busy: boolean;
  pending: boolean;
  onEdit: (id: string, field: AssignmentField, value: string) => void;
  onApply: (id: string) => void;
  onSkip: (id: string) => void;
}

const columns = [
  ["room", "room_options", "Phòng"],
  ["teacher", "teachers", "Giảng viên"],
  ["coach", "coaches", "Lab coach"],
] as const;

function SessionRow({ row, blockers, suggestion, edit, ...props }: Omit<Props, "review" | "proposal" | "changes"> & {
  row: Session;
  blockers: number;
  suggestion?: Assignment;
  edit?: Assignment;
}) {
  return (
    <tr id={"row-" + row.id}>
      <td className={blockers ? "has-alert" : undefined}>
        <div className="session-meta">{row.class_name} <span>·</span> {row.id}</div>
        <strong className="session-title">{row.topic}</strong>
        <div className="session-meta">{shortDate(row.date)} <span>·</span> {row.start}–{row.end}</div>
        {props.pending || blockers > 0 ? <span className="row-state">
          {props.pending ? "Chờ rà lại" : blockers + " lỗi chặn"}
        </span> : null}
        <details className="source">
          <summary>Xem nguồn</summary>
          <ul>
            <li>Lịch mẫu / {row.id} · {row.published_room || "chưa có bản đã thông báo"}</li>
            <li>{row.update_source || "Bảng phòng mẫu / " + row.id} · {row.room_options.join(", ") || "chưa có phòng xác nhận"}</li>
            <li>Đăng ký giảng viên / {row.id} · {row.teachers.join(", ") || "chưa có"}</li>
            <li>Đăng ký lab coach / {row.id} · {row.coaches.join(", ") || "chưa có"}</li>
            {row.online_source && <li>Online · {row.online_source}</li>}
          </ul>
        </details>
        {suggestion && <div className="row-actions">
          <button className="secondary" disabled={props.busy} onClick={() => props.onApply(row.id)}>Áp dụng buổi này</button>
          <button className="secondary" disabled={props.busy} onClick={() => props.onSkip(row.id)}>Bỏ qua</button>
        </div>}
      </td>
      {columns.map(([field, options, title]) => {
        const value = edit?.[field] ?? row[field];
        const suggested = suggestion?.[field];
        const hasSuggestion = suggested && suggested !== value;
        return <td key={field} data-label={title} className={hasSuggestion ? "proposal" : undefined}>
          {field === "room" && row.format === "online" ? "Online" : (
            <select aria-label={title + " " + row.id} value={value} disabled={props.busy}
              onChange={(event) => props.onEdit(row.id, field, event.target.value)}>
              <option value="">Chưa chọn</option>
              {row[options].map((name) => <option key={name} value={name}>{name}</option>)}
            </select>
          )}
          {hasSuggestion && <small>Đề xuất {suggested}</small>}
        </td>;
      })}
    </tr>
  );
}

export function ScheduleTable(props: Props) {
  const { review, proposal, changes, ...handlers } = props;
  const rows = review?.rows ?? [];
  return <section className="panel" aria-labelledby="schedule-heading">
    <div className="panel-title"><h2 id="schedule-heading">Bản nháp tuần</h2></div>
    <div className="table-scroll" tabIndex={0} aria-label="Bảng lịch tuần">
      <table>
        <thead><tr><th scope="col">Ngày / Buổi học</th><th scope="col">Phòng</th>
          <th scope="col">Giảng viên</th><th scope="col">Lab coach</th></tr></thead>
        <tbody id="rows">{rows.map((row) => (
          <SessionRow key={row.id} row={row} suggestion={proposal[row.id]} edit={props.pending ? changes[row.id] : undefined}
            blockers={review?.issues.filter((issue) => issue.sessions.includes(row.id)).length ?? 0} {...handlers} />
        ))}</tbody>
      </table>
    </div>
  </section>;
}
