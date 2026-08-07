# Public Repository Safety Rules

This is a public repository. Treat every committed file, branch, issue, pull request, build log, and release artifact as permanently public.

## Implementation approval

- Do not build, write code, edit implementation files, or otherwise implement a plan without the user's explicit approval.
- Treat discussion, analysis, requirements, designs, and plans as non-implementation work.
- When ready to implement, ask for approval or wait for the user to request implementation.

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
