# Dev Agent

Dev Agent is a Codex plugin for disciplined, evidence-driven software development workflows.

The project is being built as a sequence of independently reviewed slices. The current plugin can activate its portable development policy for one task or install a project-owned copy.

## Use

After installing the plugin, invoke:

```text
$activate
```

Activation loads the policy shipped with the installed plugin for the current task. It does not modify the repository, install hooks, or create persistent configuration. If the active repository contains a root `CONVENTIONS.md`, activation loads it as the project customization layer.

To propose installing the policy as the active project's durable `AGENTS.md`, invoke:

```text
$copy-agents
```

The skill inspects existing instructions, proposes a semantic merge, and waits for approval of the exact result before writing. The copied policy becomes project-owned and does not automatically synchronize with plugin updates.

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
