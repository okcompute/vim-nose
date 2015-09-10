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


def make_error_format(file_path, line_no, error):
    """
    Generate an 'error format` string recognize by Vim compiler.

    :param file_path: The file path from where the error occurred.
    :param line_no: The line number pointing to the erroneous code.
    :param error: The error description.

    :returns: An error format compatible string.
    """
    return '{file_path}:{line_no} <{error}>'.format(
        file_path=file_path,
        line_no=line_no,
        error=error,
    )
