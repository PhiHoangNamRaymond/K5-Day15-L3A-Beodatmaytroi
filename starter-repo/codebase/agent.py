"""Luồng cố định đề xuất và rà soát bản nháp tuần."""
import json
import re
from itertools import product

from ai import MODEL_PROVIDER, call_model
from tools import diff_room_updates, draft_rows, read_weekly_schedule_data, validate_schedule_draft

COMMAND = re.compile(r"(?i)(lập lịch|rà lịch|đổi phòng) (\d{4}-\d{2}-\d{2})(?: (UP-\d{2}))?")
SYSTEM = (
    "Bạn hỗ trợ key coach chọn một phương án lịch tuần từ danh sách đã qua kiểm tra. "
    "Ưu tiên giữ phòng đã thông báo nếu còn hợp lệ và phân bổ ca cân bằng. "
    "Chỉ trả về chỉ số phương án từ 1, dưới dạng một số nguyên."
)


def candidate_plans(rows):
    """Sinh tối đa bốn phương án để người duyệt có lựa chọn."""
    plans = []

    def extend(assigned):
        if len(plans) == 4:
            return
        if len(assigned) == len(rows):
            plans.append({row["id"]: {key: row[key] for key in ("room", "teacher", "coach")}
                          for row in assigned})
            return
        row = rows[len(assigned)]
        rooms = row["room_options"] if row["format"] == "offline" else [""]
        ordered_rooms = sorted(rooms, key=lambda room: room != row.get("published_room"))
        current_coaches = [coach for coach in row["coach"] if coach in row["coaches"]]
        coach_options = [current_coaches] if current_coaches else [[coach] for coach in row["coaches"]]
        for room, teacher, coach in product(ordered_rooms or [""], row["teachers"] or [""], coach_options or [[]]):
            proposal = dict(row, room=room, teacher=teacher, coach=coach)
            if not any(len(issue["sessions"]) > 1 for issue in validate_schedule_draft([*assigned, proposal])):
                extend([*assigned, proposal])

    extend([])
    return plans


def weekly_review(week_id, changes, update_id="", propose=False):
    week = read_weekly_schedule_data(week_id)
    update = diff_room_updates(week["rows"], week["updates"], update_id) if update_id else None
    rows = draft_rows(week, changes, update)
    proposal = None
    method = "rules"
    if propose:
        plans = candidate_plans(rows)
        if plans:
            choice = 0
            if MODEL_PROVIDER != "fake" and len(plans) > 1:
                payload = {"plans": plans, "published": {row["id"]: row.get("published_room") for row in rows}}
                reply = call_model(SYSTEM, json.dumps(payload, ensure_ascii=False))["text"].strip()
                if reply in {str(index + 1) for index in range(len(plans))}:
                    choice = int(reply) - 1
                    method = "model"
            proposal = plans[choice]
    issues = validate_schedule_draft(rows)
    notice = None
    if update and update["old_room"]:
        timing = f"{update['date']} · {update['start']}–{update['end']}"
        room = update["room"]
        summary = f"chuyển từ {update['old_room']} sang {room}" if room else (
            f"phòng {update['old_room']} đã bị thu hồi. Địa điểm thay thế đang chờ xác nhận"
        )
        notice = (f"Gửi BTC duyệt · Lớp {update['class_name']} ({timing})\n"
                  f"Buổi {update['session']}: {summary}.\n"
                  f"Nguồn cập nhật: {update['source']}. Đối chiếu lại lịch và thông báo trước khi phát.")
    return {"rows": rows, "issues": issues, "updates": week["updates"], "impact": update,
            "notice": notice, "proposal": proposal, "method": method}


def answer(text: str) -> dict:
    match = COMMAND.fullmatch(text.strip())
    if not match:
        return {"output": "Chọn tuần và dùng: lập lịch YYYY-MM-DD, rà lịch YYYY-MM-DD hoặc đổi phòng YYYY-MM-DD UP-xx. Mọi thông báo ở dạng nháp để BTC duyệt."}
    command, week, update = match.groups()
    if (command.casefold() == "đổi phòng") != bool(update):
        return {"output": "Để rà thay đổi phòng, chọn mã cập nhật UP-xx của tuần."}
    try:
        result = weekly_review(week, {}, update.upper() if update else "", command.casefold() == "lập lịch")
    except ValueError as error:
        return {"output": str(error)}
    lines = [f"Tuần {week} · {len(result['rows'])} buổi"]
    if result["proposal"]:
        lines.extend(f"{key} · {item['room'] or 'xem hình thức và nguồn'} · {item['teacher']} · {', '.join(item['coach'])}"
                     for key, item in result["proposal"].items())
    else:
        lines.extend(f"{', '.join(issue['sessions'])} · {issue['message']}" for issue in result["issues"])
    if result["notice"]:
        lines.append(result["notice"])
    return {"output": "\n".join(lines)}
