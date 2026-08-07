# Public Repository Safety Rules

This is a public repository. Treat every committed file, branch, issue, pull request, build log, and release artifact as permanently public.

## Implementation approval

- Do not build, write code, edit implementation files, or otherwise implement a plan without the user's explicit approval.
- Treat discussion, analysis, requirements, designs, and plans as non-implementation work.
- When ready to implement, ask for approval or wait for the user to request implementation.

## Questions and assumptions

- Investigate the repository, runtime, documentation, and current context before asking the user a question.
- Do not ask for information that can be discovered safely from available evidence.
- Do not silently assume when multiple plausible answers would materially change the result.
- Ask before deciding product intent, personal preference, public interfaces, destructive effects, new authority, or a workaround.
- Make a reasonable assumption when it is low-risk, reversible, conventional, and does not constrain later decisions.
- State any material assumption explicitly.
- Continue discoverable or independent work while a non-blocking question remains open.
- Do not disguise an implementation decision as an assumption merely to avoid asking.
- As a practical boundary, assume implementation details that are cheap to reverse and ask about intent or decisions that would be expensive or misleading to reverse.

## Engineering principles

- Follow KISS: prefer the simplest design that clearly solves the actual problem.
- Follow YAGNI: do not build speculative capabilities, compatibility layers, or extension points.
- Follow AHA: avoid hasty abstractions. Allow limited duplication until the shared concept and ownership are understood.
- Follow POLA: make behavior and interfaces match reasonable user and developer expectations.
- Follow separation of concerns: keep unrelated responsibilities and policy boundaries distinct.
- Apply DRY to authoritative knowledge, invariants, and business rules. Do not force abstractions merely because code looks similar.
- Use DDD proportionally: model code around the domain's language, responsibilities, and boundaries without adding ceremony the problem does not need.
- Use TDD to drive observable behavior and regression fixes where practical. Tests should prove requirements rather than mirror implementation details.

Avoid these failure patterns:

- BDUF: do not design a speculative system before the immediate problem and constraints are understood.
- STUPID code: avoid singleton abuse, tight coupling, untestability, premature optimization, indescriptive naming, and duplication of authoritative logic.
- Cargo-cult programming: do not copy a pattern, architecture, or abstraction without understanding why this project needs it.
- Golden Hammer: do not force every problem through a preferred language, framework, pattern, or architecture.
- Premature abstraction: do not extract similarities before the stable concept, responsibility, and ownership are clear.

Use dependency and abstraction judgment rather than a blanket NIH rule:

- Prefer the standard library or small custom code when behavior is simple, stable, and easy to verify.
- Prefer an established library when it owns substantial complexity such as protocols, parsing, security, persistence, or difficult edge cases.
- Reuse existing project dependencies and internal domain logic before adding either custom duplication or another package.
- Do not add a dependency merely to avoid writing a small amount of clear code.
- Custom code must still be idiomatic and cohesive. KISS and AHA do not justify flat, unrolled procedures without useful structure.
- Introduce abstractions at real responsibility and domain boundaries, not merely to reduce line count.
- Fix root causes at the layer that owns them. Any workaround requires the user's explicit approval after its constraints and tradeoffs are explained.
- Detect and reuse an already running development service when practical instead of starting a duplicate. Respect the user's requested execution method, including use of a plugin or agent-managed service.

## Personal data

- Do not commit, publish, or reproduce personal data unless the user explicitly approves the exact content for public release.
- Personal data includes private email addresses, phone numbers, home or precise personal locations, account identifiers, private usernames, signatures, private correspondence, and identifying metadata.
- Use neutral placeholders in examples, fixtures, screenshots, logs, and documentation.
- Remove identifying metadata from generated artifacts when practical.

## Secrets and credentials

- Never commit secrets, credentials, authentication material, or private configuration.
- This includes API keys, access tokens, passwords, cookies, session data, private keys, certificates with private material, connection strings, webhook secrets, recovery codes, and populated environment files.
- Store local secrets only in ignored files or an approved secret manager. Commit sanitized example configuration with placeholder values only.
- Do not print secrets to terminal output, logs, tests, screenshots, patches, commit messages, pull requests, or chat responses.

## Before publishing

- Inspect the complete staged diff, including generated and binary artifacts.
- Check staged content for secrets, personal data, local paths, internal hostnames, and unintended metadata.
- Confirm new configuration and generated files are safe for a public audience.
- If safety is uncertain, stop and ask the user before committing, pushing, opening a pull request, or publishing a release.

## If sensitive material is found

- Stop publishing activity immediately.
- Do not repeat the sensitive value in explanations or remediation commands.
- Tell the user what kind of material was found and where, using a redacted description.
- Treat an exposed secret as compromised. Remove it from the worktree and history as directed, then rotate or revoke it through the appropriate provider.
