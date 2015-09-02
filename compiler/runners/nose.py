#!/usr/bin/env python
# encoding: utf-8


"""
Parse nose output and insert a formatted line this plugin understand when an
error is found.
"""

from __future__ import print_function

import re

from .python import parse_traceback

COMMAND = "nosetests"
"""
Terminal command to start nosetests.
"""


def parse(lines):
    """
    Parse a list of lines from nose output.

    :param lines: list of nose error output lines.

    :returns: nose output augmented with specially formatted lines adapted to
        this plugin errorformat which will populate Vim clist.
    """
    results = []
    lines = iter(lines)

    failure = re.compile(r"^=*$")

    for line in lines:
        results.append(line)
        if failure.match(line):
            results.extend(
                parse_traceback(lines),
            )
    return results
