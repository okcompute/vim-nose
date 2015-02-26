" ftplugin/python/nose.vim
" Author: Pascal Lalancette (okcompute@icloud.com)

" Only do this when not done yet for this buffer
if exists("b:vim_nose_ftplugin")
    finish
endif
let b:vim_nose_ftplugin = 1

if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

" Set compiler
compiler nose

