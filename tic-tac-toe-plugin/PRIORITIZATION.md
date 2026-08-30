# Collaborative MCP Tic-Tac-Toe — Requirement Prioritization

## Purpose

This project-governance document fixes the intended order of completion for the normative requirements in `REQUIREMENTS.md` before implementation proceeds.

It is not itself an application requirement. It does not add behavior to the application. It records the planned order, deliverables, and technical dependencies for completing the existing requirements.

## Completion tranches

| Priority | Tranche | Objective |
|---|---|---|
| P1 | Deterministic game core | Immutable authoritative state, configuration, game rules, terminal evaluation, and server-owned execution pointer |
| P2 | Actor abstraction | Generic actor identity, type, and role model |
| P3 | Perspective boundary | Allow-listed projections and fail-closed information-flow enforcement |
| P4 | Persistent actor environments | Current projected state and bounded actor-visible history |
| P5 | Adapter boundary | State projection and semantic action adaptation while preserving server authority |
| P6 | Transactions and replay | Genesis, accepted-event persistence, rejected-action treatment, and deterministic replay |
| P7 | Concurrency and idempotency | Serialization, stale-action protection, and duplicate-action safety |
| P8 | MCP collaboration integration | Bind independent model/chat actors to the deterministic runtime without manual state relay |
| P9 | End-to-end conformance | Acceptance, security, replay, concurrency, and cross-configuration verification |

## Requirement prioritization matrix

| Order | Requirement | Descriptor | Necessary deliverables | Technical dependencies | Tranche |
|---:|---|---|---|---|---|
| 1 | TTT-STATE-001 | Server authority | Immutable authoritative `GameState`; server-only transition API; authority tests | None | P1 |
| 2 | TTT-STATE-002 | Revision | Monotonic revision; stale-revision validation; tests | TTT-STATE-001 | P1 |
| 3 | TTT-GAME-001 | Players | 2–4 player configuration and deterministic ordering | TTT-STATE-001 | P1 |
| 4 | TTT-GAME-002 | Board | Configurable `N x N` board schema | TTT-STATE-001 | P1 |
| 5 | TTT-GAME-003 | Win length | Configurable `K`; validation | TTT-GAME-002 | P1 |
| 6 | TTT-GAME-004 | Marks | Unique actor-to-mark bindings | TTT-GAME-001 | P1 |
| 7 | TTT-ORCH-001 | Single execution pointer | Authoritative active-actor pointer | TTT-GAME-001, TTT-STATE-001 | P1 |
| 8 | TTT-GAME-005 | Move | Semantic action schema; exactly-one-cell transition | TTT-GAME-002, TTT-GAME-004, TTT-ORCH-001 | P1 |
| 9 | TTT-GAME-006 | Validity | Deterministic validator and rejection codes | TTT-STATE-002, TTT-GAME-005, TTT-ORCH-001 | P1 |
| 10 | TTT-STATE-003 | Deterministic transition | Pure transition function; determinism tests | TTT-GAME-005, TTT-GAME-006 | P1 |
| 11 | TTT-GAME-007 | Win | Four-axis contiguous-`K` detector | TTT-GAME-003, TTT-STATE-003 | P1 |
| 12 | TTT-GAME-008 | Draw | Full-board/no-win terminal evaluation | TTT-GAME-007, TTT-STATE-003 | P1 |
| 13 | TTT-STATE-004 | Terminal state | Terminal lockout; cleared pointer | TTT-GAME-007, TTT-GAME-008 | P1 |
| 14 | TTT-ORCH-002 | Server assignment | Deterministic cyclic pointer advancement | TTT-ORCH-001, TTT-STATE-003 | P1 |
| 15 | TTT-ORCH-003 | Turn enforcement | Wrong-actor rejection without mutation | TTT-ORCH-001, TTT-GAME-006 | P1 |
| 16 | TTT-GAME-009 | Baseline configuration | 3x3/K3/2-player fixture plus larger/multiplayer fixtures | TTT-GAME-001 through TTT-GAME-008 | P1 |
| 17 | TTT-INV-001 | Server-only mutation | Direct invariant tests | TTT-STATE-001 | P1 |
| 18 | TTT-INV-003 | Pointer owner only | Wrong-actor invariant tests | TTT-ORCH-003 | P1 |
| 19 | TTT-INV-004 | Rejections do not mutate | Full-state equality assertions on rejection | TTT-GAME-006 | P1 |
| 20 | TTT-INV-008 | No server strategy | Boundary test/inspection proving transition core never selects moves | TTT-STATE-003, TTT-GAME-005 | P1 |
| 21 | TTT-ACTOR-001 | Typed actors | Generic `Actor` model with explicit type | P1 interfaces stable | P2 |
| 22 | TTT-ACTOR-002 | Actor identity | Stable unique actor ID validation | TTT-ACTOR-001 | P2 |
| 23 | TTT-ACTOR-003 | Role | Role distinct from type and identity | TTT-ACTOR-001, TTT-ACTOR-002 | P2 |
| 24 | TTT-ACTOR-005 | Generality | Domain-neutral actor interfaces and tests | TTT-ACTOR-001 through TTT-ACTOR-003 | P2 |
| 25 | TTT-ACTOR-004 | Perspective | Perspective binding on actor model | TTT-ACTOR-001 through TTT-ACTOR-003 | P3 |
| 26 | TTT-PERSPECTIVE-001 | Projection | `Perspective.project()` contract | TTT-ACTOR-004 | P3 |
| 27 | TTT-PERSPECTIVE-004 | Perspective independence | Separation tests between authoritative and projected schema | TTT-PERSPECTIVE-001 | P3 |
| 28 | TTT-PERSPECTIVE-005 | Allow-list behavior | Explicit allow-list projection; unknown-field tests | TTT-PERSPECTIVE-001 | P3 |
| 29 | TTT-PERSPECTIVE-006 | Fail closed | Projection-error path exposing no authoritative fallback | TTT-PERSPECTIVE-001 | P3 |
| 30 | TTT-PERSPECTIVE-003 | Actor-specific views | Multi-actor projection tests for same revision | TTT-PERSPECTIVE-001 | P3 |
| 31 | TTT-PERSPECTIVE-002 | No bypass | Single controlled ingress to actor environment; leakage tests | TTT-PERSPECTIVE-001, TTT-PERSPECTIVE-005, TTT-PERSPECTIVE-006 | P3 |
| 32 | TTT-INV-002 | Perspective boundary | Direct leakage/bypass invariant tests | TTT-PERSPECTIVE-002 | P3 |
| 33 | TTT-ENV-001 | Environment ownership | Per-actor `PersistentEnvironment` | TTT-ACTOR-002, TTT-PERSPECTIVE-001 | P4 |
| 34 | TTT-ENV-002 | Current state | Current `ProjectedState` with source revision | TTT-ENV-001 | P4 |
| 35 | TTT-ENV-003 | Bounded history | Explicit history-depth configuration | TTT-ENV-001 | P4 |
| 36 | TTT-ENV-004 | Perspective-preserving history | Projected snapshots only | TTT-ENV-002, TTT-PERSPECTIVE-002 | P4 |
| 37 | TTT-ENV-005 | Deterministic history update | Shift/truncate algorithm; depth-0 tests | TTT-ENV-002, TTT-ENV-003 | P4 |
| 38 | TTT-ENV-006 | Separation from authoritative history | Type/storage separation from transaction record | TTT-ENV-004 | P4 |
| 39 | TTT-ENV-007 | Perspective changes | Clear/rebuild policy and leakage tests | TTT-ENV-004, TTT-PERSPECTIVE-002 | P4 |
| 40 | TTT-INV-006 | History depth invariant | Direct bound tests | TTT-ENV-005, TTT-ENV-007 | P4 |
| 41 | TTT-ADAPTER-001 | Mediation | Adapter interface between authoritative state and actor environment | P3, P4 | P5 |
| 42 | TTT-ADAPTER-002 | State adaptation | Deterministic `ADAPT` operation | TTT-ADAPTER-001 | P5 |
| 43 | TTT-ADAPTER-003 | Action adaptation | `ACT` operation converting model output to semantic action | TTT-ADAPTER-001, TTT-GAME-005 | P5 |
| 44 | TTT-ADAPTER-004 | No validation authority | Server validation downstream of adapter; negative tests | TTT-ADAPTER-003, TTT-GAME-006 | P5 |
| 45 | TTT-ADAPTER-005 | Domain separation | Generic adapter plus tic-tac-toe specialization | TTT-ADAPTER-002, TTT-ADAPTER-003 | P5 |
| 46 | TTT-TXN-001 | Transaction record | Append-only authoritative event representation | P1 | P6 |
| 47 | TTT-TXN-002 | Genesis | Genesis schema with config/order/roles/pointer/state | TTT-TXN-001, TTT-ACTOR-003 | P6 |
| 48 | TTT-TXN-003 | Accepted actions | Accepted-transition event schema and persistence | TTT-TXN-001, TTT-STATE-003 | P6 |
| 49 | TTT-TXN-004 | Rejected actions | Audit-vs-transition-stream decision and implementation | TTT-TXN-001, TTT-GAME-006 | P6 |
| 50 | TTT-TXN-005 | Replay | Replay reducer from genesis and accepted events | TTT-TXN-002, TTT-TXN-003 | P6 |
| 51 | TTT-INV-007 | Replay invariant | Live-state vs replay-state equality tests | TTT-TXN-005 | P6 |
| 52 | TTT-CONCURRENCY-002 | Stale actions | Commit-time revision compare/reject | TTT-STATE-002, TTT-TXN-003 | P7 |
| 53 | TTT-CONCURRENCY-001 | Serialization | Atomic compare/commit or transaction boundary | TTT-CONCURRENCY-002, TTT-TXN-003 | P7 |
| 54 | TTT-INV-005 | One commit per revision | Race tests proving one conflicting commit | TTT-CONCURRENCY-001 | P7 |
| 55 | TTT-CONCURRENCY-003 | Retry safety | Persistent `action_id` handling and duplicate tests | TTT-TXN-003, TTT-CONCURRENCY-001 | P7 |
| 56 | TTT-STRATEGY-001 | No server strategy | Integration proof server never chooses game move | TTT-INV-008, P5 | P8 |
| 57 | TTT-STRATEGY-002 | Semantic decision | Player/model produces proposed action from environment | TTT-ADAPTER-003, TTT-ENV-002 | P8 |
| 58 | TTT-STRATEGY-003 | Strategy replacement | Multiple decision strategies through unchanged protocol | TTT-STRATEGY-002 | P8 |
| 59 | TTT-BOUNDARY-001 | Deterministic responsibilities | Integrated deterministic service boundary | P1, P3–P7 | P8 |
| 60 | TTT-BOUNDARY-002 | Semantic responsibilities | Model-facing actor boundary and semantic action contract | TTT-STRATEGY-002 | P8 |
| 61 | TTT-ORCH-004 | No manual state relay | MCP loop supplies environments and routes pointer automatically | P4, P5, P7, TTT-ORCH-002 | P8 |

## Completion rule

Requirements should be completed in this order unless a documented technical reason changes the dependency graph. A change to this plan is a project-planning change, not a change to the normative application requirements unless `REQUIREMENTS.md` is separately amended.