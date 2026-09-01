param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^tunnel_')]
    [string]$TunnelId,

    [string]$Profile = "collaborative-tic-tac-toe"
)

$ErrorActionPreference = "Stop"

if (-not $env:CONTROL_PLANE_API_KEY) {
    throw "Set CONTROL_PLANE_API_KEY in this PowerShell session before starting the tunnel."
}
if (-not (Get-Command tunnel-client -ErrorAction SilentlyContinue)) {
    throw "tunnel-client was not found on PATH. Download it from OpenAI Platform tunnel settings."
}

$ServerCommand = Join-Path $PSScriptRoot "run-server.cmd"
if (-not (Test-Path $ServerCommand)) {
    throw "MCP launcher not found: $ServerCommand"
}

& tunnel-client init `
    --sample sample_mcp_stdio_local `
    --profile $Profile `
    --tunnel-id $TunnelId `
    --mcp-command $ServerCommand

if ($LASTEXITCODE -ne 0) {
    throw "tunnel-client init failed with exit code $LASTEXITCODE"
}

& tunnel-client doctor --profile $Profile --explain
if ($LASTEXITCODE -ne 0) {
    throw "tunnel-client doctor failed with exit code $LASTEXITCODE"
}

& tunnel-client run --profile $Profile
