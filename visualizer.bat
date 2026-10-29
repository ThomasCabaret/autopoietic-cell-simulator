@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" -m visualizer %*
) else (
  python -m visualizer %*
)
if errorlevel 1 (
  echo Installation de l'interface : install_visualizer.bat
  pause
)
