---
name: planning
description: Develop unsettled software direction into an approved sequence of implementation slices through an evidence-based conversational loop. Use implicitly when the user is choosing or defining future software work, exploring requirements, design, architecture, or scope, revising earlier direction, or asking to turn an unsettled idea into implementation slices. Do not use to report already-established project state or planned next work, implement an approved slice, or troubleshoot a concrete failure.
---

# Planning

Turn uncertain direction into durable, approved implementation slices without changing product code.

## Workflow

1. Read applicable project instructions and inspect repository, runtime, and documentation evidence relevant to the discussion.
2. If project context has not been recovered, read `../recover-project-context/SKILL.md` completely and run its read-only recovery workflow.
3. Establish the current model: desired outcome, settled constraints, provisional ideas, unresolved questions, and relevant existing behavior.
4. Continue a conversational loop until the direction is coherent:
   - Advance discoverable work before asking questions.
   - Ask only questions whose answers materially affect intent, design, public behavior, ownership, risk, or scope.
   - Prefer one focused question at a time when it keeps the discussion easy to steer.
   - Treat a correction as a reset of the affected model. Reconcile it with earlier decisions instead of patching around it.
   - Distinguish settled decisions from provisional ideas and inference.
   - Challenge speculative features, unnecessary abstractions, duplicated authority, workarounds, and slices that do not produce a coherent outcome.
5. Decompose the settled direction into ordered implementation slices. Give each slice a concrete outcome, scope, constraints or invariants, non-goals, dependencies, and proportional verification expectations.
6. Present the resulting plan and obtain explicit approval before leaving planning.
7. After approval, mark the plan approved and identify its first implementation slice. Stop and leave execution to the implementation workflow.

## Project Memory

Treat a root `CURRENT_WORK.md` as the durable context for planning.

- When the file exists, read it completely and update it automatically whenever the working model materially stabilizes, a decision settles, a slice boundary changes, or planning completes.
- Favor enough context to resume accurately over an underspecified checkpoint. Rewrite stale current-state sections instead of accumulating a chronological transcript.
- Record current state, settled decisions and rationale, provisional ideas, implementation slices, immediate next work, unresolved questions or risks, and relevant files.
- Keep provisional and settled content visibly distinct.
- When the file is absent, follow the creation workflow in `../recover-project-context/SKILL.md`. Planning cannot provide durable handoff context until the user approves the initial file and its tracked or ignored ownership.
- Keep unfinished design in `CURRENT_WORK.md`. Move only completed, durable project knowledge into internal documentation as part of the slice that establishes it.

## Boundaries

- Do not use planning merely to report current project state or an already-planned next action; use project-context recovery instead.
- Do not implement a planned slice, edit implementation files, or treat planning approval as authorization for execution.
- Do not turn the loop into a fixed questionnaire or ask for facts that inspection can establish.
- Do not finalize a plan while major product or design choices remain silently unresolved.
- Do not require detailed proof work in every slice. Specify proportional verification and reserve deeper investigation for troubleshooting when ordinary work goes off course.
