#!/usr/bin/env python
# encoding: utf-8

from importlib import import_module


def get_parse_function(runner):
    """
    Return the output parse function for specified runner.

    :param runner: The name of the runner.

    :returns: A callable object.
    """
    return getattr(
        import_module(".".join(["runners", runner])),
        "parse",
    )


def get_command(runner):
    """
    Return the terminal command line use to start the test runner.

    :param runner: The name of the runner.

    :returns: Terminal command to start test runner.
    """
    return getattr(
        import_module(".".join(["runners", runner])),
        "COMMAND",
    )
