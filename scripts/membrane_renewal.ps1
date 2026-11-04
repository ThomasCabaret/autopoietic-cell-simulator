param([ValidateSet('Start','Status','Stop','Resume','Review')][string]$Action='Status')
$ErrorActionPreference='Stop'
$projectRoot=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$pythonPath=Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) { $pythonPath=(Get-Command python).Source }
$driverPath=Join-Path $projectRoot 'scripts\membrane_renewal_followup.py'
if ($Action -eq 'Start') {
    $prepared=& $pythonPath $driverPath prepare
    if ($LASTEXITCODE -ne 0) { throw 'Preparation echouee.' }
    $jobPath=[string]($prepared | Select-Object -Last 1)
} else {
    $jobPath=(Get-Content -LiteralPath (Join-Path $projectRoot 'outputs\membrane_renewal_followups\latest.txt') -Raw).Trim()
}
$jobPath=(Resolve-Path -LiteralPath $jobPath).Path
if ($Action -in @('Start','Resume')) {
    $snapshot=& $pythonPath $driverPath status --job $jobPath | ConvertFrom-Json
    if ($LASTEXITCODE -ne 0) { throw 'Statut invalide.' }
    if ($snapshot.active -or ($snapshot.campaigns | Where-Object { $_.controller_active })) { throw 'Campagne deja active.' }
    if ($snapshot.state.phase -eq 'needs_interpretation') { throw 'Termine ; utiliser Review.' }
    if ($snapshot.campaigns | Where-Object { $_.counts.failed -gt 0 }) { throw 'Inspecter les erreurs avant reprise.' }
    $frozenDriver=Join-Path $jobPath 'runtime\scripts\membrane_renewal_followup.py'
    $command=if ($Action -eq 'Start') { 'run' } else { 'resume' }
    $stamp=Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
    $process=Start-Process -FilePath $pythonPath -ArgumentList @(('"{0}"' -f $frozenDriver),$command,'--job',('"{0}"' -f $jobPath)) -WorkingDirectory $jobPath -WindowStyle Hidden -RedirectStandardOutput (Join-Path $jobPath "supervisor_$stamp.out.log") -RedirectStandardError (Join-Path $jobPath "supervisor_$stamp.err.log") -PassThru
    Write-Output "MIN1M : $jobPath ; PID $($process.Id)"
} else {
    & $pythonPath $driverPath $Action.ToLowerInvariant() --job $jobPath
    if ($LASTEXITCODE -ne 0) { throw 'Commande echouee.' }
}
