@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\membrane_renewal.ps1" -Action Status -Kind SelectiveTransport
pause
