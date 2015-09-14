#!/usr/bin/env python
# encoding: utf-8


"""
Parse standard python traceback output and insert a formatted line this plugin
understand.
"""

from __future__ import print_function

import re

from . import (
    make_error_format,
    match_pattern,
)


def match_file_location(line):
    """
    Extract filename path and line number from a *python* traceback.

    :param line: A string to pattern match against.

    :returns: A dictionary where the key `file_path` holds the file path and the
        key `line_no` the line number. If not matched, the dictionary is empty.
    """
    return match_pattern(
        r'\s+File "(?P<file_path>.*)", line (?P<line_no>.*), in .*$',
        line,
    )


def match_code_pattern(line):
    """
    Returns `True` if the `line` match a traceback source code pattern.

    :param line: A string to pattern match against.

    :returns: `True` if the line match the source code pattern.
    """
    return re.compile(r"\s+.*").match(line) is not None


def parse_traceback(lines):
    """
    Parse a standard *Python* traceback.

    :param lines: An iterator on a list of strings to pattern match against.

    :returns: A list of line where the last one is the added *error format*
        string.
    """
    file_location = None
    result = []
    for line in lines:
        result.append(line)
        location = match_file_location(line)
        if location:
            file_location = location
            continue
        elif match_code_pattern(line):
            continue
        else:
            # Iterate until lines don't match a traceback file location or a
            # source code pattern. *That* list line holds the error description.
            if file_location:
                result.append(
                    make_error_format(
                        file_location['file_path'],
                        file_location['line_no'],
                        line,
                    ),
                )
                break
    return result
