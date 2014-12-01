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

if !exists(":RunTest")
    command RunTest :call nose#run_test()
endif

if !exists(":RunModule")
    command RunModule :call nose#run_module()
endif

if !exists(":RunAll")
    command RunAllTests :call nose#run_all()
endif

if !exists(":Debug")
    command Debug :call nose#debug_test()
endif

if !exists(":DebugModule")
    command DebugModule :call nose#debug_module()
endif

if !exists(":DebugAll")
    command DebugAll :call nose#debug_all()
endif

