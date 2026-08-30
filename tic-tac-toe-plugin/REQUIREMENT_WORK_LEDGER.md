# Collaborative MCP Tic-Tac-Toe — Requirement Work Ledger

## Purpose

This is a project-governance record for work performed against the normative requirements in `REQUIREMENTS.md`.

It is **not itself an application requirement**. It does not change application behavior, acceptance criteria, or requirement dependencies.

For each requirement, the ledger records its descriptor, current work status, and every substantive commit known to have defined, designed, implemented, tested, or verified that requirement.

Ledger-only maintenance commits are not recursively recorded as work on requirements.

## Commit record format

Each entry uses:

`<timestamp UTC> — <commit SHA> — <work type>`

Known profile commits at ledger creation:

- `2026-08-30T13:41:55Z` — `78fe405665f46247a9b961d643a3a81ec8175f49` — requirement definition
- `2026-08-30T13:44:51Z` — `01242878fbf9ed77585814440aed2aec89b044af` — deterministic-core design
- `2026-08-30T13:46:03Z` — `6ef6ce2152f41d0611cfbba98fc213b05987e811` — deterministic-core test plan

## Requirement ledger

| Requirement | Descriptor | Status | Commit history |
|---|---|---|---|
| TTT-ACTOR-001 | Typed actors | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-ACTOR-002 | Actor identity | Defined / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:46:03Z — `6ef6ce2` — configuration test coverage |
| TTT-ACTOR-003 | Role | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-ACTOR-004 | Perspective | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-ACTOR-005 | Generality | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-PERSPECTIVE-001 | Projection | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-PERSPECTIVE-002 | No bypass | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-PERSPECTIVE-003 | Actor-specific views | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-PERSPECTIVE-004 | Perspective independence | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-PERSPECTIVE-005 | Allow-list behavior | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-PERSPECTIVE-006 | Fail closed | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-ENV-001 | Environment ownership | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-ENV-002 | Current state | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-ENV-003 | Bounded history | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-ENV-004 | Perspective-preserving history | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-ENV-005 | Deterministic history update | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-ENV-006 | Separation from authoritative history | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-ENV-007 | Perspective changes | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-STATE-001 | Server authority | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-STATE-002 | Revision | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-STATE-003 | Deterministic transition | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-STATE-004 | Terminal state | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-ADAPTER-001 | Mediation | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-ADAPTER-002 | State adaptation | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-ADAPTER-003 | Action adaptation | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-ADAPTER-004 | No validation authority | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-ADAPTER-005 | Domain separation | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-ORCH-001 | Single execution pointer | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-ORCH-002 | Server assignment | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-ORCH-003 | Turn enforcement | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-ORCH-004 | No manual state relay | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-GAME-001 | Players | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-GAME-002 | Board | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-GAME-003 | Win length | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-GAME-004 | Marks | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-GAME-005 | Move | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-GAME-006 | Validity | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-GAME-007 | Win | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-GAME-008 | Draw | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-GAME-009 | Baseline configuration | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-TXN-001 | Transaction record | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-TXN-002 | Genesis | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-TXN-003 | Accepted actions | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-TXN-004 | Rejected actions | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-TXN-005 | Replay | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-CONCURRENCY-001 | Serialization | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-CONCURRENCY-002 | Stale actions | Defined / partial core design | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — stale-revision core validation designed |
| TTT-CONCURRENCY-003 | Retry safety | Defined / interface anticipated | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — `action_id` retained in core action schema for later idempotency |
| TTT-STRATEGY-001 | No server strategy | Defined / core boundary designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — deterministic core excludes move selection; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-STRATEGY-002 | Semantic decision | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-STRATEGY-003 | Strategy replacement | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-BOUNDARY-001 | Deterministic responsibilities | Defined / partial core design | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — deterministic core portion designed |
| TTT-BOUNDARY-002 | Semantic responsibilities | Defined / partial core design | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — semantic/deterministic boundary described |
| TTT-INV-001 | Server-only mutation | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-INV-002 | Perspective boundary | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-INV-003 | Pointer owner only | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-INV-004 | Rejections do not mutate | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |
| TTT-INV-005 | One commit per revision | Defined / design constraint | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — core revision model designed; full concurrency mechanism deferred |
| TTT-INV-006 | History depth bound | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-INV-007 | Replay invariant | Defined | 2026-08-30T13:41:55Z — `78fe405` — defined |
| TTT-INV-008 | No server strategy | Designed / test planned | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned |

## Maintenance rule

Whenever a substantive commit is made that materially defines, designs, implements, tests, verifies, or changes one or more requirements, this ledger SHALL be updated to append that commit SHA and its GitHub commit timestamp to each affected requirement.

This rule governs project bookkeeping only. It does not create a new `TTT-*` requirement and does not alter application conformance.