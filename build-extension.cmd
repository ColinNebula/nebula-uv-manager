@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build-extension.ps1"
if errorlevel 1 (
  exit /b 1
)
exit /b 0
