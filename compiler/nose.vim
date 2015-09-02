" Vim compiler file
" Compiler:	Nose compiler for running python tests.
" Maintainer:	Pascal Lalancette <okcompute@icloud.com>
" Created: November 29th 2014

if exists(":CompilerSet") != 2		" older Vim always used :setlocal
  command -nargs=* CompilerSet setlocal <args>
endif

CompilerSet efm=%f:%l\ <%m>

" Assign a python script to 'makeprg'. It will launch the runner and transform
" its output for the configured 'errorformat' above.
let s:path="python ".expand("<sfile>:p:h")
let &l:makeprg=s:path."/run.py ".g:vim_python_runner
