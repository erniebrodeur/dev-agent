---
name: activate
description: Load the installed Dev Agent development policy for the current task without changing repository files or persistent configuration. Use only when the user explicitly invokes `$activate` or explicitly asks to activate Dev Agent for the current task.
---

# Activate

Load the plugin's canonical policy and apply it to the current task only.

## Workflow

1. Read `../../AGENTS.md` completely. Resolve the path relative to this skill directory. If it is missing or unreadable, stop and report that activation failed.
2. Treat the loaded file as the current Dev Agent baseline. Continue to honor higher-priority platform, developer, user, and unrelated project-specific instructions.
3. If the active repository has a root `CONVENTIONS.md`, read it completely after the baseline and apply supported conventions as described by the baseline.
4. If repository instructions are clearly attributable to a copied Dev Agent baseline, use the installed baseline for Dev Agent behavior during this task. Preserve unrelated project instructions. Do not classify instructions as copied merely because their wording or principles overlap.
5. State concisely that Dev Agent is active for the current task and whether `CONVENTIONS.md` was loaded.
6. Continue with the user's task under the effective instructions.

## Boundaries

- Do not modify `AGENTS.md`, `CONVENTIONS.md`, global Codex configuration, hooks, or lifecycle state.
- Do not create persistent activation markers or claim activation beyond the current task.
- If copied-policy provenance is unclear, preserve the project instructions and report any material conflict instead of suppressing them.
- Do not silently continue when the canonical policy cannot be loaded.
