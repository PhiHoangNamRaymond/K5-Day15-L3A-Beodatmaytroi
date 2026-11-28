"""Regression checks for the natural-language evaluation entry point."""
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'codebase'))
import agent


class QuestionEntryTests(unittest.TestCase):
    def test_question_reaches_model_with_source_context(self):
        source = {'weeks': {}, 'requests': [], 'workload': [], 'history': [], 'metadata': {}}
        reply = {'text': json.dumps({'answer': 'Cần xác nhận phòng với BTC.'})}
        with patch.object(agent, 'dataset', return_value=source), patch.object(agent, 'call_model', return_value=reply) as model:
            result = agent.answer('Phòng học đã xác nhận chưa?')
        self.assertEqual(result['output'], 'Cần xác nhận phòng với BTC.')
        self.assertEqual(json.loads(model.call_args.args[1])['question'], 'Phòng học đã xác nhận chưa?')

    def test_invalid_model_answer_is_not_presented_as_success(self):
        source = {'weeks': {}, 'requests': [], 'workload': [], 'history': [], 'metadata': {}}
        with patch.object(agent, 'dataset', return_value=source), patch.object(agent, 'call_model', return_value={'text': '{}'}):
            with self.assertRaises(ValueError):
                agent.answer('Phòng học đã xác nhận chưa?')
