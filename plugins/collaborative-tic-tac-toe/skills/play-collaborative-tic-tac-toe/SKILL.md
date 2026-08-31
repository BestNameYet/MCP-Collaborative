---
name: play-collaborative-tic-tac-toe
description: Create, inspect, play, and verify persistent collaborative tic-tac-toe games through the bundled MCP tools.
---

# Play Collaborative Tic-Tac-Toe

Use the bundled tools when the user wants to create or participate in a shared tic-tac-toe game.

## Create

Collect a stable `actor_id` and unique mark for each of two to four players. Call `create_game` once with the complete ordered list. Ordinary tic-tac-toe uses board size 3 and win length 3.

## Act

Before every proposed move, call `get_actor_environment` for the acting actor. Continue only when `current.is_your_turn` is true. Choose strategy semantically from the visible view; the server deliberately provides no move recommendation.

Call `submit_move` with:

- the shared `game_id`;
- the acting `actor_id`;
- a new stable `action_id` for the intended move;
- `current.revision` as `expected_revision`;
- one available row and column.

Reuse the same `action_id` only when retrying the identical request. If a move is rejected as stale, read the environment again before deciding what to do.

## Observe and verify

Actors obtain state directly from `get_actor_environment`; do not ask a human to relay the board or choose the next actor. Use `verify_replay` when integrity or deterministic reconstruction needs checking.

