"""SQLite authority boundary for games, events, environments, and replay."""

from __future__ import annotations

import hashlib
import json
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .domain import GameState, MoveAction, apply_move, state_from_dict, state_to_dict
from .projection import ProjectionError, project_state


class RepositoryError(RuntimeError):
    """Raised for missing records, unsafe projection, or persistence failures."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(value: Any) -> str:
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def _action_dict(action: MoveAction) -> dict[str, Any]:
    return {
        "game_id": action.game_id,
        "actor_id": action.actor_id,
        "action_id": action.action_id,
        "expected_revision": action.expected_revision,
        "row": action.row,
        "column": action.column,
    }


class GameRepository:
    """Opens short-lived connections so independent MCP calls share one durable DB."""

    def __init__(self, database_path: str | Path):
        self.database_path = str(database_path)
        path = Path(self.database_path)
        if self.database_path != ":memory:":
            path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.database_path,
            timeout=10,
            isolation_level=None,
            check_same_thread=False,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 10000")
        if self.database_path != ":memory:":
            connection.execute("PRAGMA journal_mode = WAL")
        return connection

    def _initialize(self) -> None:
        with closing(self._connect()) as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS games (
                    game_id TEXT PRIMARY KEY,
                    genesis_json TEXT NOT NULL,
                    state_json TEXT NOT NULL,
                    revision INTEGER NOT NULL CHECK (revision >= 0),
                    history_depth INTEGER NOT NULL CHECK (history_depth >= 0),
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS accepted_events (
                    game_id TEXT NOT NULL REFERENCES games(game_id),
                    sequence INTEGER NOT NULL,
                    action_id TEXT NOT NULL,
                    actor_id TEXT NOT NULL,
                    prior_revision INTEGER NOT NULL,
                    resulting_revision INTEGER NOT NULL,
                    event_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (game_id, sequence),
                    UNIQUE (game_id, resulting_revision),
                    UNIQUE (game_id, actor_id, action_id)
                );

                CREATE TABLE IF NOT EXISTS action_results (
                    game_id TEXT NOT NULL REFERENCES games(game_id),
                    actor_id TEXT NOT NULL,
                    action_id TEXT NOT NULL,
                    request_json TEXT NOT NULL,
                    result_json TEXT NOT NULL,
                    accepted INTEGER NOT NULL CHECK (accepted IN (0, 1)),
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (game_id, actor_id, action_id)
                );

                CREATE TABLE IF NOT EXISTS rejected_attempts (
                    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id TEXT NOT NULL,
                    actor_id TEXT NOT NULL,
                    action_id TEXT NOT NULL,
                    error_code TEXT NOT NULL,
                    prior_revision INTEGER,
                    request_json TEXT NOT NULL,
                    result_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS actor_environments (
                    game_id TEXT NOT NULL REFERENCES games(game_id),
                    actor_id TEXT NOT NULL,
                    revision INTEGER NOT NULL,
                    current_json TEXT NOT NULL,
                    history_json TEXT NOT NULL,
                    PRIMARY KEY (game_id, actor_id)
                );
                """
            )

    @staticmethod
    def _load_state(row: sqlite3.Row) -> GameState:
        return state_from_dict(json.loads(row["state_json"]))

    @staticmethod
    def _read_environment(connection: sqlite3.Connection, game_id: str, actor_id: str) -> dict[str, Any]:
        row = connection.execute(
            "SELECT revision, current_json, history_json FROM actor_environments WHERE game_id = ? AND actor_id = ?",
            (game_id, actor_id),
        ).fetchone()
        if row is None:
            raise RepositoryError("actor environment not found")
        return {
            "current": json.loads(row["current_json"]),
            "history": json.loads(row["history_json"]),
        }

    def create_game(self, initial_state: GameState) -> tuple[GameState, bool]:
        genesis = state_to_dict(initial_state)
        genesis_json = _json(genesis)
        now = _utc_now()
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                existing = connection.execute(
                    "SELECT genesis_json, state_json FROM games WHERE game_id = ?",
                    (initial_state.game_id,),
                ).fetchone()
                if existing is not None:
                    if existing["genesis_json"] != genesis_json:
                        raise RepositoryError("GAME_EXISTS: game_id belongs to a different configuration")
                    connection.commit()
                    return state_from_dict(json.loads(existing["state_json"])), False

                connection.execute(
                    """INSERT INTO games
                       (game_id, genesis_json, state_json, revision, history_depth, created_at, updated_at)
                       VALUES (?, ?, ?, 0, ?, ?, ?)""",
                    (
                        initial_state.game_id,
                        genesis_json,
                        genesis_json,
                        initial_state.history_depth,
                        now,
                        now,
                    ),
                )
                for actor in initial_state.players:
                    current = project_state(initial_state, actor.actor_id)
                    connection.execute(
                        """INSERT INTO actor_environments
                           (game_id, actor_id, revision, current_json, history_json)
                           VALUES (?, ?, 0, ?, '[]')""",
                        (initial_state.game_id, actor.actor_id, _json(current)),
                    )
                connection.commit()
                return initial_state, True
            except Exception:
                connection.rollback()
                raise

    def get_state(self, game_id: str) -> GameState:
        with closing(self._connect()) as connection:
            row = connection.execute(
                "SELECT state_json FROM games WHERE game_id = ?", (game_id,)
            ).fetchone()
            if row is None:
                raise RepositoryError("GAME_NOT_FOUND")
            return self._load_state(row)

    def get_actor_environment(self, game_id: str, actor_id: str) -> dict[str, Any]:
        with closing(self._connect()) as connection:
            return self._read_environment(connection, game_id, actor_id)

    @staticmethod
    def _safe_summary(state: GameState) -> dict[str, Any]:
        return {
            "game_id": state.game_id,
            "revision": state.revision,
            "turn_number": state.turn_number,
            "status": state.status,
            "active_actor_id": state.active_actor_id,
            "winner_actor_id": state.winner_actor_id,
        }

    @staticmethod
    def _update_environments(connection: sqlite3.Connection, state: GameState) -> None:
        for actor in state.players:
            row = connection.execute(
                """SELECT current_json, history_json
                   FROM actor_environments WHERE game_id = ? AND actor_id = ?""",
                (state.game_id, actor.actor_id),
            ).fetchone()
            if row is None:
                raise RepositoryError("actor environment missing during transition")
            prior_current = json.loads(row["current_json"])
            history = json.loads(row["history_json"])
            history.append(prior_current)
            if len(history) > state.history_depth:
                history = history[-state.history_depth :] if state.history_depth else []
            current = project_state(state, actor.actor_id)
            connection.execute(
                """UPDATE actor_environments
                   SET revision = ?, current_json = ?, history_json = ?
                   WHERE game_id = ? AND actor_id = ?""",
                (state.revision, _json(current), _json(history), state.game_id, actor.actor_id),
            )

    def submit_move(self, action: MoveAction) -> dict[str, Any]:
        request = _action_dict(action)
        request_json = _json(request)
        now = _utc_now()
        with closing(self._connect()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                cached = connection.execute(
                    """SELECT request_json, result_json FROM action_results
                       WHERE game_id = ? AND actor_id = ? AND action_id = ?""",
                    (action.game_id, action.actor_id, action.action_id),
                ).fetchone()
                if cached is not None:
                    if cached["request_json"] == request_json:
                        response = json.loads(cached["result_json"])
                        response["idempotent_replay"] = True
                        connection.commit()
                        return response
                    game_row = connection.execute(
                        "SELECT state_json FROM games WHERE game_id = ?", (action.game_id,)
                    ).fetchone()
                    if game_row is None:
                        raise RepositoryError("GAME_NOT_FOUND")
                    state = self._load_state(game_row)
                    response = {
                        "accepted": False,
                        "idempotent_replay": False,
                        "game_id": action.game_id,
                        "action_id": action.action_id,
                        "prior_revision": state.revision,
                        "resulting_revision": state.revision,
                        "error": {
                            "code": "ACTION_ID_CONFLICT",
                            "detail": "action_id was already used with a different request",
                        },
                        "environment": None,
                        "state_summary": self._safe_summary(state),
                    }
                    connection.execute(
                        """INSERT INTO rejected_attempts
                           (game_id, actor_id, action_id, error_code, prior_revision,
                            request_json, result_json, created_at)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            action.game_id,
                            action.actor_id,
                            action.action_id,
                            "ACTION_ID_CONFLICT",
                            state.revision,
                            request_json,
                            _json(response),
                            now,
                        ),
                    )
                    connection.commit()
                    return response

                game_row = connection.execute(
                    "SELECT state_json FROM games WHERE game_id = ?", (action.game_id,)
                ).fetchone()
                if game_row is None:
                    raise RepositoryError("GAME_NOT_FOUND")
                prior_state = self._load_state(game_row)
                transition = apply_move(prior_state, action)

                if transition.accepted:
                    next_state = transition.state
                    connection.execute(
                        """UPDATE games SET state_json = ?, revision = ?, updated_at = ?
                           WHERE game_id = ? AND revision = ?""",
                        (
                            _json(state_to_dict(next_state)),
                            next_state.revision,
                            now,
                            next_state.game_id,
                            prior_state.revision,
                        ),
                    )
                    if connection.execute("SELECT changes()").fetchone()[0] != 1:
                        raise RepositoryError("serialized state commit failed")
                    event = {
                        "game_id": action.game_id,
                        "actor_id": action.actor_id,
                        "action_id": action.action_id,
                        "row": action.row,
                        "column": action.column,
                        "prior_revision": prior_state.revision,
                        "resulting_revision": next_state.revision,
                        "resulting_status": next_state.status,
                        "resulting_active_actor_id": next_state.active_actor_id,
                        "winner_actor_id": next_state.winner_actor_id,
                    }
                    connection.execute(
                        """INSERT INTO accepted_events
                           (game_id, sequence, action_id, actor_id, prior_revision,
                            resulting_revision, event_json, created_at)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            action.game_id,
                            next_state.revision,
                            action.action_id,
                            action.actor_id,
                            prior_state.revision,
                            next_state.revision,
                            _json(event),
                            now,
                        ),
                    )
                    self._update_environments(connection, next_state)
                    environment = self._read_environment(connection, action.game_id, action.actor_id)
                    response = {
                        "accepted": True,
                        "idempotent_replay": False,
                        "game_id": action.game_id,
                        "action_id": action.action_id,
                        "prior_revision": prior_state.revision,
                        "resulting_revision": next_state.revision,
                        "error": None,
                        "environment": environment,
                        "state_summary": self._safe_summary(next_state),
                    }
                else:
                    try:
                        environment = self._read_environment(
                            connection, action.game_id, action.actor_id
                        )
                    except RepositoryError:
                        environment = None
                    response = {
                        "accepted": False,
                        "idempotent_replay": False,
                        "game_id": action.game_id,
                        "action_id": action.action_id,
                        "prior_revision": prior_state.revision,
                        "resulting_revision": prior_state.revision,
                        "error": {
                            "code": transition.error_code,
                            "detail": transition.detail,
                        },
                        "environment": environment,
                        "state_summary": self._safe_summary(prior_state),
                    }
                    connection.execute(
                        """INSERT INTO rejected_attempts
                           (game_id, actor_id, action_id, error_code, prior_revision,
                            request_json, result_json, created_at)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            action.game_id,
                            action.actor_id,
                            action.action_id,
                            transition.error_code,
                            prior_state.revision,
                            request_json,
                            _json(response),
                            now,
                        ),
                    )

                connection.execute(
                    """INSERT INTO action_results
                       (game_id, actor_id, action_id, request_json, result_json, accepted, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        action.game_id,
                        action.actor_id,
                        action.action_id,
                        request_json,
                        _json(response),
                        1 if response["accepted"] else 0,
                        now,
                    ),
                )
                connection.commit()
                return response
            except (ProjectionError, sqlite3.Error) as error:
                connection.rollback()
                raise RepositoryError(str(error)) from error
            except Exception:
                connection.rollback()
                raise

    def verify_replay(self, game_id: str) -> dict[str, Any]:
        with closing(self._connect()) as connection:
            game = connection.execute(
                "SELECT genesis_json, state_json, revision FROM games WHERE game_id = ?",
                (game_id,),
            ).fetchone()
            if game is None:
                raise RepositoryError("GAME_NOT_FOUND")
            current = state_from_dict(json.loads(game["state_json"]))
            replay = state_from_dict(json.loads(game["genesis_json"]))
            rows = connection.execute(
                """SELECT sequence, event_json FROM accepted_events
                   WHERE game_id = ? ORDER BY sequence""",
                (game_id,),
            ).fetchall()

        errors: list[str] = []
        for row in rows:
            event = json.loads(row["event_json"])
            if row["sequence"] != replay.revision + 1:
                errors.append(f"event sequence gap at {row['sequence']}")
                break
            action = MoveAction(
                game_id=event["game_id"],
                actor_id=event["actor_id"],
                action_id=event["action_id"],
                expected_revision=event["prior_revision"],
                row=event["row"],
                column=event["column"],
            )
            result = apply_move(replay, action)
            if not result.accepted:
                errors.append(f"replay rejected event {row['sequence']}: {result.error_code}")
                break
            replay = result.state
            if replay.revision != event["resulting_revision"]:
                errors.append(f"resulting revision mismatch at {row['sequence']}")
                break

        current_dict = state_to_dict(current)
        replay_dict = state_to_dict(replay)
        if current_dict != replay_dict:
            errors.append("replayed state does not equal authoritative current state")
        return {
            "game_id": game_id,
            "valid": not errors,
            "event_count": len(rows),
            "current_revision": current.revision,
            "replay_revision": replay.revision,
            "current_digest": _digest(current_dict),
            "replay_digest": _digest(replay_dict),
            "errors": errors,
        }

    def count_rejections(self, game_id: str) -> int:
        """Test/operations helper; intentionally not exposed as an MCP tool."""
        with closing(self._connect()) as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS count FROM rejected_attempts WHERE game_id = ?", (game_id,)
            ).fetchone()
            return int(row["count"])

