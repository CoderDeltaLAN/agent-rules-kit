# Security and Supply-Chain Evaluation

Status: read-only evaluation record.
Scope: post-v0.3.0 main.
Branch: `security/evaluate-codeql-and-private-reporting`.

This document records a conservative security and supply-chain evaluation for agent-rules-kit.

It does not enable CodeQL, code scanning, Dependabot, private vulnerability reporting, OpenSSF Scorecard, branch protection changes, release changes, PyPI changes, or any new repository setting.

## Current security posture

agent-rules-kit is a local diagnostic CLI for AI agent instruction files.

The project already documents these boundaries:

- not a security scanner;
- no security guarantees;
- read-only by default;
- no runtime network access;
- no runtime LLM dependency;
- no execution of commands from analyzed repositories;
- supported secret-like values must be redacted in supported output paths.

The current GitHub Actions workflows already use explicit workflow permissions:

- CI workflow: `contents: read`;
- PyPI publish workflow build job: `contents: read`;
- PyPI publish workflow publish job: `contents: read` and `id-token: write`.

The publish job needs `id-token: write` for PyPI Trusted Publishing. No static PyPI token, username, or password is used.

## Private vulnerability reporting

Private vulnerability reporting has since been manually enabled and documented for this repository.

Current documentation:

- `SECURITY.md` states that private vulnerability reporting is enabled;
- `docs/PRIVATE-VULNERABILITY-REPORTING.md` records the manual GitHub UI verification evidence and limits;
- the setting must still be treated as a disclosure channel, not a security guarantee.

Historical note: this document was originally created as a read-only evaluation before private vulnerability reporting was enabled. That older disabled-state wording is no longer current.

## CodeQL and code scanning

Code scanning can surface security vulnerabilities and coding errors in repository code. CodeQL is GitHub's code analysis engine for code scanning.

Potential value for this project:

- additional signal for Python security and code-quality issues;
- visibility through GitHub Security and quality views;
- useful public-repo hygiene signal for portfolio credibility.

Risks and constraints:

- it adds another GitHub Actions path and can create noisy findings;
- it should not be described as proving repository safety;
- it should not replace the existing required `local-checks / Python 3.12` gate;
- it should not be enabled blindly in this evaluation branch.

Decision for this phase:

- do not add a CodeQL workflow here;
- record CodeQL as a reasonable future hardening candidate;
- if enabled later, use a dedicated branch such as `security/add-codeql-analysis`;
- keep it separate from private vulnerability reporting and Dependabot configuration.

Recommended future CodeQL phase boundaries:

- add only CodeQL/code scanning configuration;
- preserve existing CI required check name;
- verify CodeQL results on pull request and main;
- document that CodeQL is an additional signal, not a guarantee.

## Dependabot alerts and dependency review

Dependabot alerts help identify known vulnerable dependencies when the dependency graph can detect affected packages.

Current repository setting record:

- dependency graph is manually verified as enabled;
- Dependabot alerts are manually verified as enabled;
- Dependabot security updates are manually verified as enabled;
- Dependabot version updates are deferred because no `.github/dependabot.yml` exists in this phase;
- automatic dependency submission is deferred;
- malware alerts and grouped security updates are not claimed as enabled in this record unless separately verified by a later UI check.

See `docs/DEPENDABOT-DEPENDENCY-GRAPH.md` for the dedicated settings record.

Risks and constraints:

- alerts may not cover every issue;
- only GitHub-reviewed advisories trigger alerts;
- dependency graph coverage depends on supported ecosystems and manifest visibility;
- this does not make agent-rules-kit a dependency vulnerability scanner;
- Dependabot-created PRs still require normal Always-Green review, checks, CI, and exact-head merge discipline.

Recommended future Dependabot phase boundaries:

- inspect and document the existing Dependabot rule before claiming it as a control;
- decide whether to add `.github/dependabot.yml` for version updates in a separate branch;
- do not combine version-update automation with CodeQL, release, or security-policy changes.

## OpenSSF Scorecard

OpenSSF Scorecard can provide an external supply-chain hygiene signal.

Potential value:

- independent security posture feedback;
- useful portfolio signal if interpreted honestly;
- may surface action pinning, branch protection, token permissions, and dependency update gaps.

Risks and constraints:

- scores are not proof of security;
- action pinning recommendations may create maintenance overhead;
- adopting Scorecard should not force rushed changes to CI, release, or branch protection.

Decision for this phase:

- do not add Scorecard here;
- record it as a later evaluation candidate after CodeQL and Dependabot decisions.

## GitHub Actions pinning policy

The workflows currently use version tags such as `actions/checkout@v6`, `actions/setup-python@v6`, `actions/upload-artifact@v4`, `actions/download-artifact@v5`, and `pypa/gh-action-pypi-publish@release/v1`.

Potential stronger policy:

- pin third-party actions by full commit SHA;
- document how pinned actions are reviewed and updated.

Risks and constraints:

- full SHA pinning improves immutability but increases update burden;
- a partial or stale pinning policy can create false confidence;
- changing action references must be its own CI/supply-chain phase.

Decision for this phase:

- do not change action references here;
- keep current explicit permissions;
- evaluate action pinning in a separate phase if the maintainer wants stricter supply-chain hardening.

## Decision

This phase is documentation-only evaluation.

Recommended next hardening order:

1. `security/add-codeql-analysis` if the maintainer wants an additional code-scanning signal.
2. `security/verify-private-vulnerability-reporting-setting` if the maintainer wants to enable and document private reporting.
3. `security/evaluate-dependabot-alerts-and-updates` for dependency alert and update policy.
4. `security/evaluate-action-pinning-policy` for GitHub Actions pinning.

None of these future phases should be mixed with release, PyPI, branch protection, runtime behavior, or product feature changes.
