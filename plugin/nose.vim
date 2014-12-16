" plugin/nose.vim
" Author: Pascal Lalancette (okcompute@icloud.com)

if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif


" Command Mappings
" ================

function! s:set_run_commands()
    if expand("%:r") =~ "test_.*"
        " Filename match test file pattern. Inject normal 'run' commands.
        command! -buffer -bang RunTest :call nose#run_test(<bang>0)
        command! -buffer -bang RunCase :call nose#run_case(<bang>0)
        command! -buffer -bang RunModule :call nose#run_module(<bang>0)
    else
        " For no-test files, run 'remembered' test.
        command! -buffer -bang RunTest :call nose#run_last_test(<bang>0)
        command! -buffer -bang RunCase :call nose#run_last_case(<bang>0)
        command! -buffer -bang RunModule :call nose#run_last_module(<bang>0)
    endif
    " RunAllTest is available everywhere
    command! -bang RunAllTests :call nose#run_all(<bang>0)
endfunction

" For python file, set commands relative to file being a test module or not.
"
" Note: Code is not located in ftplugin voluntary. The file pattern detection
"       requires the logic to be ran in an autocmd.
autocmd BufEnter *.py   call s:set_run_commands()
