# Pull Request

## Summary

Describe the change in one or two clear sentences.

## Why

Explain why this change is needed.

## Scope

This PR changes:

- [ ] source code
- [ ] tests
- [ ] documentation
- [ ] CI / GitHub configuration
- [ ] security-sensitive behavior
- [ ] project policy or workflow

## Checks

Before marking this PR ready, confirm:

- [ ] I read AGENTS.md.
- [ ] I changed one minimal unit.
- [ ] I did not use git add .
- [ ] I reviewed the staged diff.
- [ ] I ran ./scripts/check.sh.
- [ ] Tests pass locally.
- [ ] CI is expected to pass.
- [ ] No secrets, tokens, credentials, private URLs, or customer data were added.
- [ ] No unsupported production or security claims were added.

## Security and boundary impact

Does this change touch any of these areas?

- [ ] secret detection
- [ ] redaction
- [ ] file traversal
- [ ] symlink handling
- [ ] write behavior
- [ ] command execution boundaries
- [ ] network behavior
- [ ] LLM behavior
- [ ] GitHub Actions permissions
- [ ] none of the above

If any box except "none of the above" is checked, explain the risk and mitigation.

## Testing evidence

Paste the relevant local output or summarize it precisely.

Expected minimum:

./scripts/check.sh

## Known limitations

List any known limitation, tradeoff, or follow-up needed.

## Release notes

Should this affect CHANGELOG.md?

- [ ] yes
- [ ] no

If yes, explain the changelog entry.
