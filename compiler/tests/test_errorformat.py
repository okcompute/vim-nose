#!/usr/bin/env python
# encoding: utf-8

import unittest

from ..errorformat import _parse_lines


class TestErrorFormat(unittest.TestCase):

    """Test case for errorformat.py module"""

    def test_output(self):
        """ Test the last line beginning with "  File..." gets marked by the
        "=>" character sequence. """
        errors = [
            'E',
            '======================================================================',
            'ERROR: Failure: SyntaxError (invalid syntax (file.py, line 77))',
            '----------------------------------------------------------------------',
            'Traceback (most recent call last):',
            '  File "/venv/lib/python3.4/site-packages/nose/failure.py", line 39, in runTest',
            '    raise self.exc_val.with_traceback(self.tb)',
            '  File "/venv/lib/python3.4/site-packages/nose/loader.py", line 414, in loadTestsFromName',
            '    addr.filename, addr.module)',
            '  File "/venv/lib/python3.4/site-packages/nose/importer.py", line 47, in importFromPath',
            '    return self.importFromDir(dir_path, fqname)',
            '  File "/venv/lib/python3.4/site-packages/nose/importer.py", line 94, in importFromDir',
            '    mod = load_module(part_fqname, fh, filename, desc)',
            '  File "/usr/local/Cellar/python3/3.4.2/Frameworks/Python.framework/Versions/3.4/lib/python3.4/imp.py", line 235, in load_module',
            '    return load_source(name, filename, file)',
            '  File "/usr/local/Cellar/python3/3.4.2/Frameworks/Python.framework/Versions/3.4/lib/python3.4/imp.py", line 171, in load_source',
            '    module = methods.load()',
            '  File "<frozen importlib._bootstrap>", line 1220, in load',
            '  File "<frozen importlib._bootstrap>", line 1200, in _load_unlocked',
            '  File "<frozen importlib._bootstrap>", line 1129, in _exec',
            '  File "<frozen importlib._bootstrap>", line 1471, in exec_module',
            '  File "<frozen importlib._bootstrap>", line 321, in _call_with_frames_removed',
            '  File "/tests/file.py", line 9, in <module>',
            '    from project.test import file',
            '  File "/project/test.py", line 77',
            '    }',
            '    ^',
            'SyntaxError: invalid syntax',
            ''
            '----------------------------------------------------------------------',
            'Ran 1 test in 0.001s',
            ''
            'FAILED (errors=1)', ]

        expected = [
            'E',
            '======================================================================',
            'ERROR: Failure: SyntaxError (invalid syntax (file.py, line 77))',
            '----------------------------------------------------------------------',
            'Traceback (most recent call last):',
            '  File "/venv/lib/python3.4/site-packages/nose/failure.py", line 39, in runTest',
            '    raise self.exc_val.with_traceback(self.tb)',
            '  File "/venv/lib/python3.4/site-packages/nose/loader.py", line 414, in loadTestsFromName',
            '    addr.filename, addr.module)',
            '  File "/venv/lib/python3.4/site-packages/nose/importer.py", line 47, in importFromPath',
            '    return self.importFromDir(dir_path, fqname)',
            '  File "/venv/lib/python3.4/site-packages/nose/importer.py", line 94, in importFromDir',
            '    mod = load_module(part_fqname, fh, filename, desc)',
            '  File "/usr/local/Cellar/python3/3.4.2/Frameworks/Python.framework/Versions/3.4/lib/python3.4/imp.py", line 235, in load_module',
            '    return load_source(name, filename, file)',
            '  File "/usr/local/Cellar/python3/3.4.2/Frameworks/Python.framework/Versions/3.4/lib/python3.4/imp.py", line 171, in load_source',
            '    module = methods.load()',
            '  File "<frozen importlib._bootstrap>", line 1220, in load',
            '  File "<frozen importlib._bootstrap>", line 1200, in _load_unlocked',
            '  File "<frozen importlib._bootstrap>", line 1129, in _exec',
            '  File "<frozen importlib._bootstrap>", line 1471, in exec_module',
            '  File "<frozen importlib._bootstrap>", line 321, in _call_with_frames_removed',
            '  File "/tests/file.py", line 9, in <module>',
            '    from project.test import file',
            '*  File "/project/test.py", line 77',
            '    }',
            '    ^',
            'SyntaxError: invalid syntax',
            ''
            '----------------------------------------------------------------------',
            'Ran 1 test in 0.001s',
            ''
            'FAILED (errors=1)', ]

        result = _parse_lines(errors)
        self.assertEqual(result, expected)
