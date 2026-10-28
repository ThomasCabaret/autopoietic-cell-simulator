param(
    [ValidateSet('Start','Status','Stop','Resume')][string]$Action='Status',
    [string]$Job=''
)
$ErrorActionPreference='Stop'
$projectRoot=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$pythonPath=Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) { $pythonPath=(Get-Command python).Source }
$scriptPath=Join-Path $PSScriptRoot 'numerical_followup.py'
$latest=Join-Path $projectRoot 'outputs\followups\latest.txt'
if ($Action -eq 'Start') {
    if (Test-Path -LiteralPath $latest) {
        $previous=(Get-Content -LiteralPath $latest -Raw).Trim()
        $snapshotText=& $pythonPath $scriptPath status --job $previous
        if ($LASTEXITCODE -ne 0) { throw 'Suivi precedent invalide.' }
        $snapshot=$snapshotText | ConvertFrom-Json
        if ($snapshot.active -or $snapshot.child_controller_active -or $snapshot.child.running) { throw 'Un suivi est deja actif.' }
    }
    $parentFolder=(Get-Content -LiteralPath (Join-Path $projectRoot 'outputs\campaigns\latest.txt') -Raw).Trim()
    $prepared=& $pythonPath $scriptPath prepare --parent $parentFolder --baseline 'outputs\campaigns\campaign_20261027T192723206222Z'
    if ($LASTEXITCODE -ne 0) { throw 'Preparation du suivi echouee.' }
    $Job=[string]($prepared | Select-Object -Last 1)
} elseif (-not $Job) {
    $Job=(Get-Content -LiteralPath $latest -Raw).Trim()
}
$Job=(Resolve-Path -LiteralPath $Job).Path
if ($Action -in @('Start','Resume')) {
    $frozenScript=Join-Path $Job 'runtime\scripts\numerical_followup.py'
    $operation=if ($Action -eq 'Resume') { 'resume' } else { 'run' }
    $stamp=Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
    $process=Start-Process -FilePath $pythonPath -ArgumentList @(('"{0}"' -f $frozenScript),$operation,'--job',('"{0}"' -f $Job)) -WorkingDirectory $Job -WindowStyle Hidden -RedirectStandardOutput (Join-Path $Job "followup_$stamp.stdout.log") -RedirectStandardError (Join-Path $Job "followup_$stamp.stderr.log") -PassThru
    Write-Output "Suivi : $Job"
    Write-Output "PID : $($process.Id). Etat : .\followup_status.bat"
} else {
    & $pythonPath $scriptPath $Action.ToLowerInvariant() --job $Job
    if ($LASTEXITCODE -ne 0) { throw 'Commande de suivi echouee.' }
}
