from __future__ import annotations

import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from collaborative_ttt.projection import VISIBLE_FIELDS
from collaborative_ttt.repository import RepositoryError
from collaborative_ttt.service import GameService


PLAYERS = [
    {"actor_id": "alice", "role": "X player", "mark": "X"},
    {"actor_id": "bob", "role": "O player", "mark": "O"},
]


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "games.sqlite3"
        self.service = GameService(self.db)
        self.service.create_game("g", PLAYERS, history_depth=2)

    def tearDown(self):
        self.temp.cleanup()

    def test_create_is_idempotent_for_identical_genesis(self):
        result = self.service.create_game("g", PLAYERS, history_depth=2)
        self.assertFalse(result["created"])
        with self.assertRaises(RepositoryError):
            self.service.create_game("g", PLAYERS, board_size=4, win_length=3, history_depth=2)

    def test_projection_is_allowlisted_and_actor_specific(self):
        alice = self.service.get_actor_environment("g", "alice")["current"]
        bob = self.service.get_actor_environment("g", "bob")["current"]
        self.assertEqual(VISIBLE_FIELDS, frozenset(alice))
        self.assertEqual("alice", alice["you"]["actor_id"])
        self.assertEqual("bob", bob["you"]["actor_id"])
        self.assertTrue(alice["is_your_turn"])
        self.assertFalse(bob["is_your_turn"])
        self.assertNotIn("history_depth", alice)
        self.assertNotIn("active_player_index", alice)

    def test_unknown_actor_fails_closed(self):
        with self.assertRaises(RepositoryError):
            self.service.get_actor_environment("g", "mallory")

    def test_rejection_is_audited_without_mutation(self):
        before = self.service.get_actor_environment("g", "bob")
        result = self.service.submit_move("g", "bob", "wrong-turn", 0, 0, 0)
        after = self.service.get_actor_environment("g", "bob")
        self.assertFalse(result["accepted"])
        self.assertEqual("WRONG_ACTOR", result["error"]["code"])
        self.assertEqual(before, after)
        self.assertEqual(1, self.service.repository.count_rejections("g"))

    def test_accepted_retry_is_idempotent(self):
        first = self.service.submit_move("g", "alice", "move-1", 0, 0, 0)
        retry = self.service.submit_move("g", "alice", "move-1", 0, 0, 0)
        self.assertTrue(first["accepted"])
        self.assertTrue(retry["accepted"])
        self.assertTrue(retry["idempotent_replay"])
        self.assertEqual(1, self.service.verify_replay("g")["event_count"])

    def test_action_id_conflict_is_rejected(self):
        self.service.submit_move("g", "alice", "same", 0, 0, 0)
        conflict = self.service.submit_move("g", "alice", "same", 0, 0, 1)
        self.assertFalse(conflict["accepted"])
        self.assertEqual("ACTION_ID_CONFLICT", conflict["error"]["code"])
        self.assertEqual(1, self.service.verify_replay("g")["event_count"])

    def test_bounded_history_and_current_projection(self):
        moves = [
            ("alice", "a1", 0, 0, 0),
            ("bob", "b1", 1, 1, 0),
            ("alice", "a2", 2, 0, 1),
        ]
        for actor, action, revision, row, column in moves:
            self.assertTrue(
                self.service.submit_move("g", actor, action, revision, row, column)["accepted"]
            )
        env = self.service.get_actor_environment("g", "alice")
        self.assertEqual(3, env["current"]["revision"])
        self.assertEqual([1, 2], [item["revision"] for item in env["history"]])

    def test_zero_history_depth_retains_no_prior_views(self):
        self.service.create_game("zero", PLAYERS, history_depth=0)
        self.service.submit_move("zero", "alice", "z1", 0, 0, 0)
        env = self.service.get_actor_environment("zero", "alice")
        self.assertEqual([], env["history"])

    def test_database_reopen_preserves_state(self):
        self.service.submit_move("g", "alice", "a1", 0, 2, 2)
        reopened = GameService(self.db)
        env = reopened.get_actor_environment("g", "bob")
        self.assertEqual(1, env["current"]["revision"])
        self.assertEqual("X", env["current"]["board"][2][2])

    def test_replay_matches_authoritative_state(self):
        self.service.submit_move("g", "alice", "a1", 0, 0, 0)
        self.service.submit_move("g", "bob", "b1", 1, 1, 0)
        verified = self.service.verify_replay("g")
        self.assertTrue(verified["valid"])
        self.assertEqual(2, verified["event_count"])
        self.assertEqual(verified["current_digest"], verified["replay_digest"])

    def test_competing_moves_serialize(self):
        def submit(action_id, column):
            service = GameService(self.db)
            return service.submit_move("g", "alice", action_id, 0, 0, column)

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda args: submit(*args), [("c1", 0), ("c2", 1)]))
        self.assertEqual(1, sum(1 for result in results if result["accepted"]))
        rejected = next(result for result in results if not result["accepted"])
        self.assertEqual("STALE_REVISION", rejected["error"]["code"])
        self.assertEqual(1, self.service.verify_replay("g")["event_count"])

    def test_end_to_end_win(self):
        sequence = [
            ("alice", 0, 0), ("bob", 1, 0), ("alice", 0, 1),
            ("bob", 1, 1), ("alice", 0, 2),
        ]
        final = None
        for revision, (actor, row, column) in enumerate(sequence):
            final = self.service.submit_move(
                "g", actor, f"e2e-{revision}", revision, row, column
            )
            self.assertTrue(final["accepted"])
        self.assertEqual("won", final["state_summary"]["status"])
        self.assertEqual("alice", final["state_summary"]["winner_actor_id"])
        self.assertIsNone(final["state_summary"]["active_actor_id"])


if __name__ == "__main__":
    unittest.main()
