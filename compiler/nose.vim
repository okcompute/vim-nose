" Vim compiler file
" Compiler:	Nose compiler for running python tests.
" Maintainer:	Pascal Lalancette <okcompute@icloud.com>
" Created: November 29th 2014

if exists(":CompilerSet") != 2		" older Vim always used :setlocal
  command -nargs=* CompilerSet setlocal <args>
endif

" Modified from suggestion found in Vim documentation so the correct file and
" line number are found (see 'nose.py' to understand how the output is
" transformed for this specific 'errorformat').
" CompilerSet efm=%-C\ %.%#,%A*\ \ File\ \"%f\"\\,\ line\ %l%.%#,%Z%[%^\ ]%\\@=%m,%-G%.%#


" CompilerSet efm=
"             " \%-C\ %.%#,
"             \%A*\ \ File\ \"%f\"\\,\ line\ %l%.%#,
"             \%Z%[%^\ ]%\\@=%m,
"             " \%-G%.%#,
"             \%E_%#\ ERROR\ collecting\ %.%#,
"             \%C%f:%l:%.%#,
"             \%ZE\ %#%m

" CompilerSet efm=%A*\ \ File\ \"%f\"\\,\ line\ %l%.%#,%Z%[%^\ ]%\\@=%m,%E_%#\ ERROR\ collecting\ %.%#,%C%f:%l:%.%#,%ZE\ %#%m

" CompilerSet efm=%AE\ %#%m,%ETraceback\ %.%#,%C\  \File\"%f\"\\,\ line\ %l%.%#,%C\ %#,%Z%f:%l:\ %.%#,%Z%.%#:\ %m
CompilerSet efm=%AE\ %#%m,%C\ %#,%Z%f:%l:\ %.%#

" =================================== ERRORS ====================================
" ____________ ERROR collecting okbudget/tests/test_authentication.py ____________
" test_authentication.py:25: in <module>
"     asdfsadf
" E   NameError: name 'asdfsadf' is not defined
" =========================== 1 error in 0.22 seconds ============================
" Celle la marche pour les erreurs
" CompilerSet efm=%E_%#\ ERROR\ collecting\ %.%#,%C%f:%l:%.%#,%C\ \ %#%.%#,%ZE\ %#%m
"
" Celle la marche pour les failures simple
" CompilerSet efm=%AE\ %#%m,%C\ %#,%Z%f:%l:\ %.%#


" Assign a python script to 'makeprg'. This script will launch the test runner
" and transform its output for the configured 'errorformat' above.
let s:path="python ".expand("<sfile>:p:h")
if g:vim_python_runner == 'nose'
    let &l:makeprg=s:path."/runner.py nosetests"
elseif g:vim_python_runner == 'pytest'
    if has('win32') || has('win64')
        " let &l:makeprg=s:path."/runner.py py.test.exe --tb=native"
        let &l:makeprg=s:path."/runner.py py.test.exe --tb=native"
    else
        " let &l:makeprg=s:path."/runner.py py.test --tb=native"
        let &l:makeprg="py.test"
    endif
else
    echoerr "Unknown test runner!: ".g:vim_python_runner
endif
