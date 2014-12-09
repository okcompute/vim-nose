" plugin/nose.vim
" Author: Pascal Lalancette (okcompute@icloud.com)

if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

" Init variable for last run test 'memorization'.
let g:nose#last_test = ""
let g:nose#last_test_case = ""
let g:nose#last_test_module = ""

" Command Mappings
" ================

" On all filetype other than python, try to re-run the latest test.
command! -bang RunTest :call nose#run_last_test(<bang>0)
command! -bang RunCase :call nose#run_last_test_case(<bang>0)
command! -bang RunModule :call nose#run_last_test_module(<bang>0)

" RunAllTest is available everywhere
command! -bang RunAllTests :call nose#run_all(<bang>0)
