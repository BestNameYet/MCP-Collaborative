$ErrorActionPreference = "Stop"

$PluginRoot = Split-Path -Parent $PSScriptRoot
$VenvRoot = Join-Path $PluginRoot ".venv"
$Python = Join-Path $VenvRoot "Scripts\python.exe"
$DataRoot = if ($env:COLLAB_TTT_DATA_DIR) {
    $env:COLLAB_TTT_DATA_DIR
} else {
    Join-Path $env:LOCALAPPDATA "CollaborativeTicTacToe"
}

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "Python launcher 'py' was not found. Install Python 3.11 or newer first."
}

if (-not (Test-Path $Python)) {
    & py -3.11 -m venv $VenvRoot
}

& $Python -m pip install --upgrade pip
& $Python -m pip install $PluginRoot
New-Item -ItemType Directory -Force -Path $DataRoot | Out-Null

Write-Host "Collaborative Tic-Tac-Toe is installed."
Write-Host "Database: $(Join-Path $DataRoot 'games.sqlite3')"
Write-Host "Next: set CONTROL_PLANE_API_KEY and run scripts\start-tunnel.ps1 -TunnelId <tunnel_id>."
