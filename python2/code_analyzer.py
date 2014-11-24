"""
Tools to parse Python code.
"""

# import os
import ast


def __get_line(node):
    """
    Get the line for the given node, if it has one.
    """
    return getattr(node, 'lineno', -1)


def __get_best_matching_child(node, lineno):
    """
    Get the best matching child of `node` for the given `lineno`.
    """
    # This can be a one-liner with reversed
    # and next but way less readable...
    childs = getattr(node, 'body', [])
    result = next(iter(childs), None)
    result_lineno = __get_line(result)

    for child in childs[1:]:
        child_lineno = __get_line(child)

        if child_lineno > lineno:
            break
        elif child_lineno == lineno:
            return child
        elif child_lineno > result_lineno:
            result = child
            result_lineno = child_lineno

    return result


def __get_best_matching_chain(node, lineno):
    """
    Get the best matching chain.
    """
    result = []

    while node and __get_line(node) < lineno:
        result.append(node)
        node = __get_best_matching_child(node, lineno)

    return result


def get_complete_function_name_at(file_, position, limit=None):
    """
    Get the dot-separated name of the function at the given `position` in the
    specified `file_`.
    """
    module = ast.parse(open(file_).read())
    chain = __get_best_matching_chain(module, position[0])
    names = [node.name for node in chain[1:] if hasattr(node, 'name')]

    if limit is not None:
        names = names[:limit]

    if names:
        return '.'.join(names)
