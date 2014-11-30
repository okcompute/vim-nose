#!/usr/bin/env python
# encoding: utf-8


"""
Process python error output and marks the line of last traceback file. This
is to overcome a lack in Vim errorformat matching pattern. Of my knowlegdge, Vim
cannot match the last line of the Traceback, only the first one. To help vim,
the last line is marked by the characters `=>`.

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

import subprocess
import sys


def _parse_lines(lines):
    """Parse a list of lines from nose output.  Mark the last item of a
    traceback sequence with `*`.

    :param lines: list of nose error output lines.

    """
    results = []
    acc = []
    for line in lines:
        if line.startswith("  File"):
            # Accumulate traceback lines
            acc.append(line)
        elif line.startswith("    ") and acc:
            # Accumulate slitted traceback lines
            acc.append(line)
        else:
            if acc:
                # Traceback lines were accumulated. Find the last line starting
                # with "File  " and mark it.
                for i, l in enumerate(reversed(acc)):
                    if l.startswith("  File"):
                        acc[-(1 + i)] = "*" + l
                        break
                # Inject in results and reset accumulation
                results.extend(acc)
                acc = []
            results.append(line)
    return results


if __name__ == '__main__':
    # Call nose with the current args
    args = ['nosetests']
    args.extend(sys.argv[1:])
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Grab stdout only
    _, stdout = p.communicate()

    # In python3, the byte array needs to be decoded back to a string
    if (sys.version_info > (3, 0)):
        stdout = stdout.decode()

    # Main process
    result = _parse_lines(stdout.splitlines())

    # Send back to stdout the filtered input
    print("\n".join(result))
