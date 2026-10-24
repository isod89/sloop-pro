@echo off
title SLOOP Pro installer
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build-sloop-pro.ps1"
pause
