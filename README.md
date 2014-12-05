vim-nose
========

Plugin wrapping `nosetests` command line tool to execute python tests inside Vim. All in the name of productivity!

Features
========

This plugin improve on Vim compiler option by adding some features specific
to nose:

    - Configurable python virtual environment. Independent on your terminal or
      current virtual environment.
    - Isolate tests to be run. Run a specific test, a test case, a test module
      or all tests inside a git repository.
    - Improved vim *errorformat* detection. *quickfix* window will show the
      correct error lines (surprisingly, it was not intuitive as one would
think to enable!)

Requirements
============

For this plugin to have some values, you need this requirements to be
installed in your environment:
    - python
    - [nose](https://nose.readthedocs.org)

These requirement are optional but improve the plugin usage:
    - git
    - [vim-dispatch](https://github.com/tpope/vim-dispatch) by Tim Pope to run tests asynchronously
        .
VirtualEnv Configuration
========================

Plugin support two configuration option to help discovery of virtual environment (See plugin documentation for more details).
    1. A configuration file usually located at the root of your project.
    1. A git configuration (`vim-nose.venv`) in your git repository

If none of those configuration are set, the plugin will use either the system environment or any virtualenv already set in Vim process (terminal only).

Usage
=====

**RunTest**            Run the current test surrounding the cursor position.
                       Otherwise, run all tests in the scope the cursor is
                       located in (i.e. test case or module).

**RunTest!**           Like **RunTest** will start an interactive shell
                       instead of running in the background. This is useful
                       for debugging your test or program (ex.: pdb or ipdb).

**RunCase**            Run all tests found in the test case surrounding the
                       cursor position. If cursor is outside a test case
                       scope, all tests for the module (buffer) are run.

**RunCase!**           Like **RunCase** will start an interactive shell
                       instead of running in the background. This is useful
                       for debugging your test or program (ex.: pdb or ipdb).

**RunModule**          Run all tests found in the current module (buffer).

**RunModule!**         Like **RunModule** will start an interactive shell
                       instead of running in the background. This is useful
                       for debugging your test or program (ex.: pdb or ipdb).

**RunAllTests**        Run all tests found in the git repository of the
                       edited buffer.

**RunAllTests!**       Like **RunAllTests** but will start an interactive shell
                       instead of running in the background. This is useful
                       for debugging your test or program (ex.: pdb or ipdb).

License
=======

Copyright © Pascal Lalancette. Distributed under the same terms as Vim itself. See :help license.
