@echo off
cd /d "%~dp0"
set "MAP_PYTHON=python"
if exist ".venv\Scripts\python.exe" set "MAP_PYTHON=.venv\Scripts\python.exe"
"%MAP_PYTHON%" experiments\build_metabolism_map.py
if errorlevel 1 (
    pause
    exit /b 1
)
start "" "%~dp0docs\metabolism\index.html"
