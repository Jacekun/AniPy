pyinstaller main_win.spec
md   "dist\output" >nul 2>&1
md   "dist\files" >nul 2>&1
copy "main_win.ui" "dist\files"
copy "LICENSE" "dist"
copy "README.md" "dist"