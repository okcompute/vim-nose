#!/usr/bin/env python
# encoding: utf-8


"""
Parse *pytest* error output and insert a formatted line this plugin understand
when an error is found. It works with py.test error and failure output. It also
parse python standard traceback.
"""

from __future__ import print_function

import os
import re
from itertools import chain
from platform import system

from . import (
    make_error_format,
    match_pattern,
)
from .python import (
    parse_traceback,
)


COMMAND = "py.test --tb=short"
"""
Terminal command to start nosetests.
"""

if system() == 'windows':
    COMMAND = "py.test.exe --tb=short"


def match_scope_mismatch(line):
    """
    Extract error description from a *pytest's* `ScopeMismatch` exception
    output.

    :param line: A string to pattern match against.

    :returns: A dictionary where the key `error` holds the error description. If
        not matched, the dictionary is empty.
    """
    result = match_pattern(r"ScopeMismatch: (?P<error>.*)$", line)
    return result.get('error')


def match_file_location(line):
    """
    Extract filename path and line number from a *pytest* formatted file
    location string.

    :param line: A string to pattern match against.

    :returns: A dictionary where the key `file_path` holds the file path and the
        key `line_no` the line number. If not matched, the dictionary is empty.
    """
    return match_pattern(r"(?P<file_path>.*):(?P<line_no>.*):\s.*$", line)


def match_error(line):
    """
    Extract error description from *pytest* error description.

    :param line: A string to pattern match against.

    :returns: A dictionary where the key `error` holds the error description. If
        not matched, the dictionary is empty.
    """
    return match_pattern(r"E\s+(?P<error>.*)$", line)

match_failure = match_error
"""
Alias for `match_error`.
"""


def match_conftest_error(line):
    """
    Extract `ConftestImportFailure` error message from a string.

    :param line: A string to pattern match against.

    :returns: A dictionary where the key `file_path` holds the file path and the
        key `error` the error description. If not matched, the dictionary is
        empty.
    """
    return match_pattern(
        r"^E\s+_pytest.config.ConftestImportFailure: "
        "\(local\('(?P<file_path>.*)'\).*ImportError\(\"(?P<error>.*)\",\).*$",
        line,
    )


def parse_failure(lines):
    """
    Iterate lines to find one *pytest* error or failure. Once the error or
    failure, the iteration is stopped (i.e. iterator is not fully consumed).

    :param lines: A list of strings to pattern match against.

    :returns: A list of string where an additional element is added when the
        filename and error have been found.
    """
    location = None
    result = []

    for line in lines:
        result.append(line)
        conftest_error = match_conftest_error(line)
        if conftest_error:
            result.append(
                make_error_format(
                    conftest_error['file_path'],
                    1,
                    conftest_error['error'],
                ),
            )
            break
        failure = match_failure(line)
        if failure and location:
            result.append(
                make_error_format(
                    location['file_path'],
                    location['line_no'],
                    failure['error'],
                ),
            )
            break
        else:
            file_location = match_file_location(line)
            if file_location:
                location = file_location
    return result


parse_error = parse_failure


def parse_session_failure(lines):
    """
    Parse the output when *pytest* failed to start a session. One or more
    traceback block are displayed. Last traceback error is formatted to the
    plugin errorformat.

    :param lines: list of *pytest* error output lines.

    :returns: *pytest* output augmented with specially formatted lines adapted to
        this plugin errorformat which will populate Vim clist.
    """
    def get_traceback(lines):
        """ Iterates  on traceback block found in lines.  """
        traceback = []
        for line in lines:
            traceback.append(line)
            if line == '':
                yield traceback
                traceback = []
        yield traceback

    tracebacks = list(get_traceback(lines))

    # Note: It is possible for a session failure to output a sequence of
    # tracebacks. In all scenarios, parse only the last one because it is the
    # error origin.
    last_traceback = iter(tracebacks[-1])

    return list(
        chain(
            chain(*tracebacks[:-1]),
            parse_traceback(last_traceback),
            last_traceback,  # Note: `parse_traceback` may have not fully consumed the iterator
        ),
    )


def parse_fixture_error(root_dir, lines):
    """
    Parse *pytest* output of a *fixture error* section.

    :param root_dir: Tested project root directory
    :param lines: list of *pytest* error output lines.

    :returns: *pytest* output augmented with specially formatted lines adapted to
        this plugin errorformat which will populate Vim clist.
    """
    result = []
    for line in lines:
        result.append(line)
        error = match_scope_mismatch(line)
        if error:
            line = next(lines)
            result.append(line)
            file_location = match_file_location(line)
            if file_location:
                file_path = file_location['file_path']
                if root_dir:
                    file_path = os.path.join(root_dir, file_path)
                result.append(
                    make_error_format(
                        file_path,
                        file_location['line_no'],
                        error,
                    ),
                )
            else:
                return result
    return result


def parse(lines):
    """
    Parse a list of lines from *pytest* output and inject compatible *error
    format* lines when errors are found..

    :param lines: List of *pytest* error output lines.

    :returns: *pytest* output augmented with specially formatted lines adapted to
        this plugin *error format* which will populate Vim's clist.
    """
    if not lines:
        return []

    result = []

    if not re.match(r"=* test session starts =*", lines[0]):
        return parse_session_failure(lines)

    root_dir = None
    m = re.match(r"rootdir: (?P<root>.*), inifile: (?P<ini>.*)$", lines[2])
    if m:
        root_dir = m.group('root')

    lines = iter(lines)

    error = re.compile(r"_* ERROR collecting .* _*")
    failure = re.compile(r"_* .* _*")
    stderr_call = re.compile("-* Captured stderr call -*")
    fixture_error = re.compile("_* ERROR at setup of .*")

    for line in lines:
        result.append(line)
        if error.match(line):
            result.extend(
                parse_error(lines),
            )
        elif stderr_call.match(line):
            result.extend(
                parse_traceback(lines),
            )
        elif fixture_error.match(line):
            result.extend(
                parse_fixture_error(root_dir, lines),
            )
        elif failure.match(line):
            result.extend(
                parse_failure(lines),
            )
    return result
