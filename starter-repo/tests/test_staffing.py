"""check_staffing counts rooms vs assigned coaches per session group."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'codebase'))
from tools import check_staffing


def row(**fields):
    base = {'id': 'S1', 'group_id': 'G1', 'date': '2027-04-28', 'class_name': 'L3B', 'session': 'LAB 10',
            'start': '14:00', 'end': '18:00', 'format': 'offline', 'room': 'C104, C203, C302',
            'room_status': 'confirmed', 'extra_rooms': [], 'coach': ['Lab Coach A'], 'coaches': ['Lab Coach A', 'Lab Coach B', 'Lab Coach C'],
            'coach_required': True, 'key_coaches': ['Lab Coach K'], 'source': 'sheet!F29'}
    base.update(fields)
    return base


class StaffingTests(unittest.TestCase):
    workload = [{'name': 'Lab Coach A', 'total': '10'}, {'name': 'Lab Coach B', 'total': '2'}, {'name': 'Lab Coach C', 'total': '5'}]

    def test_reports_shortage_overload_and_low_load_candidates(self):
        [item] = check_staffing([row()], self.workload)
        self.assertEqual((item['room_count'], item['coach_count'], item['missing_coaches']), (3, 1, 2))
        self.assertEqual(item['key_coaches'], ['Lab Coach K'])
        self.assertEqual(item['overloaded_assigned'], ['Lab Coach A'])
        self.assertEqual([c['name'] for c in item['candidates_low_load']], ['Lab Coach B', 'Lab Coach C'])

    def test_busy_coach_in_overlapping_session_is_not_a_candidate(self):
        other = row(id='S2', group_id='G2', room='H201', coach=['Lab Coach B'], coaches=['Lab Coach B'])
        item = next(i for i in check_staffing([row(), other], self.workload) if i['group_id'] == 'G1')
        self.assertEqual([c['name'] for c in item['candidates_low_load']], ['Lab Coach C'])

    def test_online_session_needs_no_room_coaches(self):
        self.assertEqual(check_staffing([row(format='online', room='', coach_required=False)], self.workload), [])


if __name__ == '__main__':
    unittest.main()
