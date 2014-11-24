" ftplugin/python/nose.vim
" Author: Pascal Lalancette (okcompute@icloud.com)


if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

function! s:get_virtual_env_path()
    " TODO: Check for prensence of $VIRTUAL_ENV env var
    " TODO: Get VirtualEnv folder from Git configuration if .venv file is not
    " used.
    return s:read_virtualenv_config_from_file()
endfunction

function! s:read_virtualenv_config_from_file()
    let venv_config = findfile(".venv", ".;")
    if !filereadable(venv_config)
        return
    endif
python << EOF
import vim
import os

venv_config = vim.eval("venv_config")
path = ""
with open(venv_config) as vc:
    lines = [line for line in vc.readlines() if line]
    path = lines[0].strip()
    path = os.path.normpath(os.path.join(os.path.dirname(venv_config), path, "bin"))
    vim.command("let l:path=\"%s\"" % path)
EOF
return l:path
endfunction

function! s:read_virtualenv_config_from_git()
endfunction

function! s:read_virtualenv_config_from_env_var()
endfunction

function! s:get_current_test()
python << EOF
import code_analyzer
import vim
position = vim.current.window.cursor
filename  = vim.current.buffer.name
test_function = code_analyzer.get_complete_function_name_at(filename, position)
test = filename
if test_function:
    test = test + ":" + test_function
vim.command("let l:test=\"%s\"" % test)
EOF
    return l:test
endfunction

function! s:run_local_test() abort
    let old_path = $PATH
    let $PATH=s:get_virtual_env_path().":".$PATH
    let args = s:get_current_test()
    try
        if exists(":Make")
            echo args
            exec ":Make ".args
        else
            exec ":make". args
        endif
    finally
        let $PATH = old_path
    endtry
endfunction

function! s:run_all() abort
    let old_path = $PATH
    let $PATH=s:get_virtual_env_path().":".$PATH
    "TODO: Implement me!
endfunction

" Set compiler
compiler nose

" Command Mappings
" ================

if !exists(":RunLocal")
    command RunLocal :call <SID>run_local_test()
endif

if !exists(":Run")
    command Run :call <SID>run_all()
endif
