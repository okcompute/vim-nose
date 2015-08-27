#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Launch test runner and parse output to insert formatted lines this plugin
understand through its pre-configured Vim 'errorformat'.
"""

from __future__ import print_function

import subprocess
import sys

from output_parser import get_parse_function


def run(runner, args):
    """
    Run test tests and prints out parsed output result in stdout.

    :param runner: Name of the runner to be used.
    :param args: List of command arguments for the test runner.
    """

    # Call tests runner with the current args
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # In python3, the byte array needs to be decoded back to a string
    if (sys.version_info > (3, 0)):
        stdout = stdout.decode()
        stderr = stderr.decode()

    output = "".join([stdout, stderr])

    parse = get_parse_function(runner)

    result = parse(output.splitlines())
    print("\n".join(result))

if __name__ == "__main__":
    run(
        runner=sys.argv[1],
        args=sys.argv[2:],
    )
