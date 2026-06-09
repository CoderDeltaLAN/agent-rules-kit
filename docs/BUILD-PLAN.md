# v0.1 Build Plan

This document defines the v0.1 construction plan for agent-rules-kit.

It is a planning document, not a release announcement. It must not be used to claim that unimplemented features already exist.

## Project purpose

agent-rules-kit is a local Python CLI that diagnoses baseline quality of AI agent instruction files in repositories.

The project is positioned as a doctor/lint tool for agent instruction files, not as a universal generator, security scanner, LLM agent, or repository automation tool.

## Product boundaries

v0.1 must preserve these boundaries:

- read-only by default;
- no network access in runtime behavior;
- no LLM dependency in runtime behavior;
- no execution of commands from analyzed repositories;
- no security guarantees;
- secret-like findings must be redacted;
- write behavior must require explicit user intent;
- generated or overwritten files must be handled conservatively.

## Current baseline

The repository currently has:

- Python package metadata;
- a minimal CLI entrypoint;
- version and default help behavior;
- smoke tests;
- a local check script;
- GitHub Actions CI workflow;
- base project documentation;
- explicit security and contribution boundaries.

This baseline is not the final product.

## v0.1 target scope

The intended v0.1 scope is:

1. `check`
   - detect known agent instruction files;
   - diagnose missing, weak, duplicated, or risky instruction patterns;
   - report findings without modifying the analyzed repository.

2. `init --dry-run`
   - show which instruction files would be created;
   - avoid writing files by default;
   - explain what each proposed file is for.

3. `init --write`
   - write only when explicitly requested;
   - avoid overwriting existing files without protection;
   - create backups before replacing supported files.

4. Output formats
   - console;
   - JSON;
   - Markdown.

5. Safety behavior
   - redact secret-like values;
   - avoid executing repository commands;
   - avoid network calls;
   - avoid unsupported security claims.

## Suggested implementation phases

Build one phase at a time.

1. Add diagnostic fixtures.
2. Add a finding model.
3. Add instruction file discovery.
4. Add the `check` command with console output.
5. Add redaction coverage.
6. Add JSON output.
7. Add Markdown output.
8. Add `init --dry-run`.
9. Add `init --write` with backup behavior.
10. Add path boundary tests.
11. Add a threat model.
12. Capture the exact CI required check name from a real pull request.
13. Require the captured status check on `main`.
14. Finalize the public README.

## README rule

The final README must be the last documentation phase of the v0.1 build.

Do not turn the current README into a polished public README until the repository has:

- real CLI behavior;
- real commands;
- real tests;
- real CI evidence;
- real output examples;
- documented limits;
- verified installation and usage instructions.

Until then, README changes should be minimal and only correct real inconsistencies.

## Out of scope for v0.1

v0.1 should not include:

- runtime LLM calls;
- network integrations;
- command execution inside analyzed repositories;
- dependency vulnerability scanning;
- CI/CD security auditing;
- autonomous fixing;
- broad repository rewrites;
- claims that a repository is secure.

## Release readiness

Before a public v0.1 release, verify:

- local checks pass;
- CI passes for the release SHA;
- tests cover the implemented commands;
- output examples are generated from real commands;
- secret-like findings are redacted in all formats;
- README reflects actual behavior only;
- SECURITY.md and CHANGELOG.md are current;
- no unsupported production or security claims are present.
