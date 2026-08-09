---
name: utility-builder
description: Build authoritative repository scripts for repeatable, deterministic development or operational procedures, or recommend one when repeated agent-performed command sequences waste context or risk execution drift. Use when the user asks for a build, test-bundle, deploy, release-validation, synchronization, reset, seed, or similar repository script, and when repository or conversation evidence shows the same non-trivial deterministic procedure being reconstructed repeatedly. Do not use for fuzzy interpretation, personal automation, disposable probes, or trivial one-off commands.
---

# Utility Builder

Replace recurring agent-reconstructed procedures with authoritative, repository-owned scripts.

## Advisory mode

Use advisory mode when the user has not yet requested implementation but evidence shows a useful scripting opportunity.

1. Identify a non-trivial development or operational procedure that is repeatable and deterministic, especially one repeatedly reconstructed in conversation or one with ordering, safety, cleanup, or verification invariants.
2. Confirm that a retained script would materially reduce token and context use, execution drift, or operational risk. Do not recommend a script merely because a command could be wrapped.
3. Briefly describe the procedure, the likely repository-owned location, and the concrete benefit of scripting it.
4. Ask whether the user wants the script built. Wait for explicit approval before editing files.

Do not repeatedly offer a script the user has declined unless materially new evidence changes the proposal.

## Implementation mode

Enter implementation mode only after the user explicitly requests the script or approves a defined implementation slice.

1. Define the script's outcome, inputs, outputs, side effects, prerequisites, safety boundary, failure behavior, and observable postconditions.
2. Inspect the repository's language, toolchain, existing script conventions, directories, dependencies, and owning application logic.
3. Follow the repository's established structure. Prefer `scripts/` for development and operational procedures and `cmd/` for supported compiled commands when those conventions fit. Use `tools/` or another location only when repository evidence supports it; do not impose a new directory scheme.
4. Bash is always an acceptable implementation choice. Otherwise, use the repository's existing language and toolchain rather than introducing another language solely for the utility.
5. Encode the complete authoritative procedure. Resolve repository paths reliably, validate inputs and required commands, sequence steps explicitly, reuse owning application logic, and compose existing scripts instead of duplicating their behavior.
6. Provide direct errors, meaningful exit codes, and useful progress when work may take time. Handle cleanup and partial completion explicitly.
7. Add safeguards proportional to risk, such as clean-worktree checks, confirmation gates, change detection, idempotency, dry-run behavior, bounded waits, health checks, or postcondition verification.
8. Keep secrets and environment-specific values outside tracked scripts. Accept them through the repository's approved configuration or environment boundary and do not print them.
9. Exercise the script through its real interface. Verify ordering, failure propagation, cleanup, safety gates, and postconditions in proportion to risk. A test bundle should preserve useful results from every intended suite while returning failure when any suite fails.
10. Update repository instructions or documentation so future agents and developers invoke the script instead of manually recreating the procedure.

## Existing scripts

- Use an existing repository script when it owns the requested procedure instead of manually reenacting its commands.
- When an owning script is incomplete or incorrect, diagnose and change that script through the applicable approval workflow. Do not bypass it with a parallel manual sequence or a competing script.

## Boundaries

- Do not retain fuzzy decision-making, personal automation, disposable investigation code, or trivial one-off commands as repository utilities.
- Do not add speculative modes, compatibility layers, extension points, or dependencies unrelated to the current procedure.
- Do not implement a workaround without explaining its constraint and tradeoffs and receiving explicit approval.
- Authorization to create or change a script does not authorize executing destructive operations, deployments, releases, publication, or other separately controlled effects.
- Committing, pushing, opening a pull request, deploying, publishing, messaging others, and destructive operations remain separate actions requiring clear authorization.
