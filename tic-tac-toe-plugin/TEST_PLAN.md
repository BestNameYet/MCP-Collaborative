# Collaborative MCP Tic-Tac-Toe — Test Plan

## 1. Test Scope

This test plan verifies the first deterministic implementation tranche defined in `DESIGN.md`.

It covers:

- authoritative state ownership and immutability;
- monotonic revisions;
- deterministic state transitions;
- terminal-state lockout;
- 2–4 player configuration;
- configurable `N × N` board;
- configurable win length `K`;
- unique marks;
- single-cell moves;
- invalid action rejection;
- horizontal, vertical, and both diagonal wins;
- draws;
- authoritative execution-pointer assignment and advancement;
- core invariants related to accepted/rejected transitions;
- absence of game-playing strategy in the deterministic core.

Perspective projection, actor environment history, durable transaction replay, transport-level concurrency, persistent idempotency, and MCP integration will receive separate later test sections when those design tranches are added.

## 2. Test Environment

The deterministic core shall be testable without:

- network access;
- MCP transport;
- a language model;
- a database;
- filesystem persistence;
- wall-clock time.

Tests should instantiate value objects directly and call pure functions.

Baseline fixture:

```text
game_id = "g-baseline"
players = [(P1, X), (P2, O)]
N = 3
K = 3
revision = 0
turn_number = 0
active actor = P1
status = active
board = empty 3×3
```

Additional fixtures shall cover 3-player and 4-player games and larger boards.

## 3. Test Result Standard

Every test shall produce a binary pass/fail outcome.

For transition tests, assertions shall compare complete resulting state values rather than only selected fields whenever practical.

Rejected actions must assert that the returned state is exactly equal to the prior authoritative state.

## 4. Configuration Tests

### TST-CONFIG-001 — Baseline configuration accepted

Create a 2-player `3×3`, `K=3` game.

Expected:

- state created;
- revision `0`;
- turn `0`;
- empty board;
- active actor `P1`;
- status `active`.

Covers: `TTT-GAME-001`, `TTT-GAME-002`, `TTT-GAME-003`, `TTT-GAME-004`, `TTT-GAME-009`.

### TST-CONFIG-002 — Three players accepted

Create a valid three-player game.

Expected: deterministic player ordering is preserved.

Covers: `TTT-GAME-001`.

### TST-CONFIG-003 — Four players accepted

Create a valid four-player game.

Expected: configuration accepted.

Covers: `TTT-GAME-001`.

### TST-CONFIG-004 — Too few players rejected

Create a one-player game.

Expected: configuration rejected before authoritative state creation.

Covers: `TTT-GAME-001`.

### TST-CONFIG-005 — Too many players rejected

Create a five-player game.

Expected: configuration rejected.

Covers: `TTT-GAME-001`.

### TST-CONFIG-006 — Duplicate actor ID rejected

Expected: configuration rejected.

Covers: `TTT-ACTOR-002`.

### TST-CONFIG-007 — Duplicate mark rejected

Expected: configuration rejected.

Covers: `TTT-GAME-004`.

### TST-CONFIG-008 — Invalid win length rejected

Cases:

- `K = 0`;
- `K > N`.

Expected: configuration rejected.

Covers: `TTT-GAME-003`.

## 5. Authoritative State and Revision Tests

### TST-STATE-001 — Genesis revision

Expected: a new game begins at revision `0`.

Covers: `TTT-STATE-002`.

### TST-STATE-002 — Accepted move increments revision exactly once

Submit one valid move.

Expected:

- accepted;
- resulting revision = prior revision + 1.

Covers: `TTT-STATE-002`, `TTT-STATE-003`.

### TST-STATE-003 — Rejected move does not increment revision

Submit an invalid move.

Expected: revision unchanged.

Covers: `TTT-STATE-002`, `TTT-INV-004`.

### TST-STATE-004 — Prior snapshot is immutable

Retain reference/value of prior state, execute valid transition, then compare prior state to pre-transition copy.

Expected: prior state unchanged.

Covers: `TTT-STATE-001`, `TTT-INV-001`.

### TST-STATE-005 — Transition determinism

Apply identical valid action independently to two identical prior states.

Expected: complete resulting states equal.

Covers: `TTT-STATE-003`.

## 6. Move Validation Tests

For every rejection below, assert all of:

- `accepted == false`;
- exact expected machine-readable error code;
- returned state equals prior state;
- revision unchanged;
- board unchanged;
- execution pointer unchanged.

### TST-VALID-001 — Wrong game

Expected error: `WRONG_GAME`.

### TST-VALID-002 — Stale revision

Expected error: `STALE_REVISION`.

Covers: `TTT-GAME-006`, `TTT-STATE-002`.

### TST-VALID-003 — Wrong actor

Expected error: `WRONG_ACTOR`.

Covers: `TTT-GAME-006`, `TTT-ORCH-003`, `TTT-INV-003`.

### TST-VALID-004 — Negative row

Expected error: `OUT_OF_BOUNDS`.

### TST-VALID-005 — Negative column

Expected error: `OUT_OF_BOUNDS`.

### TST-VALID-006 — Row equal to N

Expected error: `OUT_OF_BOUNDS`.

### TST-VALID-007 — Column equal to N

Expected error: `OUT_OF_BOUNDS`.

### TST-VALID-008 — Occupied cell

Expected error: `CELL_OCCUPIED`.

### TST-VALID-009 — Malformed coordinate

Examples: wrong tuple/list length, noninteger coordinate, missing move.

Expected error: `MALFORMED_MOVE` or `MALFORMED_ACTION` according to the final schema boundary.

### TST-VALID-010 — Action after terminal state

Expected error: `GAME_TERMINAL`.

Covers: `TTT-STATE-004`, `TTT-GAME-006`.

## 7. Single-Move Transition Tests

### TST-MOVE-001 — Exactly one cell changes

Submit a valid move at `(1, 2)`.

Expected:

- exactly one board cell differs from prior board;
- target changes from null to acting player's mark;
- all other cells equal prior board;
- revision increments once;
- turn increments once.

Covers: `TTT-GAME-005`.

### TST-MOVE-002 — Mark comes from actor configuration

Expected: server writes the configured mark for the active actor, not a client-supplied arbitrary mark.

Covers: `TTT-GAME-004`, `TTT-GAME-005`.

## 8. Execution Pointer Tests

### TST-ORCH-001 — Genesis pointer

Expected: first configured player owns execution pointer.

Covers: `TTT-ORCH-001`, `TTT-ORCH-002`.

### TST-ORCH-002 — Two-player pointer advance

P1 makes valid nonterminal move.

Expected: pointer becomes P2.

P2 makes valid nonterminal move.

Expected: pointer becomes P1.

Covers: `TTT-ORCH-002`.

### TST-ORCH-003 — Four-player cyclic order

Use players P1, P2, P3, P4.

After successive valid nonterminal moves, expected pointer sequence:

```text
P1 → P2 → P3 → P4 → P1
```

Covers: `TTT-GAME-001`, `TTT-ORCH-002`.

### TST-ORCH-004 — Rejection does not advance pointer

Expected: pointer unchanged.

Covers: `TTT-INV-004`.

### TST-ORCH-005 — Terminal move clears pointer

Expected: terminal state has no active actor.

Covers: `TTT-STATE-004`, `TTT-ORCH-001`.

## 9. Win Detection Tests

Each test shall construct the state immediately before the winning move and apply that move through the public transition function rather than directly invoking only the win detector.

Expected for every win case:

- accepted transition;
- `status == "won"`;
- `winner_actor_id == acting actor`;
- pointer cleared;
- revision increments once.

### TST-WIN-001 — Horizontal K=3

### TST-WIN-002 — Vertical K=3

### TST-WIN-003 — Descending diagonal K=3

Direction `(1,1)`.

### TST-WIN-004 — Ascending diagonal K=3

Direction `(1,-1)`.

### TST-WIN-005 — K shorter than board size

Example: `N=4`, `K=3`.

Expected: contiguous run of three wins without requiring full row/column length.

### TST-WIN-006 — Run longer than K

Example: `N=5`, `K=3`, resulting contiguous run length 4.

Expected: win.

### TST-WIN-007 — Gap does not count as contiguous

Marks separated by an empty or opposing mark.

Expected: nonterminal if no other win exists.

### TST-WIN-008 — No edge wrapping

Place marks that would appear contiguous only if end of one row wrapped to start of next.

Expected: no win.

### TST-WIN-009 — Winning move fills final board cell

Expected: status `won`, not `draw`.

Covers: `TTT-GAME-007`, `TTT-GAME-008`.

## 10. Draw Tests

### TST-DRAW-001 — Full board without winner

Baseline 3×3 sequence ending in no three-in-a-row.

Expected:

- final move accepted;
- `status == "draw"`;
- winner null;
- pointer null;
- board full.

Covers: `TTT-GAME-008`.

### TST-DRAW-002 — Non-full board not draw

Expected: active state if no winner.

## 11. Terminal-State Tests

### TST-TERM-001 — Winning state rejects future move

Expected: `GAME_TERMINAL`; exact terminal state preserved.

### TST-TERM-002 — Draw state rejects future move

Expected: `GAME_TERMINAL`; exact terminal state preserved.

Covers: `TTT-STATE-004`.

## 12. Multiplayer Domain Tests

### TST-MULTI-001 — Three-player legal rotation

Expected pointer and marks follow configured ordering through several nonterminal moves.

### TST-MULTI-002 — Four-player winner

Construct a four-player board where P3 completes a valid K-run.

Expected: P3 identified as winner independent of player count.

### TST-MULTI-003 — Opponent marks break contiguity

Expected: detector counts only acting player's contiguous marks.

Covers: `TTT-GAME-001`, `TTT-GAME-003`, `TTT-GAME-007`.

## 13. Invariant Tests

### TST-INV-001 — Rejection identity

Property: for every generated invalid action, returned state equals prior state.

Covers: `TTT-INV-004`.

### TST-INV-002 — One-cell accepted delta

Property: for every accepted non-genesis action, exactly one empty board cell changes to acting mark.

### TST-INV-003 — Revision delta

Property:

```text
accepted => new_revision = old_revision + 1
rejected => new_revision = old_revision
```

### TST-INV-004 — Pointer authority

Property: no actor other than current active actor can produce an accepted move.

Covers: `TTT-INV-003`.

### TST-INV-005 — Terminal pointer absence

Property: `status != active => active_player_index is null`.

### TST-INV-006 — Winner consistency

Property:

```text
status == won  <=> winner_actor_id is not null
```

### TST-INV-007 — Draw consistency

Property: draw implies board full, winner null, pointer null.

### TST-INV-008 — Configured winner

Property: any non-null winner is one of configured actor IDs.

### TST-INV-009 — No strategic server function

Static inspection requirement: deterministic core shall contain no function whose responsibility is to rank, search, score, or choose candidate game moves for a player.

Covers: `TTT-INV-008`, `TTT-STRATEGY-001`.

## 14. Determinism / Property-Based Tests

Where the implementation language permits, add generated/property-based tests over valid configurations and action sequences.

### TST-PROP-001 — Repeatability

For generated valid state/action pairs, executing the transition twice from structurally equal states produces structurally equal results.

### TST-PROP-002 — Revision monotonicity

Across generated accepted action sequences, revisions form exactly:

```text
0, 1, 2, ..., n
```

### TST-PROP-003 — Board occupancy monotonicity

Across accepted actions, occupied-cell count increments exactly one per action until termination.

### TST-PROP-004 — Pointer follows configured cycle

For all accepted nonterminal moves, next pointer equals the successor of prior pointer modulo player count.

### TST-PROP-005 — Terminal stability

For any generated terminal state, every subsequent syntactically valid move proposal is rejected and leaves state unchanged.

## 15. First-Tranche Acceptance Scenario

A minimum end-to-end deterministic-core scenario shall execute an ordinary 3×3 two-player game entirely through the transition API.

Example accepted sequence:

```text
P1 -> (0,0)
P2 -> (1,0)
P1 -> (0,1)
P2 -> (1,1)
P1 -> (0,2)
```

Expected final state:

```text
revision = 5
turn_number = 5
status = won
winner_actor_id = P1
active_player_index = null
```

At an intermediate point, attempt at least one wrong-actor or occupied-cell move and verify that it is rejected without modifying the state or execution pointer.

This scenario establishes the deterministic core before MCP transport or actor adapters are introduced.

## 16. Requirement Coverage Matrix

| Requirement | Primary Tests |
|---|---|
| `TTT-STATE-001` | TST-STATE-004, TST-INV-001 |
| `TTT-STATE-002` | TST-STATE-001–003, TST-VALID-002, TST-PROP-002 |
| `TTT-STATE-003` | TST-STATE-005, TST-PROP-001 |
| `TTT-STATE-004` | TST-VALID-010, TST-TERM-001–002, TST-PROP-005 |
| `TTT-GAME-001` | TST-CONFIG-002–005, TST-ORCH-003, TST-MULTI-001–002 |
| `TTT-GAME-002` | TST-CONFIG-001, larger-board win tests |
| `TTT-GAME-003` | TST-CONFIG-008, TST-WIN-001–008 |
| `TTT-GAME-004` | TST-CONFIG-007, TST-MOVE-002 |
| `TTT-GAME-005` | TST-MOVE-001–002, TST-PROP-003 |
| `TTT-GAME-006` | TST-VALID-001–010 |
| `TTT-GAME-007` | TST-WIN-001–009, TST-MULTI-002 |
| `TTT-GAME-008` | TST-DRAW-001–002, TST-WIN-009 |
| `TTT-GAME-009` | TST-CONFIG-001, first-tranche acceptance scenario |
| `TTT-ORCH-001` | TST-ORCH-001, TST-ORCH-005 |
| `TTT-ORCH-002` | TST-ORCH-001–003, TST-PROP-004 |
| `TTT-ORCH-003` | TST-VALID-003, TST-INV-004 |
| `TTT-INV-001` | TST-STATE-004 |
| `TTT-INV-003` | TST-VALID-003, TST-INV-004 |
| `TTT-INV-004` | all rejection tests, TST-INV-001 |
| `TTT-INV-005` | partially supported by revision exact-match tests; full simultaneous commit test deferred to concurrency layer |
| `TTT-INV-008` | TST-INV-009 |

## 17. Implemented Integration Test Tranches

The executable suite in `../plugins/collaborative-tic-tac-toe/tests/` now adds the previously deferred coverage:

| Area | Executable coverage |
|---|---|
| Perspective | Exact view field allow-list, actor-specific `you`/turn values, no raw index/history-depth leakage, unknown actor fails closed |
| Environment | Current revision updates, projected prior states, deterministic truncation to configured depth |
| Adapter boundary | Service accepts semantic actions while pure server transition retains final validity authority |
| Transactions | Durable genesis, accepted events, separate rejection audit, state/event equality on reopen |
| Replay | Ordered reduction through the production transition function and current/replay digest equality |
| Concurrency | Two independent service instances race at revision zero; exactly one commits and the other is stale |
| Idempotency | Identical retry returns the stored result; changed request with reused ID is rejected |
| MCP | Exact four-tool registration plus a real STDIO initialize and `tools/list` exchange |
| Private deployment | Windows launchers use an isolated environment, durable database, official local-STDIO tunnel profile, doctor validation, and no embedded credential |
| End to end | Persistent two-player game reaches a win and clears the execution pointer |

## 18. Validation Commands

From repository root after installing the package in an isolated environment:

```bash
python -m compileall -q plugins/collaborative-tic-tac-toe/src plugins/collaborative-tic-tac-toe/tests
python -m unittest discover -s plugins/collaborative-tic-tac-toe/tests -v
```

The transport check launches `python -m collaborative_ttt.mcp_server` through the MCP SDK's STDIO client, initializes a session, and asserts that `tools/list` returns only `create_game`, `get_actor_environment`, `submit_move`, and `verify_replay`.

The remaining acceptance checks are installation/enabling in the user's ChatGPT desktop/Codex host and the credentialed browser route: run `tunnel-client` on the home laptop, create a ChatGPT developer-mode app using the associated Tunnel, confirm the exact four-tool discovery, create a game, read an actor environment, and submit a legal move. These checks require the user's laptop, Platform tunnel identity/runtime key, and ChatGPT account and therefore cannot be claimed by the repository unit-test process.
