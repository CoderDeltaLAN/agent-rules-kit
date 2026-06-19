# OpenSSF Scorecard Evaluation

Status: read-only evaluation record.
Scope: post-v0.3.0 maintenance hardening.
Branch: `security/evaluate-openssf-scorecard`.
Date: 2026-06-19.

This document records the OpenSSF Scorecard decision for `agent-rules-kit`.

It does not add an OpenSSF Scorecard workflow, badge, required status check, GitHub setting, release change, PyPI change, branch protection change, dependency automation, or runtime behavior change.

## Local repository state

Current workflow files in this phase:

- `.github/workflows/ci.yml`;
- `.github/workflows/codeql.yml`;
- `.github/workflows/publish-pypi.yml`.

No `.github/workflows/scorecard.yml`, `.github/workflows/scorecards.yml`, or `.github/workflows/scorecard-analysis.yml` file exists in this phase.

## Official documentation findings

OpenSSF Scorecard Action is the official GitHub Action for OpenSSF Scorecard.

Current operational constraints verified during this phase:

- the action is free for public repositories;
- the supported GitHub triggers are `push` and `schedule` on the default branch;
- `pull_request` and `workflow_dispatch` triggers are experimental;
- running Scorecard Action on fork repositories is not supported;
- publishing results requires `id-token: write`;
- publishing results has workflow restrictions, including no top-level workflow `env` or `defaults`, no workflow-level write permissions, and `id-token: write` only on the Scorecard job.

The official Scorecard checks documentation also states that checks are continually changing. Therefore, Scorecard output must be treated as an external supply-chain hygiene signal, not as a stable security guarantee.

## Value for this repository

Potential value:

- external supply-chain hygiene feedback;
- detection pressure for branch protection, CI tests, code review, dangerous workflow patterns, dependency update posture, and pinned dependency posture;
- public portfolio signal if interpreted honestly and not overclaimed;
- additional feedback loop before v0.3.1 or v0.4.0 changes.

## Risks and limits

Scorecard must not be treated as proof that `agent-rules-kit` is secure.

Known limits for this repository:

- the project is maintained as a solo-maintainer repository, so Scorecard code-review expectations may not map cleanly to the current governance profile;
- classic branch protection may not be fully reflected without broader token access, and this phase must not add an admin PAT or secret only to improve a score;
- current GitHub Actions references are version-tag based, not full-SHA pinned, so Scorecard may flag pinning posture;
- enabling Scorecard with `publish_results: true` would publish results and require OIDC permissions;
- adding SARIF/code scanning output would create another GitHub Security signal path that must be reviewed calmly;
- adding a README badge before real results are reviewed would create a premature quality claim.

## Decision

Do not add a Scorecard workflow in this phase.

Record Scorecard as a reasonable future hardening candidate, but keep it separate from:

- CodeQL;
- Dependabot;
- GitHub Actions pinning;
- branch protection;
- release preparation;
- PyPI publishing;
- runtime product features.

Recommended future branch if accepted:

- `security/add-openssf-scorecard-workflow`

Recommended future workflow boundaries if accepted:

- use `push` on `main` and a weekly `schedule`;
- avoid `pull_request` and `workflow_dispatch` unless a later phase explicitly accepts their experimental status;
- keep the workflow separate from CI and CodeQL required checks;
- do not make Scorecard a required status check at first;
- do not add a README badge until the first result is reviewed and the wording is honest;
- do not add an admin PAT or any repository secret only to improve Scorecard visibility;
- keep permissions minimal and isolated to the Scorecard job;
- document any result honestly, including expected solo-maintainer or action-pinning limitations.

## Review triggers

Revisit this evaluation when:

- a Scorecard workflow is proposed;
- OpenSSF Scorecard Action changes supported triggers or publishing requirements;
- repository rules replace or supplement classic branch protection;
- GitHub Actions pinning policy changes;
- README badges are considered;
- branch protection, required checks, or maintainer model changes.
