# Collaborative MCP Tic-Tac-Toe — Requirements

## 1. Identity

- **Profile:** Tic-Tac-Toe
- **Type:** Application Profile
- **Status:** Draft
- **Parent Framework:** MCP Collaborative
- **Parent Standard:** `APPLICATION_PROFILE_STANDARD.md`

## 2. Mission

Design and implement a minimal collaborative MCP system in which multiple independent AI actors participate in a shared, persistent environment through controlled perspectives.

The system uses turn-based tic-tac-toe as its initial test domain because the game provides simple, deterministic rules and easily verifiable outcomes while permitting strategic complexity to increase without requiring a correspondingly complex state model.

Each participant exists as a typed actor with an assigned role and perspective. Actors do not interact directly with the complete authoritative state. Instead, each actor operates through a persistent environment containing the current state visible from its perspective and a finite history of previous visible states.

The MCP server maintains authoritative shared state, enforces state transitions, persists the transaction record, and deterministically coordinates which actor is eligible to act. An adapter layer mediates between authoritative state and each actor's permitted persistent environment.

The objective is not primarily to build a tic-tac-toe application. The prototype exists to demonstrate a general collaborative architecture in which independent AI actors can reliably coordinate through shared state while maintaining distinct roles, perspectives, bounded histories, and execution authority.

The architecture must remain sufficiently domain-independent that tic-tac-toe actors can later be replaced by other collaborative actor types without changing the fundamental orchestration model.

## 3. Scope

The first prototype shall support a deterministic, turn-based tic-tac-toe game coordinated through an MCP server.

The prototype shall test multiple independent actors, authoritative server-side state, typed actors, actor roles, restricted actor perspectives, actor-specific persistent environments, bounded state history, deterministic turn assignment, deterministic state transitions, transaction persistence, concurrency protection, and deterministic reconstruction of shared state.

Tic-tac-toe strategy is not part of the MCP server's responsibility.

## 4. Relationship to MCP Collaborative

This profile exercises typed collaborative actors, role assignment, perspective-controlled state projection, actor-specific persistent environments, bounded actor-visible history, authoritative shared state, deterministic execution-pointer assignment, semantic action submission, server-side validation, persistent transaction recording, deterministic replay, concurrency protection, and idempotent action handling.

The tic-tac-toe domain specializes these capabilities without redefining them as game-specific framework behavior.

## 5. Actor Model

### TTT-ACTOR-001 — Typed actors
Every participant shall be represented as an actor with an explicit type. The initial actor type shall be `player`.

### TTT-ACTOR-002 — Actor identity
Every actor shall have a stable unique identifier within the game.

### TTT-ACTOR-003 — Role
Every actor shall have an assigned role describing its function in the game. For tic-tac-toe, the role shall identify the player's mark or equivalent game-specific position. Role and actor type shall remain distinct concepts.

### TTT-ACTOR-004 — Perspective
Every actor shall have an assigned perspective defining what portions or projections of authoritative state the actor is permitted to observe. An actor shall not receive unrestricted authoritative state merely because that state exists on the MCP server.

### TTT-ACTOR-005 — Generality
The actor abstraction shall not encode tic-tac-toe-specific assumptions that prevent later use for roles such as worker, supervisor, evaluator, planner, critic, or other collaborative participants.

## 6. Perspectives and Information Boundaries

### TTT-PERSPECTIVE-001 — Projection
The system shall derive each actor-visible state from authoritative state through that actor's assigned perspective.

### TTT-PERSPECTIVE-002 — No bypass
No authoritative information shall enter an actor's persistent environment except through an explicitly permitted projection or explicitly defined actor-visible event.

### TTT-PERSPECTIVE-003 — Actor-specific views
Different actors may receive different representations of the same authoritative revision.

### TTT-PERSPECTIVE-004 — Perspective independence
The authoritative state model shall not depend on any individual actor's perspective representation.

### TTT-PERSPECTIVE-005 — Allow-list behavior
Perspective projection should be defined by explicitly permitted information rather than unrestricted copying followed by removal of prohibited fields. New authoritative fields shall not become actor-visible merely because they were added to the authoritative state.

### TTT-PERSPECTIVE-006 — Fail closed
If perspective projection cannot be safely completed, the system shall not expose unrestricted authoritative state as a fallback.

## 7. Persistent Actor Environment

### TTT-ENV-001 — Environment ownership
Each actor shall have a persistent environment associated with its participation in the game.

### TTT-ENV-002 — Current state
The persistent environment shall contain the actor's current permitted view of the collaborative state.

### TTT-ENV-003 — Bounded history
The persistent environment shall contain a finite number of previous actor-visible states. The maximum history depth shall be explicit.

### TTT-ENV-004 — Perspective-preserving history
Historical states stored in an actor environment shall contain the state as visible to that actor at that revision, not unrestricted snapshots of authoritative state.

### TTT-ENV-005 — Deterministic history update
When a new actor-visible state becomes current, the previous visible state shall move into bounded history according to a deterministic retention policy. States exceeding the configured history depth shall cease to be part of the actor's active persistent environment.

### TTT-ENV-006 — Separation from authoritative history
Bounded actor history shall not be treated as the authoritative transaction record. The server may retain complete authoritative history while exposing only bounded history to an actor.

### TTT-ENV-007 — Perspective changes
The design shall explicitly define how historical actor-visible state is handled when an actor's role or perspective changes. Prior visibility shall not unintentionally authorize continued disclosure after a perspective change.

## 8. Authoritative State

### TTT-STATE-001 — Server authority
The MCP server shall be the sole authority for shared game state. Actors may propose actions but shall not directly mutate authoritative state.

### TTT-STATE-002 — Revision
Authoritative state shall have a monotonically advancing revision or equivalent ordering mechanism sufficient to identify the state against which an action was proposed.

### TTT-STATE-003 — Deterministic transition
Given the same valid prior authoritative state and the same accepted action, the state-transition mechanism shall produce the same resulting state.

### TTT-STATE-004 — Terminal state
Once the game reaches a terminal state, subsequent game actions shall not mutate the completed game state.

## 9. Adapter

### TTT-ADAPTER-001 — Mediation
An adapter shall mediate between authoritative MCP state and actor-facing persistent environments.

### TTT-ADAPTER-002 — State adaptation
The adapter shall use actor identity, actor type, role, perspective, authoritative state, and applicable events to construct or update the actor's permitted persistent environment.

### TTT-ADAPTER-003 — Action adaptation
The adapter shall provide a defined mechanism by which actor/model output becomes a proposed semantic action suitable for server-side validation.

### TTT-ADAPTER-004 — No validation authority
The adapter or actor-facing model shall not become the final authority on whether a proposed state mutation is valid. Authoritative validation shall remain server-side.

### TTT-ADAPTER-005 — Domain separation
Generic adapter behavior shall be separable from tic-tac-toe-specific rules.

## 10. Orchestration

### TTT-ORCH-001 — Single execution pointer
The authoritative activity state shall identify which actor currently has authority to submit the next game action.

### TTT-ORCH-002 — Server assignment
The MCP server shall deterministically assign or advance this execution pointer after an accepted nonterminal action. The acting model shall not choose its successor.

### TTT-ORCH-003 — Turn enforcement
Actions submitted by an actor that does not own the current execution pointer shall not mutate authoritative game state.

### TTT-ORCH-004 — No manual state relay
The architecture shall not require the human user to manually copy game state or determine whose turn occurs next.

## 11. Tic-Tac-Toe Domain Requirements

### TTT-GAME-001 — Players
The game shall support two to four players.

### TTT-GAME-002 — Board
The game shall use an `N × N` board. Board size shall be configurable at game creation.

### TTT-GAME-003 — Win length
The game shall use a configurable win length `K` representing the number of contiguous marks required to win. A winning sequence may be horizontal, vertical, or diagonal in either diagonal direction.

### TTT-GAME-004 — Marks
Each player shall have a unique game mark or equivalent unambiguous representation on the board.

### TTT-GAME-005 — Move
A turn shall consist of placing exactly one player's mark in one currently unoccupied board cell.

### TTT-GAME-006 — Validity
At minimum, the server shall reject moves by the wrong actor, moves against stale state revisions, moves outside the board, moves into occupied cells, malformed actions, and moves submitted after game termination. Rejected moves shall not alter authoritative game state.

### TTT-GAME-007 — Win
The game shall terminate immediately after a valid move creates a qualifying contiguous sequence of length `K` for the acting player.

### TTT-GAME-008 — Draw
If the board becomes full without a winner, the game shall terminate as a draw.

### TTT-GAME-009 — Baseline configuration
The system shall support ordinary two-player `3 × 3`, `K = 3` tic-tac-toe as the baseline verification configuration. The collaboration protocol shall remain the same when board size, win length, or supported player count changes.

## 12. Transactions and Persistence

### TTT-TXN-001 — Transaction record
Authoritative state-changing activity shall be represented by a persistent transaction/event record sufficient to establish what happened and in what order.

### TTT-TXN-002 — Genesis
The record shall include or reference sufficient initialization information to reconstruct game configuration, player ordering, actor identities, actor roles, initial execution pointer, and initial state.

### TTT-TXN-003 — Accepted actions
Each accepted action shall record enough information to identify at minimum the game, acting actor, action, prior revision, resulting revision, acceptance outcome, and resulting execution pointer or terminal condition.

### TTT-TXN-004 — Rejected actions
Whether rejected attempts belong in the authoritative state-transition log or a separate audit record shall be specified by design. Rejected actions must never be replayed as accepted state transitions.

### TTT-TXN-005 — Replay
Replaying the accepted authoritative transactions from the defined initial state shall reproduce the same authoritative final state.

## 13. Concurrency and Idempotency

### TTT-CONCURRENCY-001 — Serialization
The server shall serialize competing state-changing actions so that no two actions can both successfully commit against the same authoritative revision.

### TTT-CONCURRENCY-002 — Stale actions
An action based on a revision that is no longer current shall not silently commit against the newer state.

### TTT-CONCURRENCY-003 — Retry safety
The protocol shall provide an action identifier or equivalent mechanism for distinguishing a retry of the same proposed action from a new action. Transport or client retries shall not accidentally create duplicate state transitions.

## 14. Strategy Independence

### TTT-STRATEGY-001 — No server strategy
The MCP server shall not contain game-playing strategy used to choose player moves.

### TTT-STRATEGY-002 — Semantic decision
The substantive choice of a player's move shall be made by the player actor/model or another explicitly assigned decision-making actor, not by the deterministic orchestration layer.

### TTT-STRATEGY-003 — Strategy replacement
Changing a player's reasoning method—random, heuristic, recursive search, minimax where applicable, or another strategy—shall not require modification of the collaboration protocol.

## 15. Deterministic vs Semantic Responsibilities

### TTT-BOUNDARY-001 — Deterministic responsibilities
Deterministic infrastructure shall be responsible for validating action eligibility, applying valid state transitions, advancing revisions, detecting game termination, maintaining authoritative persistence, enforcing perspectives, maintaining bounded environments, and assigning the next execution pointer.

### TTT-BOUNDARY-002 — Semantic responsibilities
Actors/models shall be responsible for interpreting actor-visible environments, selecting strategy, choosing among valid candidate moves, and producing proposed semantic actions.

## 16. Invariants

### TTT-INV-001
Only the MCP server may mutate authoritative game state.

### TTT-INV-002
No actor-visible state may bypass the actor's perspective boundary.

### TTT-INV-003
Only the actor owning the current execution pointer may successfully advance the game.

### TTT-INV-004
Rejected actions shall not mutate authoritative state.

### TTT-INV-005
No two accepted actions may commit against the same authoritative revision.

### TTT-INV-006
Actor environment history shall never exceed its configured history depth.

### TTT-INV-007
Replay of accepted transactions shall reproduce the same authoritative state.

### TTT-INV-008
The MCP server shall not choose strategic game moves for player actors.

## 17. Failure Behavior

The design shall define deterministic handling for malformed actions, stale revisions, incorrect acting actor, occupied cells, out-of-bounds cells, actions after terminal state, duplicate action identifiers, projection failures, persistence failures, invalid actor configuration, and invalid game configuration.

Projection or authorization failure shall fail closed rather than expose unrestricted state or permit an unauthorized mutation.

## 18. Non-Goals

Unless later requirements explicitly add them, the initial prototype does not require graphical game interfaces, hidden inventories, resource economies, special player abilities, matchmaking, rankings or scoring systems across games, complex authentication, player chat, timeout/forfeit mechanics, server-side strategic game playing, or indefinite actor-visible conversational history.

These exclusions exist to keep the prototype focused on collaborative orchestration, persistence, perspective, and state transitions.

## 19. Acceptance Criteria

The prototype succeeds when two to four independent AI player actors can complete a configured tic-tac-toe game through the shared MCP system without a human manually coordinating turns or relaying state, while all of the following remain true:

1. the MCP server retains authoritative state;
2. each actor sees only its permitted perspective;
3. each actor operates from a persistent environment containing current state and bounded previous states;
4. only the actor owning the execution pointer can successfully advance the game;
5. competing or stale actions cannot corrupt state;
6. accepted transitions are persistently recorded;
7. the final authoritative state can be deterministically reconstructed from the initial state and accepted transaction history;
8. the MCP server does not choose strategic moves for the players;
9. the collaboration protocol continues to function across supported `N`, `K`, and player-count configurations; and
10. the collaboration architecture remains usable beyond the tic-tac-toe domain.

## 20. Mandatory Delivery Artifacts

The following repository artifacts are mandatory companions to this profile:

- `PRIORITIZATION.md` fixes dependency order and implementation tranches;
- `REQUIREMENT_WORK_LEDGER.md` records every substantive requirement-affecting commit with its exact UTC timestamp;
- `DESIGN.md` records the implemented deterministic and persistence boundaries;
- `TEST_PLAN.md` records executable conformance coverage; and
- `../plugins/collaborative-tic-tac-toe/` contains the installable local OpenAI plugin and MCP runtime.

The initial runnable profile uses a bundled local STDIO MCP server declared by the plugin's `.mcp.json`. The ChatGPT desktop/Codex host launches that server directly. A public endpoint, third-party tunnel, OpenAI Platform tunnel, and OpenAI API key are not requirements of this local prototype.

Local STDIO availability is a host boundary, not a change to collaboration semantics: ChatGPT web does not read a computer's local MCP configuration. Remote or public distribution may add another transport later without changing the server-owned game protocol.
