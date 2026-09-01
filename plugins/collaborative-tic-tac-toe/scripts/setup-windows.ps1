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

& py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)"
if ($LASTEXITCODE -ne 0) {
    throw "The default Python 3 installation must be Python 3.11 or newer."
}

if (-not (Test-Path $Python)) {
    & py -3 -m venv $VenvRoot
}

& $Python -m pip install --upgrade pip
& $Python -m pip install $PluginRoot
New-Item -ItemType Directory -Force -Path $DataRoot | Out-Null

Write-Host "Collaborative Tic-Tac-Toe is installed."
Write-Host "Database: $(Join-Path $DataRoot 'games.sqlite3')"
Write-Host "Next: set CONTROL_PLANE_API_KEY and run scripts\start-tunnel.ps1 -TunnelId <tunnel_id>."
