# Post-v0.3.0 Internal Readiness Audit

Status: internal readiness audit record.
Scope: current post-v0.3.0 `main` state before external audit and any future release.
Branch: `audit/internal-post-v030-current-main-readiness`.
Baseline main SHA: `4e20ed272c4b281b6b82c6d7fcad46ac342adac5`.
Date: 2026-06-20.

This document records an internal audit pass after the README current-main truth and repository-layout synchronization phases.

It does not publish a release, create a tag, publish to PyPI, change branch protection, change CI requirements, change runtime behavior, or approve a stable support/API guarantee.

## Verdict

Current `main` is internally coherent enough to move to external audit, but it is not release-ready by itself.

No release or PyPI publication is authorized from this record alone.

Before any future release, the repository still needs:

- external audit;
- correction of any external-audit findings by separate Always-Green phases;
- final release-boundary review;
- package build and clean install verification;
- GitHub Release and PyPI publication through the documented release workflow;
- post-release verification from a clean PyPI install.

## Verified evidence

The internal audit pass verified the following local evidence:

- `main` was clean and synchronized with `origin/main` before the audit branch was created;
- no open pull requests were present at audit start;
- README public truth was reviewed from the live repository;
- documentation inventory was reviewed;
- CLI command help was reviewed for the implemented command surface;
- GitHub Actions workflows were reviewed from tracked files;
- local maintenance scripts were reviewed from tracked files;
- `./scripts/check.sh` passed;
- `./scripts/post-release-audit.sh` passed;
- the test suite passed with 152 tests;
- Ruff passed;
- text hygiene checks passed;
- Git whitespace checks passed.

## Current command boundary

Current `main` documents and implements the following command surface:

- `check`;
- `init --dry-run`;
- `init --write`;
- `doctor`;
- `budget`;
- `explain`;
- `dedupe`;
- `conflicts`.

The published `v0.3.0` package includes `doctor`, `budget`, and `explain`.

`dedupe` and `conflicts` are current-main post-v0.3.0 additions and must not be represented as published PyPI package behavior until a later release is cut, published, and verified.

## Release boundary

The README now correctly distinguishes:

- current published GitHub Release and PyPI package: `v0.3.0`;
- previous published baseline: `v0.2.3`;
- current `main` additions after `v0.3.0`;
- development-from-source checks versus published-package behavior;
- future release requirements.

This boundary must remain intact until the next release is deliberately prepared.

## Findings

### AIRK-AUDIT-001 — Public README truth is coherent

Severity: pass.
Status: no action required.

The README now records the current published release boundary and current-main additions without claiming that unreleased commands are already published on PyPI.

### AIRK-AUDIT-002 — Repository layout is sufficiently current

Severity: pass.
Status: no action required.

The README repository layout now includes current workflows, Dependabot configuration, core evidence documents, post-release audit script, package modules, and test files, while excluding ignored/cache/runtime paths such as `.git/`, `.venv/`, `.ruff_cache`, and `__pycache__`.

### AIRK-AUDIT-003 — Local gates are green

Severity: pass.
Status: no action required.

The local check suite and post-release audit passed from the audit branch without tracked-file changes at audit start.

### AIRK-AUDIT-004 — Release is still blocked pending external audit

Severity: release-blocking process item.
Status: open.

The repository is not approved for a new release or PyPI publication from internal audit alone.

Required next evidence:

- external audit;
- triage of findings;
- correction phases if needed;
- final release readiness record;
- packaging verification;
- GitHub Release and PyPI workflow verification;
- clean install smoke from PyPI.

### AIRK-AUDIT-005 — Threat model should explicitly mention post-v0.3.0 commands

Severity: minor documentation alignment.
Status: follow-up recommended before next release.

`docs/THREAT-MODEL.md` describes the current post-v0.3.0 main state and the published v0.3.0 command surface, but should explicitly mention `dedupe` and `conflicts` as read-only current-main post-v0.3.0 commands before a release that includes them.

This is not a runtime blocker, but it is a useful documentation hardening item before external audit or release closeout.

Recommended follow-up branch:

- `docs/sync-threat-model-current-main-commands`

## Non-findings

This audit did not find evidence that current `main` introduces:

- runtime network access;
- runtime LLM dependency;
- repository command execution;
- dependency vulnerability scanning as a product feature;
- unsupported security-product claims;
- new write behavior beyond explicit `init --write`.

## Limits of this internal audit

This record is not:

- an external audit;
- a line-by-line formal security review;
- proof that the project is secure;
- proof that PyPI publication will succeed;
- proof that GitHub branch protection or repository settings are perfect;
- a stable API or support guarantee;
- approval to cut a release.

## Recommended next phases

Recommended order:

1. `docs/sync-threat-model-current-main-commands`
2. external audit prompt/report for current `main`
3. correction phases for external audit findings
4. final release readiness record
5. packaging and clean install verification
6. GitHub Release and PyPI publication only if all prior evidence is green

## Closeout rule

This audit phase is complete only after this record is merged by PR, `main` is clean and synchronized, CI is green for the merge SHA, and the audit branch is deleted locally and remotely.
