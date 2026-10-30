param([ValidateSet('Start','Status','Stop','Resume')][string]$Action='Status')
$ErrorActionPreference='Stop'
$projectRoot=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$pythonPath=Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) { $pythonPath=(Get-Command python).Source }
$driver=Join-Path $PSScriptRoot 'expression_followup.py'
if ($Action -eq 'Start') {
    $prepared=& $pythonPath $driver prepare
    if ($LASTEXITCODE -ne 0) { throw 'Preparation T9E echouee.' }
    $job=[string]($prepared | Select-Object -Last 1)
} else {
    $job=(Get-Content -LiteralPath (Join-Path $projectRoot 'outputs\expression_followups\latest.txt') -Raw).Trim()
}
$job=(Resolve-Path -LiteralPath $job).Path
if ($Action -in @('Start','Resume')) {
    $runAction=if ($Action -eq 'Resume') { 'resume' } else { 'run' }
    $frozenDriver=Join-Path $job 'runtime\scripts\expression_followup.py'
    $stamp=Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
    $process=Start-Process -FilePath $pythonPath -ArgumentList @(('"{0}"' -f $frozenDriver),$runAction,'--job',('"{0}"' -f $job)) -WorkingDirectory $job -WindowStyle Hidden -RedirectStandardOutput (Join-Path $job "supervisor_$stamp.out.log") -RedirectStandardError (Join-Path $job "supervisor_$stamp.err.log") -PassThru
    Write-Output "T9E : $job"
    Write-Output "Suivi PID $($process.Id). Etat : expression_status.bat ; pause : stop_expression.bat"
} else {
    & $pythonPath $driver $Action.ToLowerInvariant() --job $job
    if ($LASTEXITCODE -ne 0) { throw 'Commande T9E echouee.' }
}
