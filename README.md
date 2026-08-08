# Dev Agent

Dev Agent is a Codex plugin for disciplined, evidence-driven software development workflows.

The project is being built as a sequence of independently reviewed slices. The current repository contains the plugin and marketplace foundation. User-facing skills will be added in later slices.

## Repository layout

- `plugins/dev-agent/` contains the installable plugin.
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
