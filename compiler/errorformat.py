#!/usr/bin/env python
# encoding: utf-8


"""
Process python error output and marks the line of last traceback file. This
is to overcome a lack in Vim errorformat matching pattern. To my knowledge, Vim
cannot match the last line of the Traceback, only the first one. To help Vim,
the last line is marked by the characters `*`.

Before:
=======

  File "<X>", line 1, in function
  File "<Y>", line 2, in function
  File "<Y>", line 3, in function
SyntaxError: invalid syntax

After:
======

  File "<X>", line 1, in function
  File "<Y>", line 2, in function
=>File "<Y>", line 3, in function
SyntaxError: invalid syntax
"""

from __future__ import print_function

import re
import subprocess
import sys


# def _parse_lines(lines):
#     """Parse a list of lines from nose output.  Mark the last item of a
#     traceback sequence with `*`.

#     :param lines: list of nose error output lines.

#     """
#     results = []
#     acc = []
#     for line in lines:
#         if line.startswith("  File"):
#             # Accumulate traceback lines
#             acc.append(line)
#         elif line.startswith("    ") and acc:
#             # Accumulate slitted traceback lines
#             acc.append(line)
#         else:
#             if acc:
#                 # Traceback lines were accumulated. Find the last line starting
#                 # with "File  " and mark it.
#                 for i, l in enumerate(reversed(acc)):
#                     if l.startswith("  File"):
#                         acc[-(1 + i)] = "*" + l
#                         break
#                 # Inject in results and reset accumulation
#                 results.extend(acc)
#                 acc = []
#             results.append(line)
#     return results


def parse_python_file_traceback(line):
    return []


def parse_pytest_error(lines):
    """
    Iterate lines to find expected `pytest` error pattern.
    """
    error_pattern = re.compile(r"E\s+(?P<error>.*)$")
    for line in lines:
        m = error_pattern.match(line)
        if m:
            return '<{}>'.format(m.group('error'))
    return '<>'


def parse_pytest_filename_and_line_no(lines):
    """
    Iterate lines to find expected `pytest` filename and line number pattern.
    """
    file_pattern = re.compile(r"(?P<file>.*):(?P<line>.*):.*$")
    result = None
    for line in lines:
        m = file_pattern.match(line)
        if m:
            error = parse_pytest_error(lines)
            result = ":".join(
                [
                    m.group('file'),
                    m.group('line'),
                    error,
                ],
            )
            break
    return result

def parse_pytest_errors(lines):
    """
    Iterate lines to find expected `pytest` error section.
    """
    error_pattern = re.compile(r"*- .* -*")
    for line in lines:
        m = error_pattern.match(line)
        if m:
            return '<{}>'.format(m.group('error'))
    return '<>'




def _parse_lines(lines):
    """
    Parse a list of lines from nose output.  Mark the last item of a
    traceback sequence with `*`.

    :param lines: list of nose error output lines.

    """
    results = []
    lines = iter(lines)

    pytest_errors = re.compile("=* ERRORS =*")
    pytest_failures = re.compile("=* FAILURES =*")
    pytest_stderr = re.compile("-*  Captured stderr cal -*")
    pytest_error = re.compile(r"*- ERROR .* -*")
    pytest_failure = re.compile(r"*- .* -*")

    for line in lines:
        if python_errors.match(line):
            continue
        if python_failures.match(line):
            continue
        if python_std_error.match(line):
            results.extend(
                parse_python_file_traceback(lines),
            )
        elif pytest_error.match(line):
            results.extend(
                parse_filelane_(lines),
            )
            results.extend(
                parse_pytest_error(lines),
            )
        elif pytest_failure.match(line):
            results.extend(
                parse_pytest_failures(lines),
            )
    return results


def run_tests(args):
    """
    Run test tests and prints out result in stdout.

    :param args: List of command arguments for launching the test runner. The
        first element of the list is the test runner command.
    """
    # Call tests runner with the current args
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Grab stdout only
    stdout, stderr = p.communicate()

    # In python3, the byte array needs to be decoded back to a string
    if (sys.version_info > (3, 0)):
        stdout = stdout.decode()
        stderr = stderr.decode()

    output = "".join([stdout, stderr])

    # Main process
    result = _parse_lines(output.splitlines())

    # Send back to stdout the filtered input
    print("\n".join(result))

if __name__ == '__main__':
    run_tests(sys.argv[1:])
