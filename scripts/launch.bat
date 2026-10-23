@echo off
setlocal
cd /d "%~dp0.."
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" scripts\dispatch.py %*
) else (
  python scripts\dispatch.py %*
)
set "SIM_EXIT=%ERRORLEVEL%"
if not "%SIM_EXIT%"=="0" (
  echo.
  echo La simulation a signale une erreur. Les details sont affiches ci-dessus.
  pause
)
exit /b %SIM_EXIT%
