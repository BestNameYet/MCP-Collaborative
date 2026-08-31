"""Bundled STDIO MCP tool surface."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from .service import GameService


SERVER_INSTRUCTIONS = (
    "This server coordinates shared tic-tac-toe games. Create a complete ordered player list, "
    "give each independent actor its game_id and actor_id, and have actors read only through "
    "get_actor_environment. Only the active actor may submit_move. Use a new unique action_id "
    "for each intended move and pass the environment's exact revision. The server chooses no moves."
)

mcp = FastMCP("collaborative-tic-tac-toe", instructions=SERVER_INSTRUCTIONS)


def _database_path() -> Path:
    explicit = os.environ.get("COLLAB_TTT_DB")
    if explicit:
        return Path(explicit).expanduser()
    data_root = os.environ.get("PLUGIN_DATA") or os.environ.get("CLAUDE_PLUGIN_DATA")
    if data_root:
        return Path(data_root) / "games.sqlite3"
    return Path.home() / ".collaborative-tic-tac-toe" / "games.sqlite3"


@lru_cache(maxsize=1)
def _service() -> GameService:
    return GameService(_database_path())


@mcp.tool(
    name="create_game",
    description=(
        "Create an authoritative persistent game from a complete ordered list of 2-4 players. "
        "Each player object requires actor_id and unique mark; role is optional. The first player "
        "owns the initial turn. Reusing game_id with the identical genesis is idempotent."
    ),
    annotations=ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
def create_game(
    game_id: str,
    players: list[dict[str, Any]],
    board_size: int = 3,
    win_length: int = 3,
    history_depth: int = 5,
) -> dict[str, Any]:
    return _service().create_game(game_id, players, board_size, win_length, history_depth)


@mcp.tool(
    name="get_actor_environment",
    description=(
        "Read one configured actor's allow-listed current game view and bounded prior visible "
        "states. Use its revision and is_your_turn fields before proposing a move."
    ),
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
def get_actor_environment(game_id: str, actor_id: str) -> dict[str, Any]:
    return _service().get_actor_environment(game_id, actor_id)


@mcp.tool(
    name="submit_move",
    description=(
        "Propose one mark placement for an actor. The actor must own the turn, expected_revision "
        "must equal current revision, the cell must be empty/in bounds, and action_id must be "
        "stable across transport retries. The server atomically validates and commits or rejects."
    ),
    annotations=ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
def submit_move(
    game_id: str,
    actor_id: str,
    action_id: str,
    expected_revision: int,
    row: int,
    column: int,
) -> dict[str, Any]:
    return _service().submit_move(
        game_id, actor_id, action_id, expected_revision, row, column
    )


@mcp.tool(
    name="verify_replay",
    description=(
        "Verify that replaying the persisted genesis and accepted events reproduces the current "
        "authoritative state. Returns digests and validation errors, never raw authoritative state."
    ),
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
def verify_replay(game_id: str) -> dict[str, Any]:
    return _service().verify_replay(game_id)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

