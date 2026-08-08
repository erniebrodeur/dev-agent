---
name: security-check
description: Run a user-authorized Semgrep security analysis in partial mode over only files changed by the relevant work, or in comprehensive mode over the entire applicable repository when the user requests a security check without narrowing its scope. Use when the user explicitly requests or approves a security check. The agent may recommend a check, but must not run one automatically. Report evidence and propose corrective slices without implementing fixes.
---

# Security Check

Perform a scoped, evidence-based security assessment and report its limits. This workflow is analysis-only even when the original request also asks for fixes.

## Workflow

1. Read applicable project instructions and inspect repository evidence relevant to the request. If project context has not been recovered in the current task, read `../recover-project-context/SKILL.md` completely and run its recovery workflow.
2. Confirm that the user requested or approved the check. The agent may suggest a check when risk justifies it, but a suggestion is not authorization to run one.
3. Resolve the mode and exact scope:
   - Use partial mode when the user requests a partial check. Scan only files changed by the relevant implementation slice, branch, pull request, commit range, or working-tree work. Determine the comparison from context and repository evidence; ask when materially ambiguous.
   - Use comprehensive mode when the user requests a security check without narrowing its scope. Scan all applicable repository-owned source and configuration files. Exclude dependencies, generated output, caches, and unsupported files, and report every material exclusion.
   - Honor a narrower or otherwise explicit user-defined scope.
4. Read a root `CONVENTIONS.md`, when present, for additional required security tools or project-specific checks.
5. Run Semgrep over the resolved scope. Semgrep is mandatory in both modes. Run convention-required tools in addition to Semgrep, not instead of it.
6. If Semgrep is unavailable, fails, or cannot cover the resolved scope, report the check as incomplete. Do not claim success or silently substitute another tool. Report tool errors, skipped rules, unsupported files, and other material coverage limits without exposing secrets.
7. Triage findings rather than repeating scanner output. For each material finding, establish the location, evidence, plausible impact, severity, and confidence. Distinguish supported vulnerabilities, unresolved findings, and false positives; do not dismiss a result without evidence.
8. Report the mode, exact scope, Semgrep configuration and completion status, additional tools used, findings, exclusions, false positives, unresolved findings, and remaining uncertainty. State that a clean scan does not prove the absence of vulnerabilities.
9. Propose the smallest coherent corrective slice for each related group of supported findings. Include outcome, scope, constraints or invariants, non-goals, dependencies, and verification expectations. Do not implement a correction.
10. Update `CURRENT_WORK.md`, when the project uses it, with a non-sensitive summary of material findings, incomplete coverage, and proposed corrections. Report the result and wait for explicit correction approval.

## Boundaries

- Do not run either mode automatically.
- Do not expand partial mode beyond files changed by the relevant work unless the user approves a broader scope.
- Do not treat raw scanner output as confirmed vulnerabilities or a clean scan as proof of security.
- Do not expose secret values, credentials, personal data, or sensitive configuration in output or project memory.
- Do not edit implementation files, tests, configuration, or product documentation during the check.
- Do not inherit correction authority from a request to check and fix. Security diagnosis and correction remain separate approval boundaries.
- Do not turn a comprehensive security check into a full public-release audit. Documentation, licensing, packaging, publication, and other release-readiness concerns belong to the release workflow.
- Committing, pushing, opening a pull request, deploying, publishing, messaging others, destructive operations, and implementation of corrective slices remain outside this skill.
