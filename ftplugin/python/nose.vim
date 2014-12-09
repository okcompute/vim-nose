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

if expand("%:r") =~ "test_.*"
    " This is expected to be a test file.
    command! -bang RunTest :call nose#run_test(<bang>0)
    command! -bang RunCase :call nose#run_case(<bang>0)
    command! -bang RunModule :call nose#run_module(<bang>0)
else
    " This is expected to not be a test file. Launch last test instead of
    " trying to find which one to run
    command! -bang RunTest :call nose#run_last_test(<bang>0)
    command! -bang RunCase :call nose#run_last_case(<bang>0)
    command! -bang RunModule :call nose#run_last_module(<bang>0)
endif
