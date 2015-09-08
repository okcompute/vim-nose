#!/usr/bin/env python
# encoding: utf-8


"""
Parse pytest error output and insert a formatted line this plugin understand
when an error is found. It works with py.test error and failure output. It also
parse python standard traceback.
"""

from __future__ import print_function

import os
import re
from itertools import chain
from platform import system

from .python import parse_traceback


COMMAND = "py.test --tb=short"
"""
Terminal command to start nosetests.
"""

if system() == 'windows':
    COMMAND = "py.test.exe --tb=short"


def extract_error(line):
    """
    Find and extract a `pytest` error message.

    :param line: A string to pattern match against.

    :returns: If found, the error as a string extracted from the lines.
        Otherwise, `None`.
    """
    error_pattern = re.compile(r"E\s+(?P<error>.*)$")
    m = error_pattern.match(line)
    if not m:
        return None
    return '{}'.format(m.group('error'))


def extract_conftest_error(line):
    """
    Find and extract `ConftestImportFailure` error message.

    :param line: A string to pattern match against.

    :returns: If found, the error as a string extracted from the lines.
        Otherwise, `None`.
    """
    error_pattern = re.compile(
        r"^E\s+_pytest.config.ConftestImportFailure: "
        "\(local\('(?P<filename>.*)'\).*ImportError\(\"(?P<error>.*)\",\).*$",
    )
    m = error_pattern.match(line)
    if not m:
        return None
    return '{filename}:1 <{error}>'.format(
        filename=m.group('filename'),
        error=m.group('error'),
    )


def extract_filename_and_line_no(line):
    """
    Find and extract `pytest` filename and line number from a string.

    :param line: A string to pattern match against.

    :returns: If ound, The error as a string extracted from the lines.
        Otherwise, `None`.
    """
    file_pattern = re.compile(r"(?P<file>.*):(?P<line>.*):.*$")
    m = file_pattern.match(line)
    if not m:
        return None
    result = ":".join(
        [
            m.group('file'),
            m.group('line'),
        ],
    )
    return result


def parse_stderr_call(lines):
    """
    Iterate lines to find `python` error and its location.Return the information
    in a concatenated string.

    :param lines: A list of strings to pattern match against.

    :returns: A string with this pattern: `filename:line <error>`
    """
    filename = None
    results = []
    file_pattern = re.compile(r'\s+File "(?P<file>.*)", line (?P<line>.*), in .*$')
    code_pattern = re.compile(r"\s+.*")
    for line in lines:
        results.append(line)
        m = file_pattern.match(line)
        if m:
            filename = ":".join(
                [
                    m.group('file'),
                    m.group('line'),
                ],
            )
        elif code_pattern.match(line):
            continue
        else:
            if filename:
                results.append(
                    '{filename} <{error}>'.format(
                        filename=filename,
                        error=line,
                    ),
                )
                break
    return results


def parse_failure(lines):
    """
    Iterate lines to find one `pytest` error or failure. Once the error or
    failure, the iteration is stopped (i.e. iterator is not fully consumed).

    :param lines: A list of strings to pattern match against.

    :returns: A list of string where an additional element is added when the
        filename and error have been found.
    """
    filename = None
    error = None
    result = []

    for line in lines:
        result.append(line)
        error = extract_conftest_error(line)
        if error:
            result.append(error)
            break
        error = extract_error(line)
        if error:
            result.append(
                '{filename} <{error}>'.format(
                    filename=filename,
                    error=error,
                ),
            )
            break
        else:
            f = extract_filename_and_line_no(line)
            if f:
                filename = f
    return result


parse_error = parse_failure


def parse_session_failure(lines):
    """
    Parse the output when pytest failed to start a session. One or more
    traceback block are displayed. Last traceback error is formatted to the
    plugin errorformat.

    :param lines: list of pytest error output lines.

    :returns: pytest output augmented with specially formatted lines adapted to
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

    return chain(
        chain(*tracebacks[:-1]),
        parse_traceback(last_traceback),
        last_traceback,  # Note: `parse_traceback` may have not fully consumed the iterator
    )


def parse_fixture_error(root_dir, lines):
    """
    Parse pytest output for a scope error section.

    :param root_dir: Tested project root directory
    :param lines: list of pytest error output lines.

    :returns: pytest output augmented with specially formatted lines adapted to
        this plugin errorformat which will populate Vim clist.
    """
    error_pattern = re.compile(r"ScopeMismatch: (?P<error>.*)$")
    file_pattern = re.compile(r"(?P<file>.*):(?P<line>.*):\s.*$")
    result = []
    for line in lines:
        result.append(line)
        m = error_pattern.match(line)
        if m:
            line = next(lines)
            result.append(line)
            fm = file_pattern.match(line)
            if fm:
                filename = fm.group('file')
                if root_dir:
                    filename = os.path.join(root_dir, filename)
                result.append(
                    '{filename}:{line} <{error}>'.format(
                        filename=filename,
                        line=fm.group('line'),
                        error=m.group('error'),
                    ),
                )
            else:
                return result
    return result


def parse(lines):
    """
    Parse a list of lines from nose output.  Mark the last item of a
    traceback sequence with `*`.

    :param lines: list of pytest error output lines.

    :returns: pytest output augmented with specially formatted lines adapted to
        this plugin errorformat which will populate Vim clist.
    """
    if not lines:
        return []

    results = []

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
        results.append(line)
        if error.match(line):
            results.extend(
                parse_error(lines),
            )
        elif stderr_call.match(line):
            results.extend(
                parse_stderr_call(lines),
            )
        elif fixture_error.match(line):
            results.extend(
                parse_fixture_error(root_dir, lines),
            )
        elif failure.match(line):
            results.extend(
                parse_failure(lines),
            )
    return results
