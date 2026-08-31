"""Fail-closed actor-visible projections."""

from __future__ import annotations

from typing import Any

from .domain import Actor, GameState


class ProjectionError(RuntimeError):
    """Raised rather than falling back to unrestricted authoritative state."""


VISIBLE_FIELDS = frozenset(
    {
        "game_id",
        "revision",
        "turn_number",
        "status",
        "board_size",
        "win_length",
        "board",
        "players",
        "active_actor_id",
        "winner_actor_id",
        "you",
        "is_your_turn",
        "available_cells",
    }
)


def _visible_actor(actor: Actor) -> dict[str, str]:
    return {"actor_id": actor.actor_id, "role": actor.role, "mark": actor.mark}


def project_state(state: GameState, actor_id: str) -> dict[str, Any]:
    """Construct a view from an explicit allow-list; unknown actors receive nothing."""

    actor = next((candidate for candidate in state.players if candidate.actor_id == actor_id), None)
    if actor is None:
        raise ProjectionError("actor is not configured for this game")
    if actor.perspective != "player":
        raise ProjectionError("unsupported perspective")
    view: dict[str, Any] = {
        "game_id": state.game_id,
        "revision": state.revision,
        "turn_number": state.turn_number,
        "status": state.status,
        "board_size": state.board_size,
        "win_length": state.win_length,
        "board": [list(row) for row in state.board],
        "players": [_visible_actor(player) for player in state.players],
        "active_actor_id": state.active_actor_id,
        "winner_actor_id": state.winner_actor_id,
        "you": {
            "actor_id": actor.actor_id,
            "actor_type": actor.actor_type,
            "role": actor.role,
            "mark": actor.mark,
            "perspective": actor.perspective,
        },
        "is_your_turn": state.active_actor_id == actor_id,
        "available_cells": [
            {"row": row_index, "column": column_index}
            for row_index, row in enumerate(state.board)
            for column_index, cell in enumerate(row)
            if cell is None
        ],
    }
    if frozenset(view) != VISIBLE_FIELDS:
        raise ProjectionError("projection schema did not match the allow-list")
    return view
