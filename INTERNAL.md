# Internal project guide

## Purpose

Pilot packages the user's general development method into reusable Codex skills. It should help an agent discuss work freely, wait for implementation authorization, make the smallest coherent change, verify it proportionally, and troubleshoot deeply when needed.

## Architecture

The repository and installed plugin have separate responsibilities:

- Repository-root documentation, tests, and scripts support development and release of Pilot.
- `plugins/pilot/` contains everything required at plugin runtime.
- `.agents/plugins/marketplace.json` describes the repository-local plugin source.
- The portable development policy lives at `plugins/pilot/AGENTS.md`. Installing the plugin alone does not activate that file in another project.
- `activate` loads the installed policy for one task after an explicit user request, including a natural-language request made through the selected plugin, and then reads an existing repository-root `CONVENTIONS.md` as the customization layer. Its metadata permits implicit skill matching instead of requiring the `$activate` mention form.
- `help` reproduces one canonical, version-current capability guide when the user explicitly asks for Pilot help or asks for help while Pilot is active for the current task. It does not claim generic help requests while inactive or create persistent activation state.
- `copy-agents` runs only through explicit `$copy-agents` invocation, proposes a semantic merge into the repository-root `AGENTS.md`, and writes only after approval of the exact result.
- `recover-project-context` owns read-only recovery of already-established project state and planned next work, and runs whenever `activate` is invoked. It does not choose new future work or implement the recorded next action. It verifies `CURRENT_WORK.md` with a surface scan or performs a deep repository scan when no checkpoint exists.
- `planning` owns choosing or defining unsettled future software work. It does not report already-established state or planned next work. It runs an evidence-based conversational loop, keeps `CURRENT_WORK.md` current, and produces approved implementation slices without executing them.
- `next-slice` activates implicitly after clear implementation authorization and owns every already-approved slice, including an approved correction or a slice that creates a repository utility. It resolves exactly one approved slice, best-effort renames the current task from the slice outcome before editing, implements the slice, verifies it proportionally, updates project memory, and stops before later work. It distinguishes implementation from an established result and calls a problem fixed only after user acceptance or current, relevant evidence shows the actual problem is gone.
- `utility-builder` owns direct requests to create or change authoritative repository scripts for repeatable, deterministic procedures, plus advisory recommendations when agents repeatedly reconstruct such a procedure. It does not own ordinary requests to run a script or build, test, deploy, release, reset, or seed an application. An already-approved utility slice remains owned by `next-slice`, which applies the utility-building standards. Utility building follows the repository's existing structure, always permits Bash, otherwise uses the repository's language and toolchain, verifies the real interface and postconditions, and teaches future agents to invoke the owning script.
- `git-status` provides one concise, read-only owner for repeated Git-state inspection. It reports locally known branch, upstream, divergence, worktree, and current-work state without fetching or performing branch management, and it is the mandatory first step of `commit`.
- `commit` activates for requests to prepare, stage, or create a local commit and enforces two authorization phases. A standalone request to suggest, review, or discuss a possible message is read-only and does not authorize staging. The first phase resolves scope, verifies, stages, inspects, and proposes the exact commit. A later approval permits that exact commit after a drift check. It never pushes implicitly.
- `troubleshoot` activates implicitly for an undiagnosed concrete failure with no approved correction. A request to fix such a failure authorizes diagnosis only. Ordinary in-scope failures during an active approved slice remain with `next-slice`, and an approved corrective slice returns there for implementation. Troubleshooting reproduces the mismatch, tests competing hypotheses, reports confidence and uncertainty, proposes the discovered corrective slice, and waits for its approval without editing implementation files.
- `security-check` is optional and runs only after explicit user authorization. It uses required Semgrep analysis in partial mode over files changed by the relevant work or comprehensive mode over the applicable repository, supplements it with convention-required tools, reports incomplete coverage, and waits before correction.
- Conversation-mode detection, implementation authorization, and question-versus-assumption discipline remain ambient policy behavior rather than a standalone skill.

Do not make installed skills depend on repository-root development documents. `activate` resolves the portable policy relative to its installed skill directory.

## Artifact ownership

- `AGENTS.md` contains mandatory rules for changing this public repository.
- `INTERNAL.md` contains the durable project model and design rationale.
- `CURRENT_WORK.md` is an ignored, mutable scratch pad for active discussion and immediate work.
- `README.md` describes the public project and supported usage.

## Delivery slices

Build the plugin skeleton first, then `activate`, followed by one complete slice per approved skill. Each skill slice owns its runtime metadata, instructions, focused tests, and relevant documentation. Do not create empty resource directories for planned capabilities.

Prefer instruction-only skills. Add runtime scripts, assets, hooks, MCP servers, or apps only when an approved skill demonstrates a concrete need.

Create skills for workflows that need consistent repetition or meaningful authorization boundaries, not for individual commands. Ordinary contextual operations remain agent decisions unless repeated evidence establishes a distinct workflow.

### Why conversation-gate is not a skill

A standalone skill should own a recognizable user trigger and produce a concrete outcome. Conversation gating does neither. It is baseline conduct that must already be active when the agent interprets whether a request is discussion, planning, documentation, diagnosis, or authorization to implement.

Explicit invocation would require the user to request the safeguard after it was already needed. Implicit invocation would load it across ordinary development turns, duplicate the portable policy, and spend context without adding a distinct workflow. The proposed responsibility to preserve a current mode is also misleading because authorization is inferred from the active conversation and instruction hierarchy, not maintained as durable lifecycle state.

The behavior therefore remains in the portable policy's authorization and questions-and-assumptions sections. Other skills may rely on that shared decision boundary, but should not repeat or claim ownership of it. `conversation-gate` is rejected as a standalone candidate.
