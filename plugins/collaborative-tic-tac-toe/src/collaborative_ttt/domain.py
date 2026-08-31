"""Pure, deterministic tic-tac-toe domain model and transitions."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Iterable


class ConfigurationError(ValueError):
    """Raised before genesis when a game configuration is invalid."""


@dataclass(frozen=True, slots=True)
class Actor:
    actor_id: str
    actor_type: str
    role: str
    mark: str
    perspective: str = "player"


@dataclass(frozen=True, slots=True)
class GameState:
    game_id: str
    players: tuple[Actor, ...]
    board_size: int
    win_length: int
    history_depth: int
    board: tuple[tuple[str | None, ...], ...]
    revision: int = 0
    turn_number: int = 0
    active_player_index: int | None = 0
    status: str = "active"
    winner_actor_id: str | None = None

    @property
    def active_actor_id(self) -> str | None:
        if self.active_player_index is None:
            return None
        return self.players[self.active_player_index].actor_id


@dataclass(frozen=True, slots=True)
class MoveAction:
    game_id: str
    actor_id: str
    action_id: str
    expected_revision: Any
    row: Any
    column: Any


@dataclass(frozen=True, slots=True)
class TransitionResult:
    accepted: bool
    state: GameState
    error_code: str | None = None
    detail: str | None = None


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _clean_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"{field} must be a non-empty string")
    return value.strip()


def create_initial_state(
    game_id: str,
    players: Iterable[Actor],
    board_size: int = 3,
    win_length: int = 3,
    history_depth: int = 5,
) -> GameState:
    """Validate a complete configuration and return immutable revision-zero state."""

    clean_game_id = _clean_text(game_id, "game_id")
    player_tuple = tuple(players)
    if not 2 <= len(player_tuple) <= 4:
        raise ConfigurationError("player count must be between 2 and 4")
    if not _is_int(board_size) or board_size < 2:
        raise ConfigurationError("board_size must be an integer of at least 2")
    if not _is_int(win_length) or not 1 <= win_length <= board_size:
        raise ConfigurationError("win_length must be between 1 and board_size")
    if not _is_int(history_depth) or history_depth < 0:
        raise ConfigurationError("history_depth must be a non-negative integer")

    actor_ids: set[str] = set()
    marks: set[str] = set()
    normalized: list[Actor] = []
    for actor in player_tuple:
        if actor.actor_type != "player":
            raise ConfigurationError("initial actors must have type 'player'")
        actor_id = _clean_text(actor.actor_id, "actor_id")
        role = _clean_text(actor.role, "role")
        mark = _clean_text(actor.mark, "mark")
        perspective = _clean_text(actor.perspective, "perspective")
        if actor_id in actor_ids:
            raise ConfigurationError("actor IDs must be unique")
        if mark in marks:
            raise ConfigurationError("marks must be unique")
        actor_ids.add(actor_id)
        marks.add(mark)
        normalized.append(Actor(actor_id, "player", role, mark, perspective))

    empty_row = tuple(None for _ in range(board_size))
    board = tuple(empty_row for _ in range(board_size))
    return GameState(
        game_id=clean_game_id,
        players=tuple(normalized),
        board_size=board_size,
        win_length=win_length,
        history_depth=history_depth,
        board=board,
    )


def _reject(state: GameState, code: str, detail: str) -> TransitionResult:
    return TransitionResult(False, state, code, detail)


def _has_winning_run(state: GameState, row: int, column: int, mark: str) -> bool:
    for row_step, column_step in ((0, 1), (1, 0), (1, 1), (1, -1)):
        count = 1
        for direction in (1, -1):
            r = row + row_step * direction
            c = column + column_step * direction
            while 0 <= r < state.board_size and 0 <= c < state.board_size:
                if state.board[r][c] != mark:
                    break
                count += 1
                r += row_step * direction
                c += column_step * direction
        if count >= state.win_length:
            return True
    return False


def apply_move(state: GameState, action: MoveAction) -> TransitionResult:
    """Apply one action without I/O, clocks, randomness, or strategy."""

    if not isinstance(action.game_id, str) or action.game_id != state.game_id:
        return _reject(state, "WRONG_GAME", "action game_id does not match authoritative state")
    if state.status != "active":
        return _reject(state, "GAME_TERMINAL", "terminal games cannot accept moves")
    if not _is_int(action.expected_revision):
        return _reject(state, "MALFORMED_ACTION", "expected_revision must be an integer")
    if action.expected_revision != state.revision:
        return _reject(state, "STALE_REVISION", "expected_revision is not current")
    if not isinstance(action.actor_id, str) or action.actor_id != state.active_actor_id:
        return _reject(state, "WRONG_ACTOR", "actor does not own the execution pointer")
    if not isinstance(action.action_id, str) or not action.action_id.strip():
        return _reject(state, "MALFORMED_ACTION", "action_id must be a non-empty string")
    if not _is_int(action.row) or not _is_int(action.column):
        return _reject(state, "MALFORMED_MOVE", "row and column must be integers")
    if not (0 <= action.row < state.board_size and 0 <= action.column < state.board_size):
        return _reject(state, "OUT_OF_BOUNDS", "row or column is outside the board")
    if state.board[action.row][action.column] is not None:
        return _reject(state, "CELL_OCCUPIED", "the selected cell is occupied")

    acting_index = state.active_player_index
    assert acting_index is not None
    actor = state.players[acting_index]
    rows = [list(existing) for existing in state.board]
    rows[action.row][action.column] = actor.mark
    next_state = replace(
        state,
        board=tuple(tuple(row) for row in rows),
        revision=state.revision + 1,
        turn_number=state.turn_number + 1,
    )

    if _has_winning_run(next_state, action.row, action.column, actor.mark):
        next_state = replace(
            next_state,
            status="won",
            winner_actor_id=actor.actor_id,
            active_player_index=None,
        )
    elif all(cell is not None for row in next_state.board for cell in row):
        next_state = replace(
            next_state,
            status="draw",
            winner_actor_id=None,
            active_player_index=None,
        )
    else:
        next_state = replace(
            next_state,
            active_player_index=(acting_index + 1) % len(state.players),
        )
    return TransitionResult(True, next_state)


def actor_to_dict(actor: Actor) -> dict[str, str]:
    return {
        "actor_id": actor.actor_id,
        "actor_type": actor.actor_type,
        "role": actor.role,
        "mark": actor.mark,
        "perspective": actor.perspective,
    }


def state_to_dict(state: GameState) -> dict[str, Any]:
    return {
        "game_id": state.game_id,
        "players": [actor_to_dict(actor) for actor in state.players],
        "board_size": state.board_size,
        "win_length": state.win_length,
        "history_depth": state.history_depth,
        "board": [list(row) for row in state.board],
        "revision": state.revision,
        "turn_number": state.turn_number,
        "active_player_index": state.active_player_index,
        "status": state.status,
        "winner_actor_id": state.winner_actor_id,
    }


def state_from_dict(value: dict[str, Any]) -> GameState:
    return GameState(
        game_id=value["game_id"],
        players=tuple(Actor(**actor) for actor in value["players"]),
        board_size=value["board_size"],
        win_length=value["win_length"],
        history_depth=value["history_depth"],
        board=tuple(tuple(row) for row in value["board"]),
        revision=value["revision"],
        turn_number=value["turn_number"],
        active_player_index=value["active_player_index"],
        status=value["status"],
        winner_actor_id=value["winner_actor_id"],
    )
