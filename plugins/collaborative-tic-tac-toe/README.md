# Collaborative Tic-Tac-Toe

This is a private, laptop-hosted MCP server. It keeps its existing STDIO transport and can be used in two ways:

- ChatGPT desktop or Codex can launch it directly from `.mcp.json`.
- Browser-based ChatGPT can reach the same private server through OpenAI Secure MCP Tunnel in Developer mode.

The tunnel is outbound-only: the laptop does not need a public endpoint or an inbound firewall rule.

## Exposed tools

- `create_game` — create an idempotent genesis for an ordered two-to-four-player game.
- `get_actor_environment` — read one actor's allow-listed current view and bounded visible history.
- `submit_move` — atomically validate and commit or reject one retry-safe move.
- `verify_replay` — prove that genesis plus accepted events reconstructs current state.

The server never chooses a move. Strategy remains with the actor/model.

## Install from the repository

The `python` executable used below must be the `python` executable available to ChatGPT desktop/Codex.

```bash
python -m pip install "git+https://github.com/BestNameYet/MCP-Collaborative.git#subdirectory=plugins/collaborative-tic-tac-toe"
codex plugin marketplace add BestNameYet/MCP-Collaborative --ref main
codex plugin add collaborative-tic-tac-toe@mcp-collaborative
```

Then restart ChatGPT desktop, enable/install **Collaborative Tic Tac Toe** from the `MCP Collaborative` marketplace if needed, and type `/mcp`. The connected server must list exactly the four tools above.

This local STDIO route is supported by the ChatGPT desktop/Codex host. ChatGPT web does not read the computer's local MCP configuration; use the Secure MCP Tunnel procedure below for web access.

## Private laptop to browser ChatGPT (Windows)

Prerequisites:

1. Python 3.11 or newer.
2. Developer mode enabled in ChatGPT under **Settings → Security and login**.
3. An OpenAI Platform tunnel associated with the ChatGPT workspace/account that will use it.
4. Tunnels **Read + Use** permission (and **Read + Manage** to create or edit it).
5. `tunnel-client` downloaded from OpenAI Platform tunnel settings and available on `PATH`.

In PowerShell, from this plugin directory:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\setup-windows.ps1
$env:CONTROL_PLANE_API_KEY = "<runtime API key>"
.\scripts\start-tunnel.ps1 -TunnelId "tunnel_<your id>"
```

The scripts create an isolated `.venv`, keep game data at
`%LOCALAPPDATA%\CollaborativeTicTacToe\games.sqlite3`, initialize a named tunnel profile,
run `tunnel-client doctor --explain`, and keep the tunnel running. The API key and tunnel ID
are never written into this repository.

While `tunnel-client run` remains healthy, open **ChatGPT Plugins**, select **+**, create a
developer-mode app, choose **Tunnel**, and select or paste the same `tunnel_id`. Confirm that
ChatGPT discovers exactly `create_game`, `get_actor_environment`, `submit_move`, and
`verify_replay`. After changing tool metadata, restart the server and use **Refresh** on the app.

The final browser-to-laptop check must be run on the home laptop because it requires that
laptop's process, tunnel credentials, and ChatGPT account. No public plugin submission is needed.

## Local development

From the repository root:

```bash
python -m venv .venv
.venv/bin/python -m pip install -e ./plugins/collaborative-tic-tac-toe
codex plugin marketplace add .
codex plugin add collaborative-tic-tac-toe@mcp-collaborative
```

On Windows, `scripts\setup-windows.ps1` provides the repeatable isolated installation used by
both the local desktop route and Secure MCP Tunnel.

Persistent data uses `PLUGIN_DATA/games.sqlite3` when the OpenAI host supplies `PLUGIN_DATA`, then `CLAUDE_PLUGIN_DATA`, then `~/.collaborative-tic-tac-toe/games.sqlite3`. Set `COLLAB_TTT_DB` to an explicit database file when testing or operating a dedicated instance.

## Test

```bash
python -m compileall -q src tests
python -m unittest discover -s tests -v
```

All tests use temporary databases. Runtime SQLite files, WAL files, caches, and virtual environments are excluded from version control.

## Collaboration flow

1. Create a game with a complete ordered player list and unique marks.
2. Give each independent participant the same `game_id` and its own `actor_id`.
3. Each participant calls `get_actor_environment` directly against the shared server.
4. Only the participant whose view has `is_your_turn: true` submits a move using the exact visible revision and a new action ID.
5. The server serializes the move, advances the execution pointer, updates every actor environment, and persists the event.
