# Pilot

Pilot is a Codex plugin for disciplined, evidence-driven software development workflows.

Pilot can activate its portable development policy for one task, show a canonical capability guide, install a project-owned copy, recover project context, plan and implement focused changes, build deterministic repository utilities, report Git status, prepare local commits, execute distinct version releases, diagnose failures, and run user-authorized Semgrep security checks.

[Documentation](https://erniebrodeur.github.io/pilot/) · [Privacy](https://erniebrodeur.github.io/pilot/privacy/) · [Terms](https://erniebrodeur.github.io/pilot/terms/)

## Use

After installing the plugin, invoke:

```text
$activate
```

You can also select the Pilot plugin and ask it to activate. Activation remains opt-in, but the skill permits natural-language matching instead of requiring the `$activate` mention form.

Activation loads the policy shipped with the installed plugin for the current task, applies an existing root `CONVENTIONS.md`, and recovers the repository's current state. It does not modify the repository, install hooks, or create persistent configuration without separate approval.

Ask for help while Pilot is active to show its canonical, version-current capability guide. Pilot also responds when the user explicitly asks for Pilot help, but it does not claim generic help requests while inactive.

To propose bootstrapping the active repository with project-owned policy and skills, invoke:

```text
$bootstrap-repo-with-agent
```

Before writing, the skill explains that it will merge Pilot policy into the root `AGENTS.md` and copy Pilot's other skills into `.agents/skills/`. It asks whether that result is intended, inspects existing files, proposes the exact changes, and waits for final approval. The copied policy and skills become project-owned and do not automatically synchronize with plugin updates.

Project context recovery also activates implicitly for read-only requests such as “where are we?”, “what is already planned next?”, or “catch me up before I resume.” It recovers established project state and planned next work without choosing new direction or implementing anything. It verifies an existing root `CURRENT_WORK.md` against repository evidence. `CURRENT_WORK.md` is a Pilot convention for a mutable project scratch pad rather than a standard development artifact or design authority. Without that file, recovery performs a deeper scan, explains the convention, and offers to create either tracked or ignored project memory after reporting its findings.

Planning activates implicitly when the user is choosing or defining unsettled future work, such as requirements, design, architecture, scope, or implementation slices. It does not own requests merely to report established state or already-planned next work. It uses repository evidence and a conversational correction loop to resolve major decisions, maintain `CURRENT_WORK.md`, and produce an approved sequence of implementation slices without implementing them.

After the user clearly authorizes an approved slice, `next-slice` owns its implementation, including an approved corrective slice or a slice that creates a repository utility. It resolves that slice, gives the current task a concise title based on its outcome when the host supports task renaming, implements exactly the slice, verifies it proportionally, updates project memory, and stops. Task renaming is best-effort and never blocks implementation. A slice is a coherent, independently reviewable unit of work and an implementation authorization boundary, not necessarily a commit, release, or deployment. Pilot does not treat implementation alone as proof of success. It calls a problem fixed only when the user accepts the result or current, relevant evidence shows the actual problem is gone; otherwise it reports what remains unproven.

Utility building owns direct requests to create or change authoritative repository scripts for repeatable, deterministic development or operational procedures. Typical examples include build scripts, complete test bundles, deploy procedures, release validation, synchronization, resets, and seeds. It does not own ordinary requests to build, test, deploy, release, reset, seed, or run an existing script. An already-approved slice remains owned by `next-slice`, which applies the utility-building standards when the slice creates or changes a repository utility. Utility building follows existing repository structure such as `scripts/` or `cmd/`, always permits Bash, otherwise uses the repository's language and toolchain, and verifies the script through its real interface. When repeated manual command sequences waste context or risk drift, Pilot offers to script them and waits for approval.

Troubleshooting activates implicitly for an undiagnosed concrete software failure with no approved correction. It reproduces the mismatch through the real interface, tests competing hypotheses, distinguishes evidence from inference, and proposes a corrective slice. A request to fix an undiagnosed failure authorizes diagnosis only. Ordinary in-scope failures encountered during an active approved slice stay with `next-slice`, and an approved corrective slice returns there for implementation.

Security checking is optional and runs only after the user explicitly requests or approves it. A partial check scans only files changed by the relevant work. A security-check request without narrower scope runs a comprehensive Semgrep scan over the applicable repository, plus any additional tools required by `CONVENTIONS.md`. Failed or unavailable Semgrep makes the check incomplete. Findings are triaged and reported before any separately approved correction.

Git status is an explicit read-only workflow and Pilot's sole automatic Git-status checkpoint. Pilot runs it when asked, or as the final local preflight immediately before executing an authorized release. It does not run automatically during activation, recovery, implementation, verification, or commit preparation.

Local commits use a two-phase workflow. An initial request to prepare, stage, or create a commit authorizes Pilot to resolve and stage only the intended changes, inspect the complete staged diff, and show the exact scope and proposed message. It does not invoke the Git-status workflow. A standalone request to suggest, review, or discuss a possible message remains read-only and does not authorize staging. The workflow creates no commit until the user explicitly approves its exact proposal in a later message, rechecks for drift before committing, and never pushes implicitly.

Releases use a separate approval-gated workflow. The user must supply the exact release version; Pilot never infers the increment. Pilot first requires every intended substantive change to be committed. It then prepares a dedicated `version bump` commit containing only version changes and proposes the exact commit, tag, branch, remote, and push operation. After explicit approval, it runs the final Git preflight, creates the version commit and matching tag, pushes the branch and tag atomically when supported, and verifies remote publication when possible.

## Repository layout

- `plugins/pilot/` contains the installable plugin.
- `plugins/pilot/AGENTS.md` is the canonical portable development policy.
- `.agents/plugins/marketplace.json` exposes the plugin through a repository-local marketplace.
- `submission/test-cases.json` contains the five positive and three negative plugin-submission test cases.
- `scripts/package-plugin` creates a deterministic plugin archive.
- `tests/` verifies the repository and packaged-plugin structure.
- `INTERNAL.md` records the durable project model for maintainers and development agents.

## Development

Run the repository checks with:

```sh
python3 -m unittest discover -s tests
```

Create `dist/pilot.zip` with:

```sh
scripts/package-plugin
```

The archive contains only Git-tracked regular files under `plugins/pilot`; tracked
symlinks are rejected. Archive paths, timestamps, and permissions are normalized
for deterministic output. The generated `dist/` directory is ignored by Git.

## Release

Ask Pilot to prepare a release, or manually create a dedicated version boundary:

```sh
python3 -m unittest discover -s tests
# Update only version metadata, then commit it separately.
git add plugins/pilot/.codex-plugin/plugin.json tests/test_plugin_layout.py docs/index.html
git commit -m "version bump"
git tag -a v1.0.0 -m "Pilot 1.0.0"
git push --atomic origin main v1.0.0
```

The tag must match the version in the plugin manifest and resolve to the isolated
`version bump` commit. The GitHub workflow reruns the tests, builds the plugin
archive once, and publishes it as a versioned release asset such as
`pilot-v1.0.0.zip`.

## License

Pilot is licensed under the [GNU General Public License v3.0 only](LICENSE).
