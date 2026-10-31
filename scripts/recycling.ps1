param([ValidateSet('Start','Status','Stop','Resume')][string]$Action='Status')
$ErrorActionPreference='Stop'
$projectRoot=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$pythonPath=Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) { $pythonPath=(Get-Command python).Source }
$driver=Join-Path $PSScriptRoot 'recycling_followup.py'
if ($Action -eq 'Start') {
    $prepared=& $pythonPath $driver prepare
    if ($LASTEXITCODE -ne 0) { throw 'Preparation RV1 echouee.' }
    $job=[string]($prepared | Select-Object -Last 1)
} else {
    $job=(Get-Content -LiteralPath (Join-Path $projectRoot 'outputs\recycling_followups\latest.txt') -Raw).Trim()
}
$job=(Resolve-Path -LiteralPath $job).Path
if ($Action -in @('Start','Resume')) {
    $runAction=if ($Action -eq 'Resume') { 'resume' } else { 'run' }
    $frozenDriver=Join-Path $job 'runtime\scripts\recycling_followup.py'
    $stamp=Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
    $process=Start-Process -FilePath $pythonPath -ArgumentList @(('"{0}"' -f $frozenDriver),$runAction,'--job',('"{0}"' -f $job)) -WorkingDirectory $job -WindowStyle Hidden -RedirectStandardOutput (Join-Path $job "supervisor_$stamp.out.log") -RedirectStandardError (Join-Path $job "supervisor_$stamp.err.log") -PassThru
    Write-Output "RV1 : $job"
    Write-Output "Suivi PID $($process.Id). Etat : recycling_status.bat ; pause : stop_recycling.bat"
} else {
    & $pythonPath $driver $Action.ToLowerInvariant() --job $job
    if ($LASTEXITCODE -ne 0) { throw 'Commande RV1 echouee.' }
}
