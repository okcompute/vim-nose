

if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

function! s:GetVirtualEnv()
    " TODO: Check for prensence of $VIRTUAL_ENV env var
    " TODO: Get VirtualEnv folder from Git configuration if .venv file is not
    " used.
    return s:GetVirtualEnvFromConfig()
endfunction

function! s:GetVirtualEnvFromConfig()
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

function! s:GetVirtualEnvFromGit()
endfunction

function! s:GetFilename()
    return expand("%")
endfunction

function! s:GetTest()
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

function! s:GetArguments()
    let filename = s:GetFilename()
    let test_function = s:GetTest()
    " return filename.":".test_function
    return test_function
endfunction


function! s:RunLocal()
    let old_path = $PATH
    let $PATH=s:GetVirtualEnv().":".$PATH
    let args = s:GetArguments()
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

function! s:Run()
    let old_path = $PATH
    let $PATH=s:GetVirtualEnv().":".$PATH
    "TODO: Implement me!
    " let args = s:GetArguments()
    " try
    "     if exists(":Make")
    "         echo args
    "         exec ":Make ".args
    "     else
    "         exec ":make". args
    "     endif
    " finally
    "     let $PATH = old_path
    " endtry
endfunction

" Set compiler
compiler nose

" Command Mappings
" ================

if !exists(":RunLocal")
    command RunLocal :call <SID>RunLocal()
endif

if !exists(":Run")
    command Run :call <SID>Run()
endif
