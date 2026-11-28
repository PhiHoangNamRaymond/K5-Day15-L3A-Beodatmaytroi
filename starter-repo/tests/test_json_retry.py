"""A malformed model reply is retried once; a second failure is still reported, never shown as success."""
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'codebase'))
import agent

SOURCE = {'weeks': {}, 'requests': [], 'workload': [], 'history': [], 'metadata': {}}


def reply(text):
    return {'text': text, 'model': 'test', 'tokens_in': 1, 'tokens_out': 1}


class JsonRetryTests(unittest.TestCase):
    def test_invalid_json_then_valid_answer_succeeds(self):
        replies = [reply('not json {'), reply(json.dumps({'answer': 'Cần BTC xác nhận phòng.'}))]
        with patch.object(agent, 'dataset', return_value=SOURCE), patch.object(agent, 'call_model', side_effect=replies) as model:
            result = agent.answer('Phòng học đã xác nhận chưa?')
        self.assertEqual(result['output'], 'Cần BTC xác nhận phòng.')
        self.assertEqual(model.call_count, 2)

    def test_missing_answer_is_retried_only_once(self):
        with patch.object(agent, 'dataset', return_value=SOURCE), patch.object(agent, 'call_model', return_value=reply('{}')) as model:
            with self.assertRaises(ValueError):
                agent.answer('Phòng học đã xác nhận chưa?')
        self.assertEqual(model.call_count, 2)

    def test_provider_error_is_not_retried(self):
        with patch.object(agent, 'call_model', side_effect=RuntimeError('Nhà cung cấp đang giới hạn lượt gọi.')) as model:
            with self.assertRaises(RuntimeError):
                agent.ask_json({'task': 'x'})
        self.assertEqual(model.call_count, 1)


if __name__ == '__main__':
    unittest.main()
