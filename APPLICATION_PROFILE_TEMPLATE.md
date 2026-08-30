# MCP Collaborative — Application Profile Template

Use this template when creating a new MCP Collaborative application profile.

The profile SHALL conform to `APPLICATION_PROFILE_STANDARD.md`.

## Required Directory Structure

```text
<application-profile>/
├── README.md
├── REQUIREMENTS.md
├── DESIGN.md
├── TEST_PLAN.md
├── TRACEABILITY.md
└── src/
```

Add `SECURITY.md` and `OPERATIONS.md` when required by the application profile standard.

---

# README.md Template

## Profile Identity

- **Name:** `<profile-name>`
- **Type:** Application Profile
- **Status:** Draft
- **Parent Framework:** MCP Collaborative

## Purpose

Describe the application profile and the capability it exists to demonstrate or provide.

## Relationship to MCP Collaborative

Describe which MCP Collaborative mechanisms this profile exercises.

## Actors

Identify the primary actor types and roles.

## Controlling Documents

- `REQUIREMENTS.md`
- `DESIGN.md`
- `TEST_PLAN.md`
- `TRACEABILITY.md`
- `SECURITY.md`, if applicable
- `OPERATIONS.md`, if applicable

## Implementation

Identify the implementation entry point when one exists.

## Execution

Describe how the profile is run or demonstrated after implementation exists.

---

# REQUIREMENTS.md Template

## 1. Identity

- **Profile:** `<profile-name>`
- **Type:** Application Profile
- **Status:** Draft
- **Parent Standard:** `APPLICATION_PROFILE_STANDARD.md`

## 2. Mission

State the capability the profile exists to provide or demonstrate.

## 3. Scope

Define what is included.

## 4. Relationship to MCP Collaborative

Define which framework capabilities are used, specialized, exercised, or constrained.

## 5. Actors

Define actor types, identities, roles, lifecycle, and relevant relationships. Use stable requirement identifiers such as `<PROFILE>-ACTOR-001`.

## 6. Perspectives and Information Boundaries

Define what each actor may observe, what each actor may not observe, how perspective projection is enforced, and information-flow invariants.

## 7. Persistent Environments

Define current actor-visible state, bounded history, history depth, retention semantics, and behavior when roles or perspectives change.

## 8. Authoritative State

Define authoritative state fields, ownership, revision/order mechanism, and mutation authority.

## 9. Actions and State Transitions

Define permitted semantic actions, action schema, validation, accepted transitions, rejected transitions, and deterministic transition requirements.

## 10. Orchestration

Define execution pointer, actor eligibility, sequencing, role assignment or reassignment, and next-actor selection.

## 11. Persistence and Replay

Define transaction/event records, genesis state, replay requirements, and reconstruction guarantees.

## 12. Concurrency and Idempotency

Define stale-action handling, conflicting actions, duplicate delivery, retry behavior, and idempotency identifiers.

## 13. Domain Requirements

Define application-specific rules.

## 14. Invariants

List properties that must never be violated.

## 15. Failure Behavior

Define behavior for applicable failures.

## 16. Non-Goals

List deliberately excluded functionality.

## 17. Acceptance Criteria

Define observable conditions that establish successful conformance.

---

# DESIGN.md Template

## 1. Design Scope

Identify the requirements implemented by this design.

## 2. Architecture

Describe the major components and their relationships.

## 3. Component Responsibilities

Define each component's authority and responsibility.

## 4. Actor Model

Define actor representation and lifecycle.

## 5. Perspective Model

Define projection and information-boundary behavior.

## 6. Persistent Environment Model

Define current state, bounded history, and update semantics.

## 7. Authoritative State Model

Define schemas and ownership.

## 8. Adapter Architecture

Define state adaptation and semantic-action adaptation.

## 9. Action Model

Define the semantic action schema and validation path.

## 10. State Transition Model

Define the deterministic transition algorithm.

## 11. Orchestration Model

Define execution-pointer behavior and actor sequencing.

## 12. Transaction Model

Define event and persistence schemas.

## 13. Concurrency and Idempotency

Define serialization and retry protection.

## 14. Failure Handling

Define fail-closed and recovery behavior.

## 15. Domain Boundary

Identify generic framework behavior versus application-specific behavior.

## 16. Deterministic vs Semantic Responsibilities

Explicitly identify which behavior belongs to deterministic infrastructure and which belongs to actors/models.

## 17. Requirement Mapping

Map design components to requirement IDs.

---

# TEST_PLAN.md Template

## 1. Test Scope

Describe what is being verified.

## 2. Test Environment

Define fixtures, dependencies, configuration, and execution conditions.

## 3. Unit Tests

List unit-level verification.

## 4. State Transition Tests

Verify deterministic state transitions.

## 5. Perspective Tests

Verify actor-visible projections and prohibited information leakage.

## 6. Persistent Environment Tests

Verify current state, bounded history, ordering, and retention behavior.

## 7. Invalid Action Tests

Verify malformed, stale, unauthorized, or otherwise invalid actions do not mutate authoritative state.

## 8. Persistence and Replay Tests

Verify deterministic reconstruction where required.

## 9. Concurrency Tests

Verify competing actions cannot corrupt state.

## 10. Idempotency Tests

Verify retries cannot duplicate transitions.

## 11. Failure Tests

Verify applicable failure paths and fail-closed behavior.

## 12. Integration Tests

Verify collaboration among components.

## 13. End-to-End Acceptance Tests

Define full application-profile scenarios.

## 14. Requirement Coverage

Map each test to one or more requirement IDs.

---

# TRACEABILITY.md Template

Maintain a table or equivalent structured mapping.

| Requirement | Design | Test | Implementation | Status |
|---|---|---|---|---|
| `<REQ-ID>` | `<design section/component>` | `<test-id>` | `<source component>` | Planned |

Every normative requirement must appear.

---

# SECURITY.md Template

Use when required.

## Trust Boundaries

Define all relevant trust boundaries.

## Actor Authorization

Define how actor identity, role, and perspective are bound.

## Information Flow

Define what authoritative information can reach each actor.

## Perspective Changes

Define handling of historical information after perspective or role changes.

## Untrusted Model Output

Define validation boundaries for semantic/model output.

## Fail-Closed Behavior

Define behavior when projection, authorization, or validation fails.

## Persistence and Audit

Define security-sensitive persistence/audit considerations.

---

# OPERATIONS.md Template

Use when required.

## Startup

Define initialization.

## Shutdown

Define shutdown behavior.

## Persistence

Define durable state ownership and location.

## Restart and Recovery

Define reconstruction/recovery behavior.

## Health and Readiness

Define runtime health checks.

## Failure Recovery

Define operational failure procedures.

## Migration and Compatibility

Define version-transition behavior where applicable.

## Operational Verification

Define procedures used to confirm correct runtime operation.
