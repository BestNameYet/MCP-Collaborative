from __future__ import annotations

import unittest

from collaborative_ttt.domain import (
    Actor,
    ConfigurationError,
    MoveAction,
    apply_move,
    create_initial_state,
)


def players(count: int = 2) -> list[Actor]:
    marks = ["X", "O", "A", "B"]
    return [Actor(f"p{i + 1}", "player", f"player-{i + 1}", marks[i]) for i in range(count)]


def game(count: int = 2, size: int = 3, win: int = 3):
    return create_initial_state("g", players(count), size, win, 3)


def move(state, actor: str, row: int, column: int, action_id: str | None = None):
    return apply_move(
        state,
        MoveAction("g", actor, action_id or f"a-{state.revision}", state.revision, row, column),
    )


def play(sequence: list[tuple[str, int, int]], *, size: int = 3, win: int = 3):
    state = game(size=size, win=win)
    for actor, row, column in sequence:
        result = move(state, actor, row, column)
        if not result.accepted:
            raise AssertionError(result)
        state = result.state
    return state


class ConfigurationTests(unittest.TestCase):
    def test_baseline_genesis(self):
        state = game()
        self.assertEqual(0, state.revision)
        self.assertEqual("p1", state.active_actor_id)
        self.assertTrue(all(cell is None for row in state.board for cell in row))

    def test_two_to_four_players(self):
        for count in (2, 3, 4):
            self.assertEqual(count, len(game(count=count, size=4, win=3).players))
        with self.assertRaises(ConfigurationError):
            create_initial_state("g", players(1))
        with self.assertRaises(ConfigurationError):
            create_initial_state("g", players(4) + [Actor("p5", "player", "p5", "C")])

    def test_duplicate_actor_and_mark_rejected(self):
        with self.assertRaises(ConfigurationError):
            create_initial_state(
                "g", [Actor("p", "player", "one", "X"), Actor("p", "player", "two", "O")]
            )
        with self.assertRaises(ConfigurationError):
            create_initial_state(
                "g", [Actor("p1", "player", "one", "X"), Actor("p2", "player", "two", "X")]
            )

    def test_invalid_board_win_and_history(self):
        for kwargs in (
            {"board_size": 1},
            {"win_length": 0},
            {"board_size": 3, "win_length": 4},
            {"history_depth": -1},
        ):
            with self.assertRaises(ConfigurationError):
                create_initial_state("g", players(), **kwargs)


class TransitionTests(unittest.TestCase):
    def assert_rejected_unchanged(self, state, action, code):
        result = apply_move(state, action)
        self.assertFalse(result.accepted)
        self.assertEqual(code, result.error_code)
        self.assertIs(state, result.state)
        self.assertEqual(0, state.revision)

    def test_accepted_move_changes_exactly_one_cell(self):
        prior = game()
        result = move(prior, "p1", 1, 2)
        self.assertTrue(result.accepted)
        self.assertEqual(1, result.state.revision)
        self.assertEqual(1, result.state.turn_number)
        self.assertEqual("X", result.state.board[1][2])
        self.assertEqual("p2", result.state.active_actor_id)
        self.assertTrue(all(cell is None for row in prior.board for cell in row))

    def test_expected_rejections_preserve_identity(self):
        state = game()
        cases = [
            (MoveAction("other", "p1", "a", 0, 0, 0), "WRONG_GAME"),
            (MoveAction("g", "p1", "a", 1, 0, 0), "STALE_REVISION"),
            (MoveAction("g", "p2", "a", 0, 0, 0), "WRONG_ACTOR"),
            (MoveAction("g", "p1", "a", 0, -1, 0), "OUT_OF_BOUNDS"),
            (MoveAction("g", "p1", "a", 0, 0, 3), "OUT_OF_BOUNDS"),
            (MoveAction("g", "p1", "a", 0, "0", 0), "MALFORMED_MOVE"),
            (MoveAction("g", "p1", "", 0, 0, 0), "MALFORMED_ACTION"),
        ]
        for action, code in cases:
            with self.subTest(code=code):
                self.assert_rejected_unchanged(state, action, code)

    def test_occupied_cell_rejected(self):
        state = move(game(), "p1", 0, 0).state
        result = move(state, "p2", 0, 0)
        self.assertFalse(result.accepted)
        self.assertEqual("CELL_OCCUPIED", result.error_code)
        self.assertIs(state, result.state)

    def test_four_player_pointer_cycle(self):
        state = game(count=4, size=4, win=4)
        expected = ["p2", "p3", "p4", "p1"]
        for index, actor in enumerate(("p1", "p2", "p3", "p4")):
            result = move(state, actor, index // 4, index % 4)
            self.assertTrue(result.accepted)
            state = result.state
            self.assertEqual(expected[index], state.active_actor_id)

    def test_all_four_win_axes(self):
        scenarios = {
            "horizontal": [("p1", 0, 0), ("p2", 1, 0), ("p1", 0, 1), ("p2", 1, 1), ("p1", 0, 2)],
            "vertical": [("p1", 0, 0), ("p2", 0, 1), ("p1", 1, 0), ("p2", 1, 1), ("p1", 2, 0)],
            "descending": [("p1", 0, 0), ("p2", 0, 1), ("p1", 1, 1), ("p2", 0, 2), ("p1", 2, 2)],
            "ascending": [("p1", 0, 2), ("p2", 0, 0), ("p1", 1, 1), ("p2", 1, 0), ("p1", 2, 0)],
        }
        for name, sequence in scenarios.items():
            with self.subTest(name=name):
                state = play(sequence)
                self.assertEqual("won", state.status)
                self.assertEqual("p1", state.winner_actor_id)
                self.assertIsNone(state.active_actor_id)

    def test_shorter_k_and_long_run(self):
        state = play(
            [("p1", 0, 0), ("p2", 1, 0), ("p1", 0, 1), ("p2", 1, 1), ("p1", 0, 2)],
            size=4,
            win=3,
        )
        self.assertEqual("won", state.status)

    def test_draw_and_terminal_lockout(self):
        state = play(
            [
                ("p1", 0, 0), ("p2", 0, 1), ("p1", 0, 2),
                ("p2", 1, 1), ("p1", 1, 0), ("p2", 1, 2),
                ("p1", 2, 1), ("p2", 2, 0), ("p1", 2, 2),
            ]
        )
        self.assertEqual("draw", state.status)
        self.assertIsNone(state.active_actor_id)
        after = apply_move(state, MoveAction("g", "p1", "later", 9, 0, 0))
        self.assertFalse(after.accepted)
        self.assertEqual("GAME_TERMINAL", after.error_code)
        self.assertIs(state, after.state)

    def test_board_filling_win_precedes_draw(self):
        state = play(
            [
                ("p1", 0, 0), ("p2", 0, 1), ("p1", 0, 2),
                ("p2", 1, 0), ("p1", 1, 1), ("p2", 1, 2),
                ("p1", 2, 1), ("p2", 2, 0), ("p1", 2, 2),
            ]
        )
        self.assertEqual("won", state.status)
        self.assertEqual("p1", state.winner_actor_id)

    def test_transition_repeatability(self):
        state = game()
        action = MoveAction("g", "p1", "repeatable", 0, 2, 2)
        self.assertEqual(apply_move(state, action), apply_move(state, action))


if __name__ == "__main__":
    unittest.main()
