param([ValidateSet('Start','Status','Stop','Resume','Review')][string]$Action='Status')
$ErrorActionPreference='Stop'
$projectRoot=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$pythonPath=Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) { $pythonPath=(Get-Command python).Source }
$driver=Join-Path $PSScriptRoot 'minimal_tool_followup.py'
if ($Action -eq 'Start') {
    $prepared=& $pythonPath $driver prepare
    if ($LASTEXITCODE -ne 0) { throw 'Preparation MIN1 echouee.' }
    $job=[string]($prepared | Select-Object -Last 1)
} else {
    $job=(Get-Content -LiteralPath (Join-Path $projectRoot 'outputs\minimal_tool_followups\latest.txt') -Raw).Trim()
}
$job=(Resolve-Path -LiteralPath $job).Path
if ($Action -in @('Start','Resume')) {
    $runAction=if ($Action -eq 'Resume') { 'resume' } else { 'run' }
    $frozenDriver=Join-Path $job 'runtime\scripts\minimal_tool_followup.py'
    $stamp=Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
    $process=Start-Process -FilePath $pythonPath -ArgumentList @(('"{0}"' -f $frozenDriver),$runAction,'--job',('"{0}"' -f $job)) -WorkingDirectory $job -WindowStyle Hidden -RedirectStandardOutput (Join-Path $job "supervisor_$stamp.out.log") -RedirectStandardError (Join-Path $job "supervisor_$stamp.err.log") -PassThru
    Write-Output "MIN1 : $job"
    Write-Output "Suivi PID $($process.Id). Etat : minimal_tool_status.bat ; pause : stop_minimal_tool.bat"
} else {
    & $pythonPath $driver $Action.ToLowerInvariant() --job $job
    if ($LASTEXITCODE -ne 0) { throw 'Commande MIN1 echouee.' }
}
