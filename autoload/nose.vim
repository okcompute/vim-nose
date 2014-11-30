" autoload/nose.vim
" Author: Pascal Lalancette (okcompute@icloud.com)


if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

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

function! nose#run(args, ...) abort
    let l:foreground = a:0 > 0 ? a:1 : 0
    let old_path = $PATH
    if has('win32')
        let $PATH=nose#get_virtual_env_path().";".$PATH
    else
        let $PATH=nose#get_virtual_env_path().":".$PATH
    endif
    try
        if exists(":Make") && !l:foreground
            exec ":Make ".a:args
        else
            exec ":make". a:args
        endif
    finally
        let $PATH = old_path
    endtry
endfunction

function! nose#run_local() abort
    let args = nose#get_current_test()
    call nose#run(args)
endfunction

function! nose#debug() abort
    let args = nose#get_current_test()
    call nose#run(args." -s", 1)
endfunction

function! nose#run_all() abort
    let args = nose#get_all_test()
    call nose#run(args)
endfunction