"""
Tools to parse Python code.
"""

# import os
import ast
import _ast
import re
import os


# Shamelessly copied from nose.
testMatch = re.compile(r'(?:^|[\\b_\\.%s-])[Tt]est' % os.sep)


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

    while node and __get_line(node) <= lineno:
        result.append(node)
        node = __get_best_matching_child(node, lineno)

    return result


def __is_test_case(node):
    """ Return `True` if the node match a test case.
    """
    if type(node) is _ast.ClassDef:
        bases = [base.attr for base in node.bases if hasattr(base, 'attr')]
        if 'TestCase' in bases:
            # inherits from unitttet.TestCase
            return True
        if testMatch.match(node.name):
            # Match nose `Test` pattern
            return True
    return False


def __is_test_function(node):
    """ Return `True` if the node match a test function.
    """
    if type(node) is _ast.FunctionDef and \
            testMatch.match(node.name):
        return True


def get_ast_branch_at(file_, position):
    """
    Return the full abstract syntax tree branch up to the root for the requested
    position inside the file.

    :param file_: Filename path.
    :param position: Cursor position. (line,column) tuple.
    """
    module = ast.parse(open(file_).read())
    return __get_best_matching_chain(module, position[0])


def get_test_case_at(file_, position, separator="."):
    """
    Get the dotted separated name of a test class at give `position` in `file_`.
    If no test case can be found, an empty string is returned.

    :param file_: Filename path.
    :param position: Cursor position. (line,column) tuple.
    :param separator: String separator to inject between scope.
    """
    branch = get_ast_branch_at(file_, position)

    # Remove module name
    chain = branch[1:]

    # Traverse the chain to find the first node name matching a test case
    # pattern.
    for node in reversed(chain):
        if __is_test_case(node):
            break
        chain.pop()

    return separator.join([node.name for node in chain])


def get_test_function_at(file_, position, separator="."):
    """
    Get the dot-separated name of a test function at the given `position` in the
    specified `file_`. Stops at the test case, if current position is not inside
    a test function. Finally, returns empty string if position is not inside a
    test case.

    :param file_: Filename path.
    :param position: Cursor position. (line,column) tuple.
    :param separator: String separator to inject between scope.
    """
    branch = get_ast_branch_at(file_, position)

    # Remove module name
    chain = branch[1:]

    for node in reversed(chain):
        if __is_test_function(node):
            break
        # The search stop at test case level if no function found
        if __is_test_case(node):
            return ""
        chain.pop()

    return separator.join([node.name for node in chain])
