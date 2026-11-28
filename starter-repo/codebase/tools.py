"""Workbook-backed tools. No automatic writes to source workbooks or notifications."""
import copy
import hashlib
import json
import os
import re
from itertools import combinations
from pathlib import Path

from excel_data import ROOM, import_workbooks, monday, people
import store
from tracing import tool

ROOT = Path(__file__).resolve().parents[1]
_cache = None
_signatures = None


def source_paths():
    folder = Path(os.environ.get('SCHEDULE_SOURCE_DIR', ROOT.parent / 'data-btc'))
    return (Path(os.environ.get('TEACHING_FILE', folder / 'teaching-schedule.xlsx')),
            Path(os.environ.get('COACH_FILE', folder / 'lab-coach-schedule.xlsx')))


def dataset(force=False):
    global _cache, _signatures
    paths = source_paths()
    if not all(path.is_file() for path in paths):
        raise ValueError('Thiếu hai file Excel. Đặt teaching-schedule.xlsx và lab-coach-schedule.xlsx trong data-btc ở gốc repo hoặc cấu hình TEACHING_FILE/COACH_FILE.')
    signatures = tuple((str(p), p.stat().st_mtime_ns, p.stat().st_size) for p in paths)
    if force or _cache is None or signatures != _signatures:
        new = import_workbooks(*paths)
        new['metadata']['fingerprint'] = hashlib.sha256(''.join(f['sha256'] for f in new['metadata']['files']).encode()).hexdigest()[:20]
        _cache, _signatures = new, signatures
    return _cache


def weeks():
    return dataset()['weeks']


def fingerprint():
    return dataset()['metadata']['fingerprint']


def additional_updates(week):
    return store.get('updates', store.draft_key(week, fingerprint()), [])


@tool
def read_weekly_schedule_data(week_id: str) -> dict:
    """Đọc tuần. Input: thứ Hai ISO. Output: lịch và nguồn Excel, cập nhật do người nhập. Chỉ đọc."""
    original = weeks().get(week_id)
    if original is None:
        raise ValueError('Tuần này không có trong hai workbook đã nhập.')
    week = copy.deepcopy(original)
    week['updates'] = additional_updates(week_id)
    published = store.get('published', store.draft_key(week_id, fingerprint()))
    if published:
        for row in week['rows']:
            baseline = next((item for item in published['rows'] if item['id'] == row['id']), None)
            if baseline:
                row['published_room'] = baseline['room']
    for update in week['updates']:
        row = next((r for r in week['rows'] if r['id'] == update['session']), None)
        if row:
            row.update(room=update['room'], room_options=[update['room']] if update['room'] and update['confirmed'] else [],
                       room_status='confirmed' if update['room'] and update['confirmed'] else 'pending', update_source=update['source'])
            row['sources'].append({'kind': 'Cập nhật người dùng', 'ref': update['source'], 'value': update['room'] or 'Thu hồi phòng'})
    return week


def create_update(body):
    week_id = body.get('week')
    week = read_weekly_schedule_data(week_id)
    row = next((r for r in week['rows'] if r['id'] == body.get('session')), None)
    if row is None:
        raise ValueError('Chọn một buổi trong tuần hiện tại.')
    room = body.get('room', '').strip().upper()
    source = body.get('source', '').strip()
    confirmed = body.get('confirmed', False)
    if not isinstance(confirmed, bool) or not 8 <= len(source) <= 300:
        raise ValueError('Ghi nguồn xác nhận/cập nhật từ 8 đến 300 ký tự.')
    if room and (not ROOM.findall(room) or re.sub(r'[\s,;]', '', ROOM.sub('', room))):
        raise ValueError('Phòng dùng mã như H209 hoặc C401, E403; để trống nếu bị thu hồi.')
    room = ', '.join(dict.fromkeys(ROOM.findall(room)))
    items = additional_updates(week_id)
    if len(items) >= 100:
        raise ValueError('Tuần đã có 100 cập nhật; kiểm tra lại nguồn trước khi bổ sung.')
    item = {'id': 'UP-' + store.stamp().replace(':', '').replace('.', ''), 'session': row['id'],
            'room': room, 'source': source, 'confirmed': confirmed,
            'previous_room': row['room'],
            'label': row['class_name'] + ' / ' + row['date'] + ' / ' + (room or 'Thu hồi phòng'),
            'created_at': store.stamp()}
    store.put('updates', store.draft_key(week_id, fingerprint()), items + [item])
    return item


@tool
def diff_room_updates(rows: list, updates: list, update_id: str) -> dict:
    """Đối chiếu cập nhật. Input: lịch, mã cập nhật. Output: lớp bị ảnh hưởng, phòng và nguồn. Chỉ đọc."""
    update = next((item for item in updates if item['id'] == update_id), None)
    if update is None:
        raise ValueError('Cập nhật không thuộc tuần hoặc phiên bản dữ liệu hiện tại.')
    row = next(item for item in rows if item['id'] == update['session'])
    return dict(update, old_room=row.get('published_room'), baseline_room=update.get('previous_room', row['room']),
                baseline_kind='published' if row.get('published_room') is not None else 'source',
                class_name=row['class_name'], date=row['date'], start=row['start'], end=row['end'])


def coach_list(value):
    if isinstance(value, str):
        value = [value] if value.strip() else []
    if not isinstance(value, list) or len(value) > 80 or any(not isinstance(n, str) or not n.strip() or len(n) > 100 for n in value):
        raise ValueError('Lab coach phải là danh sách tên hợp lệ.')
    return list(dict.fromkeys(n.strip() for n in value))


def draft_rows(week, changes, update):
    if not isinstance(changes, dict) or changes.keys() - {r['id'] for r in week['rows']}:
        raise ValueError('Mã buổi không thuộc tuần đã chọn.')
    rows = copy.deepcopy(week['rows'])
    for row in rows:
        if update and update['session'] == row['id']:
            row.update(room=update['room'], room_options=[update['room']] if update['room'] and update['confirmed'] else [],
                       room_status='confirmed' if update['room'] and update['confirmed'] else 'pending', update_source=update['source'])
            row['sources'].append({'kind': 'Cập nhật người dùng', 'ref': update['source'], 'value': update['room'] or 'Thu hồi phòng'})
        fields = changes.get(row['id'], {})
        if not isinstance(fields, dict) or fields.keys() - {'room', 'teacher', 'coach', 'resolution_note', 'meeting_url'}:
            raise ValueError('Bản nháp có trường ngoài phạm vi chỉnh sửa.')
        for key, value in fields.items():
            if key == 'coach':
                row[key] = coach_list(value)
            else:
                if not isinstance(value, str) or len(value) > (1200 if key == 'resolution_note' else 500):
                    raise ValueError('Giá trị chỉnh sửa không hợp lệ.')
                row[key] = value.strip()
    return rows


def overlaps(left, right):
    return left['date'] == right['date'] and max(left['start'], right['start']) < min(left['end'], right['end'])


@tool
def validate_schedule_draft(rows: list) -> list:
    """Kiểm ràng buộc. Input: bản nháp với nguồn. Output: lỗi chặn và cảnh báo. Chỉ tính toán."""
    issues = []
    def add(row, field, message, other=None, severity='error'):
        issues.append({'sessions': [row['id']] + ([other['id']] if other else []), 'field': field,
                       'message': message, 'severity': severity, 'source': row.get('source', '')})
    for row in rows:
        if row['format'] == 'online':
            if row['room']:
                add(row, 'room', 'Buổi online không dùng phòng vật lý.')
            if not re.match(r'^https://[^\s]+$', row.get('meeting_url', '')):
                add(row, 'meeting_url', 'Bổ sung đường dẫn học online HTTPS trước khi bàn giao.')
        elif row['room'] not in row['room_options'] or not row['room']:
            add(row, 'room', 'Phòng chưa được xác nhận hoặc không khớp nguồn; nhập cập nhật có căn cứ ở Cập nhật phòng.')
        if row['teacher'] not in row['teachers'] or not row['teacher']:
            add(row, 'teacher', 'Chọn giảng viên có căn cứ trong lịch hoặc đăng ký đúng buổi.')
        if row['coach_required'] and not row['coach']:
            add(row, 'coach', 'Buổi lab/hackathon chưa có coach được phân công.')
        if not set(row['coach']).issubset(row['coaches']):
            add(row, 'coach', 'Coach được chọn không có nguồn phân công/đăng ký đúng buổi.')
        for warning in row.get('data_warnings', []):
            if len(row.get('resolution_note', '')) < 10:
                add(row, 'source', warning + ' Ghi kết quả xác minh trong buổi học trước khi duyệt.')
    for left, right in combinations(rows, 2):
        if not overlaps(left, right):
            continue
        # A lecturer/coach can cover parallel rooms of the same class session.
        same_group = left['group_id'] == right['group_id']
        if left['format'] == right['format'] == 'offline':
            left_rooms = set(ROOM.findall(left['room'])) | (set(left.get('extra_rooms', [])) if not same_group else set())
            right_rooms = set(ROOM.findall(right['room'])) | (set(right.get('extra_rooms', [])) if not same_group else set())
            shared = left_rooms & right_rooms
            if shared:
                add(left, 'room', 'Trùng phòng ' + ', '.join(sorted(shared)) + ' trong cùng thời gian.', right)
        if not same_group:
            shared_teachers = set(people(left['teacher'], 'Lecturer')) & set(people(right['teacher'], 'Lecturer'))
            if shared_teachers:
                add(left, 'teacher', 'Giảng viên trùng ca: ' + ', '.join(sorted(shared_teachers)), right)
            shared_coaches = set(left['coach']) & set(right['coach'])
            if shared_coaches:
                add(left, 'coach', 'Lab coach trùng ca: ' + ', '.join(sorted(shared_coaches)), right)
    return issues


@tool
def check_staffing(rows: list, workload: list) -> list:
    """Kiểm định biên. Input: lịch, workload. Output: số phòng/coach, thiếu, Key Coach, ứng viên tải thấp. Chỉ tính toán."""
    load = {item['name']: int(item['total']) if str(item.get('total', '')).isdigit() else None for item in workload}
    peak = max((value for value in load.values() if value is not None), default=None)
    groups = {}
    for row in rows:
        groups.setdefault(row['group_id'], []).append(row)
    result = []
    for group_id, members in groups.items():
        first = members[0]
        rooms = list(dict.fromkeys(code for row in members for code in ROOM.findall(row['room']) + row.get('extra_rooms', [])))
        if not (any(row['coach_required'] for row in members) or len(rooms) > 1):
            continue
        assigned = list(dict.fromkeys(name for row in members for name in row['coach']))
        keys = list(dict.fromkeys(name for row in members for name in row.get('key_coaches', [])))
        busy = {name for other in rows if other['group_id'] != group_id and overlaps(other, first) for name in other['coach']}
        registered = list(dict.fromkeys(name for row in members for name in row['coaches']))
        candidates = sorted((name for name in registered if name not in assigned and name not in busy),
                            key=lambda name: (load.get(name) is None, load.get(name) or 0))
        missing = max(0, len(rooms) - len(assigned)) if first['format'] == 'offline' else 0
        if len(rooms) < 2 and not missing and keys:
            continue
        result.append({
            'group_id': group_id, 'date': first['date'], 'class': first['class_name'], 'session': first['session'],
            'time': first['start'] + '-' + first['end'], 'format': first['format'],
            'rooms': rooms, 'room_count': len(rooms),
            'room_status': sorted({row['room_status'] for row in members}),
            'assigned_coaches': assigned, 'coach_count': len(assigned),
            'missing_coaches': missing,
            'key_coaches': keys,
            'overloaded_assigned': [name for name in assigned if peak is not None and load.get(name) == peak],
            'candidates_low_load': [{'name': name, 'total_shifts': load.get(name)} for name in candidates[:5]],
            'max_shifts_in_workload': peak,
            'sources': [row['source'] for row in members]})
    return result
