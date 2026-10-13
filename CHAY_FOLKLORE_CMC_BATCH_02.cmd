@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0CHAY_CMC_BATCH_02.ps1"
set RET=%ERRORLEVEL%
echo.
if not "%RET%"=="0" echo Tool reported an error. No success claimed.
echo Press any key to close this window.
pause >nul
exit /b %RET%
