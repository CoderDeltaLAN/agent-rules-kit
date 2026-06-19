# Changelog

All notable changes to agent-rules-kit will be documented in this file.

This project has a published GitHub Release line, but no stable support or API guarantee yet.

## [Unreleased]

No unreleased changes.

## [0.3.0] - 2026-06-19

### Added

- Prepared v0.3.0 release documentation and final release notes.

- Added v0.3 architecture and roadmap planning documentation.
- Added initial output and exit-code contract documentation for existing `check` and `init` behavior and planned v0.3 `doctor`, `budget`, and `explain` commands.
- Added golden output foundation tests for current `check` and `init` console, JSON, Markdown, stdout, stderr, and exit-code behavior.
- Added a CLI contract regression matrix for current version, help, `check`, and `init` output channels and exit codes.
- Added the read-only `doctor` baseline command for repository-level instruction diagnosis summaries.
- Added the read-only `budget` baseline command for deterministic local instruction-file size metrics.
- Added the read-only `explain` baseline command for local governance rule explanations.

## [0.2.3] - 2026-06-18

### Changed

- Released a documentation-only patch for the public `v0.2.3` GitHub Release and PyPI package line.
- Synced SUPPORT.md with the current `v0.2.3` GitHub Release and PyPI package state.
- Updated package metadata, README.md, SECURITY.md, and CHANGELOG.md release references from `v0.2.2` to `v0.2.3` without changing runtime behavior.
- Preserved the existing runtime behavior, governance diagnostics, CI workflow, PyPI Trusted Publishing workflow, and previous release tags.

### Release notes

- No runtime code or behavior changes are included in this patch release.
- The existing `v0.2.2` tag was not moved; `v0.2.3` is cut as a new docs-only patch release.

## [0.2.2] - 2026-06-18

### Changed

- Released a documentation-only patch for the public `v0.2.2` GitHub Release and PyPI package line.
- Synced SECURITY.md, README.md, CHANGELOG.md, package metadata, and release references so the published package no longer points users at stale `v0.2.1` public-truth wording.
- Preserved the existing runtime behavior, governance diagnostics, CI workflow, PyPI Trusted Publishing workflow, and previous release tags.

### Release notes

- No runtime code or behavior changes are included in this patch release.
- The existing `v0.2.1` tag was not moved; `v0.2.2` is cut as a new docs-only patch release.

## [0.2.1] - 2026-06-17

### Added

- Added a PyPI Trusted Publishing workflow for the final `v0.2.1` release path, triggered only by GitHub Release publication and configured for the `pypi` environment without static PyPI credentials.
- Added discovery support for Claude Code project instructions stored at `.claude/CLAUDE.md`.
- Added CI smoke checks for the installed `agent-rules-kit` console script and a minimal JSON `check` command.

### Fixed

- Scoped governance finding suppression to same-line negation or approval cues so adjacent safe guidance no longer hides unrelated risky instructions.
- Reject symlinked supported instruction files and harden `init --write` temporary and backup paths against symlink escapes.
- Report non-UTF-8 supported instruction files as `AIRK-SYS001` findings instead of silently skipping governance analysis.
- Updated generated `AGENTS.md` baseline content so `init --write` no longer creates instructions that fail the current governance scope or authority check.
- Fixed secret redaction pattern order so Anthropic-style `sk-ant-` keys match the specific Anthropic pattern before the generic `sk-` pattern.
- Tightened governance regex coverage for review/CI bypass, unsafe command guidance, and runtime network or LLM dependency findings.
- Expanded secret-like token redaction coverage.
- Added context-aware governance finding suppression so nearby negative guidance can avoid false positives.
- Added final runtime API phrase parity coverage for GOV005-style local-first boundary checks.

### Changed

- Split the PyPI publishing workflow into separate build and publish jobs so distributions are built, checked, smoke-tested, uploaded as a short-lived workflow artifact, and published with OIDC `id-token: write` scoped only to the publish job.
- Clarified packaging smoke documentation to distinguish console-script execution from `python -m agent_rules_kit.cli` module execution.
- Clarified README installation, normal CLI usage, development virtual environment requirements, local checks, and next-release audit readiness.
- Added Ruff linting to local checks and CI by installing project development dependencies before running `./scripts/check.sh`.
- Synced product strategy and threat model wording with the published `v0.2.0` release line and the pre-`v0.2.1` main state.
- Synced support, security, README, and release-truth documentation after the published `v0.2.0` GitHub Release.
- Added CLI output examples and governance rules reference documentation after the `v0.2.0` tag.

### Release notes

- These changes were accumulated on `main` after `v0.2.0` and are released in `v0.2.1`.
- The existing `v0.2.0` tag was not moved; `v0.2.1` was cut as a new patch release.

## [0.2.0] - 2026-06-15

### Added

- Documented the v0.2 product direction toward local-first AI agent instruction governance.
- Added the v0.2 governance rules specification for conservative, deterministic instruction-file diagnostics.
- Added governance findings for unsupported security or maturity claims, review or CI bypass guidance, unsafe command execution guidance, runtime network or LLM dependency guidance, missing secret-handling boundaries, and missing instruction scope or authority.
- Added governance finding coverage across console, JSON, and Markdown output paths.
- Added golden contract coverage for current governance console, JSON, and Markdown output behavior.
- Added structured finding evidence for line-based governance findings.
- Added regression coverage for redacting secret-like values from finding evidence in JSON output.
- Added v0.2 release-readiness, packaging dry-run, and governance-boundaries evidence documents.

### Changed

- Updated GitHub Actions workflow actions to Node 24-compatible major versions.
- Preserved the published `v0.1.0` pre-release while preparing v0.2.0 metadata.
- Updated package metadata from `0.1.0` to `0.2.0`.

### Security

- Kept governance diagnostics conservative, heuristic, and pattern-based.
- Preserved the runtime boundary: read-only by default, no runtime network calls, no runtime LLM calls, and no execution of commands from analyzed repositories.
- Redacted secret-like values in finding message, path, and evidence payload fields before emitting supported output.
- Documented that governance findings are not proof that a repository is safe and do not replace maintainer review.
- Captured branch protection, required status check, admin enforcement, force-push prevention, deletion prevention, solo-maintainer review profile, and private vulnerability reporting evidence for v0.2 release preparation.
- Documented that private vulnerability reporting is currently verified as disabled and must not be claimed as enabled.

## [0.1.0] - 2026-06-09

### Added

- Repository identity baseline with README, MIT license, and .gitignore.
- Python project metadata in pyproject.toml.
- Minimal package version module.
- Initial CLI entrypoint with version and help behavior.
- CLI smoke tests.
- Local check script for syntax, tests, text hygiene, and Git whitespace checks.
- GitHub Actions CI workflow using `local-checks / Python 3.12`.
- AGENTS.md with mandatory AI assistant operating rules.
- SECURITY.md with explicit security boundaries and non-goals.
- SUPPORT.md with pre-release support boundaries.
- CONTRIBUTING.md with Genesis and Always-Green workflow rules.
- GitHub issue templates and pull request template.
- Diagnostic fixtures for supported and risky instruction file scenarios.
- Finding model for diagnostic output.
- Instruction file discovery for `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Cursor rules, GitHub Copilot instructions, and GitHub instruction files.
- `check` command with console output.
- JSON output for `check`.
- Markdown output for `check`.
- Secret-like value redaction helpers and tests.
- `init --dry-run` planning behavior.
- Explicit `init --write` behavior for root `AGENTS.md`.
- Backup behavior before replacing an existing root `AGENTS.md`.
- Path boundary tests for discovery and init write behavior.
- Threat model in `docs/THREAT-MODEL.md`.
- Public README with real CLI screenshots, command examples, safety boundaries, quality gates, maintainer workflow, and optional support badge.

### Security

- Runtime boundaries documented: read-only by default, no network behavior, no LLM dependency, and no execution of commands from analyzed repositories.
- `check` and `init --dry-run` documented as non-writing behavior.
- `init --write` documented as explicit write behavior only.
- Existing root `AGENTS.md` is backed up before replacement.
- Secret-like values are redacted in supported output paths.
- Path boundary tests cover root-only init write behavior and repository-relative discovery paths.
- Threat model documents assets, trust boundaries, threats, mitigations, and residual risk.
- The project is explicitly documented as not a security scanner and as providing no security guarantees.

### Changed

- Replaced the inception README with a public README reflecting implemented behavior and verified output examples.
- Updated security and support documentation from local-inception wording to current pre-release public repository status.

### Deprecated

- No deprecated entries.

### Removed

- No removed entries.

### Fixed

- Corrected release-readiness documentation that still referred to future write behavior after `init --write` had been implemented.
- Corrected stale local-inception wording in support and security documentation.

## Release policy

Before publishing any GitHub release, the maintainer must verify:

- local checks pass;
- CI passes for the release SHA;
- README reflects actual behavior;
- sdist and wheel build and install from clean temporary environments;
- SECURITY.md has a private reporting channel or clearly documents the absence of one;
- CHANGELOG.md describes the released changes;
- version number matches pyproject.toml and package metadata;
- the tag and GitHub Release point to the verified release SHA;
- no unsupported security, production, or maturity claims are present.

## Notes for maintainers

Do not use this changelog to exaggerate maturity.

A change is not released because it exists locally. A change is released only when it is tagged, documented, pushed, and verified.
