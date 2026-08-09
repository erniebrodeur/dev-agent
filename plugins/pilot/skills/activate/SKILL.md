---
name: activate
description: Activate Pilot for the current task by loading its installed development policy and recovering the active project's current state without changing repository files or persistent configuration. Use when the user invokes `$activate`, asks to activate Pilot, or selects the Pilot plugin and requests activation.
---

# Activate

Load the plugin's canonical policy and apply it to the current task only.

## Required completion condition

Activation is incomplete until the canonical policy is loaded, applicable conventions are applied, and project-context recovery finishes. Do not report Pilot as active, ready, or successfully activated before completing the recovery workflow. Recovery may be skipped only when no active repository exists, and that skip must be reported.

## Workflow

1. Resolve the Pilot policy from this skill's location. For an installed plugin skill, read `../../AGENTS.md`. For a repository-owned copy under `.agents/skills/activate`, read the repository root `AGENTS.md` at `../../../AGENTS.md`. Read the resolved file completely. If it is missing or unreadable, stop and report that activation failed.
2. Treat the loaded file as the current Pilot baseline. Continue to honor higher-priority platform, developer, user, and unrelated project-specific instructions.
3. If the active repository has a root `CONVENTIONS.md`, read it completely after the baseline and apply supported conventions as described by the baseline.
4. When running from the installed plugin, use the installed baseline for Pilot behavior during this task while preserving unrelated project instructions. When running from a repository-owned copy, use the repository policy as its intentionally drifted baseline. Do not classify instructions as copied merely because their wording or principles overlap.
5. Read `../recover-project-context/SKILL.md` completely and run its recovery workflow for the active repository. This step is mandatory and blocking even when repository context appears obvious or was supplied elsewhere. If no active repository exists, report that recovery was skipped.
6. State concisely that Pilot is active for the current task, whether `CONVENTIONS.md` was loaded, and the recovered project state.
7. Continue with the user's task under the effective instructions.

## Boundaries

- Do not modify `AGENTS.md`, `CONVENTIONS.md`, global Codex configuration, hooks, or lifecycle state.
- Do not create persistent activation markers or claim activation beyond the current task.
- Do not defer project-context recovery or claim activation before it finishes.
- If copied-policy provenance is unclear, preserve the project instructions and report any material conflict instead of suppressing them.
- Do not silently continue when the canonical policy cannot be loaded.
