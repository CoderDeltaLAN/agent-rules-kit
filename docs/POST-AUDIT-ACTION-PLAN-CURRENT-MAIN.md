# Post-audit action plan for current main before v0.4.0

Status: planning and release-boundary record.
Repo: CoderDeltaLAN/agent-rules-kit.
Current baseline SHA for this record: 34b5f337c28b1fd7923f6d8f20174919b9b95682.
Published package line: v0.3.0.
Next public release target: v0.4.0, not v0.3.1.
Release authorization: not granted.

This document consolidates the external audit findings and the current live repository state after the first blocker fixes were already merged. It exists to prevent an impulsive release and to define the remaining minimum Always-Green phases before any future GitHub Release or PyPI publication.

## Executive decision

agent-rules-kit is healthy as a current-main technical repository and portfolio artifact, but it is not release-ready.

Do not publish a new GitHub Release or PyPI package from this state.

The next release that includes dedupe and conflicts must be v0.4.0 because those commands are new compatible functionality, not a patch-only fix line.

## Product boundaries that must not change

agent-rules-kit remains a local-first Python CLI for diagnosing AI agent instruction files.

The project must remain:

- read-only by default;
- no runtime network calls;
- no runtime LLM calls;
- no execution of commands from analyzed repositories;
- zero runtime dependencies unless a future phase explicitly decides otherwise;
- conservative, deterministic, and pattern-based;
- honest that it is not a security scanner, not a CI/CD auditor, not a dependency vulnerability scanner, not an autonomous fixer, and not proof that a repository is safe.

## Audits consolidated

The external audits agreed on the same core result:

- current main is externally-audit-ready or strong as a repository;
- current main is not release-ready;
- no new release or PyPI publication is authorized;
- dedupe and conflicts make the next public version a minor release: v0.4.0;
- release requires more contract coverage, release evidence, and a final audit pass.

## Live state after merged fixes

This plan is recorded after these fixes were already merged into main:

1. fix/check-console-path-redaction
   - Fixed the check console path redaction gap.
   - Current cli.py prints the check repository path through redact_secret_like_values.

2. fix/post-release-audit-dynamic-version
   - Fixed the post-release audit CLI version smoke so it derives the expected version from pyproject.toml instead of hardcoding 0.3.0.

3. fix/conflicts-block-polarity-negation
   - Fixed negated pull request guidance handling for conflicts.
   - Added regression coverage for negated PR guidance.

Those items must not be re-opened as if they were still pending unless a later audit finds a new issue in the actual merged code.

## Release blockers and high-priority remaining work

### RB-01: no release from current main

Status: open until release/prepare-v040 is complete.

main contains post-v0.3.0 functionality, including dedupe and conflicts. Publishing without a formal release phase would break the public truth boundary.

Required future phase:

- release/prepare-v040

### RB-02: final release evidence is missing

Status: open.

Before v0.4.0, the repo needs evidence for:

- exact release SHA;
- CI success for that SHA;
- CodeQL result for that SHA or explicit documented policy if informative only;
- wheel and sdist build;
- twine check;
- wheel smoke;
- sdist smoke;
- GitHub Release;
- PyPI publish workflow success;
- clean install smoke from PyPI;
- final post-release audit.

Required future document:

- docs/V0.4.0-RELEASE-EVIDENCE.md

### RB-03: final external audit package must include core files

Status: open.

A prior audit marked the evidence package incomplete. The final audit package must include core files, workflows, docs, tests, exact SHA, and CI evidence.

Minimum core files to include:

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
- README.md
- CHANGELOG.md
- pyproject.toml
- AGENTS.md
- SECURITY.md
- SUPPORT.md
- CONTRIBUTING.md
- LICENSE
- .github/workflows/ci.yml
- .github/workflows/codeql.yml
- .github/workflows/publish-pypi.yml
- .github/dependabot.yml
- scripts/check.sh
- scripts/post-release-audit.sh
- docs/THREAT-MODEL.md
- docs/RULES.md
- docs/OUTPUTS.md
- docs/EXIT-CODES.md
- docs/SECURITY-SUPPLY-CHAIN-EVALUATION.md
- docs/PRIVATE-VULNERABILITY-REPORTING.md
- docs/OPENSSF-SCORECARD-EVALUATION.md

### H-01: SECURITY-SUPPLY-CHAIN-EVALUATION action versions are stale

Status: closed by PR #121.

docs/SECURITY-SUPPLY-CHAIN-EVALUATION.md still mentions older GitHub Actions versions, while current workflows include actions/checkout@v7 and actions/download-artifact@v8.

Completed phase:

- docs/sync-supply-chain-evaluation-action-versions

Acceptance criteria:

- document reflects current workflow action versions;
- explicitly verifies the publish workflow upload-artifact@v4 and download-artifact@v8 pairing;
- does not pin actions by SHA in this documentation-only phase;
- does not change CI.

### H-02: dedupe and conflicts need CLI error-contract tests

Status: closed by PR #122.

Before publishing dedupe and conflicts in v0.4.0, their error paths need tests matching docs/OUTPUTS.md and docs/EXIT-CODES.md.

Completed phase:

- test/add-dedupe-conflicts-error-contracts

Acceptance criteria:

- dedupe non-UTF-8 supported instruction file returns exit code 2;
- conflicts non-UTF-8 supported instruction file returns exit code 2;
- dedupe symlink via CLI returns exit code 2;
- conflicts symlink via CLI returns exit code 2;
- stderr redacts token-like values where relevant;
- commands do not mutate fixture files;
- scripts/check.sh passes.

### H-03: conflicts needs rule-family fixtures

Status: closed by PR #123.

conflicts is more reputation-sensitive than dedupe because it reports contradictory guidance. It needs coverage for the implemented families, not broad semantic analysis.

Completed phase:

- test/add-conflicts-rule-family-fixtures

Acceptance criteria:

- main integration family covered;
- checks family covered;
- runtime network or LLM family covered;
- secrets family covered;
- unsafe commands family covered;
- negation/adversarial cases covered;
- aligned guidance no-conflict case covered;
- no LLM, network, or broad semantic expansion.

### H-04: dedupe needs a representative golden or contract test

Status: closed by PR #124.

dedupe is a new v0.4.0 command surface and needs a stable representative output contract.

Completed phase:

- test/add-dedupe-golden-contract

Acceptance criteria:

- representative dedupe output is covered by golden or contract assertions;
- no fragile hardcoded byte or line counts unless intentionally derived or centralized;
- scripts/check.sh passes.

### M-01: symlink behavior needs clearer documentation

Status: closed by PR #125.

check degrades symlinked supported instruction files to SYS002 findings, while budget, dedupe, and conflicts fail hard with exit code 2. This can be valid, but must be documented as a deliberate UX and safety choice.

Completed phase:

- docs/sync-outputs-symlink-behavior-clarification

Acceptance criteria:

- docs/OUTPUTS.md explains the behavior difference;
- docs/EXIT-CODES.md remains consistent;
- docs/THREAT-MODEL.md explains the safety reason if needed;
- no code changes unless explicitly approved.

### M-02: Python 3.13 classifier decision

Status: closed by PR #126.

The project has a Python 3.13 compatibility job, but package classifiers currently communicate only Python 3.12 support.

Completed phase:

- packaging/sync-python-313-classifier

Acceptance criteria:

- decide whether Python 3.13 is supported or only compatibility-informative;
- if supported, add the Python 3.13 classifier;
- if not supported, document the compatibility job as informative;
- do not mix this with release.

### M-03: GitHub Actions pinning policy remains a separate decision

Status: deferred.

GitHub Actions currently use version tags rather than full commit SHAs. This is not a blocker for the immediate hardening sequence, but it should be decided explicitly before claiming stronger supply-chain posture.

Potential future phase:

- supply-chain/decide-actions-pinning-policy

Do not pin by SHA blindly.

## Deferred non-blockers

The following are not required before v0.4.0 unless a later audit makes them blocking:

- block-level dedupe;
- JSON output for doctor, budget, dedupe, conflicts, and explain;
- refactor cli.py renderers and handlers;
- explicit system-finding pass in governance.py;
- static typing with mypy or pyright;
- py.typed marker;
- ruff format --check;
- property-based tests;
- SBOM.

## Mandatory phase order from this point

The first three blocker-fix phases are already merged before this plan record. From the current branch forward, use this order:

1. audit/record-post-audit-action-plan
2. docs/sync-supply-chain-evaluation-action-versions
3. test/add-dedupe-conflicts-error-contracts
4. test/add-conflicts-rule-family-fixtures
5. test/add-dedupe-golden-contract
6. docs/sync-outputs-symlink-behavior-clarification
7. packaging/sync-python-313-classifier
8. audit/internal-post-fixes-pre-v040-readiness
9. audit/provide-complete-core-files
10. release/prepare-v040

Do not start release/prepare-v040 until the final internal readiness pass and the complete external audit package are done.

## Definition of done for the full cycle

The full cycle is done only when:

- all release-blocking findings are closed;
- high findings are closed or explicitly deferred with evidence;
- current docs match the implemented command surface;
- v0.4.0 version bump is deliberate and isolated to the release phase;
- README, SECURITY, SUPPORT, CHANGELOG, THREAT-MODEL, OUTPUTS, EXIT-CODES, release notes, and release evidence agree;
- CI is green for the exact release SHA;
- CodeQL is green or explicitly documented as informative;
- wheel and sdist are built and verified;
- twine check passes;
- wheel smoke passes;
- sdist smoke passes;
- GitHub Release is published for the verified tag;
- PyPI publishes agent-rules-kit==0.4.0;
- clean install smoke from PyPI passes;
- post-release audit passes;
- main local and origin/main match the release SHA;
- release branch is deleted locally and remotely;
- no unintended open PRs remain.

## Stop rules

Stop immediately if:

- CI is red or pending when a phase requires green checks;
- main is not clean and synchronized;
- an unexpected file appears in the diff;
- a command fails and the reason is not understood;
- a release-blocking finding remains open;
- dedupe or conflicts are described as PyPI-published before v0.4.0 is actually published and verified;
- release, tag, PyPI, branch protection, CI, dependencies, or security settings are touched outside an explicit phase;
- a real secret or suspicious credential pattern appears.

## Current phase scope

Current branch:

- audit/record-post-audit-action-plan

Allowed files:

- docs/POST-AUDIT-ACTION-PLAN-CURRENT-MAIN.md
- CHANGELOG.md

This phase must not change code, tests, workflows, pyproject.toml, release metadata, tags, PyPI, branch protection, or dependency configuration.

## Supply-chain resolution note

GitHub Actions SHA pinning has been implemented after the original current-main action plan. CI, CodeQL, artifact upload/download, setup-python, checkout, and PyPI publishing actions are now pinned to full-length commit SHAs, with the local audit script enforcing the policy.
