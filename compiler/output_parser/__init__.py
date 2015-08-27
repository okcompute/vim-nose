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
        import_module(".".join(["output_parser", runner])),
        "parse",
    )
