---
name: bootstrap-repo-with-agent
description: Bootstrap the active repository with project-owned copies of Pilot's portable development policy and skills after explaining the effects, reviewing existing files, and receiving approval for the exact result. Use only when the user explicitly invokes `$bootstrap-repo-with-agent`. Do not use for a natural-language request to edit AGENTS.md or bootstrap, install, copy, or merge policy or skills without that skill invocation.
---

# Bootstrap Repository with Agent

Install the canonical Pilot policy and skills as durable, project-owned files.

## Workflow

1. Read `../../AGENTS.md` completely. Resolve the path relative to this skill directory. If it is missing or unreadable, stop and report that bootstrapping failed.
2. Enumerate every sibling skill directory under `../`. The bootstrap payload includes every Pilot skill except `bootstrap-repo-with-agent` itself.
3. Resolve the active repository root, its root `AGENTS.md`, and its `.agents/skills/` directory. Confirm the target is the repository the user intends to modify.
4. Before modifying anything, explain the complete effect of the bootstrap:
   - Pilot policy will be semantically merged into the root `AGENTS.md`.
   - The named payload skills will be copied into `.agents/skills/` using their existing directory names.
   - The repository copies will take the unqualified skill names while installed plugin skills remain available under the plugin namespace.
   - Every copied file becomes project-owned, may drift intentionally, and will not synchronize with later Pilot releases.
   - Existing instructions and skill directories will not be overwritten silently.
   Ask whether this is the intended result and stop until the user explicitly confirms. Do not treat invocation of this skill as confirmation.
5. After confirmation, read the existing root `AGENTS.md` and every colliding target skill directory completely. Preserve instructions and skills unrelated to Pilot.
6. If no root policy exists, propose the canonical policy as the new file. If one exists, prepare a semantic merge. Reconcile overlapping rules by meaning, preserve stricter compatible constraints, retain project-specific instructions, and surface material conflicts for the user to decide. Do not use a mechanical append, marked block, or text replacement as a substitute for reasoning about the combined policy.
7. Prepare the skill-copy proposal. Add absent payload skills exactly as shipped. Treat an existing same-named skill as a project-owned fork: preserve it unless the user explicitly requests replacement, and show any proposed replacement completely.
8. Show the complete proposed `AGENTS.md` or an inspectable diff, the full skill inventory, and an inspectable diff for every skill file that would be added or changed. State any material interpretation or conflict resolution.
9. Wait for explicit approval of the exact proposed result. The earlier intent confirmation does not authorize these writes.
10. After approval, write only the approved root `AGENTS.md` and approved `.agents/skills/` files. Re-read them, confirm each copied skill's frontmatter name matches its directory, and verify the result matches the approved proposal.
11. Report that the policy and skills are now project-owned and will not automatically synchronize with later Pilot versions.

## Boundaries

- Do not modify repository files before approval of the exact proposed policy and skill changes.
- Do not overwrite or silently remove existing instructions.
- Do not overwrite or silently remove existing project skills.
- Do not copy `bootstrap-repo-with-agent` into the target repository.
- Do not change nested `AGENTS.md` files, `CONVENTIONS.md`, global Codex configuration, hooks, or lifecycle state.
- Do not add synchronization markers or claim that the copied policy remains managed by Pilot.
- Treat existing copied Pilot policy and skills as local forks. Preserve local changes unless the user explicitly approves replacing them.
- If the target repository, existing-file relationship, or conflict resolution is unclear and would materially change the result, ask rather than assume.
