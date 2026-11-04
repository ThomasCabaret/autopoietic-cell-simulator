param([ValidateSet('Start','Status','Stop','Resume','Review')][string]$Action='Status',
      [ValidateSet('Membrane','Lipids','Curvature','Tail','Capture','Mixed')][string]$Kind='Membrane')
$ErrorActionPreference='Stop'
$projectRoot=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$pythonPath=Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) { $pythonPath=(Get-Command python).Source }
$driverName=if ($Kind -eq 'Lipids') { 'lipid_energy_followup.py' } else { 'membrane_renewal_followup.py' }
$parentName=if ($Kind -eq 'Lipids') { 'lipid_energy_followups' } else { 'membrane_renewal_followups' }
$kindLabel=if ($Kind -eq 'Lipids') { 'L2' } else { 'MIN1M' }
if ($Kind -eq 'Curvature') { $driverName='lipid_curvature_followup.py'; $parentName='lipid_curvature_followups'; $kindLabel='L3' }
if ($Kind -eq 'Capture') { $driverName='capture_transfer_followup.py'; $parentName='capture_transfer_followups'; $kindLabel='CT1' }
if ($Kind -eq 'Mixed') { $driverName='mixed_synthesis_followup.py'; $parentName='mixed_synthesis_followups'; $kindLabel='MX1' }
$modeArgs=@()
if ($Kind -eq 'Tail') { $driverName='lipid_curvature_followup.py'; $parentName='lipid_thermal_tail_followups'; $kindLabel='L4'; $modeArgs=@('--tail') }
$driverPath=Join-Path $projectRoot "scripts\$driverName"
if ($Action -eq 'Start') {
    $prepared=& $pythonPath $driverPath prepare @modeArgs
    if ($LASTEXITCODE -ne 0) { throw 'Preparation echouee.' }
    $jobPath=[string]($prepared | Select-Object -Last 1)
} else {
    $jobPath=(Get-Content -LiteralPath (Join-Path $projectRoot "outputs\$parentName\latest.txt") -Raw).Trim()
}
$jobPath=(Resolve-Path -LiteralPath $jobPath).Path
if ($Action -in @('Start','Resume')) {
    $snapshot=& $pythonPath $driverPath status --job $jobPath @modeArgs | ConvertFrom-Json
    if ($LASTEXITCODE -ne 0) { throw 'Statut invalide.' }
    if ($snapshot.active -or ($snapshot.campaigns | Where-Object { $_.controller_active })) { throw 'Campagne deja active.' }
    if ($snapshot.state.phase -eq 'needs_interpretation') { throw 'Termine ; utiliser Review.' }
    if ($snapshot.campaigns | Where-Object { $_.counts.failed -gt 0 }) { throw 'Inspecter les erreurs avant reprise.' }
    $frozenDriver=Join-Path $jobPath "runtime\scripts\$driverName"
    $command=if ($Action -eq 'Start') { 'run' } else { 'resume' }
    $stamp=Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
    $arguments=@(('"{0}"' -f $frozenDriver),$command,'--job',('"{0}"' -f $jobPath))+$modeArgs
    $process=Start-Process -FilePath $pythonPath -ArgumentList $arguments -WorkingDirectory $jobPath -WindowStyle Hidden -RedirectStandardOutput (Join-Path $jobPath "supervisor_$stamp.out.log") -RedirectStandardError (Join-Path $jobPath "supervisor_$stamp.err.log") -PassThru
    Write-Output "$kindLabel : $jobPath ; PID $($process.Id)"
} else {
    & $pythonPath $driverPath $Action.ToLowerInvariant() --job $jobPath @modeArgs
    if ($LASTEXITCODE -ne 0) { throw 'Commande echouee.' }
}
