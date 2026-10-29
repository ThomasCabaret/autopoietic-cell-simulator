param(
    [ValidateSet('Start','Status','Stop','Resume','Analyze')][string]$Action='Status'
)
$ErrorActionPreference='Stop'
$projectRoot=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$pythonPath=Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) { $pythonPath=(Get-Command python).Source }
$parent=Join-Path $projectRoot 'outputs\mixing_campaigns'
$latest=Join-Path $parent 'latest.txt'
$controller=Join-Path $PSScriptRoot 'campaign.py'
if ($Action -eq 'Start') {
    if (Test-Path -LiteralPath $latest) {
        $previous=(Get-Content -LiteralPath $latest -Raw).Trim()
        $text=& $pythonPath $controller status $previous --json
        if ($LASTEXITCODE -ne 0) { throw 'Inspecter la campagne de mélange précédente.' }
        $state=$text | ConvertFrom-Json
        if ($state.controller_active -or ($state.tasks | Where-Object { $_.worker_active })) {
            throw 'Un diagnostic de mélange est déjà actif. Utiliser mixing_status.bat.'
        }
    }
    $prepared=& $pythonPath $controller prepare 'campaigns\mixing.json' --output $parent
    if ($LASTEXITCODE -ne 0) { throw 'Préparation MIX1 échouée.' }
    $folder=[string]($prepared | Select-Object -Last 1)
} else {
    $folder=(Get-Content -LiteralPath $latest -Raw).Trim()
}
$folder=(Resolve-Path -LiteralPath $folder).Path
if ($Action -in @('Start','Resume')) {
    $frozen=Join-Path $folder 'runtime\campaign.py'
    $stamp=Get-Date -Format 'yyyyMMdd_HHmmss_fffffff'
    $process=Start-Process -FilePath $pythonPath -ArgumentList @(('"{0}"' -f $frozen),'run',('"{0}"' -f $folder)) -WorkingDirectory $folder -WindowStyle Hidden -RedirectStandardOutput (Join-Path $folder "controller_$stamp.stdout.log") -RedirectStandardError (Join-Path $folder "controller_$stamp.stderr.log") -PassThru
    Write-Output "MIX1 : $folder"
    Write-Output "Contrôleur PID : $($process.Id). Un travailleur. Suivi : mixing_status.bat"
} elseif ($Action -eq 'Analyze') {
    & $pythonPath (Join-Path $folder 'runtime\mixing_report.py') $folder
    if ($LASTEXITCODE -ne 0) { throw 'Analyse MIX1 échouée.' }
} else {
    & $pythonPath $controller $Action.ToLowerInvariant() $folder
    if ($LASTEXITCODE -ne 0) { throw 'Commande MIX1 échouée.' }
    if ($Action -eq 'Status') {
        & $pythonPath (Join-Path $folder 'runtime\mixing_report.py') $folder --no-plots
    }
}
