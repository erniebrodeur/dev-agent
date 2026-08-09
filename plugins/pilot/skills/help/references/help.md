# Pilot Help

Pilot provides development workflows with clear boundaries between planning, implementation, diagnosis, commits, and publication.

## Start here

- **Activate Pilot:** Say “activate Pilot” to load its policy and recover the current project state.
- **Resume work:** Ask “where are we?” or “what’s left?” to recover context without changing files.
- **Plan a change:** Describe the desired outcome. Pilot develops unsettled direction into an approved implementation slice.
- **Implement a slice:** Approve a defined slice and ask Pilot to build it. Pilot implements and verifies exactly that slice, then stops.
- **Get help:** Ask for help while Pilot is active to show this guide.

## Other workflows

- **Install Pilot policy:** Invoke `$copy-agents` to propose a project-owned `AGENTS.md`. Pilot shows the exact result and waits before writing.
- **Build a utility:** Ask Pilot to turn a repeatable procedure into an authoritative repository script.
- **Troubleshoot:** Give Pilot a concrete failure to diagnose. It gathers evidence and proposes a corrective slice without applying it.
- **Check security:** Request a security check to run Semgrep and report findings without applying fixes.
- **Inspect Git:** Ask for Git status to receive a concise, read-only repository report.
- **Commit:** Ask Pilot to prepare a commit. It stages and inspects the exact scope, proposes a message, and waits for approval before committing.

## Authorization boundaries

- Planning does not authorize implementation.
- Slice approval authorizes only that slice.
- Troubleshooting and security checks do not authorize fixes.
- Commit creation requires approval of the exact staged scope and message.
- Pushing, pull requests, releases, deployments, and destructive actions require separate authorization.
