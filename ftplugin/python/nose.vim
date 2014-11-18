

" autocmd BufRead * call s:SetLocalVimrc()
"
if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

function! s:GetVirtualEnv()
    " TODO: Check for prensence of $VIRTALENV env var
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
    path = lines[0]
    path = os.path.normpath(os.path.join(os.path.dirname(venv_config), path))
    path = os.path.join(path, "bin")
    vim.command("let l:path=\"%s\"" % path)
EOF
return l:path
endfunction

function! s:GetVirtualEnvFromGit()
endfunction

function! s:GetFilename()
    return "/users/okcompute/Developer/Git/OkBudgetBackend/okbudget/tests/test_dal.py"
endfunction

function! s:GetTest()
    return "TestDal.test_create_envelope"
endfunction

function! s:GetArguments()
    let filename = s:GetFilename()
    let test = s:GetTest()
    return filename.":".test
endfunction

    " " Read the .vimproj file one line at a time
    " let lines = readfile(venv_config)
    " for n in lines
    "     " Look for commented line
    "     let endIndex = matchend(n, '\c\s*\zs'.s:VIMPROJ_COMMENTS_LINE.'.*')
    "     if endIndex != -1
    "         " Skip this line
    "         continue
    "     endif
    "     " Look for 'files' tag
    "     let endIndex = matchend(n, '\c\s*\zs'.s:VIMPROJ_KEY_FILES.'\s*=')
    "     if endIndex != -1
    "         call s:ShowDebugMsg("Found files list: ".n)
    "         let projectFiles = s:ResolveFiles(a:projectPath, split(strpart(n,endIndex)))
    "         continue
    "     endif
    " endfor

    " if !exists("g:vimprojDict")
    "     " Make sure the project dict is initialized
    "     let g:vimprojDict = {}
    "     echomsg "VimProj : Project \'".a:projectPath."\' added (".len(projectFiles)." files)"
    " endif

    " "This is the first time this project is added to the dictionnary.
    " "Now is the good time to generate tags.
    " "Note: Auto updates of tags are not handled by vimproj.
    " "Suggestion: Install the Autotags.vim plugin.
    " call s:CreateCtags(a:projectPath)

    " " Save the project info in a global dict shared by all buffers
    " let g:vimprojDict[a:projectPath] = [projectFiles]

function! s:RunTest()
    let virtualenv = s:GetVirtualEnv()
    let path = $PATH
    let $PATH = virtualenv.":".$PATH
    try
        if exists(":Make")
            " echo $PATH
            " exec "echo $PATH"
            exec "echo \"using dispatch\" $PATH"
            exec ":Make ".s:GetArguments()
        else
            exec "echo \"not using dispatch\"".$PATH
            exec ":make"
        endif
    finally
        let $PATH = path
    endtry
endfunction

command! RunTest call s:RunTest()
