---
name: copy-agents
description: Install Dev Agent's portable development policy into the active project's root AGENTS.md after reviewing any existing instructions, proposing a semantic merge, and receiving approval for the exact result. Use only when the user explicitly invokes `$copy-agents` or explicitly asks to copy, install, or merge the Dev Agent policy into a project.
---

# Copy Agents

Install the canonical Dev Agent policy as durable, project-owned instructions.

## Workflow

1. Read `../../AGENTS.md` completely. Resolve the path relative to this skill directory. If it is missing or unreadable, stop and report that installation failed.
2. Resolve the active repository root and its root `AGENTS.md`. Confirm the target is the project the user intends to modify before proposing a change.
3. Read the existing target completely when it exists. Preserve instructions unrelated to Dev Agent.
4. If no target exists, propose the canonical policy as the new file. If a target exists, explain that the copied policy becomes project-owned and ask what relationship the user wants between the existing instructions and Dev Agent policy when that intent is not already clear.
5. Prepare a semantic merge. Reconcile overlapping rules by meaning, preserve stricter compatible constraints, retain project-specific instructions, and surface material conflicts for the user to decide. Do not use a mechanical append, marked block, or text replacement as a substitute for reasoning about the combined policy.
6. Show the complete proposed `AGENTS.md` or a complete inspectable diff. State any material interpretation or conflict resolution.
7. Wait for explicit approval of the proposed result. Do not treat the original invocation as approval to write the file.
8. After approval, write only the approved root `AGENTS.md`. Re-read it and verify that it matches the approved proposal.
9. Report that the policy is now project-owned and will not automatically synchronize with later Dev Agent versions.

## Boundaries

- Do not modify repository files before approval of the exact proposed `AGENTS.md`.
- Do not overwrite or silently remove existing instructions.
- Do not change nested `AGENTS.md` files, `CONVENTIONS.md`, global Codex configuration, hooks, or lifecycle state.
- Do not add synchronization markers or claim that the copied policy remains managed by Dev Agent.
- Treat an existing copied Dev Agent policy as a local fork. Preserve local changes unless the user explicitly approves replacing them.
- If the target project, existing-policy relationship, or conflict resolution is unclear and would materially change the result, ask rather than assume.
