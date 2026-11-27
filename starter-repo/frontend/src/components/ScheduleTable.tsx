import { Icon } from "./Icon";
import { shortDate } from "../features/schedule/types";
import type { Assignment, Changes, Review, Session } from "../features/schedule/types";

interface Props {
  review?: Review;
  proposal: Changes;
  changes: Changes;
  busy: boolean;
  pending: boolean;
  onEdit: (id: string, changes: Assignment) => void;
  onApply: (id: string) => void;
  onSkip: (id: string) => void;
}

const columns = [
  ["room", "room_options", "Phòng"],
  ["teacher", "teachers", "Giảng viên"],
] as const;

function SessionRow({ row, blockers, suggestion, edit, ...props }: Omit<Props, "review" | "proposal" | "changes"> & {
  row: Session;
  blockers: number;
  suggestion?: Assignment;
  edit?: Assignment;
}) {
  const coaches = edit?.coach ?? row.coach;
  const suggestedCoaches = suggestion?.coach?.filter((coach) => !coaches.includes(coach)) ?? [];
  return (
    <tr id={"row-" + row.id}>
      <td className={blockers ? "has-alert" : undefined}>
        <div className="session-meta"><span className="class-badge">{row.class_name}</span><span className="session-id">{row.id}</span></div>
        <strong className="session-title">{row.topic}</strong>
        <div className="session-time"><Icon name="clock" />{shortDate(row.date)}<span className="time-divider" />{row.start}–{row.end}</div>
        {props.pending || blockers > 0 ? <span className="row-state">
          <Icon name="alert" />{props.pending ? "Chờ rà lại" : blockers + " điểm cần xử lý"}
        </span> : <span className="row-ready"><Icon name="check" />Đủ căn cứ</span>}
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
          {field === "room" && row.format === "online" ? <span className="online-badge"><Icon name="video" />Online</span> : (
            <select aria-label={title + " " + row.id} value={hasSuggestion ? "__suggestion__" : value} disabled={props.busy}
              onChange={(event) => props.onEdit(row.id, { [field]: event.target.value })}>
              {hasSuggestion && <option value="__suggestion__" disabled>{suggested} · Đề xuất</option>}
              <option value="">Chưa chọn</option>
              {row[options].map((name) => <option key={name} value={name}>{name}</option>)}
            </select>
          )}
        </td>;
      })}
      <td data-label="Lab coach" className={suggestedCoaches.length ? "proposal" : undefined}>
        <details className="coach-picker">
          <summary aria-label={"Lab coach " + row.id}>
            {suggestedCoaches.length ? (
              <>{suggestedCoaches.join(", ")} <span>· Đề xuất</span></>
            ) : coaches.join(", ") || "Chưa chọn"}
          </summary>
          <fieldset disabled={props.busy}>
            <legend className="sr-only">Chọn lab coach {row.id}</legend>
            {row.coaches.map((coach) => (
              <label key={coach}>
                <input type="checkbox" checked={coaches.includes(coach)} onChange={(event) => {
                  const selected = event.currentTarget.checked;
                  props.onEdit(row.id, { coach: selected ? [...coaches, coach] : coaches.filter((name) => name !== coach) });
                }} />
                {coach}{suggestedCoaches.includes(coach) ? " · Đề xuất" : ""}
              </label>
            ))}
            {!row.coaches.length && <span>Chưa có coach đăng ký</span>}
          </fieldset>
        </details>
      </td>
    </tr>
  );
}

export function ScheduleTable(props: Props) {
  const { review, proposal, changes, ...handlers } = props;
  const rows = review?.rows ?? [];
  return <section className="panel" aria-labelledby="schedule-heading">
    <div className="panel-title"><div><h2 id="schedule-heading">Bản nháp lịch tuần</h2><p>Rà soát phòng, giảng viên và coach cho từng buổi học.</p></div><span className="panel-count">{rows.length} buổi học</span></div>
    <div className="table-scroll" tabIndex={0} aria-label="Bảng lịch tuần">
      <table>
        <thead><tr><th scope="col">Ngày / Buổi học</th><th scope="col">Phòng</th>
          <th scope="col">Giảng viên</th><th scope="col">Lab coach</th></tr></thead>
        <tbody id="rows">{!rows.length && <tr><td colSpan={4} className="empty-state"><Icon name="calendar" /><strong>{props.busy ? "Đang tải lịch giảng dạy…" : "Chưa có buổi học"}</strong><p>{props.busy ? "Thông tin phân công sẽ xuất hiện tại đây." : "Chọn tuần có dữ liệu để bắt đầu lập lịch."}</p></td></tr>}{rows.map((row) => (
          <SessionRow key={row.id} row={row} suggestion={proposal[row.id]} edit={props.pending ? changes[row.id] : undefined}
            blockers={review?.issues.filter((issue) => issue.sessions.includes(row.id)).length ?? 0} {...handlers} />
        ))}</tbody>
      </table>
    </div>
  </section>;
}
