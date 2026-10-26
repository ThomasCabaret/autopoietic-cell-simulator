@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\campaign.ps1" -Action Status
pause
