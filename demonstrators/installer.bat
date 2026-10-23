@echo off
setlocal
cd /d "%~dp0.."
echo Installation locale dans .venv pour Python 3.12.
if not exist ".venv\Scripts\python.exe" (
  py -3.12 -m venv .venv
  if errorlevel 1 goto failed
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto failed
echo Installation terminee.
pause
exit /b 0
:failed
echo Installation interrompue. Python 3.12 et un acces au reseau sont necessaires.
pause
exit /b 1
