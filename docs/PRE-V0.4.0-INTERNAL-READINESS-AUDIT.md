# Pre-v0.4.0 internal readiness audit

Status: internal audit record for current main after post-audit hardening phases.
Repository: CoderDeltaLAN/agent-rules-kit.
Audited main SHA: 40060c6bb359e42ca9d46a64c8373be09b58a25f.
Published package line: v0.3.0.
Next eligible public release target: v0.4.0.
Release authorization: not granted.

## Executive verdict

Current main is healthier than the previous post-audit baseline and the immediate hardening sequence has closed the main test, documentation, and package-metadata gaps identified for dedupe, conflicts, symlink behavior, supply-chain documentation, and Python 3.13 package metadata.

This is still not a release approval.

The repository is fit to proceed to the final external audit package phase, but not fit to publish a GitHub Release or PyPI package until the release phase captures exact release evidence, builds and verifies artifacts, publishes the release, verifies PyPI, and records final post-release evidence.

## Scope of this audit

This audit reviewed the current main state after the following merged phases:

- PR #121: docs: sync supply chain action versions.
- PR #122: test: add dedupe conflicts error contracts.
- PR #123: test: add conflicts rule family fixtures.
- PR #124: test: add dedupe golden output contract.
- PR #125: docs: clarify symlink command behavior.
- PR #126: packaging: add Python 3.13 classifier.

This audit did not publish a release, move tags, build release artifacts, upload to GitHub Releases, upload to PyPI, change branch protection, change CI, change runtime behavior, or change dependencies.

## Current command surface

Current main exposes the following CLI commands:

- check;
- init;
- doctor;
- budget;
- dedupe;
- conflicts;
- explain.

The package metadata still reports version 0.3.0. That is correct for current main before the dedicated release phase because dedupe and conflicts are present on main but are not yet published as a verified public package release.

## Evidence accepted

The following evidence is accepted for this internal audit:

- local checks pass with 161 unit tests;
- Ruff passes;
- text hygiene passes;
- git whitespace checks pass;
- current package metadata includes Python 3.12 and Python 3.13 classifiers;
- pyproject.toml still keeps requires-python as >=3.12;
- workflows include the current action versions documented in SECURITY-SUPPLY-CHAIN-EVALUATION.md;
- dedupe and conflicts have CLI error-contract coverage;
- conflicts has representative current rule-family fixture coverage;
- dedupe has a representative golden output contract;
- OUTPUTS and EXIT-CODES document hard-fail symlink behavior for budget, dedupe, and conflicts.

## Closed findings from the post-audit hardening sequence

### H-01: supply-chain action-version documentation

Status: closed by PR #121.

The supply-chain evaluation now reflects the current workflow action versions, including checkout v7 and download-artifact v8. No workflow or pinning-policy change was made in that documentation-only phase.

### H-02: dedupe and conflicts CLI error-contract tests

Status: closed by PR #122.

The CLI error contract now covers the important failure paths for the new dedupe and conflicts command surfaces, including symlink behavior and invalid input paths returning exit code 2.

### H-03: conflicts rule-family fixtures

Status: closed by PR #123.

The conflicts command now has representative fixture coverage for the implemented deterministic rule families. This does not turn conflicts into broad semantic contradiction analysis, and the command must not be documented as such.

### H-04: dedupe golden output contract

Status: closed by PR #124.

The dedupe command now has a stable representative output contract. This reduces the risk of accidental CLI output drift before v0.4.0.

### M-01: symlink command behavior documentation

Status: closed by PR #125.

OUTPUTS and EXIT-CODES now document that budget, dedupe, and conflicts reject symlinked supported instruction-file paths with exit code 2 instead of following them or silently producing partial reports.

### M-02: Python 3.13 classifier decision

Status: closed by PR #126.

The repository already had Python 3.13 compatibility CI. The package metadata now includes the Python 3.13 classifier while keeping requires-python unchanged at >=3.12.

## Remaining release blockers

### RB-01: no release from current main

Status: still open until release/prepare-v040 is complete.

Current main includes post-v0.3.0 functionality, including dedupe and conflicts. Publishing from main without a dedicated release phase would break the public truth boundary.

### RB-02: final release evidence is missing

Status: closed by docs/triage-v040-release-truth-wording.

The v0.4.0 release still needs exact release evidence, including:

- exact release SHA;
- CI success for the exact release SHA;
- CodeQL result for the exact release SHA or explicit documented policy if treated as informative;
- wheel and sdist build;
- twine check;
- wheel smoke;
- sdist smoke;
- GitHub Release publication;
- PyPI publish workflow success;
- clean install smoke from PyPI;
- final post-release audit.

### RB-03: final external audit package must include core files

Status: open.

Before release/prepare-v040, the external audit package must include the core source files, workflow files, current docs, relevant tests, exact SHA, CI evidence, and the current action-plan state. A previous audit marked an evidence package incomplete, so this must not be skipped.

## New internal finding

### F-01: stale or historical release-target wording needs final triage before v0.4.0

Severity: medium.
Status: open.

The stale-truth scan found older v0.3.1 and v0.2.x wording in historical docs, changelog entries, and product-strategy material. The v0.3.1 wording that could read like current guidance in docs/V0.3.0-POST-RELEASE-AUDIT.md was triaged and marked as superseded historical planning. Historical v0.2.x release evidence remains intentionally unchanged.

Resolution:

- v0.3.1 wording in the v0.3.0 post-release audit is now explicitly labeled as superseded historical planning;
- current release guidance remains v0.4.0;
- historical v0.2.x release evidence is retained and not rewritten.

## Deferred non-blockers

The following are not blockers for the immediate v0.4.0 release path unless a later audit upgrades them:

- GitHub Actions SHA pinning policy;
- JSON output for doctor, budget, dedupe, conflicts, and explain;
- static typing marker or py.typed;
- mypy or pyright;
- ruff format --check;
- property-based tests;
- SBOM;
- block-level dedupe;
- CLI renderer refactor.

## Release decision

Do not publish v0.4.0 from this audit branch.

The next safe step is to close or explicitly triage F-01, then prepare the complete external audit package. Only after that external audit is complete and any findings are addressed should release/prepare-v040 begin.

## Next phases

Recommended order:

1. docs/triage-v040-release-truth-wording
2. audit/provide-complete-core-files
3. external audit pass
4. fixes from external audit if any
5. release/prepare-v040
6. release/v0.4.0
7. audit/post-v0.4.0-release

## Final verdict

Current main is a strong pre-release candidate for the v0.4.0 release train, but it is not release-ready yet. The technical blockers around dedupe, conflicts, symlink behavior, supply-chain documentation, and Python 3.13 metadata are closed. The remaining work is release truth, complete external audit evidence, and disciplined release execution.
