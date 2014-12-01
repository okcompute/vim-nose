" autoload/nose.vim
" Author: Pascal Lalancette (okcompute@icloud.com)


if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

function! nose#pre_command()
    let old_path = $PATH
    if has('win32')
        let $PATH=nose#get_virtual_env_path().";".$PATH
    else
        let $PATH=nose#get_virtual_env_path().":".$PATH
    endif
    return old_path
endfunction

function! nose#post_command(old_path)
    let $PATH = a:old_path
endfunction

function! nose#get_virtual_env_path()
    " TODO: Check for prensence of $VIRTUAL_ENV env var
    " TODO: Get VirtualEnv folder from Git configuration if .venv file is not
    " used.
    return nose#read_virtualenv_config_from_file()
endfunction

function! nose#read_virtualenv_config_from_file()
    let venv_config = findfile(".venv", "./;")
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
    path = os.path.normpath(os.path.join(os.path.dirname(venv_config), path))
    if os.name == 'nt':
        path = os.path.join(path, "scripts")
    else:
        path = os.path.join(path, "bin")
    path = path.replace("\\", "/")
    vim.command("let l:path=\"%s\"" % path)
EOF
return l:path
endfunction

function! nose#read_virtualenv_config_from_git()
endfunction

function! nose#read_virtualenv_config_from_env_var()
endfunction

function! nose#get_current_test()
python << EOF
import code_analyzer
import vim
position = vim.current.window.cursor
filename  = vim.current.buffer.name
try:
    test_function = code_analyzer.get_complete_function_name_at(filename, position)
except:
    # No function found because there is an error in the parsed file. Let nose
    # found the error too and show it in the quickfix window.
    test_function = ""
test = filename
if test_function:
    test = test + ":" + test_function
# Always use Posix path (even on Windows)
test = test.replace("\\", "/")
vim.command("let l:test=\"%s\"" % test)
EOF
    return l:test
endfunction

function! nose#run() abort
    let old_path = nose#pre_command()
    let cmd = "make "
    if exists(":Make")
        let l:cmd = ":Make "
    endif
    let args = nose#get_current_test()
    try
        exec l:cmd.l:args
    finally
        call nose#post_command(old_path)
    endtry
endfunction

function! nose#run_all() abort
    let old_path = nose#pre_command()
    echo "Not implemented!"
    call nose#post_command(old_path)
endfunction

function! nose#debug() abort
    let old_path = nose#pre_command()
    let cmd = ":!"
    if exists(":Start")
        let cmd = ":Start "
    elseif has('win32')
        let cmd = ":!start "
    endif
    let args = nose#get_current_test()
    try
        exec l:cmd."nosetests -s ".l:args
    finally
        call nose#post_command(old_path)
    endtry
endfunction
