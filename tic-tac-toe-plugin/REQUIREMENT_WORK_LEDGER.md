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
| TTT-ACTOR-001 | Typed actors | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ACTOR-002 | Actor identity | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:46:03Z — `6ef6ce2` — configuration test coverage; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ACTOR-003 | Role | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ACTOR-004 | Perspective | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ACTOR-005 | Generality | Implemented player abstraction / broader actor types pending | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-PERSPECTIVE-001 | Projection | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-PERSPECTIVE-002 | No bypass | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-PERSPECTIVE-003 | Actor-specific views | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-PERSPECTIVE-004 | Perspective independence | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-PERSPECTIVE-005 | Allow-list behavior | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-PERSPECTIVE-006 | Fail closed | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ENV-001 | Environment ownership | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ENV-002 | Current state | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ENV-003 | Bounded history | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ENV-004 | Perspective-preserving history | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ENV-005 | Deterministic history update | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ENV-006 | Separation from authoritative history | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ENV-007 | Perspective changes | Immutable-role policy implemented / documented | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-STATE-001 | Server authority | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-STATE-002 | Revision | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-STATE-003 | Deterministic transition | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-STATE-004 | Terminal state | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ADAPTER-001 | Mediation | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ADAPTER-002 | State adaptation | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ADAPTER-003 | Action adaptation | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ADAPTER-004 | No validation authority | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ADAPTER-005 | Domain separation | Separated / broader-domain reuse pending | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ORCH-001 | Single execution pointer | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ORCH-002 | Server assignment | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ORCH-003 | Turn enforcement | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-ORCH-004 | No manual state relay | Protocol implemented / host acceptance pending | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-GAME-001 | Players | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-GAME-002 | Board | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-GAME-003 | Win length | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-GAME-004 | Marks | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-GAME-005 | Move | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-GAME-006 | Validity | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-GAME-007 | Win | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-GAME-008 | Draw | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-GAME-009 | Baseline configuration | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-TXN-001 | Transaction record | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-TXN-002 | Genesis | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-TXN-003 | Accepted actions | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-TXN-004 | Rejected actions | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-TXN-005 | Replay | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-CONCURRENCY-001 | Serialization | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-CONCURRENCY-002 | Stale actions | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — stale-revision core validation designed; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-CONCURRENCY-003 | Retry safety | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — `action_id` retained in core action schema for later idempotency; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-STRATEGY-001 | No server strategy | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — deterministic core excludes move selection; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-STRATEGY-002 | Semantic decision | Protocol implemented / decisions remain host-side | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-STRATEGY-003 | Strategy replacement | Protocol independent / strategy variants not acceptance-tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-BOUNDARY-001 | Deterministic responsibilities | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — deterministic core portion designed; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-BOUNDARY-002 | Semantic responsibilities | Protocol implemented / decisions remain host-side | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — semantic/deterministic boundary described; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-INV-001 | Server-only mutation | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-INV-002 | Perspective boundary | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-INV-003 | Pointer owner only | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-INV-004 | Rejections do not mutate | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-INV-005 | One commit per revision | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — core revision model designed; full concurrency mechanism deferred; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-INV-006 | History depth bound | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-INV-007 | Replay invariant | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |
| TTT-INV-008 | No server strategy | Implemented / locally tested | 2026-08-30T13:41:55Z — `78fe405` — defined; 2026-08-30T13:44:51Z — `0124287` — designed; 2026-08-30T13:46:03Z — `6ef6ce2` — test planned; 2026-08-31T23:45:47Z — `d328e8f` — implemented, tested, and locally verified |

## Maintenance rule

Whenever a substantive commit is made that materially defines, designs, implements, tests, verifies, or changes one or more requirements, this ledger SHALL be updated to append that commit SHA and its GitHub commit timestamp to each affected requirement.

This rule governs project bookkeeping only. It does not create a new `TTT-*` requirement and does not alter application conformance.

## Private deployment extension

| Requirement | Descriptor | Status | Commit history |
|---|---|---|---|
| TTT-DEPLOY-001 | Private laptop runtime | Implemented / locally tested | 2026-09-01T03:10:40Z — `0e5657b` — Windows isolated install, durable database path, and stable STDIO launcher |
| TTT-DEPLOY-002 | Browser developer connector | Implemented / credentialed laptop acceptance pending | 2026-09-01T03:10:40Z — `0e5657b` — OpenAI Secure MCP Tunnel STDIO profile and ChatGPT Developer-mode runbook |
| TTT-DEPLOY-003 | Credential hygiene | Implemented / locally tested | 2026-09-01T03:10:40Z — `0e5657b` — runtime-only key and tunnel identity with no embedded secret |
| TTT-DEPLOY-004 | Acceptance boundary | Implemented / local portion tested | 2026-09-01T03:10:40Z — `0e5657b` — launcher tests and explicit user-side browser-to-laptop acceptance boundary |
