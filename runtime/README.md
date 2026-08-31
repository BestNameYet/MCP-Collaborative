# MCP Collaborative Runtime

This directory is reserved for domain-independent runtime components of the MCP Collaborative framework.

The first application-profile runtime is now implemented at `../plugins/collaborative-tic-tac-toe/`. It keeps the deterministic domain, SQLite authority boundary, projection adapter, and bundled STDIO MCP surface together while the framework-level abstractions remain under evaluation.

Initial runtime responsibilities expected to be designed before implementation include:

- authoritative shared-state ownership;
- actor registration and identity;
- role assignment;
- perspective projection;
- actor-specific persistent environments;
- bounded actor-visible history;
- semantic action intake;
- server-side action validation;
- deterministic state transitions;
- execution-pointer assignment;
- transaction persistence and replay;
- concurrency serialization;
- idempotency handling;
- domain-adapter boundaries.

No game-playing strategy belongs in the runtime orchestration layer. The tic-tac-toe implementation preserves that boundary and can be mined for domain-independent framework components after profile conformance is verified in the local OpenAI host.
