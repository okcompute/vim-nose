#!/usr/bin/env python
# encoding: utf-8

import unittest


class NotATestCase(object):

    """Class not inheriting from `TestCase`"""

    def not_really_a_test(self):
        pass


class MyTestClass(unittest.TestCase):

    """Template for testing `code_analyzer` behaviour. """

    def __init__(self):
        pass

    def not_a_test_function(self):
        pass

    def test_function_1(self):
        pass

    def test_function_2(self):
        def innner_function():
            def inner_function2():
                pass
        pass
