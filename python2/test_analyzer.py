#!/usr/bin/env python
# encoding: utf-8

import os
import unittest

import code_analyzer


class TestCodeAnalyzer(unittest.TestCase):

    """Test 'code_analyzer.py' module."""

    def setUp(self):
        self.source = os.path.join(os.path.dirname(__file__), "fixture", "code_template.py")

    def tearDown(self):
        pass

    def test_get_function_name_on_definition(self):
        """ Test lookup for function name when the line number is set on the
        function definition. """
        # Note: See `fixture\code_template.py` line # 8
        result = code_analyzer.get_complete_function_name_at(self.source, (12, 0))
        self.assertEqual(result, "MyClass.function_1")

    def test_get_function_name_on_module_last_line(self):
        """ Test lookup for function name when the line number is set to the
        module last line. """
        # Note: See `fixture\code_template.py` line # 16
        result = code_analyzer.get_complete_function_name_at(self.source, (16, 0))
        self.assertEqual(result, "MyClass.function_2")

    def test_get_function_name_on_module_first_line(self):
        """ Test lookup for function name when the line number is set to the
        module first line. """
        # Note: See `fixture\code_template.py` line # 0
        result = code_analyzer.get_complete_function_name_at(self.source, (0, 0))
        self.assertIsNone(result)
