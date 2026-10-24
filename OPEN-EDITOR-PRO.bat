@echo off
title SLOOP Pro editor
cd /d "%~dp0"
if not exist build\sloop-pro-site\webapp\editor\index.html (
  echo The editor is not built yet: run INSTALL-SLOOP-PRO.bat first.
  pause
  exit /b 1
)
start "" http://localhost:8767/webapp/editor/
echo SLOOP Pro editor: http://localhost:8767/webapp/editor/  (keep this window open while you use it)
python -m http.server 8767 --bind 127.0.0.1 --directory build/sloop-pro-site
pause
