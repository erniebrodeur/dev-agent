# Internal project guide

## Purpose

Dev Agent packages the user's general development method into reusable Codex skills. It should help an agent discuss work freely, wait for implementation authorization, make the smallest coherent change, and prove the result.

## Architecture

The repository and installed plugin have separate responsibilities:

- Repository-root documentation, tests, and scripts support development and release of Dev Agent.
- `plugins/dev-agent/` contains everything required at plugin runtime.
- `.agents/plugins/marketplace.json` describes the repository-local plugin source.
- The portable development policy will live at `plugins/dev-agent/AGENTS.md`. Installing the plugin alone will not activate that file in another project.

Do not make installed skills depend on repository-root development documents.

## Artifact ownership

- `AGENTS.md` contains mandatory rules for changing this public repository.
- `INTERNAL.md` contains the durable project model and design rationale.
- `CURRENT_WORK.md` is an ignored, mutable scratch pad for active discussion and immediate work.
- `README.md` describes the public project and supported usage.

## Delivery slices

Build the plugin skeleton first, then `activate`, followed by one complete slice per approved skill. Each skill slice owns its runtime metadata, instructions, focused tests, and relevant documentation. Do not create empty resource directories for planned capabilities.

Prefer instruction-only skills. Add runtime scripts, assets, hooks, MCP servers, or apps only when an approved skill demonstrates a concrete need.
