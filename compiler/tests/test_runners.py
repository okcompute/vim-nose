#!/usr/bin/env python
# encoding: utf-8

import unittest
from platform import system

from runners import (
    get_parse_function,
    get_command,
    make_error_format,
)
from runners.pytest import parse as pytest_parse
from runners.nose import parse as nose_parse


class TestRunners(unittest.TestCase):

    """Test case for runners package."""

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

    def test_nose_command(self):
        self.assertEqual(
            get_command('nose'),
            "nosetests",
        )

    def test_pytest__command(self):
        if system() == 'windows':
            self.assertEqual(
                get_command('pytest'),
                "py.test.exe --tb=short",
            )
        else:
            self.assertEqual(
                get_command('pytest'),
                "py.test --tb=short",
            )

    def test_make_error_format(self):
        self.assertEqual(
            make_error_format("/a/path", "10", "an error"),
            "/a/path:10 <an error>",
        )
