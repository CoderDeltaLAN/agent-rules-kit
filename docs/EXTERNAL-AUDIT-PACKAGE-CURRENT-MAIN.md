# External audit package for current main

Status: required external audit package manifest before v0.4.0.
Published package line: v0.3.0.
Next intended public release line: v0.4.0, only after external audit, release preparation, GitHub Release publication, PyPI publication, and post-release verification.
Release authorization: none. This document must not be treated as permission to publish a GitHub Release or PyPI package.

## Purpose

This document closes the evidence gap described by RB-03: the final external audit package must include core files, workflow files, current documentation, relevant tests, exact SHA evidence, CI evidence, and the current action-plan state.

A previous audit marked an evidence package incomplete because it did not include enough source, test, workflow, and documentation material for a serious review. This document defines the minimum complete package. An external audit based only on summaries, screenshots, selected snippets, or a high-level repo description is not acceptable.

## Audit target rule

The external audit target must be current main after this manifest is merged.

The final package must capture, outside this document if necessary:

- exact main SHA under audit;
- origin/main SHA;
- PR number that introduced this manifest;
- GitHub Actions CI run for that exact SHA;
- GitHub Actions CodeQL run for that exact SHA;
- local check output for that exact SHA;
- post-release audit output for that exact SHA;
- confirmation that no release, tag, PyPI publication, dependency update, workflow permission change, or branch-protection change was made by this manifest phase.

The exact SHA in this document's creation branch is not enough after merge. The final audit packet must refresh the SHA and CI evidence from main.

## Baseline evidence at manifest creation

This manifest was created from:

- branch: audit/provide-complete-core-files;
- base main SHA before this manifest commit: 378bf5a41dd355e3e219a0a3b54408c039bdeca8;
- CI push run for that base SHA: 27885987180, success;
- CodeQL push run for that base SHA: 27885987214, success;
- required file existence check: 45 required files, 0 missing;
- command surface observed from source tree: check, init, doctor, budget, dedupe, conflicts, explain.

This baseline is evidence of the state before adding this manifest. The final external audit must still use the post-merge main SHA for the actual audit target.

## Package completeness rule

The audit package must include the full contents of every file listed below.

A file-name list alone is not enough. A summary is not enough. A partial excerpt is not enough. The auditor must be able to inspect the actual source, tests, workflows, release boundaries, security boundaries, and documentation truth from the files.

Ignored or generated runtime artifacts must not be included as evidence, including .git, .venv, .ruff_cache, __pycache__, build outputs, dist outputs, coverage outputs, local editor state, or temporary files.

## Core package source files

Include full contents of:

- src/agent_rules_kit/__init__.py
- src/agent_rules_kit/cli.py
- src/agent_rules_kit/findings.py
- src/agent_rules_kit/init_plan.py
- src/agent_rules_kit/init_write.py
- src/agent_rules_kit/discovery.py
- src/agent_rules_kit/governance.py
- src/agent_rules_kit/redaction.py
- src/agent_rules_kit/budget.py
- src/agent_rules_kit/explain.py
- src/agent_rules_kit/dedupe.py
- src/agent_rules_kit/conflicts.py

## Core test files

Include full contents of:

- tests/test_cli.py
- tests/test_golden_outputs.py
- tests/test_governance.py
- tests/test_findings.py
- tests/test_discovery.py
- tests/test_diagnostic_fixtures.py
- tests/test_init_plan.py
- tests/test_init_write.py
- tests/test_path_boundaries.py
- tests/test_redaction.py
- tests/test_dedupe.py
- tests/test_conflicts.py

## Project metadata and public-truth files

Include full contents of:

- README.md
- CHANGELOG.md
- pyproject.toml
- AGENTS.md
- SECURITY.md
- SUPPORT.md
- CONTRIBUTING.md
- LICENSE

## GitHub, CI, release, and supply-chain files

Include full contents of:

- .github/workflows/ci.yml
- .github/workflows/codeql.yml
- .github/workflows/publish-pypi.yml
- .github/dependabot.yml
- scripts/check.sh
- scripts/post-release-audit.sh

## Security, output-contract, and audit documentation

Include full contents of:

- docs/THREAT-MODEL.md
- docs/RULES.md
- docs/OUTPUTS.md
- docs/EXIT-CODES.md
- docs/SECURITY-SUPPLY-CHAIN-EVALUATION.md
- docs/PRIVATE-VULNERABILITY-REPORTING.md
- docs/OPENSSF-SCORECARD-EVALUATION.md
- docs/POST-AUDIT-ACTION-PLAN-CURRENT-MAIN.md
- docs/PRE-V0.4.0-INTERNAL-READINESS-AUDIT.md
- docs/POST-V0.3.0-FUNCTIONAL-CONTRACT-EVIDENCE.md
- docs/POST-V0.3.0-INTERNAL-READINESS-AUDIT.md
- docs/V0.3.0-POST-RELEASE-AUDIT.md
- docs/V0.3.0-RELEASE-NOTES.md
- docs/V0.3-ARCHITECTURE-ROADMAP.md
- docs/PRODUCT-STRATEGY.md

## Minimum command evidence to include with the package

The final external audit package must include terminal output for:

- git status --short --branch
- git rev-parse HEAD
- git rev-parse origin/main
- git log --oneline --decorate -8
- gh pr view for the PR that merged this manifest
- gh run list for CI and CodeQL on the exact main SHA
- ./scripts/check.sh
- ./scripts/post-release-audit.sh
- python -m agent_rules_kit.cli --help
- python -m agent_rules_kit.cli --version

The package should also include a short statement that the audit target is source-tree behavior on current main before v0.4.0, not the already published v0.3.0 PyPI package.

## Boundaries for the auditor

The auditor should treat the project as:

- a local-first Python CLI;
- read-only by default;
- no network calls during repository analysis;
- no LLM calls during runtime;
- no execution of commands found in analyzed repositories;
- no stable support promise yet;
- no claim that dedupe or conflicts are already published on PyPI before v0.4.0 is actually released and verified.

The auditor should reject or flag any package that omits core files, hides workflows, omits tests, omits release workflow details, omits the current action plan, omits exact SHA evidence, or presents v0.4.0 as already published before release verification exists.

## Release gate

Do not start release/prepare-v040 until this external audit package is assembled from current main, externally reviewed, and any resulting findings are either fixed through separate Always-Green phases or explicitly deferred with written rationale.
