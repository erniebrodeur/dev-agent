# Dev Agent

Dev Agent is a Codex plugin for disciplined, evidence-driven software development workflows.

The project is being built as a sequence of independently reviewed slices. The current plugin can activate its portable development policy for one task, install a project-owned copy, recover project context, develop uncertain direction into approved implementation slices, implement one approved slice at a time, report reusable read-only Git status, prepare and approve local commits in two phases, diagnose concrete failures before proposing corrections, and run user-authorized Semgrep security checks.

## Use

After installing the plugin, invoke:

```text
$activate
```

You can also select the Dev Agent plugin and ask it to activate. Activation remains opt-in, but the skill permits natural-language matching instead of requiring the `$activate` mention form.

Activation loads the policy shipped with the installed plugin for the current task, applies an existing root `CONVENTIONS.md`, and recovers the repository's current state. It does not modify the repository, install hooks, or create persistent configuration without separate approval.

To propose installing the policy as the active project's durable `AGENTS.md`, invoke:

```text
$copy-agents
```

The skill inspects existing instructions, proposes a semantic merge, and waits for approval of the exact result before writing. The copied policy becomes project-owned and does not automatically synchronize with plugin updates.

Project context recovery also activates implicitly for requests such as “where are we?”, “resume,” or “what is next?” It verifies an existing root `CURRENT_WORK.md` against repository evidence. `CURRENT_WORK.md` is a Dev Agent convention for a mutable project scratch pad rather than a standard development artifact or design authority. Without that file, recovery performs a deeper scan, explains the convention, and offers to create either tracked or ignored project memory after reporting its findings.

Planning activates implicitly when software direction is unsettled or no approved implementation slice exists. It uses repository evidence and a conversational correction loop to resolve major decisions, maintain `CURRENT_WORK.md`, and produce an approved sequence of implementation slices without implementing them.

After the user clearly authorizes an approved slice, `next-slice` resolves that slice, gives the current task a concise title based on its outcome when the host supports task renaming, implements exactly the slice, verifies it proportionally, updates project memory, and stops. Task renaming is best-effort and never blocks implementation. A slice is a coherent, independently reviewable unit of work and an implementation authorization boundary, not necessarily a commit, release, or deployment.

Troubleshooting activates implicitly for a concrete software failure. It reproduces the mismatch through the real interface, tests competing hypotheses, distinguishes evidence from inference, and proposes a corrective slice. It remains diagnosis-only and waits for approval before any implementation change, even when the original request asked for a fix.

Security checking runs only after the user requests or approves it. A partial check scans only files changed by the relevant work. A security-check request without narrower scope runs a comprehensive Semgrep scan over the applicable repository, plus any additional tools required by `CONVENTIONS.md`. Failed or unavailable Semgrep makes the check incomplete. Findings are triaged and reported before any separately approved correction.

Git status is a first-class read-only workflow because agents repeat it frequently and local commits depend on it. It reports branch and upstream state, locally known divergence, in-progress operations, working-tree changes, and commit readiness without fetching or performing branch management. It does not turn individual Git commands into skills.

Local commits use a two-phase workflow. `commit` begins with the shared Git status workflow, then an initial commit request authorizes it to resolve and stage only the intended changes, inspect the complete staged diff, and show the exact scope and proposed message. It creates no commit until the user explicitly approves that proposal in a later message. The skill rechecks for drift before committing and never pushes implicitly.

## Repository layout

- `plugins/dev-agent/` contains the installable plugin.
- `plugins/dev-agent/AGENTS.md` is the canonical portable development policy.
- `.agents/plugins/marketplace.json` exposes the plugin through a repository-local marketplace.
- `scripts/package-plugin` creates a deterministic plugin archive.
- `tests/` verifies the repository and packaged-plugin structure.
- `INTERNAL.md` records the durable project model for maintainers and development agents.

## Development

Run the repository checks with:

```sh
python3 -m unittest discover -s tests
```

Create `dist/dev-agent.zip` with:

```sh
scripts/package-plugin
```

The generated `dist/` directory is ignored by Git.
