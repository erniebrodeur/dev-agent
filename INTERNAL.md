# Internal project guide

## Purpose

Dev Agent packages the user's general development method into reusable Codex skills. It should help an agent discuss work freely, wait for implementation authorization, make the smallest coherent change, verify it proportionally, and troubleshoot deeply when needed.

## Architecture

The repository and installed plugin have separate responsibilities:

- Repository-root documentation, tests, and scripts support development and release of Dev Agent.
- `plugins/dev-agent/` contains everything required at plugin runtime.
- `.agents/plugins/marketplace.json` describes the repository-local plugin source.
- The portable development policy lives at `plugins/dev-agent/AGENTS.md`. Installing the plugin alone does not activate that file in another project.
- `activate` explicitly loads the installed policy for one task and then reads an existing repository-root `CONVENTIONS.md` as the customization layer.
- `copy-agents` proposes a semantic merge into the repository-root `AGENTS.md` and writes only after approval of the exact result.
- `recover-project-context` restores project state implicitly from recovery intent and runs whenever `activate` is invoked. It verifies `CURRENT_WORK.md` with a surface scan or performs a deep repository scan when no checkpoint exists.
- `planning` activates implicitly when direction is unsettled or no approved implementation slice exists. It runs an evidence-based conversational loop, keeps `CURRENT_WORK.md` current, and produces approved implementation slices without executing them.
- Conversation-mode detection, implementation authorization, and question-versus-assumption discipline remain ambient policy behavior rather than a standalone skill.

Do not make installed skills depend on repository-root development documents. `activate` resolves the portable policy relative to its installed skill directory.

## Artifact ownership

- `AGENTS.md` contains mandatory rules for changing this public repository.
- `INTERNAL.md` contains the durable project model and design rationale.
- `CURRENT_WORK.md` is an ignored, mutable scratch pad for active discussion and immediate work.
- `README.md` describes the public project and supported usage.

## Delivery slices

Build the plugin skeleton first, then `activate`, followed by one complete slice per approved skill. Each skill slice owns its runtime metadata, instructions, focused tests, and relevant documentation. Do not create empty resource directories for planned capabilities.

Prefer instruction-only skills. Add runtime scripts, assets, hooks, MCP servers, or apps only when an approved skill demonstrates a concrete need.

### Why conversation-gate is not a skill

A standalone skill should own a recognizable user trigger and produce a concrete outcome. Conversation gating does neither. It is baseline conduct that must already be active when the agent interprets whether a request is discussion, planning, documentation, diagnosis, or authorization to implement.

Explicit invocation would require the user to request the safeguard after it was already needed. Implicit invocation would load it across ordinary development turns, duplicate the portable policy, and spend context without adding a distinct workflow. The proposed responsibility to preserve a current mode is also misleading because authorization is inferred from the active conversation and instruction hierarchy, not maintained as durable lifecycle state.

The behavior therefore remains in the portable policy's authorization and questions-and-assumptions sections. Other skills may rely on that shared decision boundary, but should not repeat or claim ownership of it. `conversation-gate` is rejected as a standalone candidate.
