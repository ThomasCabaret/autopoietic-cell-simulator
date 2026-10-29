@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\mixing.ps1" -Bench motion -Action Status
pause
