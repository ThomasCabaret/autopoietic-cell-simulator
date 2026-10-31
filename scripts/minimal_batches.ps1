param(
    [ValidateSet('Diagnostic','Renewal')][string]$Kind='Renewal',
    [ValidateSet('Start','Status','Stop','Resume','Review')][string]$Action='Status'
)
$ErrorActionPreference='Stop'
$projectRoot=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$pythonPath=Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) { $pythonPath=(Get-Command python).Source }
$parentName=if ($Kind -eq 'Diagnostic') { 'minimal_diagnostic_campaigns' } else { 'renewal_campaigns' }
$prepareName=if ($Kind -eq 'Diagnostic') { 'prepare_minimal_diagnostic.py' } else { 'prepare_renewal_campaign.py' }
$reviewName=if ($Kind -eq 'Diagnostic') { 'review_minimal_diagnostic.py' } else { 'review_renewal.py' }
if ($Action -eq 'Start') {
    $prepared=& $pythonPath (Join-Path $projectRoot "experiments\$prepareName")
    if ($LASTEXITCODE -ne 0) { throw 'Preparation echouee.' }
    $folderPath=[string]($prepared | Select-Object -Last 1)
} else {
    $folderPath=(Get-Content -LiteralPath (Join-Path $projectRoot "outputs\$parentName\latest.txt") -Raw).Trim()
}
$folderPath=(Resolve-Path -LiteralPath $folderPath).Path
if ($Action -in @('Start','Resume')) {
    $snapshot=& $pythonPath scripts\campaign.py status $folderPath --json | ConvertFrom-Json
    if ($LASTEXITCODE -ne 0) { throw 'Statut invalide.' }
    if ($snapshot.controller_active -or ($snapshot.tasks | Where-Object { $_.worker_active })) { throw 'Campagne deja active.' }
    if ($snapshot.counts.failed -gt 0) { throw 'Inspecter les echecs ; aucune relance automatique.' }
    if ($snapshot.counts.complete -eq $snapshot.tasks.Count) { throw 'Campagne terminee ; utiliser Status ou Review.' }
    $driverPath=Join-Path $folderPath 'runtime\campaign.py'
    $stamp=Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
    $process=Start-Process -FilePath $pythonPath -ArgumentList @(('"{0}"' -f $driverPath),'run',('"{0}"' -f $folderPath)) -WorkingDirectory $folderPath -WindowStyle Hidden -RedirectStandardOutput (Join-Path $folderPath "controller_$stamp.out.log") -RedirectStandardError (Join-Path $folderPath "controller_$stamp.err.log") -PassThru
    Write-Output "$Kind : $folderPath ; PID $($process.Id)"
} elseif ($Action -eq 'Review') {
    & $pythonPath (Join-Path $projectRoot "experiments\$reviewName")
    if ($LASTEXITCODE -ne 0) { throw 'Revue echouee.' }
} else {
    & $pythonPath scripts\campaign.py $Action.ToLowerInvariant() $folderPath
    if ($LASTEXITCODE -ne 0) { throw 'Commande echouee.' }
}
