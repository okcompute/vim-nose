#!/usr/bin/env python
# encoding: utf-8

import os
import unittest

import code_analyzer


class TestCodeAnalyzer(unittest.TestCase):

    """Test 'code_analyzer.py' module."""

    def setUp(self):
        # Load a python test template module
        self.source = os.path.join(os.path.dirname(__file__), "fixture", "code_template.py")

    def tearDown(self):
        pass

    def test_get_test_function_at_on_definition(self):
        """ Test lookup for function name when the line number is set on the
        function definition. """
        result = code_analyzer.get_test_function_at(self.source, (25, 0))
        self.assertEqual(result, "MyTestClass.test_function_1")

    def test_get_test_function_at_on_module_last_line(self):
        """ Test lookup for function name when the line number is set to the
        module last line. """
        result = code_analyzer.get_test_function_at(self.source, (32, 0))
        self.assertEqual(result, "MyTestClass.test_function_2")

    def test_get_test_function_at_on_module_first_line(self):
        """ Test lookup for function name when the line number is set to the
        module first line. """
        result = code_analyzer.get_test_function_at(self.source, (0, 0))
        self.assertEqual(result, '')

    def test_get_test_function_at_inside_inner_function(self):
        """ Test when cursor position is located inside an inner function of a
        test will return the function name of the test and not the inner
        function. """
        result = code_analyzer.get_test_function_at(self.source, (31, 0))
        self.assertEqual(result, "MyTestClass.test_function_2")

    def test_get_test_function_at_inside_non_test_case(self):
        """ Test when cursor position is located inside a non test case class
        will return an empty string. """
        result = code_analyzer.get_test_function_at(self.source, (9, 0))
        self.assertEqual(result, "")

    def test_get_test_function_at_no_test(self):
        """ Test when cursor position is located inside a non test case class
        and a non test function. """
        result = code_analyzer.get_test_function_at(self.source, (12, 0))
        self.assertEqual(result, "")

    def test_get_test_case_at_on_definition(self):
        """ Test lookup for test case name when the line number is set on the
        case definition. """
        result = code_analyzer.get_test_case_at(self.source, (15, 0))
        self.assertEqual(result, "MyTestClass")

    def test_get_test_case_at_on_module_last_line(self):
        """ Test lookup for case name when the line number is set to the
        module last line. """
        result = code_analyzer.get_test_case_at(self.source, (32, 0))
        self.assertEqual(result, "MyTestClass")

    def test_get_test_case_at_on_module_first_line(self):
        """ Test lookup for case name when the line number is set to the
        module first line. """
        result = code_analyzer.get_test_case_at(self.source, (0, 0))
        self.assertEqual(result, '')
