@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\mixing.ps1" -Bench membrane_diagnostic -Action Analyze
pause
