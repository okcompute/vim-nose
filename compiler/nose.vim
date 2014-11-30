" Vim compiler file
" Compiler:	Nose compiler for running python tests.
" Maintainer:	Pascal Lalancette <okcompute@icloud.com>
" Created: November 29th 2014

if exists("current_compiler")
  finish
endif
let current_compiler = "nose"

if exists(":CompilerSet") != 2		" older Vim always used :setlocal
  command -nargs=* CompilerSet setlocal <args>
endif

" Modified from vim documentation so the correct file is found (see 'nose.py'
" to understand how the output is transformed for this specific 'errorformat').
CompilerSet efm=%-C\ %.%#,%A*\ \ File\ \"%f\"\\,\ line\ %l%.%#,%Z%[%^\ ]%\\@=%m,%-G%.%#

" Assign a python script to 'makeprg'. This script will launch 'nose' and
" transform its output for the configured 'errorformat' above.
let s:nose="python ".expand("<sfile>:p:h")."/nose.py"
let &l:makeprg=s:nose
