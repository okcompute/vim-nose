" Vim compiler file
" Compiler:	Nose compiler for running python tests.
" Maintainer:	Pascal Lalancette <okcompute@icloud.com>
" Created: November 29th 2014

if exists(":CompilerSet") != 2		" older Vim always used :setlocal
  command -nargs=* CompilerSet setlocal <args>
endif

CompilerSet efm=%f:%l\ <%m>

" Assign a python script to 'makeprg'. This script will launch the test runner
" and transform its output for the configured 'errorformat' above.
let s:path="python ".expand("<sfile>:p:h")
if g:vim_python_runner == 'nose'
    let &l:makeprg=s:path."/run.py nose nosetests"
elseif g:vim_python_runner == 'pytest'
    if has('win32') || has('win64')
        let &l:makeprg=s:path."/run.py pytest py.test.exe --tb=short"
    else
        let &l:makeprg=s:path."/run.py pytest py.test --tb=short"
    endif
else
    echoerr "Unknown test runner!: ".g:vim_python_runner
endif
