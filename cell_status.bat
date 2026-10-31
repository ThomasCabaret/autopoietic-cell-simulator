@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
set "READINESS_PYTHON=python"
if exist ".venv\Scripts\python.exe" set "READINESS_PYTHON=.venv\Scripts\python.exe"
"%READINESS_PYTHON%" experiments\cell_readiness.py status
pause
