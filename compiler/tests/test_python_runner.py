#!/usr/bin/env python
# encoding: utf-8

import unittest

from runners.python import (
    match_file_location,
    match_code_pattern,
    parse_traceback,
)


class TestPythonRunner(unittest.TestCase):

    """Test case for runner.python.py module"""

    def test_match_file_location(self):
        input = "  File \"/Users/okcompute/Developer/venv/lib/python3.4/site-packages//config.py\", line 513, in getconftestmodules"
        expected = {
            "file_path": "/Users/okcompute/Developer/venv/lib/python3.4/site-packages//config.py",
            "line_no": "513",
        }
        result = match_file_location(input)
        self.assertEqual(expected, result)

    def test_match_code_pattern(self):
        input = "    mod = conftestpath.pyimport()"
        result = match_code_pattern(input)
        self.assertTrue(result)

    def test_parse_traceback(self):
        input = [
            "ERROR:tornado.application:Uncaught exception POST /api/signup (127.0.0.1)",
            "HTTPServerRequest(protocol='http', host='localhost:55219', method='POST', uri='/api/signup', version='HTTP/1.1', remote_ip='127.0.0.1', headers={'Connection': 'close', 'Content-Type': 'application/json charset=utf-8', 'Host': 'localhost:55219', 'Content-Length': '66', 'Accept-Encoding': 'gzip'})",
            "Traceback (most recent call last):",
            "  File \"/Git/Backend/venv/lib/python3.4/site-packages/tornado/web.py\", line 1332, in _execute",
            "    result = method(*self.path_args, **self.path_kwargs)",
            "  File \"/Git/Backend/application/rest/__init__.py\", line 135, in wrapper",
            "    return method(self, *args, **kwargs)",
            "  File \"/Git/Backend/application/rest/__init__.py\", line 105, in request_wrapper",
            "    response = request(self, arguments, *args, **kwargs)",
            "  File \"/Git/Backend/application/rest/authentication.py\", line 105, in post",
            "    body['email']",
            "  File \"/Git/Backend/application/dal.py\", line 257, in create_user",
            "    return self._convert_to_user(user)",
            "  File \"/Git/Backend/application/dal.py\", line 236, in _convert_to_user",
            "    blarg",
            "NameError: name 'blarg' is not defined",
            "ERROR:tornado.access:500 POST /api/signup (127.0.0.1) 4.70ms",
        ]
        expected = [
            "ERROR:tornado.application:Uncaught exception POST /api/signup (127.0.0.1)",
            "HTTPServerRequest(protocol='http', host='localhost:55219', method='POST', uri='/api/signup', version='HTTP/1.1', remote_ip='127.0.0.1', headers={'Connection': 'close', 'Content-Type': 'application/json charset=utf-8', 'Host': 'localhost:55219', 'Content-Length': '66', 'Accept-Encoding': 'gzip'})",
            "Traceback (most recent call last):",
            "  File \"/Git/Backend/venv/lib/python3.4/site-packages/tornado/web.py\", line 1332, in _execute",
            "    result = method(*self.path_args, **self.path_kwargs)",
            "  File \"/Git/Backend/application/rest/__init__.py\", line 135, in wrapper",
            "    return method(self, *args, **kwargs)",
            "  File \"/Git/Backend/application/rest/__init__.py\", line 105, in request_wrapper",
            "    response = request(self, arguments, *args, **kwargs)",
            "  File \"/Git/Backend/application/rest/authentication.py\", line 105, in post",
            "    body['email']",
            "  File \"/Git/Backend/application/dal.py\", line 257, in create_user",
            "    return self._convert_to_user(user)",
            "  File \"/Git/Backend/application/dal.py\", line 236, in _convert_to_user",
            "    blarg",
            "NameError: name 'blarg' is not defined",
            "/Git/Backend/application/dal.py:236 <NameError: name 'blarg' is not defined>",
        ]
        result = parse_traceback(input)
        self.assertEqual(expected, result)
