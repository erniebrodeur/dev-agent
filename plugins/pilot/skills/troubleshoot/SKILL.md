---
name: troubleshoot
description: Diagnose a concrete software failure through reproduction, competing hypotheses, and direct evidence, then propose a corrective slice and wait for approval. Use implicitly when implementation goes off course, verification fails or contradicts the expected outcome, observed behavior is wrong, or the user asks to debug, troubleshoot, or fix a concrete failure. Do not use for routine implementation verification, unsettled product intent, or implementation of an already-approved correction.
---

# Troubleshoot

Diagnose the failure rigorously, propose the narrowest supported correction, and wait. This workflow is diagnosis-only even when the original request asks for a fix.

## Workflow

1. Read applicable project instructions and inspect repository evidence relevant to the failure. If project context has not been recovered in the current task, read `../recover-project-context/SKILL.md` completely and run its recovery workflow.
2. Establish the intended behavior, observed behavior, environment, reproduction conditions, and relevant recent change. Treat recent changes as evidence to examine, not assumed causes.
3. If intended behavior or the acceptance condition is materially unclear, return to planning or ask the user rather than treating the symptom as the requirement.
4. Reproduce the failure through the real interface when practical. Reduce it to the smallest useful case and separate observed facts from inference.
5. Form a small set of credible hypotheses. Choose discriminating checks that can falsify them, and resist anchoring on the first plausible explanation.
6. Gather only the evidence needed to distinguish those hypotheses. Use relevant tests, logs, runtime inspection, screenshots, browser behavior, coverage, security checks, or disposable probes without modifying project implementation.
7. Identify the root cause and its owning layer only when the evidence supports that conclusion. State confidence and remaining uncertainty. If the failure cannot be reproduced or the cause remains uncertain, report what is known, what was ruled out, and the next useful diagnostic step.
8. Propose the smallest coherent corrective slice, including its outcome, scope, constraints or invariants, non-goals, dependencies, and verification expectations. Do not implement it.
9. Update `CURRENT_WORK.md`, when the project uses it, with the failure, evidence, diagnosis or blocker, confidence, remaining uncertainty, and proposed correction.
10. Report the diagnosis and proposed corrective slice, then wait for explicit approval. Once approved, correction belongs to the `next-slice` workflow.

## Boundaries

- Do not edit implementation files, tests, configuration, or product documentation during troubleshooting.
- Do not inherit correction authority from an earlier fix request or active implementation slice.
- Do not state a root cause from correlation, timing, intuition, or code inspection alone when a discriminating check is practical.
- Do not silently introduce a workaround, speculative refactor, adjacent cleanup, or broader redesign.
- Do not require exhaustive investigation after the evidence is sufficient to distinguish the cause and define a safe correction.
- Committing, pushing, opening a pull request, deploying, publishing, messaging others, destructive operations, and implementation of the corrective slice remain outside this skill.
