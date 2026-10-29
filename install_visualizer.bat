@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  py -3.12 -m venv .venv
  if errorlevel 1 goto failed
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt -r requirements-viewer.txt
if errorlevel 1 goto failed
echo Interface Qt/OpenGL installee. Lancer visualizer.bat
pause
exit /b 0
:failed
echo Installation interrompue. Consulter le message ci-dessus.
pause
exit /b 1
