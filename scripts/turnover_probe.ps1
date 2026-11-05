param([ValidateSet('Start','Status','Stop','Resume')][string]$Action='Status',
      [ValidateSet('Turnover','Thermal')][string]$Kind='Turnover')
$ErrorActionPreference='Stop'
$projectRoot=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$pythonPath=(Get-Command python).Source
$driver=if ($Kind -eq 'Thermal') { 'experiments\inspect_contact_heat.py' } else { 'experiments\inspect_turnover_exposure.py' }
$latest=if ($Kind -eq 'Thermal') { 'outputs\diagnostics\EL1_latest.txt' } else { 'outputs\diagnostics\RX1_latest.txt' }
$probe=if ($Kind -eq 'Thermal') { 'contact_heat_probe.py' } else { 'turnover_probe.py' }
$tag=if ($Kind -eq 'Thermal') { 'EL1' } else { 'RX1' }
if ($Action -eq 'Start') {
    $prepared=& $pythonPath $driver
    if ($LASTEXITCODE -ne 0) { throw 'Preparation echouee.' }
    $jobPath=[string]($prepared | Select-Object -Last 1)
} else { $jobPath=(Get-Content -LiteralPath $latest -Raw).Trim() }
$state=Get-Content -LiteralPath (Join-Path $jobPath 'status.json') -Raw | ConvertFrom-Json
if ($Action -eq 'Status') { $state | ConvertTo-Json -Depth 8; exit }
if ($Action -eq 'Stop') { Set-Content -LiteralPath (Join-Path $jobPath 'STOP') -Value 'pause requested'; exit }
if ($state.phase -in @('complete','failed')) { throw 'Termine ou en erreur : interpreter avant toute relance.' }
if ($state.pid -and (Get-Process -Id $state.pid -ErrorAction SilentlyContinue)) { throw 'Sonde deja active.' }
$stopPath=Join-Path $jobPath 'STOP'
if (Test-Path -LiteralPath $stopPath) { Remove-Item -LiteralPath $stopPath }
$probePath=Join-Path $jobPath $probe
$outPath=Join-Path $jobPath 'probe.out.log'
$errPath=Join-Path $jobPath 'probe.err.log'
$arguments=@(('"'+$probePath+'"'),'--run',('"'+$jobPath+'"'))
$proc=Start-Process -FilePath $pythonPath -ArgumentList $arguments -WorkingDirectory $projectRoot -WindowStyle Hidden -RedirectStandardOutput $outPath -RedirectStandardError $errPath -PassThru
Write-Output "$tag PID $($proc.Id) : $jobPath"
