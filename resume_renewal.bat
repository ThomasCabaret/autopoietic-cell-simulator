@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\minimal_batches.ps1 Renewal Resume
pause
