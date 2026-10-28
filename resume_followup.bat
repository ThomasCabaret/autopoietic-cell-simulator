@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\numerical_followup.ps1" -Action Resume
pause
