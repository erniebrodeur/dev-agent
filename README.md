# Dev Agent

Dev Agent is a Codex plugin for disciplined, evidence-driven software development workflows.

The project is being built as a sequence of independently reviewed slices. The current plugin can activate its portable development policy for one task, install a project-owned copy, recover project context, and develop uncertain direction into approved implementation slices.

## Use

After installing the plugin, invoke:

```text
$activate
```

Activation loads the policy shipped with the installed plugin for the current task, applies an existing root `CONVENTIONS.md`, and recovers the repository's current state. It does not modify the repository, install hooks, or create persistent configuration without separate approval.

To propose installing the policy as the active project's durable `AGENTS.md`, invoke:

```text
$copy-agents
```

The skill inspects existing instructions, proposes a semantic merge, and waits for approval of the exact result before writing. The copied policy becomes project-owned and does not automatically synchronize with plugin updates.

Project context recovery also activates implicitly for requests such as “where are we?”, “resume,” or “what is next?” It verifies an existing root `CURRENT_WORK.md` against repository evidence. `CURRENT_WORK.md` is a Dev Agent convention for a mutable project scratch pad rather than a standard development artifact or design authority. Without that file, recovery performs a deeper scan, explains the convention, and offers to create either tracked or ignored project memory after reporting its findings.

Planning activates implicitly when software direction is unsettled or no approved implementation slice exists. It uses repository evidence and a conversational correction loop to resolve major decisions, maintain `CURRENT_WORK.md`, and produce an approved sequence of implementation slices without implementing them.

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
