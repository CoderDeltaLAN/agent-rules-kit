# Changelog

All notable changes to agent-rules-kit will be documented in this file.

This project has no public release yet.

## [Unreleased]

### Added

- Repository identity baseline with README, MIT license, and .gitignore.
- Python project metadata in pyproject.toml.
- Minimal package version module.
- Initial CLI entrypoint with version and help behavior.
- CLI smoke tests.
- Local check script for syntax, tests, text hygiene, and Git whitespace checks.
- AGENTS.md with mandatory AI assistant operating rules.
- SECURITY.md with explicit security boundaries and non-goals.
- CONTRIBUTING.md with Genesis and Always-Green workflow rules.

### Security

- Runtime boundaries documented: read-only by default, no network behavior, no LLM dependency, and no execution of commands from analyzed repositories.
- Secret-like findings must be redacted.
- The project is explicitly documented as not a security scanner and as providing no security guarantees.

### Changed

- Nothing yet.

### Deprecated

- Nothing yet.

### Removed

- Nothing yet.

### Fixed

- Nothing yet.

## Release policy

Before the first public release, the maintainer must verify:

- local checks pass;
- CI passes;
- README reflects actual behavior;
- SECURITY.md has a real reporting channel or clearly documents the absence of one;
- CHANGELOG.md describes the released changes;
- version number matches pyproject.toml and package metadata;
- no unsupported security, production, or maturity claims are present.

## Notes for maintainers

Do not use this changelog to exaggerate maturity.

A change is not released because it exists locally. A change is released only when it is tagged, documented, pushed, and verified.
