"""Application service used by both MCP tools and tests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .domain import Actor, ConfigurationError, MoveAction, create_initial_state
from .repository import GameRepository, RepositoryError


class GameService:
    def __init__(self, database_path: str | Path):
        self.repository = GameRepository(database_path)

    def create_game(
        self,
        game_id: str,
        players: list[dict[str, Any]],
        board_size: int = 3,
        win_length: int = 3,
        history_depth: int = 5,
    ) -> dict[str, Any]:
        if not isinstance(players, list):
            raise ConfigurationError("players must be a list")
        actors: list[Actor] = []
        for index, value in enumerate(players):
            if not isinstance(value, dict):
                raise ConfigurationError("each player must be an object")
            actors.append(
                Actor(
                    actor_id=value.get("actor_id"),
                    actor_type=value.get("actor_type", "player"),
                    role=value.get("role", f"player-{index + 1}"),
                    mark=value.get("mark"),
                    perspective=value.get("perspective", "player"),
                )
            )
        state = create_initial_state(
            game_id=game_id,
            players=actors,
            board_size=board_size,
            win_length=win_length,
            history_depth=history_depth,
        )
        persisted, created = self.repository.create_game(state)
        return {
            "created": created,
            "game_id": persisted.game_id,
            "revision": persisted.revision,
            "status": persisted.status,
            "active_actor_id": persisted.active_actor_id,
            "players": [
                {"actor_id": actor.actor_id, "role": actor.role, "mark": actor.mark}
                for actor in persisted.players
            ],
            "message": "Game ready. Each actor should call get_actor_environment with its actor_id.",
        }

    def get_actor_environment(self, game_id: str, actor_id: str) -> dict[str, Any]:
        environment = self.repository.get_actor_environment(game_id, actor_id)
        return {"game_id": game_id, "actor_id": actor_id, **environment}

    def submit_move(
        self,
        game_id: str,
        actor_id: str,
        action_id: str,
        expected_revision: int,
        row: int,
        column: int,
    ) -> dict[str, Any]:
        return self.repository.submit_move(
            MoveAction(
                game_id=game_id,
                actor_id=actor_id,
                action_id=action_id,
                expected_revision=expected_revision,
                row=row,
                column=column,
            )
        )

    def verify_replay(self, game_id: str) -> dict[str, Any]:
        return self.repository.verify_replay(game_id)


__all__ = ["ConfigurationError", "GameService", "RepositoryError"]
