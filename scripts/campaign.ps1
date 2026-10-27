param(
    [ValidateSet('Start','Status','Stop','Resume','Analyze')][string]$Action='Status',
    [string]$Plan='campaigns\constructed_tool.json',
    [string]$Folder=''
)
$ErrorActionPreference='Stop'
$projectRoot=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$pythonPath=Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) { $pythonPath=(Get-Command python).Source }
$controllerScript=Join-Path $PSScriptRoot 'campaign.py'
if ($Action -eq 'Start') {
    $latest=Join-Path $projectRoot 'outputs\campaigns\latest.txt'
    if (Test-Path -LiteralPath $latest) {
        $lastFolder=(Get-Content -LiteralPath $latest -Raw).Trim()
        $snapshotText=& $pythonPath $controllerScript status $lastFolder --json
        if ($LASTEXITCODE -ne 0) { throw 'Impossible de verifier la campagne precedente.' }
        $snapshot=$snapshotText | ConvertFrom-Json
        if ($snapshot.controller_active -or ($snapshot.tasks | Where-Object { $_.worker_active })) {
            throw 'Une campagne est encore active. Consulter campaign_status.bat.'
        }
    }
    $prepared=& $pythonPath $controllerScript prepare $Plan
    if ($LASTEXITCODE -ne 0) { throw 'Préparation de campagne échouée.' }
    $Folder=[string]($prepared | Select-Object -Last 1)
} elseif (-not $Folder) {
    $Folder=(Get-Content -LiteralPath (Join-Path $projectRoot 'outputs\campaigns\latest.txt') -Raw).Trim()
}
$Folder=(Resolve-Path -LiteralPath $Folder).Path
if ($Action -in @('Start','Resume')) {
    $frozenController=Join-Path $Folder 'runtime\campaign.py'
    $stamp=Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
    $stdout=Join-Path $Folder "controller_$stamp.stdout.log"
    $stderr=Join-Path $Folder "controller_$stamp.stderr.log"
    $process=Start-Process -FilePath $pythonPath -ArgumentList @(('"{0}"' -f $frozenController),'run',('"{0}"' -f $Folder)) -WorkingDirectory $Folder -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru
    Write-Output "Campagne : $Folder"
    Write-Output "Contrôleur PID : $($process.Id). Suivi : .\campaign_status.bat"
} else {
    & $pythonPath $controllerScript $Action.ToLowerInvariant() $Folder
    if ($LASTEXITCODE -ne 0) { throw 'Commande de campagne échouée.' }
}
