import unittest
from unittest.mock import Mock, seal

from random import random


class TestMain(unittest.TestCase):
    def test_bpmn_exception(self):
        from capython.main import BpmnException
        code = 123
        exc = BpmnException(code)
        self.assertIsInstance(exc, Exception)
        self.assertEqual(exc.bpmn_code, code)

    def test_vars_prepare(self):
        from capython.main import prepare_vars
        task = Mock()
        storage = {}
        task.get_variables.return_value = storage
        task.get_task_id.return_value = "123"
        task.get_topic_name.return_value = "topic"
        seal(task)
        reserved = ["BpmnException", "__task__", "__task_id__", "__topic__"]

        task.assert_not_called()
        out = prepare_vars(task)
        task.get_task_id.assert_called_once_with()
        task.get_topic_name.assert_called_once_with()
        task.get_variables.assert_called_once_with()

        for key in reserved:
            self.assertIn(key, out)

    def test_vars_clean(self):
        from capython.main import clean_vars, CAPYTHON_KNOWN_VARS
        out = {}
        for key in CAPYTHON_KNOWN_VARS:
            out[key] = random()
        clean_vars(out)
        self.assertEqual(out, {})


if __name__ == "__main__":
    unittest.main()
