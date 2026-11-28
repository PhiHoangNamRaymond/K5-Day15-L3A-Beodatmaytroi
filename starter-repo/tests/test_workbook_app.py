import copy
import importlib
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import urllib.request
import urllib.error
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'codebase'))
import tools
import agent
import ai
import store
from excel_data import import_workbooks, room_info, monday, parse_schedule
from xlsx_reader import read_workbook


class WorkbookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = tools.dataset()

    def test_actual_workbooks_and_source_refs(self):
        self.assertEqual([f['name'] for f in self.data['metadata']['files']], ['teaching-schedule.xlsx', 'lab-coach-schedule.xlsx'])
        self.assertEqual(self.data['metadata']['registrations'], 204)
        self.assertEqual(self.data['metadata']['requests'], 22)
        rows = [r for week in self.data['weeks'].values() for r in week['rows']]
        self.assertEqual(len(rows), 129)
        self.assertEqual(len({r['id'] for r in rows}), len(rows))
        self.assertTrue(all('!' in r['source'] and r['sources'] for r in rows))
        self.assertEqual(max(r['date'] for r in rows), '2027-05-08')

    def test_pending_rooms_never_become_confirmed(self):
        room, confirmed = room_info('Phòng dự kiến: C401, E403 (chờ xác nhận)')
        self.assertEqual(room, 'C401, E403')
        self.assertFalse(confirmed)
        for week in self.data['weeks'].values():
            for row in week['rows']:
                if row['room_status'] == 'pending':
                    self.assertEqual(row['room_options'], [])

    def test_merged_dates_and_online_classes_not_duplicated(self):
        sheet = read_workbook(tools.source_paths()[0])['Khoá 9 (GĐ1)']
        self.assertEqual(sheet.cell(7, 1), '15/04/2027')
        rows = parse_schedule(sheet)
        online = [r for r in rows if r['date'] == '2027-04-21' and r['class_name'] == 'L3AB']
        self.assertEqual(len(online), 1)
        self.assertEqual(online[0]['format'], 'online')

    def test_both_sources_joined_and_no_email_in_context(self):
        rows = self.data['weeks']['2027-04-26']['rows']
        self.assertTrue(any(r['coach'] and any('lab-coach-schedule.xlsx' in s['ref'] for s in r['sources']) for r in rows))
        self.assertNotIn('@', json.dumps(agent.context_for(rows)))
        self.assertTrue(any(len(r['room'].split(', ')) > 1 for r in rows))

    def test_monday_and_cross_month(self):
        self.assertEqual(monday('2027-05-01'), '2027-04-26')


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.old_db = store.DB
        store.DB = Path(self.temp.name) / 'test.sqlite3'
        self.week = '2027-04-26'

    def tearDown(self):
        store.DB = self.old_db
        self.temp.cleanup()

    def test_proposal_is_bounded_and_all_assignments_are_from_source(self):
        week = tools.read_weekly_schedule_data(self.week)
        plans = agent.candidate_plans(week['rows'])
        self.assertLessEqual(len(plans), 3)
        for plan in plans:
            self.assertEqual(set(plan['assignments']), {r['id'] for r in week['rows']})
            for row in week['rows']:
                p = plan['assignments'][row['id']]
                self.assertTrue(not p['room'] or p['room'] in row['room_options'])
                self.assertTrue(not p['teacher'] or p['teacher'] in row['teachers'])
                self.assertTrue(set(p['coach']).issubset(row['coaches']))

    def test_arbitrary_fields_and_bad_coach_rejected(self):
        week = tools.read_weekly_schedule_data(self.week)
        with self.assertRaises(ValueError): tools.draft_rows(week, {'missing': {}}, None)
        row = week['rows'][0]
        with self.assertRaises(ValueError): tools.draft_rows(week, {row['id']: {'approved': True}}, None)
        with self.assertRaises(ValueError): tools.draft_rows(week, {row['id']: {'coach': [42]}}, None)

    def test_multiple_room_updates_persist_without_replacing_each_other(self):
        rows = [r for r in tools.read_weekly_schedule_data(self.week)['rows'] if r['format'] == 'offline']
        for row, room in zip(rows[:2], ['H209', 'C401']):
            tools.create_update({'week': self.week, 'session': row['id'], 'room': room, 'source': 'Nguồn kiểm thử xác nhận', 'confirmed': True})
        loaded = tools.read_weekly_schedule_data(self.week)
        self.assertEqual(len(loaded['updates']), 2)
        self.assertEqual(next(r for r in loaded['rows'] if r['id'] == rows[0]['id'])['room'], 'H209')
        self.assertEqual(next(r for r in loaded['rows'] if r['id'] == rows[1]['id'])['room'], 'C401')

    def test_unconfirmed_update_still_blocks(self):
        row = next(r for r in tools.read_weekly_schedule_data(self.week)['rows'] if r['format'] == 'offline')
        update = tools.create_update({'week': self.week, 'session': row['id'], 'room': 'H209', 'source': 'Chưa được trường xác nhận', 'confirmed': False})
        result = agent.weekly_review(self.week, {}, update['id'])
        self.assertTrue(any(i['field'] == 'room' and row['id'] in i['sessions'] for i in result['issues']))
        self.assertIn('Chưa xác nhận', result['notice'])
        self.assertEqual(result['impact']['baseline_kind'], 'source')

    def test_draft_storage_and_no_false_published_history(self):
        saved = store.save_draft({'week': self.week, 'changes': {}, 'update': ''}, tools.fingerprint())
        self.assertEqual(store.get('draft', store.draft_key(self.week, tools.fingerprint()))['saved_at'], saved['saved_at'])
        self.assertIsNone(store.get('published', store.draft_key(self.week, tools.fingerprint())))

    def test_room_conflict_detects_set_overlap(self):
        rows = copy.deepcopy(tools.read_weekly_schedule_data(self.week)['rows'][:2])
        for row in rows:
            row.update(date='2027-04-26', start='09:00', end='13:00', format='offline', room_options=['H209, C401'])
        rows[0]['room'] = 'H209, C401'
        rows[1]['room'] = 'C401'
        issues = tools.validate_schedule_draft(rows)
        self.assertTrue(any(i['field'] == 'room' and len(i['sessions']) == 2 for i in issues))

    def test_parallel_class_shared_lecturer_allowed_but_other_class_blocked(self):
        row = copy.deepcopy(tools.read_weekly_schedule_data(self.week)['rows'][0])
        row.update(teacher='Lecturer A', teachers=['Lecturer A'], room='', format='online', meeting_url='https://meet.example/test')
        other = copy.deepcopy(row); other['id'] += '-parallel'
        self.assertFalse(any(i['field'] == 'teacher' and len(i['sessions']) == 2 for i in tools.validate_schedule_draft([row, other])))
        other['group_id'] = 'other-class'
        self.assertTrue(any(i['field'] == 'teacher' and len(i['sessions']) == 2 for i in tools.validate_schedule_draft([row, other])))

    def test_keyless_mode_is_explicit_not_fake_success(self):
        with patch('agent.model_status', return_value={'ready': False, 'message': 'Chưa có key'}):
            result = agent.weekly_review(self.week, {}, propose=True)
        self.assertEqual(result['method'], 'rules')
        self.assertEqual(result['ai_error'], 'Chưa có key')
        self.assertIsNone(result['usage'])

    def test_real_model_path_with_mocked_transport(self):
        reply = {'text': json.dumps({'choice': 1, 'summary': 'Cần kiểm tra phòng đang chờ xác nhận', 'questions': []}), 'model': 'test-deepseek', 'tokens_in': 55, 'tokens_out': 22}
        with patch('agent.model_status', return_value={'ready': True}), patch('agent.call_model', return_value=reply) as call:
            result = agent.weekly_review(self.week, {}, propose=True)
        call.assert_called_once()
        self.assertEqual(result['method'], 'model')
        self.assertEqual(result['usage']['tokens_in'], 55)

    def test_invalid_ai_plan_rejected(self):
        with patch('agent.model_status', return_value={'ready': True}), patch('agent.call_model', return_value={'text': '{"choice":999}'}):
            result = agent.weekly_review(self.week, {}, propose=True)
        self.assertEqual(result['method'], 'rules')
        self.assertIn('ngoài danh sách', result['ai_error'])

    def test_ai_hallucinated_reference_rejected(self):
        with patch('agent.model_status', return_value={'ready': True}), patch('agent.call_model', return_value={'text': '{"answer":"test", "references":["invented"]}'}):
            with self.assertRaises(ValueError): agent.assistant(self.week, {}, 'Nguồn nào?')

    def test_http_persistence_approval_and_stale_publish(self):
        from web_app import LocalServer, Handler
        server = LocalServer(('127.0.0.1', 0), Handler)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        base = 'http://127.0.0.1:' + str(server.server_port)
        def request(path, body=None):
            req = urllib.request.Request(base + path, data=json.dumps(body).encode() if body is not None else None,
                                         headers={'Content-Type': 'application/json'})
            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    return response.status, json.load(response)
            except urllib.error.HTTPError as response:
                try:
                    return response.code, json.load(response)
                finally:
                    response.close()
        try:
            self.assertEqual(request('/api/weeks')[0], 200)
            week = '2027-04-12'
            draft = {'week': week, 'changes': {row['id']: {'resolution_note': 'Kiểm thử trong DB tạm: xác minh và xử lý ghi chú vận hành.'} for row in tools.read_weekly_schedule_data(week)['rows'] if row['data_warnings']}, 'update': ''}
            self.assertEqual(request('/api/review', draft)[0], 200)
            self.assertIsNotNone(request('/api/draft?week=' + week)[1]['draft'])
            code, approved = request('/api/approve', draft)
            self.assertEqual(code, 200)
            self.assertEqual(request('/api/publish', {'week': week, 'approved_at': approved['approved_at']})[0], 200)
            self.assertEqual(request('/api/review', draft)[0], 200)
            self.assertEqual(request('/api/publish', {'week': week, 'approved_at': approved['approved_at']})[0], 400)
            bad = {'week': week, 'changes': {approved['rows'][0]['id']: {'teacher': 'Invented'}}, 'update': ''}
            self.assertEqual(request('/api/approve', bad)[0], 409)
            self.assertEqual(request('/api/review', {'week': '1900-01-01'})[0], 400)
        finally:
            server.shutdown(); server.server_close(); worker.join(timeout=3)


if __name__ == '__main__':
    unittest.main()
