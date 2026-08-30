# Collaborative MCP Tic-Tac-Toe — Design

## 1. Design Scope

This design defines the first implementation tranche of the Tic-Tac-Toe application profile. It directly addresses:

- `TTT-STATE-001` through `TTT-STATE-004`;
- `TTT-GAME-001` through `TTT-GAME-009`;
- `TTT-ORCH-001` through `TTT-ORCH-003`;
- `TTT-INV-001`, `TTT-INV-003`, `TTT-INV-004`, `TTT-INV-005`, and `TTT-INV-008`;
- the applicable portions of `TTT-BOUNDARY-001` and `TTT-BOUNDARY-002`.

Perspective projection, persistent actor environments, transaction persistence/replay, concurrency transport mechanics, idempotency persistence, and MCP protocol binding remain later design tranches. The core defined here must not preclude them.

## 2. Architectural Principle

The game engine is a pure deterministic state machine. Models may select proposed moves, but only deterministic server-side code validates and applies them.

```text
semantic actor decision
        │
        ▼
 proposed GameAction
        │
        ▼
 deterministic validator
        │
   reject│accept
        │
        ▼
 deterministic transition
        │
        ▼
 authoritative GameState
```

No game-playing strategy belongs in this state machine.

## 3. Core Components

### 3.1 `GameConfig`

Immutable game configuration established at game creation.

Responsibilities:

- define board size `N`;
- define win length `K`;
- define deterministic player ordering;
- bind player IDs to unique marks;
- reject invalid configurations before authoritative state is created.

### 3.2 `GameState`

Immutable authoritative snapshot of one game revision.

Responsibilities:

- represent the complete current board;
- identify the current revision;
- identify the current execution pointer;
- represent game status and winner;
- expose no mutation methods to actors.

### 3.3 `GameAction`

Semantic proposal to place one mark in one board cell.

The core action schema is:

```json
{
  "game_id": "game-123",
  "actor_id": "P1",
  "revision": 7,
  "move": [1, 2],
  "action_id": "client-generated-id"
}
```

`action_id` is carried now so the core interface remains compatible with later idempotency enforcement, although persistent duplicate detection is outside this tranche.

### 3.4 Validator

Pure function that evaluates a `GameAction` against one `GameState`.

It performs eligibility and domain validation only. It never mutates state.

### 3.5 Transition function

Pure function that applies an already validated action and derives the next authoritative state.

### 3.6 Terminal evaluator

Pure functions that detect a win or draw after a move.

## 4. State Model

### 4.1 Game configuration

Conceptual schema:

```text
GameConfig
├── game_id: str
├── board_size: int            # N
├── win_length: int            # K
└── players: ordered tuple
    └── PlayerConfig
        ├── actor_id: str
        └── mark: str
```

Constraints:

- player count: 2 through 4 inclusive;
- `board_size >= 1`;
- `1 <= win_length <= board_size`;
- all actor IDs unique;
- all marks unique;
- player order preserved exactly as supplied after successful configuration validation.

The baseline configuration is 2 players, `N=3`, `K=3`.

### 4.2 Authoritative game state

Conceptual schema:

```text
GameState
├── game_id: str
├── revision: int
├── board_size: int
├── win_length: int
├── players: ordered tuple[PlayerConfig]
├── board: tuple[tuple[str | null, ...], ...]
├── active_player_index: int | null
├── turn_number: int
├── status: "active" | "won" | "draw"
└── winner_actor_id: str | null
```

Derived execution pointer:

```text
active_actor_id = players[active_player_index].actor_id
```

when `status == "active"`.

For terminal states, `active_player_index` must be `null`.

### 4.3 Initial state

A valid new game begins as:

```text
revision = 0
turn_number = 0
board = all null cells
active_player_index = 0
status = "active"
winner_actor_id = null
```

The initial execution pointer is therefore the first player in deterministic player order.

## 5. Immutability and Authority

Authoritative snapshots are treated as immutable values.

A transition creates a new `GameState`; it does not modify the prior instance in place. This simplifies replay, invariant testing, stale-action checking, and later concurrent commit control.

Actor/model code receives no reference that grants mutation authority over authoritative state.

This design satisfies `TTT-STATE-001` and supports `TTT-INV-001` mechanically rather than procedurally.

## 6. Action Validation

Define:

```text
validate_action(state, action) -> ValidationResult
```

Validation is deterministic and side-effect free.

The validator SHALL reject, at minimum, in this order or with equivalent deterministic precedence:

1. malformed action structure;
2. `action.game_id != state.game_id`;
3. `state.status != "active"`;
4. `action.revision != state.revision`;
5. `action.actor_id != active_actor_id`;
6. malformed move coordinate;
7. row or column outside `[0, N-1]`;
8. target cell already occupied.

A rejection returns a machine-readable error code and leaves the supplied state unchanged.

Recommended error codes:

```text
MALFORMED_ACTION
WRONG_GAME
GAME_TERMINAL
STALE_REVISION
WRONG_ACTOR
MALFORMED_MOVE
OUT_OF_BOUNDS
CELL_OCCUPIED
```

Validation does not choose an alternate move and does not repair an invalid actor proposal.

## 7. State Transition Algorithm

Define the authoritative pure transition interface:

```text
transition(state, action) -> TransitionResult
```

Algorithm:

```text
1. validation = validate_action(state, action)
2. if validation rejects:
       return rejected result containing original state
3. identify acting player's mark
4. construct a new board with exactly the target cell changed
5. increment revision by exactly 1
6. increment turn_number by exactly 1
7. evaluate whether acting player now has a win
8. if win:
       status = "won"
       winner_actor_id = acting actor
       active_player_index = null
       return accepted next state
9. else if board is full:
       status = "draw"
       winner_actor_id = null
       active_player_index = null
       return accepted next state
10. else:
       status = "active"
       winner_actor_id = null
       active_player_index =
           (prior active_player_index + 1) mod player_count
       return accepted next state
```

No other state field may change as a side effect of a move.

## 8. Win Detection

Win detection must support arbitrary valid `N`, `K`, and 2–4 player configurations.

A win exists if the acting player's mark occupies at least `K` contiguous cells along any one of four axes:

- horizontal `(0, 1)`;
- vertical `(1, 0)`;
- descending diagonal `(1, 1)`;
- ascending diagonal `(1, -1)`.

The preferred algorithm evaluates only lines passing through the newly placed mark.

For each axis:

```text
count = 1
count same mark moving in positive direction
count same mark moving in negative direction
if count >= K: win
```

This correctly handles winning runs longer than `K` and avoids scanning unrelated board positions.

The algorithm must not wrap across board edges.

## 9. Draw Detection

A draw exists iff:

```text
status was active before the accepted move
AND no win exists after the move
AND every board cell is occupied
```

Win evaluation precedes draw evaluation so a board-filling winning move is recorded as a win, not a draw.

## 10. Execution Pointer

The execution pointer is authoritative state, represented by `active_player_index` and derived `active_actor_id`.

Rules:

- at genesis, pointer = first configured player;
- rejected actions do not change the pointer;
- accepted nonterminal actions advance the pointer exactly once in configured cyclic player order;
- terminal transitions clear the pointer;
- actors cannot nominate or select the next actor.

This directly implements `TTT-ORCH-001` through `TTT-ORCH-003`.

## 11. Revision Semantics

Revision is a monotonic state-transition counter.

Rules:

- genesis revision is `0`;
- each accepted action increments revision by exactly `1`;
- rejected actions do not increment revision;
- no valid transition may decrease revision;
- a proposed action must identify the current revision exactly.

This establishes the local stale-action rule required by `TTT-STATE-002` and prepares the implementation for later compare-and-commit concurrency control.

## 12. Deterministic vs Semantic Boundary

### Deterministic core owns

- configuration validation;
- turn eligibility;
- stale revision validation;
- board bounds and occupancy validation;
- move application;
- win detection;
- draw detection;
- revision advancement;
- turn-number advancement;
- execution-pointer advancement;
- terminal-state lockout.

### Actor/model owns

- interpreting its later projected environment;
- selecting strategy;
- selecting a candidate cell;
- emitting a semantic action proposal.

The deterministic core must never rank legal cells, suggest a move, invoke minimax, or otherwise choose strategy.

## 13. Failure Semantics

All domain/eligibility failures are represented as rejected transition results rather than exceptions where the failure is an expected invalid proposal.

Programming errors, structurally impossible internal states, or invariant corruption may raise internal exceptions because they represent server defects rather than actor-invalid actions.

Expected rejection result shape:

```text
TransitionResult
├── accepted: false
├── state: exact original GameState
└── error
    ├── code
    └── detail
```

Accepted result shape:

```text
TransitionResult
├── accepted: true
├── state: new GameState
└── error: null
```

## 14. Core Invariants

The implementation shall mechanically preserve the following after every transition attempt:

1. rejected transition => returned state equals prior state;
2. accepted transition => revision = prior revision + 1;
3. accepted transition => exactly one previously empty board cell becomes the acting player's mark;
4. only current execution-pointer actor can receive an accepted result;
5. nonterminal accepted transition advances pointer to the next configured actor;
6. terminal transition clears the pointer;
7. terminal state cannot accept a later move;
8. winner is either null or one configured actor;
9. `status == "won"` iff `winner_actor_id` is non-null;
10. `status == "draw"` implies winner is null and board is full;
11. server core contains no strategic move-selection function.

## 15. Future Integration Boundaries

The core shall be implementable independently of MCP transport and persistence.

Later layers will wrap this core:

```text
MCP transport
    ↓
actor/action adapter
    ↓
transaction + concurrency boundary
    ↓
THIS deterministic game core
    ↓
authoritative next state
    ↓
transaction persistence
    ↓
perspective/environment projection
```

The core API must therefore consume ordinary data structures/value objects and return deterministic results without requiring network, model, filesystem, or database access.

## 16. Requirement Mapping

| Design Element | Requirements |
|---|---|
| Immutable authoritative state | `TTT-STATE-001`, `TTT-STATE-003`, `TTT-INV-001` |
| Revision field and exact-match validation | `TTT-STATE-002`, `TTT-GAME-006` |
| Terminal lockout | `TTT-STATE-004`, `TTT-GAME-006` |
| Configurable player/board/win schemas | `TTT-GAME-001`–`TTT-GAME-004`, `TTT-GAME-009` |
| Single-cell move transition | `TTT-GAME-005` |
| Validation pipeline | `TTT-GAME-006`, `TTT-INV-003`, `TTT-INV-004` |
| Four-axis contiguous win detector | `TTT-GAME-003`, `TTT-GAME-007` |
| Full-board draw detector | `TTT-GAME-008` |
| Authoritative execution pointer | `TTT-ORCH-001`–`TTT-ORCH-003`, `TTT-INV-003` |
| Pure transition boundary | `TTT-STATE-003`, `TTT-BOUNDARY-001` |
| No strategy in core | `TTT-INV-008`, `TTT-STRATEGY-001`, `TTT-BOUNDARY-002` |
| One-revision-per-accepted-transition rule | supports `TTT-INV-005`; full concurrent commit serialization remains a later layer |
