@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\membrane_renewal.ps1" -Action Stop -Kind Mixed
pause
