#!/usr/bin/env python
# encoding: utf-8

import unittest

from ..errorformat import (
    # _parse_lines,
    parse_pytest_errors,
    # parse_pytest_failures,
)

input = [
    "===================================================================================== ERRORS =====================================================================================",
    "__________________________________________________________________ ERROR collecting okbudget/tests/test_dal.py ___________________________________________________________________",
    "okbudget/tests/test_dal.py:19: in <module>",
    "    asdfasdf",
    "E   NameError: name 'asdfasdf' is not defined",
    "==================================================================================== FAILURES ====================================================================================",
    "_________________________________________________________________________ TestAuthentication.test_false __________________________________________________________________________",
    "",
    "self = <okbudget.tests.test_authentication.TestAuthentication testMethod=test_false>",
    "",
    "    def setUp(self):",
    ">       super(TestAuthentication, self).setUp()",
    "",
    "okbudget/tests/test_authentication.py:56:",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "okbudget/tests/__init__.py:46: in setUp",
    "    self.user = self.create_user(\"test\", \"test\", \"test@test.com\")",
    "okbudget/tests/__init__.py:96: in create_user",
    "    self.assertEqual(response.code, 200)",
    "E   AssertionError: 500 != 200",
    "------------------------------------------------------------------------------ Captured stderr call ------------------------------------------------------------------------------",
    "ERROR:tornado.application:Uncaught exception POST /api/signup (127.0.0.1)",
    "HTTPServerRequest(protocol='http', host='localhost:55219', method='POST', uri='/api/signup', version='HTTP/1.1', remote_ip='127.0.0.1', headers={'Connection': 'close', 'Content-Type': 'application/json charset=utf-8', 'Host': 'localhost:55219', 'Content-Length': '66', 'Accept-Encoding': 'gzip'})",
    "Traceback (most recent call last):",
    "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/venv/lib/python3.4/site-packages/tornado/web.py\", line 1332, in _execute",
    "    result = method(*self.path_args, **self.path_kwargs)",
    "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/rest/__init__.py\", line 135, in wrapper",
    "    return method(self, *args, **kwargs)",
    "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/rest/__init__.py\", line 105, in request_wrapper",
    "    response = request(self, arguments, *args, **kwargs)",
    "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/rest/authentication.py\", line 105, in post",
    "    body['email']",
    "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/dal.py\", line 257, in create_user",
    "    return self._convert_to_user(user)",
    "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/dal.py\", line 236, in _convert_to_user",
    "    blarg",
    "NameError: name 'blarg' is not defined",
    "ERROR:tornado.access:500 POST /api/signup (127.0.0.1) 4.70ms",
]

expected = [
    "===================================================================================== ERRORS =====================================================================================",
    "__________________________________________________________________ ERROR collecting okbudget/tests/test_dal.py ___________________________________________________________________",
    "okbudget/tests/test_dal.py:19: in <module>",
    "    asdfasdf",
    "*E   NameError: name 'asdfasdf' is not defined",
    "==================================================================================== FAILURES ====================================================================================",
    "_________________________________________________________________________ TestAuthentication.test_false __________________________________________________________________________",
    "",
    "self = <okbudget.tests.test_authentication.TestAuthentication testMethod=test_false>",
    "",
    "    def setUp(self):",
    ">       super(TestAuthentication, self).setUp()",
    "",
    "okbudget/tests/test_authentication.py:56:",
    "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
    "okbudget/tests/__init__.py:46: in setUp",
    "    self.user = self.create_user(\"test\", \"test\", \"test@test.com\")",
    "okbudget/tests/__init__.py:96: in create_user",
    "    self.assertEqual(response.code, 200)",
    "E   AssertionError: 500 != 200",
    "------------------------------------------------------------------------------ Captured stderr call ------------------------------------------------------------------------------",
    "ERROR:tornado.application:Uncaught exception POST /api/signup (127.0.0.1)",
    "HTTPServerRequest(protocol='http', host='localhost:55219', method='POST', uri='/api/signup', version='HTTP/1.1', remote_ip='127.0.0.1', headers={'Connection': 'close', 'Content-Type': 'application/json charset=utf-8', 'Host': 'localhost:55219', 'Content-Length': '66', 'Accept-Encoding': 'gzip'})",
    "Traceback (most recent call last):",
    "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/venv/lib/python3.4/site-packages/tornado/web.py\", line 1332, in _execute",
    "    result = method(*self.path_args, **self.path_kwargs)",
    "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/rest/__init__.py\", line 135, in wrapper",
    "    return method(self, *args, **kwargs)",
    "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/rest/__init__.py\", line 105, in request_wrapper",
    "    response = request(self, arguments, *args, **kwargs)",
    "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/rest/authentication.py\", line 105, in post",
    "    body['email']",
    "  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/dal.py\", line 257, in create_user",
    "    return self._convert_to_user(user)",
    "*  File \"/Users/okcompute/Developer/Git/OkBudgetBackend/okbudget/dal.py\", line 236, in _convert_to_user",
    "    blarg",
    "*NameError: name 'blarg' is not defined",
    "ERROR:tornado.access:500 POST /api/signup (127.0.0.1) 4.70ms",
]


class TestErrorFormat(unittest.TestCase):

    """Test case for errorformat.py module"""

    def test_output(self):
        pass
        # result = _parse_lines(input)
        # self.assertEqual(result, expected)

    def test_parse_python_traceback_file_and_line(self):
        pass

    def test_parse_pytest_failures(self):
        input = [
            "==================================================================================== FAILURES ====================================================================================",
            "_________________________________________________________________________ TestAuthentication.test_false __________________________________________________________________________",
            "",
            "self = <okbudget.tests.test_authentication.TestAuthentication testMethod=test_false>",
            "",
            "    def setUp(self):",
            ">       super(TestAuthentication, self).setUp()",
            "",
            "okbudget/tests/test_authentication.py:56:",
            "_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _",
            "okbudget/tests/__init__.py:46: in setUp",
            "    self.user = self.create_user(\"test\", \"test\", \"test@test.com\")",
            "okbudget/tests/__init__.py:96: in create_user",
            "    self.assertEqual(response.code, 200)",
            "E   AssertionError: 500 != 200",
        ]
        expected = "okbudget/tests/test_authentication.py:56:<AssertionError: 500 != 200>"
        result = parse_pytest_errors(iter(input))
        self.assertEqual(expected, result)

    def test_parse_pytest_errors(self):
        input = [
            "===================================================================================== ERRORS =====================================================================================",
            "__________________________________________________________________ ERROR collecting okbudget/tests/test_dal.py ___________________________________________________________________",
            "okbudget/tests/test_dal.py:19: in <module>",
            "    asdfasdf",
            "E   NameError: name 'asdfasdf' is not defined",
        ]
        expected = "okbudget/tests/test_dal.py:19:<NameError: name 'asdfasdf' is not defined>"
        result = parse_pytest_errors(iter(input))
        self.assertEqual(expected, result)
