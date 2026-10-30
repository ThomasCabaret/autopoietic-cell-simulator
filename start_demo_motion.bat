@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\mixing.ps1" -Bench demo_motion -Action Start
pause
