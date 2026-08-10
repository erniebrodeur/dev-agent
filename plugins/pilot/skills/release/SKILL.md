---
name: release
description: Prepare and execute a versioned release through explicit approval checkpoints. Use when the user asks to prepare, create, publish, or execute a release, or approves an exact release proposal. Require all intended substantive changes to be committed first, create a dedicated `version bump` commit containing only version changes, tag that commit, and push the branch and tag. Do not use for release discussion, readiness advice, changelog drafting, or merely running existing release tooling.
---

# Release

Create a distinct release boundary consisting of an isolated version commit and its matching tag.

## Authorization boundary

An initial request to release authorizes preparation only. Do not create the version commit, tag, push, or publish until a later user message explicitly approves the exact staged version scope, commit message, tag, remote, branch, and push operation.

Release discussion and readiness advice remain read-only. Approval of a release proposal authorizes only the listed release actions. Do not infer authorization for unrelated commits, pull requests, deployments, or destructive operations.

## Preparation

1. Read applicable project instructions. Inspect the repository's version source, tag format, release automation, verification commands, active branch, remote, and existing release conventions. Determine the target version from the user's request; ask when choosing it requires product intent. Do not invoke the Git-status workflow during preparation.
2. Confirm that the target version and tag are valid, unused, and consistent with the repository's versioning scheme. Never move, replace, or reuse an existing release tag.
3. Identify every intentional substantive change for the release. All such changes must be committed before the version bump. Do not treat ignored, generated, unrelated, ambiguous, sensitive, or unsafe material as release content merely because it exists locally.
4. When substantive changes remain uncommitted, read `../commit/SKILL.md` completely and apply its preparation workflow to those changes. Stop for approval of that exact substantive commit. Resume release preparation only after the commit exists and the intended substantive work is committed.
5. Run the repository's proportional pre-release verification against the substantive release commit. Inspect the complete content that the release will make public for secrets, personal data, local paths, internal hostnames, unintended metadata, and unexpected generated or binary artifacts. Stop on any failure or safety concern.
6. Change only the files and fields required to advance the repository's declared version. Matching version assertions or displayed version metadata count as version changes; behavioral changes, release notes, cleanup, and unrelated documentation do not.
7. Run focused version checks and the repository's required release verification. Stage only the version changes with explicit paths and inspect the complete staged diff.
8. Propose the exact release transaction:
   - staged version-only paths;
   - commit message `version bump`;
   - target version and tag;
   - tag type and message, following the repository's established convention;
   - remote and branch to push;
   - verification and public-content inspection results.
9. Wait for explicit approval of the complete proposal. Do not commit, tag, or push during preparation.

## Execution

1. Confirm that approval applies to the exact proposal. Reinspect the staged diff, intended paths, branch, remote, target version, and tag. Return to preparation if anything materially drifted.
2. Read `../git-status/SKILL.md` completely and run it as the final local release preflight. Proceed only when all local changes are the exact staged version changes and no operation, divergence, ambiguity, or safety concern blocks release.
3. Create one commit with the exact message `version bump` and only the approved version changes.
4. Create the approved tag at that commit. Verify locally that the tag resolves to the new version-bump commit and that the committed version matches the tag.
5. Push the approved branch and tag together atomically when the remote supports it. Do not silently fall back to a potentially partial push. Never force-push a branch or tag.
6. When the push triggers release automation, monitor its required result when the repository provides an accessible mechanism. Call the release published only after the remote confirms the expected release and artifacts; otherwise report that publication was triggered but remains unverified.
7. Report the version commit identifier, tag, pushed refs, remote result, automation result, and any remaining uncertainty. Then stop.

## Failure handling

- Stop immediately on verification, commit, tag, push, or publication failure.
- Report the exact completed boundary and remaining actions without rewriting history or repeating sensitive output.
- Do not delete a commit or tag, amend, reset, retry non-atomically, or invent a workaround without explicit approval.

## Boundaries

- Keep substantive work out of the `version bump` commit.
- Do not create an empty release or release from an unintended branch or detached HEAD.
- Do not select a semantic-version increment when the user's intent is unclear.
- Do not bypass tests, hooks, branch protection, release checks, or public-repository safety review.
- Do not claim a pushed tag proves that remote publication succeeded.
