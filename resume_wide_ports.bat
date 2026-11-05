@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\membrane_renewal.ps1 -Action Resume -Kind Wide
pause
