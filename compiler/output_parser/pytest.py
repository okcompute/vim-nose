#!/usr/bin/env python
# encoding: utf-8


"""
Parse pytest error output and insert a formatted line this plugin understand
when an error is found. It works with py.test error and failure output. It also
parse python standard traceback.
"""

from __future__ import print_function

import re


def parse_error(line):
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


def parse_filename_and_line_no(line):
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


def parse_error_or_failure(lines):
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
        error = parse_error(line)
        if error:
            result.append(
                '{filename} <{error}>'.format(
                    filename=filename,
                    error=error,
                ),
            )
            break
        else:
            f = parse_filename_and_line_no(line)
            if f:
                filename = f
    return result


def parse(lines):
    """
    Parse a list of lines from nose output.  Mark the last item of a
    traceback sequence with `*`.

    :param lines: list of nose error output lines.

    """
    results = []
    lines = iter(lines)

    error = re.compile(r"_* ERROR collecting .* _*")
    failure = re.compile(r"_* .* _*")
    stderr_call = re.compile("-* Captured stderr call -*")

    for line in lines:
        results.append(line)
        if error.match(line):
            results.extend(
                parse_error_or_failure(lines),
            )
        elif stderr_call.match(line):
            results.extend(
                parse_stderr_call(lines),
            )
        elif failure.match(line):
            results.extend(
                parse_error_or_failure(lines),
            )
    return results
