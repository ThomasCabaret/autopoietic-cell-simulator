@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\campaign.ps1" -Action Status
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" scripts\population_report.py
) else (
  python scripts\population_report.py
)
pause
