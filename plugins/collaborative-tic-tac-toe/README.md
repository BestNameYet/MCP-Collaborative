# Collaborative Tic-Tac-Toe

This is a local OpenAI plugin with a bundled STDIO MCP server. ChatGPT desktop or Codex launches the server directly from `.mcp.json`; there is no public endpoint, tunnel, or OpenAI API key.

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

This local STDIO route is supported by the ChatGPT desktop/Codex host. ChatGPT web does not read the computer's local MCP configuration.

## Local development

From the repository root:

```bash
python -m venv .venv
.venv/bin/python -m pip install -e ./plugins/collaborative-tic-tac-toe
codex plugin marketplace add .
codex plugin add collaborative-tic-tac-toe@mcp-collaborative
```

On Windows, activate the virtual environment or install into the `python` interpreter on `PATH`, then restart ChatGPT desktop after installing the plugin.

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

