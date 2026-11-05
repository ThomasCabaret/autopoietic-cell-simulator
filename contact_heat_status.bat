@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\turnover_probe.ps1 -Action Status -Kind Thermal
pause
