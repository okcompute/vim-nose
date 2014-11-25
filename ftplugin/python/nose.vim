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

if !exists(":RunLocal")
    command RunLocal :call nose#run_local()
endif

if !exists(":RunLocalForeground")
    command RunLocalForeground :call nose#run_local_foreground()
endif

if !exists(":Run")
    command Run :call nose#run_all()
endif
