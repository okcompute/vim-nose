#!/usr/bin/env python
# encoding: utf-8

import unittest

from output_parser import (
    get_parse_function,
)
from output_parser.pytest import parse as pytest_parse
from output_parser.nose import parse as nose_parse


class TestParser(unittest.TestCase):

    """Test case for parser.py module"""

    def test_get_pytest_parse_function(self):
        self.assertEqual(
            get_parse_function('pytest'),
            pytest_parse,
        )

    def test_get_nose_parse_function(self):
        self.assertEqual(
            get_parse_function('nose'),
            nose_parse,
        )
