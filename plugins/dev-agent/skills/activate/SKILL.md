---
name: activate
description: Activate Dev Agent for the current task by loading its installed development policy and recovering the active project's current state without changing repository files or persistent configuration. Use when the user invokes `$activate`, asks to activate Dev Agent, or selects the Dev Agent plugin and requests activation.
---

# Activate

Load the plugin's canonical policy and apply it to the current task only.

## Required completion condition

Activation is incomplete until the canonical policy is loaded, applicable conventions are applied, and project-context recovery finishes. Do not report Dev Agent as active, ready, or successfully activated before completing the recovery workflow. Recovery may be skipped only when no active repository exists, and that skip must be reported.

## Workflow

1. Read `../../AGENTS.md` completely. Resolve the path relative to this skill directory. If it is missing or unreadable, stop and report that activation failed.
2. Treat the loaded file as the current Dev Agent baseline. Continue to honor higher-priority platform, developer, user, and unrelated project-specific instructions.
3. If the active repository has a root `CONVENTIONS.md`, read it completely after the baseline and apply supported conventions as described by the baseline.
4. If repository instructions are clearly attributable to a copied Dev Agent baseline, use the installed baseline for Dev Agent behavior during this task. Preserve unrelated project instructions. Do not classify instructions as copied merely because their wording or principles overlap.
5. Read `../recover-project-context/SKILL.md` completely and run its recovery workflow for the active repository. This step is mandatory and blocking even when repository context appears obvious or was supplied elsewhere. If no active repository exists, report that recovery was skipped.
6. State concisely that Dev Agent is active for the current task, whether `CONVENTIONS.md` was loaded, and the recovered project state.
7. Continue with the user's task under the effective instructions.

## Boundaries

- Do not modify `AGENTS.md`, `CONVENTIONS.md`, global Codex configuration, hooks, or lifecycle state.
- Do not create persistent activation markers or claim activation beyond the current task.
- Do not defer project-context recovery or claim activation before it finishes.
- If copied-policy provenance is unclear, preserve the project instructions and report any material conflict instead of suppressing them.
- Do not silently continue when the canonical policy cannot be loaded.
