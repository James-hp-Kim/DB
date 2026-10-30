@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Setup-NewPC.ps1" %*
set "expertSetupExit=%errorlevel%"
echo.
if not "%expertSetupExit%"=="0" echo Setup did not complete. Read INSTALL_NEW_PC_KO.md.
pause
exit /b %expertSetupExit%
