"""Normalize the two supplied AI20K workbooks with cell-level provenance."""
from collections import defaultdict
from datetime import datetime, timedelta
from hashlib import sha256
from pathlib import Path
import re
import unicodedata

from xlsx_reader import read_workbook, col_name

ROOM = re.compile(r'\b[A-Z]\d{3}\b')
SESSION = re.compile(r'(L[23](?:A\+B|AB|A|B))\s*[—–-]\s*(LEC|LAB|HACKATHON)(?:\s*(\d+))?', re.I)


def norm(value):
    return ' '.join(unicodedata.normalize('NFC', str(value)).casefold().split())


def iso_date(value):
    match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', value)
    if not match:
        raise ValueError('Ngày không hợp lệ: ' + value[:80])
    return datetime(int(match[3]), int(match[2]), int(match[1])).date().isoformat()


def monday(value):
    day = datetime.fromisoformat(value).date()
    return (day - timedelta(days=day.weekday())).isoformat()


def room_info(text, default=''):
    pending = any(word in norm(text) for word in ('chờ xác nhận', 'dự kiến', 'dk:'))
    rooms = list(dict.fromkeys(ROOM.findall(text.upper())))
    return ', '.join(rooms) or default, not pending and bool(rooms or default)


def people(text, prefix):
    return list(dict.fromkeys(re.findall(r'\b' + prefix + r'\s+[A-Z]{1,2}\b', text)))


def parse_schedule(sheet):
    output = []
    for r in range(6, sheet.max_row + 1):
        try:
            date = iso_date(sheet.cell(r, 1))
        except ValueError:
            continue
        slot = 'Sáng' if 'Sáng' in sheet.cell(r, 3) else 'Chiều'
        for c in range(4, 9):
            text = sheet.cell(r, c, merged=False)
            match = SESSION.search(text)
            if not match:
                continue
            cls, kind, number = match.groups()
            number = number or '15'
            cls, kind = cls.upper().replace('A+B', 'AB'), kind.upper()
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            timing = re.search(r'(\d{1,2}:\d{2})\s*[–—-]\s*(\d{1,2}:\d{2})', text)
            if not timing:
                timing = re.search(r'(\d{1,2}:\d{2})\s*[–—-]\s*(\d{1,2}:\d{2})', sheet.cell(r, 3))
            start, end = (timing.groups() if timing else ('09:00', '13:00') if slot == 'Sáng' else ('14:00', '18:00'))
            start, end = start.zfill(5), end.zfill(5)
            online = any(norm(line) == 'online' for line in lines)
            main_line = next((line for line in lines if re.match(r'^Phòng(?: dự kiến)?:', line, re.I)), '')
            extra_line = next((line for line in lines if re.match(r'^Phòng thêm:', line, re.I)), '')
            default = 'H209' if c == 4 else 'H210' if c == 5 else ''
            room, confirmed = room_info(main_line, '' if main_line else default)
            if online:
                room, confirmed = '', False
            topic = next((line for line in lines[1:] if not re.match(r'^(Online$|\d{1,2}:\d{2}|Phòng|Giảng)', line, re.I)), kind + ' ' + number)
            teachers = people('\n'.join(line for line in lines if norm(line).startswith('giảng viên')), 'Lecturer')
            current_teacher = '; '.join(teachers)
            identity = f'{date}-{cls}-{kind}{number}-{col_name(c)}'
            output.append({
                'id': identity, 'date': date, 'class_name': cls, 'session': kind + ' ' + number,
                'group_id': f'{date}-{cls}-{kind}{number}', 'slot': slot, 'topic': topic,
                'start': start, 'end': end, 'format': 'online' if online else 'offline',
                'room': room, 'room_options': [room] if confirmed and not online else [],
                'room_status': 'online' if online else 'confirmed' if confirmed else 'pending',
                'teacher': current_teacher, 'teachers': list(dict.fromkeys(([current_teacher] if current_teacher else []) + teachers)),
                'coach': [], 'coaches': [], 'coach_required': kind in ('LAB', 'HACKATHON'),
                'key_coaches': [], 'extra_rooms': ROOM.findall(extra_line),
                'online_source': sheet.source(r, c) if online else '', 'meeting_url': '',
                'published_room': None, 'source': sheet.source(r, c),
                'sources': [{'kind': 'Lịch giảng dạy', 'ref': sheet.source(r, c), 'value': text}],
                'data_warnings': [], 'resolution_note': '',
            })
    return output


def class_matches(left, right):
    if left == right:
        return True
    return left[:2] == right[:2] and (left.endswith('AB') or right.endswith('AB'))


def session_key(value):
    if 'hackathon' in norm(value):
        return 'HACKATHON15'
    match = re.search(r'(LEC|LAB)\s*(\d+)', value, re.I)
    return match[1].upper() + str(int(match[2])) if match else norm(value)


def import_workbooks(teaching_path, coach_path):
    teaching, coaching = read_workbook(teaching_path), read_workbook(coach_path)
    required = {'Khoá 9 (GĐ1)', 'Dang_ky_chi_tiet', 'Nhan_su', 'Lịch sử chỉnh sửa'}
    if not required.issubset(teaching):
        raise ValueError('File teaching thiếu sheet: ' + ', '.join(sorted(required - set(teaching))))
    if not {'Lịch lab 1504-2404', 'Lịch lab 2604-0805', 'Đổi buổi (form)'}.issubset(coaching):
        raise ValueError('File lab-coach không đúng cấu trúc được hỗ trợ.')
    rows = parse_schedule(teaching['Khoá 9 (GĐ1)'])
    aliases = {}
    for _, record in teaching['Nhan_su'].records():
        aliases[norm(record['Họ tên đăng ký'])] = record['Tên khớp chuẩn']
    registration_count = 0
    for r, record in teaching['Dang_ky_chi_tiet'].records():
        registration_count += 1
        try:
            date = iso_date(record['Ngày'])
        except ValueError:
            continue
        name = record['Tên khớp chuẩn'] or aliases.get(norm(record['Họ tên đăng ký']), '')
        role = record['Vai trò nguồn']
        for row in rows:
            if row['date'] != date or row['slot'] != record['Buổi'] or not row['class_name'].startswith('L3'):
                continue
            if norm(row['topic']) != norm(record['Chuyên đề']):
                continue
            if role == 'Giảng viên' and name.startswith('Lecturer '):
                if name not in row['teachers']:
                    row['teachers'].append(name)
            elif 'Lab Coach' in role and name.startswith('Lab Coach '):
                if name not in row['coaches']:
                    row['coaches'].append(name)
            if name:
                row['sources'].append({'kind': 'Đăng ký nhân sự', 'ref': teaching['Dang_ky_chi_tiet'].source(r, 4),
                                       'value': name + ' / ' + role + ' / ' + record['Chuyên đề']})
                if record['Họ tên đăng ký'] != name:
                    row['sources'].append({'kind': 'Chuẩn hóa tên', 'ref': teaching['Dang_ky_chi_tiet'].source(r, 2),
                                           'value': record['Họ tên đăng ký'] + ' → ' + name})
    coach_records = 0
    for sheet_name in ('Lịch lab 1504-2404', 'Lịch lab 2604-0805'):
        sheet = coaching[sheet_name]
        date = ''
        for r in range(1, sheet.max_row + 1):
            first = sheet.cell(r, 1, False)
            if re.search(r'\d{2}/\d{2}/\d{4}', first):
                date = iso_date(first)
            if not date or not re.fullmatch(r'\d+', first):
                continue
            cls, session = sheet.cell(r, 2).replace('A+B', 'AB'), sheet.cell(r, 3)
            coach = sheet.cell(r, 4, False)
            key = sheet.cell(r, 5)
            room_col, slot_col = (6, 7) if sheet_name.endswith('0805') else (None, 6)
            slot = sheet.cell(r, slot_col)
            if not re.fullmatch(r'Lab Coach [A-Z]{1,2}', coach):
                coach = ''
            if coach:
                coach_records += 1
            for row in rows:
                if row['date'] != date or not class_matches(row['class_name'], cls) or session_key(row['session']) != session_key(session) or row['slot'] != slot:
                    continue
                if coach and coach not in row['coach']:
                    row['coach'].append(coach)
                if coach and coach not in row['coaches']:
                    row['coaches'].append(coach)
                if key and key not in row['key_coaches']:
                    row['key_coaches'].append(key)
                row['sources'].append({'kind': 'Phân công lab coach', 'ref': sheet.source(r, 4), 'value': coach or 'Chưa phân công'})
                notes = sheet.cell(r, 8) if room_col is None else sheet.cell(r, 10)
                if notes and not re.fullmatch(r'\d+', notes):
                    row['sources'].append({'kind': 'Ghi chú vận hành coach', 'ref': sheet.source(r, 8 if room_col is None else 10), 'value': notes})
                    if 'cần bổ sung' in norm(notes):
                        warning = 'Bảng coach có ghi chú cần bổ sung nhân sự; xác minh đủ định biên trước khi duyệt.'
                        if warning not in row['data_warnings']:
                            row['data_warnings'].append(warning)
                if room_col:
                    room_text = sheet.cell(r, room_col)
                    other_room, other_confirmed = room_info(room_text)
                    row['sources'].append({'kind': 'Phòng trong bảng coach', 'ref': sheet.source(r, room_col), 'value': room_text})
                    if other_room and set(ROOM.findall(other_room)) != set(ROOM.findall(row['room'])):
                        warning = 'Bảng coach ghi phòng khác bảng teaching; cần xác minh nguồn mới nhất.'
                        if warning not in row['data_warnings']:
                            row['data_warnings'].append(warning)
    histories = []
    for r, record in teaching['Lịch sử chỉnh sửa'].records():
        targets = re.findall(r'\b[D-H]\d+\b', record['Ô'])
        matches = [row for row in rows if row['source'].split('!')[-1] in targets]
        for row in matches:
            item = dict(record, source=teaching['Lịch sử chỉnh sửa'].source(r, 6), session=row['id'])
            histories.append(item)
            row['sources'].append({'kind': 'Lịch sử chỉnh sửa', 'ref': item['source'],
                                   'value': record['Thời điểm sửa'] + ': ' + record['Trước'] + ' → ' + record['Sau']})
    # The other workbook is a dated copy, not evidence of a sent notification.
    copied = parse_schedule(coaching['Lịch lớp K9 (bản chép)']) if 'Lịch lớp K9 (bản chép)' in coaching else []
    copied_map = {row['id']: row for row in copied}
    for row in rows:
        older = copied_map.get(row['id'])
        if older:
            row['sources'].append({'kind': 'Bản chép lịch trong bảng coach', 'ref': older['source'],
                                   'value': older['room'] or older['format']})
            if older['room'] != row['room'] or older['format'] != row['format']:
                row['data_warnings'].append('Bản chép lịch ở workbook coach khác lịch teaching; bản chép không chứng minh đã gửi thông báo.')
    requests = []
    for r, record in coaching['Đổi buổi (form)'].records():
        # No email is needed for scheduling or sent to the model.
        requests.append({'id': f'REQ-{r}', 'name': record['Họ tên'], 'from': record['Buổi đang nhận'],
                         'to': record['Muốn đổi sang'], 'reason': record['Lý do'],
                         'status': record['Đã xử lý?'], 'note': record['Ghi chú BTC'],
                         'source': coaching['Đổi buổi (form)'].source(r, 2)})
    workload = []
    if 'Workload - Lab coach' in coaching:
        sheet = coaching['Workload - Lab coach']
        for r in range(5, sheet.max_row + 1):
            if re.fullmatch(r'Lab Coach [A-Z]{1,2}', sheet.cell(r, 3)):
                workload.append({'name': sheet.cell(r, 3), 'key': sheet.cell(r, 67), 'lab': sheet.cell(r, 68),
                                 'total': sheet.cell(r, 69), 'source': sheet.source(r, 3)})
    weeks = defaultdict(lambda: {'rows': [], 'updates': []})
    for row in rows:
        row['sources'] = list({(s['kind'], s['ref'], s['value']): s for s in row['sources']}.values())
        weeks[monday(row['date'])]['rows'].append(row)
    for week in weeks.values():
        week['rows'].sort(key=lambda row: (row['date'], row['start'], row['class_name'], row['id']))
    files = [{'name': Path(path).name, 'sha256': sha256(Path(path).read_bytes()).hexdigest(),
              'sheets': list(book)} for path, book in ((teaching_path, teaching), (coach_path, coaching))]
    return {'weeks': dict(weeks), 'metadata': {'files': files, 'sessions': len(rows),
            'registrations': registration_count, 'coach_assignments': coach_records,
            'requests': len(requests), 'date_start': min(row['date'] for row in rows),
            'date_end': max(row['date'] for row in rows), 'course': 'Khoá 9 (dữ liệu BTC giả lập)',
            'notes': ['Phòng dự kiến không được coi là đã xác nhận.', 'Lịch sử sửa không chứng minh thông báo đã gửi.',
                      'Đăng ký một buổi không chứng minh nhân sự rảnh ở các buổi khác.']},
            'requests': requests, 'workload': workload, 'history': histories}
