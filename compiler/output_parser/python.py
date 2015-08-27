#!/usr/bin/env python
# encoding: utf-8


"""
Parse standard python traceback output and insert a formatted line this plugin
understand.
"""

from __future__ import print_function

import re


def parse_traceback(lines):
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
