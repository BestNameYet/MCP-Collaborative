# Tic-Tac-Toe Application Profile

This directory contains the normative requirements, architecture, prioritization, work ledger, and test plan for the Collaborative MCP tic-tac-toe profile.

The runnable private OpenAI plugin is [`../plugins/collaborative-tic-tac-toe/`](../plugins/collaborative-tic-tac-toe/). It bundles a STDIO MCP server through `.mcp.json`, is listed by the repository marketplace at `../.agents/plugins/marketplace.json`, and includes Windows launchers for OpenAI Secure MCP Tunnel so browser ChatGPT can reach the laptop-hosted server without public ingress.

Mandatory governance files:

- `REQUIREMENTS.md`
- `DESIGN.md`
- `PRIORITIZATION.md`
- `REQUIREMENT_WORK_LEDGER.md`
- `TEST_PLAN.md`
