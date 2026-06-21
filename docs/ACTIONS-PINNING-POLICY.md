# GitHub Actions Pinning Policy

Status: accepted policy decision.
Scope: GitHub Actions workflow references for this repository.
Current phase: policy decision only; no workflow action references are changed here.

## Decision

agent-rules-kit accepts full-length commit SHA pinning as the stricter long-term supply-chain policy for GitHub Actions.

The implementation is intentionally separated from this documentation phase. Action references must not be converted by string replacement or broad automation. Each action must preserve its full repository path, including sub-actions such as github/codeql-action/init and github/codeql-action/analyze.

## Why this policy exists

GitHub's security guidance states that pinning an action to a full-length commit SHA is currently the only way to use an action as an immutable release.

The same guidance also notes that tag-based references are more convenient and common, but tags can move or be deleted if an action repository is compromised.

This project currently uses explicit version tags for trusted actions. That is acceptable as a transitional state, not as the final strictest policy.

## Required implementation rules

A future implementation phase must:

- use a dedicated branch;
- update only workflow action references and the local audit inventory needed to verify them;
- verify each SHA belongs to the canonical action repository, not a fork;
- preserve sub-action paths exactly;
- keep workflow permissions minimal;
- run local checks before stage;
- stage exact files only;
- run a strong pre-push before push;
- verify PR checks and main checks by exact SHA;
- document the update path for future Dependabot or manual refreshes.

## Prohibited implementation shortcuts

Do not:

- rewrite action references with blind regex replacement;
- collapse sub-actions such as github/codeql-action/init into github/codeql-action;
- invent SHAs;
- copy SHAs from unofficial sources;
- combine pinning with release, PyPI, README final, dependency changes, branch protection, Scorecard, CodeQL, or product behavior;
- describe SHA pinning as a security guarantee.

## Current workflow references

Current transitional references:

- actions/checkout@v7
- actions/setup-python@v6
- github/codeql-action/init@v4
- github/codeql-action/analyze@v4
- actions/upload-artifact@v4
- actions/download-artifact@v8
- pypa/gh-action-pypi-publish@release/v1

## Release-train impact

For v0.4.0, this policy closes the decision gap.

The actual conversion to full-length SHA pinning remains a separate supply-chain implementation phase and must not be rushed into a release branch without exact repository/SHA verification and a clean Always-Green run.
