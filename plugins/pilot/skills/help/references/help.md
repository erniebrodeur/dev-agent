# Pilot Help

Pilot provides development workflows with clear boundaries between planning, implementation, diagnosis, commits, and publication.

## Start here

- **Activate Pilot:** Say “activate Pilot” to load its policy and recover the current project state.
- **Resume work:** Ask “where are we?”, “what’s left?”, or “what is already planned next?” to recover established context without changing files.
- **Plan a change:** Ask Pilot to choose or define unsettled future work. Pilot develops that direction into an approved implementation slice.
- **Implement a slice:** Approve a defined slice and ask Pilot to build it. `next-slice` owns approved corrections and utility slices as well as ordinary slices, reports whether user acceptance or evidence establishes the result, then stops.
- **Get help:** Ask for help while Pilot is active to show this guide.

## Other workflows

- **Install Pilot policy:** Invoke `$copy-agents` to propose a project-owned `AGENTS.md`. Pilot shows the exact result and waits before writing.
- **Build a utility:** Ask Pilot to create or change an authoritative repository script for a repeatable procedure. Merely running a build, test, deployment, or existing script is not utility building.
- **Troubleshoot:** Give Pilot an undiagnosed concrete failure with no approved correction. A fix request starts diagnosis, but an approved correction returns to `next-slice` for implementation.
- **Check security:** Optionally request a security check to run Semgrep and report findings without applying fixes.
- **Inspect Git:** Ask for Git status to receive a concise, read-only repository report.
- **Commit:** Ask Pilot to prepare, stage, or create a commit. It stages and inspects the exact scope, proposes a message, and waits for approval before committing. Asking only for help with a possible message remains read-only.

## Authorization boundaries

- Planning does not authorize implementation.
- Slice approval authorizes only that slice.
- Pilot does not call a problem fixed from an edit alone. Success requires user acceptance or current, relevant evidence that the actual problem is gone.
- Troubleshooting and security checks do not authorize fixes.
- Commit creation requires approval of the exact staged scope and message.
- Pushing, pull requests, releases, deployments, and destructive actions require separate authorization.
