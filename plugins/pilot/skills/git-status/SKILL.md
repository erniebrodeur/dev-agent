---
name: git-status
description: Report concise, read-only Git repository state. Use when the user explicitly asks for Git status, repository status, branch state, working-tree changes, staged changes, or commit readiness. Also use automatically as the final local preflight immediately before executing an authorized release. Do not invoke automatically during activation, context recovery, implementation, verification, or commit preparation, and do not use as a general wrapper for other Git commands.
---

# Git Status

Inspect and report the repository's locally known Git state without changing it.

Automatic invocation is limited to the final local preflight immediately before an authorized release. Release discussion, planning, or readiness advice does not authorize either this workflow or the release.

## Workflow

1. Read applicable project instructions. Confirm the active directory belongs to a Git worktree; if not, report that status is unavailable without searching parent directories beyond the active project.
2. Inspect only local repository state using appropriate read-only Git commands:
   - Identify the repository, active branch, detached HEAD, or unborn branch.
   - Identify merge or rebase state and other material in-progress operations.
   - Identify the configured upstream and locally known ahead or behind counts. State that these use local tracking refs and may be stale. Do not fetch automatically.
   - Classify staged, unstaged, and untracked paths. Preserve rename, deletion, conflict, and submodule distinctions when material.
   - Inspect the relevant local commits and diff summaries needed to explain the current work. Read patch content only when necessary to summarize scope.
3. Report a compact status with:
   - repository and branch state;
   - upstream and locally known divergence;
   - in-progress operation, when present;
   - staged, unstaged, and untracked changes;
   - concise current-work or commit-readiness summary;
   - any ambiguity, stale upstream limitation, or safety concern.
4. When the worktree is clean, say so directly. Do not inflate an empty report.
5. For a release preflight, stop the release when the status exposes unresolved, ambiguous, or unintended local changes. This check supplements rather than replaces the release's complete public-content inspection.

## Safety

- Remain read-only. Do not alter the worktree, index, refs, configuration, remotes, or repository metadata.
- Do not fetch, pull, push, stage, unstage, commit, switch branches, create branches, merge, rebase, reset, restore, clean, stash, or run hooks.
- Do not reproduce suspected secrets, credentials, personal data, private configuration, or sensitive diff content. Identify the affected path and material type with redaction when reporting a concern.
- Do not treat ordinary branch management or individual Git commands as responsibilities of this skill.
- Do not claim the remote's current state from local tracking refs.
