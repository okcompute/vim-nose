" ftplugin/python/nose.vim
" Author: Pascal Lalancette (okcompute@icloud.com)

if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

" Set compiler
compiler nose

" Command Mappings
" ================

command! -bang RunTest :call nose#run_test(<bang>0)
command! -bang RunCase :call nose#run_case(<bang>0)
command! -bang RunModule :call nose#run_module(<bang>0)
command! -bang RunAllTests :call nose#run_all(<bang>0)
