#!/usr/bin/env python
# encoding: utf-8


"""
Parse nose output and insert a formatted line this plugin understand when an
error is found.
"""

from __future__ import print_function

import re

from .python import parse_traceback


def parse(lines):
    """
    Parse a list of lines from nose output.  Mark the last item of a
    traceback sequence with `*`.

    :param lines: list of nose error output lines.

    """
    results = []
    lines = iter(lines)

    # 1. Extract 'ERROR collecting', 'failures' and 'captured stderr call'.
    # 2. for each parse filename and error
    # 2. for each case, insert the new formatted line and error message below
    # the error string.

    failure = re.compile(r"^=*$")

    for line in lines:
        results.append(line)
        if failure.match(line):
            results.extend(
                parse_traceback(lines),
            )
    return results
