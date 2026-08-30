# MCP Collaborative — Application Profile Standard

## 1. Purpose

This document defines the mandatory specification and documentation contract for every application profile implemented within MCP Collaborative.

MCP Collaborative is the general collaborative orchestration framework. An application profile is a domain-specific use of that framework. A profile may package or deploy as a plugin, service, test application, or other artifact; `application profile` describes its architectural relationship to MCP Collaborative.

Examples include `tic-tac-toe-plugin`, supervisor/worker collaboration, evaluator workflows, and future multi-actor applications.

## 2. Governing Principle

Application profiles shall be specified before they are implemented.

The required development sequence is:

1. Requirements
2. Design
3. Test plan
4. Traceability review
5. Prioritization/dependency planning
6. Implementation
7. Verification

Implementation is subordinate to the approved requirements and design. Existing code does not silently redefine its requirements.

## 3. Required Application Profile Structure

Every application profile SHALL contain, at minimum:

```text
<application-profile>/
├── README.md
├── REQUIREMENTS.md
├── DESIGN.md
├── TEST_PLAN.md
├── TRACEABILITY.md
├── REQUIREMENT_WORK_LEDGER.md
├── PRIORITIZATION.md
└── src/
```

`REQUIREMENT_WORK_LEDGER.md` and `PRIORITIZATION.md` are mandatory project-governance artifacts. They do **not** create application behavior requirements and SHALL NOT be assigned application requirement identifiers merely because their maintenance is mandatory under this standard.

Additional documents and directories may be added where needed.

### Conditionally mandatory documents

`SECURITY.md` SHALL be present when the profile includes any meaningful trust boundary, actor-specific visibility, hidden state, permissions, credentials, cross-user information, untrusted inputs, or security-sensitive operation.

`OPERATIONS.md` SHALL be present when the profile has deployment, restart, recovery, external service, health-check, durable-storage, migration, or runtime lifecycle requirements requiring operational definition.

A profile MAY include both documents even when they are not mandatory.

## 4. Document Authority

Within an application profile, authority flows in this order:

```text
MCP Collaborative framework requirements/standards
                ↓
Application profile REQUIREMENTS.md
                ↓
Application profile DESIGN.md
                ↓
Application profile implementation
                ↓
Verification evidence
```

`TEST_PLAN.md` defines how requirements and design claims are verified. `TRACEABILITY.md` records the relationships among these artifacts. `PRIORITIZATION.md` records planned implementation order and technical dependencies. `REQUIREMENT_WORK_LEDGER.md` records the commit history of substantive work against requirements.

Neither governance artifact may silently add, remove, or modify a normative application requirement. Normative application behavior remains controlled by `REQUIREMENTS.md` and applicable framework standards.

A lower-level artifact SHALL NOT silently override a higher-level normative artifact.

If an implementation cannot satisfy an approved requirement, the conflict must be resolved by explicitly revising the appropriate requirement or design rather than treating implementation behavior as the new specification.

## 5. README.md Requirements

Every profile README SHALL identify:

- profile name;
- profile type (`application profile`);
- profile purpose;
- current lifecycle/status;
- relationship to MCP Collaborative;
- primary actors or participants;
- controlling documents;
- implementation entry point when one exists;
- basic execution or demonstration instructions when implementation exists.

The README is an orientation document. It is not the authoritative substitute for requirements or design.

## 6. REQUIREMENTS.md Requirements

Every requirements document SHALL contain the following sections or their explicit equivalents.

### 6.1 Identity

Profile name, profile type, version/status, and applicable parent framework/standard.

### 6.2 Mission

A concise statement of the capability the profile exists to provide or demonstrate.

### 6.3 Scope

What is included in the profile.

### 6.4 Relationship to MCP Collaborative

Which framework capabilities the profile uses, specializes, exercises, or constrains.

### 6.5 Actors

Required actor types, identities, roles, lifecycle, and relevant relationships.

### 6.6 Perspectives and information boundaries

What each actor may observe and what information-flow guarantees must hold.

### 6.7 Persistent environments

Requirements for current actor-visible state, bounded history, retention, and persistence.

### 6.8 Authoritative state

State owned by the orchestration system and the authority rules governing mutation.

### 6.9 Actions and state transitions

Permitted semantic actions, validation requirements, deterministic transitions, and rejection behavior.

### 6.10 Orchestration

Execution pointer, eligibility, sequencing, role assignment, or other coordination requirements.

### 6.11 Persistence and replay

Transaction/event requirements and any reconstruction guarantees.

### 6.12 Concurrency and idempotency

Required behavior for simultaneous actions, stale state, duplicate delivery, and retries.

### 6.13 Domain requirements

Rules specific to the application domain. Domain rules SHALL NOT be promoted into generic framework behavior merely because the first implementation requires them.

### 6.14 Invariants

Properties that must remain true throughout valid system operation.

### 6.15 Failure behavior

Required behavior for invalid input, projection failure, persistence failure, stale actions, malformed model output, unavailable actors, and other applicable failures.

### 6.16 Non-goals

Functionality deliberately excluded from the current profile/version.

### 6.17 Acceptance criteria

Observable conditions sufficient to establish that the profile meets its stated requirements.

### 6.18 Requirement identifiers

Normative requirements SHALL have stable identifiers suitable for traceability.

Profile-specific IDs SHOULD use a stable profile prefix, for example:

```text
TTT-ACTOR-001
TTT-STATE-001
TTT-TURN-001
```

Identifiers SHALL NOT be silently reused for a materially different requirement.

## 7. DESIGN.md Requirements

Every design document SHALL describe how the approved requirements will be satisfied.

At minimum it SHALL define:

- architectural components;
- component responsibilities;
- state models and schemas;
- actor model;
- perspective/projection mechanism;
- persistent environment model;
- adapter boundaries;
- semantic action representation;
- authoritative validation and transition path;
- execution-pointer/orchestration mechanism;
- transaction/event model;
- concurrency and idempotency mechanism;
- failure handling;
- persistence/recovery design where applicable;
- interfaces between generic framework code and domain-specific code;
- major design decisions and their rationale;
- explicit mapping to the requirements being satisfied.

The design SHALL distinguish deterministic responsibilities from semantic/model responsibilities.

The design SHALL NOT grant an actor/model authority that the requirements reserve to the deterministic orchestration layer.

## 8. TEST_PLAN.md Requirements

Every test plan SHALL define how conformance will be demonstrated before implementation is considered complete.

It SHALL include:

- test scope;
- test environment and fixtures;
- unit tests;
- integration tests where applicable;
- deterministic transition tests;
- negative/invalid-action tests;
- perspective and information-boundary tests;
- persistence/replay tests where required;
- concurrency/idempotency tests where required;
- failure-path tests;
- end-to-end acceptance scenarios;
- expected outcomes;
- mapping from tests to requirement IDs.

Critical invariants SHALL have direct tests whenever mechanically testable.

A successful happy-path demonstration alone is insufficient evidence of conformance.

## 9. TRACEABILITY.md Requirements

Every profile SHALL maintain explicit requirements traceability.

At minimum, each normative requirement SHALL map to:

- its requirement ID;
- one or more design elements or an explicit statement that no implementation design is required;
- one or more verification methods/tests;
- implementation component(s) once implementation exists;
- current verification status.

Recommended form:

```text
Requirement → Design → Test → Implementation → Result
```

A requirement without a verification method SHALL be treated as incomplete unless it is explicitly documented as non-testable with justification.

An implementation component that materially affects externally observable or invariant behavior SHOULD trace back to a requirement or documented design decision.

## 10. REQUIREMENT_WORK_LEDGER.md Requirements

Every profile SHALL maintain a requirement work ledger as a project-governance artifact.

For every normative application requirement, the ledger SHALL include:

- requirement identifier;
- requirement name or concise descriptor;
- current work status;
- a chronological history of each substantive commit that materially defines, designs, implements, tests, verifies, or changes that requirement;
- the commit SHA;
- the commit timestamp.

A commit affecting multiple requirements SHALL be recorded against each affected requirement.

Ledger-only commits whose sole purpose is maintaining the ledger SHALL NOT be recursively treated as substantive work on every listed requirement.

The ledger SHALL NOT introduce new application requirements. Its maintenance obligation originates from this profile standard, not from the application domain specification.

## 11. PRIORITIZATION.md Requirements

Every profile SHALL maintain a requirement prioritization and dependency plan as a project-governance artifact.

It SHALL list every normative application requirement and, for each requirement:

- requirement identifier;
- requirement name or concise descriptor;
- necessary deliverables;
- technical prerequisite requirements or prerequisite implementation tranches;
- planned completion order or priority/tranche.

The document SHALL establish an intended dependency-respecting completion order before implementation proceeds materially beyond the specification stage.

Changes to prioritization do not themselves modify normative application requirements. If the underlying application behavior or normative dependency changes, `REQUIREMENTS.md` and other controlling artifacts must be amended separately as appropriate.

## 12. SECURITY.md Requirements

When required, `SECURITY.md` SHALL document applicable trust boundaries and information-flow controls.

For actor-perspective systems it SHALL address, at minimum:

- authoritative-state exposure boundaries;
- actor identity and perspective binding;
- prevention of unauthorized state disclosure;
- history leakage across perspective/role changes;
- fail-closed behavior for projection failures;
- treatment of untrusted semantic/model output;
- relevant persistence/audit boundaries.

## 13. OPERATIONS.md Requirements

When required, `OPERATIONS.md` SHALL define applicable operational behavior including:

- startup and initialization;
- shutdown;
- persistence location/ownership;
- restart behavior;
- state recovery;
- health/readiness behavior;
- failure recovery;
- migration/version compatibility where applicable;
- operational verification procedures.

## 14. Framework vs Application Requirements

Application requirements may specialize framework requirements but SHALL NOT weaken a framework invariant unless the framework standard explicitly permits that specialization.

Example:

```text
Framework invariant:
Every actor-visible state originates through the actor's assigned perspective.

Application specialization:
A tic-tac-toe player's perspective exposes the board, game status, and information required to determine whether that player may act.
```

The application-specific rule defines the permitted projection. It does not replace the framework information boundary.

## 15. Specification Completeness Gate

An application profile SHALL NOT be considered specification-complete until:

1. all mandatory documents and governance artifacts exist;
2. all normative requirements have stable IDs;
3. the design addresses every applicable normative requirement;
4. the test plan provides verification for every testable normative requirement;
5. traceability is complete through the currently existing lifecycle stage;
6. the requirement work ledger has an entry for every normative requirement;
7. the prioritization plan lists every normative requirement with deliverables and dependencies;
8. contradictions among requirements, design, tests, and framework standards are resolved;
9. required security and operations documents exist when their triggering conditions apply.

Implementation SHOULD NOT begin before this gate is satisfied.

Items 6 and 7 are governance completeness conditions only. They are not application runtime requirements.

## 16. Implementation Conformance Gate

An implemented application profile SHALL NOT be considered conforming until:

1. implementation is traceable to approved requirements/design;
2. required tests have been executed;
3. acceptance criteria pass;
4. critical invariants pass their verification;
5. unresolved deviations are explicitly documented;
6. replay, perspective, concurrency, persistence, and failure guarantees required by the profile have been demonstrated;
7. substantive requirement-related commits have been recorded in the requirement work ledger.

The ledger condition records evidence of the development process; it does not change application runtime semantics.

## 17. Required Template

New application profiles SHALL begin from `APPLICATION_PROFILE_TEMPLATE.md` or an equivalent structure that preserves all mandatory sections and governance artifacts defined by this standard.
