" autoload/nose.vim
" Author: Pascal Lalancette (okcompute@icloud.com)


if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

function! nose#prepare_virtualenv()
    let l:old_path = $PATH
    try
        let l:venv=nose#get_virtual_env_path()
    catch /^No virtualenv/
        if !exists('$VIRTUALENV')
            echo "vim-nose: No virtualenv found!"
            return l:old_path
        endif
    endtry
    if has('win32')
        let $PATH=l:venv.";".$PATH
    else
        let $PATH=l:venv.":".$PATH
    endif
    return l:old_path
endfunction

function! nose#reset_virtualenv(old_path)
    let $PATH = a:old_path
endfunction

function! nose#get_virtual_env_path()
    try
        return nose#read_virtualenv_config_from_file()
    catch /^Configuration not found/
    endtry
    try
        return nose#read_virtualenv_config_from_git()
    catch /^Configuration not found/
    endtry
    throw "No virtualenv configuration found"
endfunction

function! nose#read_virtualenv_config_from_file()
    let venv_config = findfile(".venv", "./;")
    if !filereadable(venv_config)
        throw "Configuration not found.`.venv` file not found."
    endif
python << EOF
import vim
import os
venv_config = vim.eval("venv_config")
path = ""
with open(venv_config) as vc:
    lines = [line for line in vc.readlines() if line]
    path = lines[0].strip()
    # `path` comes from a configured value. Make sure possible `~` gets
    # expanded
    path = os.path.expanduser(path)
    # reminder: os.path.join works with relative and absolute path. If second
    # parameter is an existing absolute path, it will be the returned value.
    path = os.path.normpath(os.path.join(os.path.dirname(venv_config), path))
    if os.name == 'nt':
        path = os.path.join(path, "scripts")
    else:
        path = os.path.join(path, "bin")
    # python is portable and rightfully manage correct path separators on
    # every platform. Vim does it differently. Its all POSIX internally.
    path = path.replace("\\", "/")
    vim.command("let l:path=\"%s\"" % path)
EOF
    return l:path
    endfunction

function! nose#read_virtualenv_config_from_git()
    let l:venv =  system('git config vim-nose.venv')
    if v:shell_error
        throw "Configuration not found. Git not available or virtualenv \
        configuration not set."
    endif
    let l:root = nose#git_repository_root()
python << EOF
import vim
import os
venv = vim.eval("l:venv").strip()
# `venv` comes from a configured value. Make sure possible `~` gets expanded
venv = os.path.expanduser(venv)
root = vim.eval("l:root").strip()
path = os.path.normpath(os.path.join(root, venv))
if os.name == 'nt':
    path = os.path.join(path, "scripts")
else:
    path = os.path.join(path, "bin")
# python is portable and rightfully manage correct path separators on
# every platform. Vim does it differently. Its all POSIX internally.
path = path.replace("\\", "/")
vim.command("let l:path=\"%s\"" % path)
EOF
    return l:path
endfunction

function! nose#git_repository_root()
    let root =  system('git rev-parse --show-toplevel')
    if v:shell_error
        throw "Git not available for project root discovery!"
    endif
    return l:root
endfunction

function! nose#get_current_test(...)
    let l:limit=""
    if a:0
        let l:limit=a:1
    endif
python << EOF
import code_analyzer
import vim
position = vim.current.window.cursor
filename  = vim.current.buffer.name
limit = vim.eval("l:limit")
limit = int(limit) if limit else None
try:
    test_function = code_analyzer.get_complete_function_name_at(filename, position, limit)
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

function! nose#get_current_module()
    return expand("%:p")
endfunction

function! nose#run(...) abort
    let cmd = "make "
    if exists(":Make")
        let l:cmd = ":Make "
    endif
    exec l:cmd.join(a:000)
endfunction

function! nose#debug(...) abort
    let old_path = nose#prepare_virtualenv()
    let cmd = ":!"
    if exists(":Start")
        let cmd = ":Start "
    elseif has('win32')
        let cmd = ":!start "
    endif
    try
        exec l:cmd."nosetests -s ".join(a:000)
    finally
        call nose#reset_virtualenv(old_path)
    endtry
endfunction

function! nose#run_test() abort
    let old_path = nose#prepare_virtualenv()
    try
        call nose#run(nose#get_current_test())
    finally
        call nose#reset_virtualenv(old_path)
    endtry
endfunction

function! nose#run_case() abort
    let level=1
    call nose#run(nose#get_current_test(level))
endfunction

function! nose#run_module() abort
    call nose#run(nose#get_current_module())
endfunction

function! nose#run_all() abort
    try
        call nose#run(nose#git_repository_root())
    catch /^Git/
        echo "Cannot run all tests: ".v:exception
    endtry
endfunction

function! nose#debug_test() abort
    call nose#debug(nose#get_current_test())
endfunction

function! nose#debug_case() abort
    let level=1
    call nose#debug(nose#get_current_test(level))
endfunction

function! nose#debug_module() abort
    call nose#debug(nose#get_current_test())
endfunction

function! nose#debug_all() abort
    try
        call nose#debug(nose#git_repository_root())
    catch /^Git/
        echo "Cannot debug all tests: ".v:exception
    endtry
endfunction
