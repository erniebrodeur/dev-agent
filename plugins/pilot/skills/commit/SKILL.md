---
name: commit
description: Prepare and create a local Git commit through two explicit authorization phases. Use when the user asks to prepare or stage changes for a commit, asks to create a local commit, or approves the exact staged scope and message previously prepared by this skill. A request only to suggest, review, or discuss a possible commit message is read-only and does not invoke this workflow. An initial commit request stages the intended changes and proposes the exact commit but never creates it without later approval.
---

# Commit

Prepare a safe, reviewable local commit, obtain approval for its exact staged scope and message, then create only that commit.

## Required authorization boundary

A request to commit, including a direct instruction such as `commit`, authorizes preparation only. Never treat it as approval to create the commit. Wait for explicit approval of the exact staged scope and proposed message in a later user message.

A standalone request to suggest, review, or discuss a possible commit message does not authorize preparation or staging. Treat it as read-only unless the user also requests commit preparation or approves an existing exact proposal.

## Preparation phase

1. Read applicable project instructions. Resolve the intended change set from the request, current work, and repository evidence. Preserve unrelated changes. If scope is ambiguous or unrelated changes are already staged, stop and ask before modifying the index. Do not invoke the Git-status workflow during commit preparation.
2. Run or confirm proportional verification for the intended changes. Report any relevant verification that is incomplete or failing rather than concealing it.
3. Review the intended content, then stage only the intended files with explicit paths. Include deletions only when they are clearly in scope. Do not use a broad staging command while scope is unresolved.
4. Inspect the complete staged diff, including generated and binary artifacts. Check it for secrets, personal data, local paths, internal hostnames, unintended metadata, and unrelated content. Stop and report any safety concern without repeating sensitive values.
5. Derive a concise commit message that describes the staged outcome. If the user supplied a message, preserve it as the proposal unless it is misleading or unsafe; report any required correction.
6. Show the exact staged scope and proposed message, along with relevant verification and safety findings. Wait for explicit approval. Do not create the commit during this phase, even when the original request said to commit.

## Commit phase

1. Confirm that the user's approval clearly applies to the exact staged scope and proposed message.
2. Reinspect the staged diff and intended paths for material drift. If the staged content, intended scope, relevant verification, or message has changed materially, do not commit. Return to the preparation phase and show the revised proposal.
3. Create the local commit with the approved message and exactly the approved staged content.
4. Report the commit identifier, message, and any hook or commit failure. Then stop.

## Boundaries

- Do not commit before the separate approval phase.
- Do not stage ambiguous, unrelated, ignored, or sensitive content.
- Do not unstage or rewrite pre-existing staged work without explicit approval.
- Do not amend, reset, rebase, merge, or tag unless separately authorized.
- Do not push, open a pull request, deploy, publish, or perform another remote action unless separately authorized.
- Do not bypass hooks or weaken verification to make the commit succeed.
