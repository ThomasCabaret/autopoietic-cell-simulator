@echo off
setlocal
cd /d "%~dp0.."
for %%C in (copy membrane expression no_gene) do (
  call scripts\launch.bat --config demonstrators/configs/%%C.json --no-trajectory
  if errorlevel 1 goto failed
)
echo.
echo Toutes les simulations sont terminees. Resultats dans outputs\.
pause
exit /b 0
:failed
echo Au moins une verification de demonstration a echoue.
pause
exit /b 1
