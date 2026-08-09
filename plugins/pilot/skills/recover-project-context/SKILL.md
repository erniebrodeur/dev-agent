---
name: recover-project-context
description: Recover the active project's already-established current state and planned next work from repository evidence. Use when the user asks for a read-only checkpoint, including where we are, where we were, what remains in an existing plan, what work is already planned next, or what they need to know before resuming prior work. Do not use to implement an approved slice or choose or design new future work. Recovery starts read-only unless checkpoint creation is separately approved. Also run this workflow when Pilot's `$activate` skill directs it.
---

# Recover Project Context

Reconstruct the project's present state and return a compact, evidence-based checkpoint.

## Workflow

1. Resolve the active repository root. Read applicable project instructions before interpreting other files.
2. Check explicitly for a root `CURRENT_WORK.md`, including when ignored by Git.
3. When `CURRENT_WORK.md` exists, read it completely, then surface-scan the repository to verify it:
   - Inspect the working tree, branch, recent history, and diff summary.
   - Inspect the top-level tracked structure and relevant internal or public documentation.
   - Read configuration, tests, or source only as needed to confirm present-state claims.
   - Identify stale, unsupported, or contradictory checkpoint content instead of repeating it as fact.
4. When `CURRENT_WORK.md` is absent, deep-scan the repository:
   - Inspect the working tree, branch, recent history, recent changes, and tracked structure.
   - Read applicable instructions, internal documentation, public documentation, manifests, configuration, test structure, and representative source entry points.
   - Follow evidence into additional files until the current work, settled decisions, and likely next work are reasonably supported.
   - Exclude dependencies, generated output, caches, large vendored content, and sensitive ignored files unless the task specifically requires them.
5. Distinguish repository evidence from inference. Resolve safe factual discrepancies through further inspection rather than asking the user.
6. Summarize completed work, active changes, settled decisions, unresolved questions or risks, and the best-supported next action. Keep the result compact enough to resume work immediately.

## Creating Current Work

When no root `CURRENT_WORK.md` exists:

1. Finish and report the recovery summary first.
2. Explain that `CURRENT_WORK.md` is a Pilot convention, not a standard development artifact. Describe it as a project scratch pad containing current state, settled decisions, immediate next work, unresolved questions, and relevant files so a later task can resume without reconstructing the entire project. Clarify that it is mutable working context, not design authority, a changelog, or a replacement for durable documentation.
3. Ask whether the user wants a `CURRENT_WORK.md` created from the recovered state.
4. Only after the user accepts, ask whether the file should be tracked or ignored. Explain that tracked files support shared, reviewable project memory, while ignored files support local, temporary, or personal working context.
5. Inspect the repository's ignore rules before proposing an ignored file. Do not assume that `CURRENT_WORK.md` is already ignored.
6. Draft a compact checkpoint containing current state, settled decisions, immediate next work, unresolved questions, and relevant files. Keep personal data and sensitive material out of any tracked proposal.
7. Show the complete proposed file and any required ignore-rule change. Wait for explicit approval before writing either file.

## Boundaries

- Keep recovery read-only unless the user separately approves creating or updating project memory.
- Do not choose or design new future work; use planning when direction is unsettled.
- Do not implement the inferred next action.
- Do not treat a checkpoint as design authority when repository evidence disagrees.
- Do not scan parent directories or unrelated repositories.
- Do not claim certainty for conclusions that remain inferred.
