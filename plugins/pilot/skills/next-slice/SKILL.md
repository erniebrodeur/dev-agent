---
name: next-slice
description: Implement exactly one approved implementation slice and verify its outcome without beginning later work. Use implicitly when the user clearly authorizes implementation of an already-approved slice, including an approved corrective slice or an approved slice that creates or changes a repository utility, or explicitly asks to implement the next approved slice. Do not use to diagnose a new failure, infer an unapproved correction, choose unsettled direction, or act on unapproved work.
---

# Next Slice

Implement exactly one approved implementation slice, verify it proportionally, record the result, and stop.

## Workflow

1. Read applicable project instructions and inspect repository evidence relevant to the approved work.
2. If project context has not been recovered in the current task, read `../recover-project-context/SKILL.md` completely and run its recovery workflow.
3. Resolve exactly one approved implementation slice from the current conversation and project memory. Identify its outcome, scope, constraints or invariants, non-goals, dependencies, and verification expectations before editing. Success depends on the problem: use user acceptance for a subjective outcome or current, relevant evidence for a testable failure. This workflow remains the owner when the approved slice creates or changes an authoritative repository utility; read `../utility-builder/SKILL.md` completely and apply its relevant implementation standards without starting a separate workflow.
4. If no slice is approved, the selected slice is ambiguous, or a material product, public-interface, ownership, workaround, or scope decision remains unresolved, stop. Return to planning or ask for the required user decision rather than choosing silently.
5. Derive a concise task title from the approved slice's outcome and rename the current task through the host's task-title capability before editing. Prefer the concrete outcome over a generic workflow label. If the capability is unavailable or the rename fails, report the limitation and continue; task naming does not block implementation.
6. Inspect the relevant implementation, tests, documentation, and files in scope. Preserve unrelated user changes and identify the smallest coherent change that can complete the slice. Do not invoke Git status as a routine implementation check.
7. Implement the slice. Use tests to drive observable behavior where practical. Settle details during implementation only when they are minor, conventional, and reversible and do not constrain later decisions.
8. Run focused verification first, followed by broader checks only when justified by the change's risk. For a concrete failure, rerun its original reproducer when practical. Evidence must come from the final relevant code, build, service, and environment and exercise the intended target. Confirm that checks completed and actually ran; skipped or empty checks, timeouts, partial results, and wrong-target checks are not proof. Recheck affected behavior after any later relevant change. Diagnose ordinary failures within the slice, but do not add a workaround or expand scope without explicit approval.
9. Update relevant durable documentation and `CURRENT_WORK.md` to reflect the actual result, including incomplete work, failed verification, remaining risks, and the next planned slice. Claim an issue fixed, resolved, or complete only when the user accepts the result or current, relevant evidence clearly shows the actual problem is gone. A passing test proves only what it exercised. Otherwise report the change as implemented but unverified, partially verified, incomplete, or still failing. Do not infer broader correctness or no regressions from narrow checks.
10. Report the implementation result, changed areas, evidence gathered, anything not verified, and the next planned work. When the user asks for evidence, provide the concrete observed result or inspectable artifact and its limits rather than restating the conclusion. Then stop.

## Boundaries

- Do not begin another slice, even when it appears small or closely related.
- Do not reinterpret a discussion, plan, diagnosis, or vague request to continue as implementation authorization.
- Do not broaden the approved outcome to include adjacent cleanup, speculative capabilities, refactors, or follow-up fixes.
- Do not silently work around a root cause or unresolved constraint. Explain the proposed workaround and wait for approval.
- Committing, pushing, opening a pull request, deploying, publishing, messaging others, destructive operations, and other separately controlled actions remain outside this skill unless the user authorizes them explicitly.
- Preserve unrelated working-tree changes and report any conflict that prevents a safe implementation.
