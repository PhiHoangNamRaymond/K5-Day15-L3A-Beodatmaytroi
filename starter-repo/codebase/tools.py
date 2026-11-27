"""Đọc và kiểm ràng buộc cho lịch tuần giả lập."""
import json
from itertools import combinations
from pathlib import Path

from tracing import tool

DATA = Path(__file__).resolve().parents[1] / "data" / "weekly-demo.json"
FIELDS = ("room", "teacher", "coach", "format")


def weeks():
    return json.loads(DATA.read_text(encoding="utf-8-sig"))


@tool
def read_weekly_schedule_data(week_id: str) -> dict:
    """Đọc nguồn của tuần. Input: ngày thứ Hai ISO. Output: buổi học và cập nhật phòng. Chỉ đọc."""
    week = weeks().get(week_id)
    if week is None:
        raise ValueError("Tuần này chưa có dữ liệu mẫu.")
    return week


@tool
def diff_room_updates(rows: list, updates: list, update_id: str) -> dict:
    """Đối chiếu cập nhật. Input: lịch, bản cập nhật, mã chọn. Output: lớp, phòng cũ/mới và nguồn. Chỉ đọc."""
    update = next((item for item in updates if item["id"] == update_id), None)
    if update is None:
        raise ValueError("Cập nhật phòng không thuộc tuần đã chọn.")
    row = next(item for item in rows if item["id"] == update["session"])
    return dict(update, old_room=row.get("published_room"), class_name=row["class_name"],
                date=row["date"], start=row["start"], end=row["end"])


def draft_rows(week, changes, update):
    if not isinstance(changes, dict) or changes.keys() - {row["id"] for row in week["rows"]}:
        raise ValueError("Mã buổi không thuộc tuần đã chọn.")
    rows = []
    for source in week["rows"]:
        row = dict(source, format="online" if source.get("online_source") else "offline")
        if update and update["session"] == row["id"]:
            row.update(room_options=[update["room"]] if update["room"] else [],
                       room=update["room"], update_source=update["source"])
            row["missing_published"] = not update["old_room"]
        fields = changes.get(row["id"], {})
        if not isinstance(fields, dict) or fields.keys() - set(FIELDS):
            raise ValueError("Bản nháp chứa trường ngoài phạm vi chỉnh sửa.")
        if any(not isinstance(value, str) or len(value) > 80 for value in fields.values()):
            raise ValueError("Giá trị chỉnh sửa phải là văn bản tối đa 80 ký tự.")
        row.update({key: value.strip() for key, value in fields.items()})
        rows.append(row)
    return rows


@tool
def validate_schedule_draft(rows: list) -> list:
    """Kiểm lịch. Input: các dòng nháp và nguồn. Output: lỗi chặn, mã buổi và nguồn. Chỉ tính toán."""
    issues = []

    def add(row, field, message, other=None):
        sessions = [row["id"]] if other is None else [row["id"], other["id"]]
        issues.append({"sessions": sessions, "field": field, "message": message})

    for row in rows:
        if row.get("missing_published"):
            add(row, "published", "Bổ sung bản lịch đã thông báo để xác định lớp cần báo lại.")
        if row["format"] == "online":
            if not row.get("online_source"):
                add(row, "format", "Chưa có nguồn xác nhận chuyển online và đường dẫn học.")
            if row["room"]:
                add(row, "room", "Buổi online vẫn có phòng vật lý.")
        elif row["format"] != "offline" or row.get("online_source"):
            add(row, "format", "Hình thức chưa khớp nguồn xác nhận.")
        elif row["room"] not in row["room_options"]:
            add(row, "room", "Chưa có phòng khớp nguồn xác nhận.")
        for field, choices, name in (("teacher", "teachers", "giảng viên"), ("coach", "coaches", "lab coach")):
            if row[field] not in row[choices]:
                add(row, field, f"Chọn {name} có đăng ký đúng buổi.")

    for left, right in combinations(rows, 2):
        if left["date"] != right["date"] or max(left["start"], right["start"]) >= min(left["end"], right["end"]):
            continue
        for field, name in (("room", "Phòng"), ("teacher", "Giảng viên"), ("coach", "Lab coach")):
            if field == "room" and (left["format"] != "offline" or right["format"] != "offline"):
                continue
            if left[field] and left[field] == right[field]:
                overlap = f"{max(left['start'], right['start'])}–{min(left['end'], right['end'])}"
                add(left, field, f"{name} {left[field]} trùng ca {overlap}.", right)
    return issues
