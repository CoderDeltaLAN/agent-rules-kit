# Dependency Graph and Dependabot Settings

Status: manual GitHub UI verification record.
Scope: post-v0.3.0 maintenance hardening.
Branch: `security/evaluate-dependabot-dependency-graph`; updated by `security/verify-dependabot-settings`.
Date: 2026-06-19.

This document records GitHub repository security settings that affect dependency visibility and Dependabot behavior for `agent-rules-kit`.

It is not a security guarantee. It does not make `agent-rules-kit` a dependency scanner, vulnerability scanner, or repository security product.

## Evidence rules

Evidence is ranked in this record as follows:

1. Official GitHub documentation for feature behavior and supported API endpoints.
2. Read-only terminal/API probes against the live repository.
3. GitHub Advanced Security UI evidence when no clear API field exposes a setting.
4. Trusted external sources only as secondary context, never as the source of truth for this repository state.

In the GitHub `Settings` -> `Advanced Security` page:

- a `Disable` button means the setting is currently enabled;
- an `Enable` button means the setting is currently disabled;
- a `Disabled` dropdown value means the setting is currently disabled.

The GitHub REST and GraphQL APIs are preferred when they expose clear repository state. The GitHub UI remains the evidence source for settings that were visible in Advanced Security but not clearly exposed by the available API probes in this phase.

Follow-up verification notes from `security/verify-dependabot-settings`:

- `GET /repos/{owner}/{repo}/vulnerability-alerts` returned HTTP `204`, matching GitHub's documented enabled response for vulnerability/dependency alerts;
- `GET /repos/{owner}/{repo}/automated-security-fixes` returned `enabled: true` and `paused: false`;
- `GET /repos/{owner}/{repo}/private-vulnerability-reporting` returned `enabled: true`;
- GraphQL exposed dependency/vulnerability alert fields, including `hasVulnerabilityAlertsEnabled`;
- `GET /repos/{owner}/{repo}/dependabot/alerts` returned an empty list, so no open Dependabot alerts were visible at verification time;
- no REST or GraphQL field was found in this phase that clearly exposes the Grouped security updates or Dependabot malware alerts toggle state;
- the GitHub Advanced Security UI screenshots are therefore the evidence source for the malware alerts and grouped security updates claims;
- no `.github/dependabot.yml` exists, so Dependabot version updates remain not configured by repository file.

## Current repository setting record

| Setting | Status recorded | Evidence | Notes |
| --- | --- | --- | --- |
| Private vulnerability reporting | Enabled | Advanced Security UI showed `Disable` | Documented separately in `docs/PRIVATE-VULNERABILITY-REPORTING.md`. |
| Dependency graph | Enabled | Advanced Security UI showed `Disable` | Required baseline for dependency visibility and Dependabot alerting. |
| Automatic dependency submission | Disabled / deferred | Advanced Security UI showed `Disabled` | Deferred because the current project has only `pyproject.toml` as a dependency manifest and no lockfile or complex build-time dependency submission need. |
| Dependabot alerts | Enabled | Advanced Security UI showed `Disable` | Alerts depend on dependency graph coverage and GitHub Advisory Database data. |
| Dependabot rules | Present, not fully evaluated | Advanced Security UI showed `1 rule enabled` | This record does not claim what the rule does because the rule content was not inspected. |
| Dependabot malware alerts | Enabled | Advanced Security UI showed `Disable` in the follow-up verification phase | Alerts when malware is detected in dependencies; this is a repository-maintenance signal, not a product guarantee. |
| Dependabot security updates | Enabled | Advanced Security UI showed `Disable` | May open security PRs when Dependabot alerts have available patches. |
| Grouped security updates | Enabled | Advanced Security UI showed `Disable` in the follow-up verification phase | Groups available Dependabot alert fixes into one pull request per package manager and manifest directory, unless overridden by rules. |
| Dependabot version updates | Disabled / not configured | Advanced Security UI showed `Enable`; no `.github/dependabot.yml` exists | Version updates require a committed `.github/dependabot.yml` and should be handled in a dedicated phase. |
| CodeQL analysis | Enabled | Advanced Security UI showed CodeQL advanced setup and recent scan | Additional signal only; not a guarantee. |
| Copilot Autofix | Enabled as suggestion source | Advanced Security UI showed `On` | Suggestions must not bypass branch, diff, tests, CI, or PR review. |
| Secret Protection | Enabled | Advanced Security UI showed `Disable` | Keep active; this record does not configure custom patterns. |
| Push protection | Enabled | Advanced Security UI showed `Disable` | Keep active; bypasses, if any, require human review. |

## Dependency graph boundary

The dependency graph is useful for identifying declared dependencies from supported manifest and lock files and for supporting dependency review and Dependabot alerts.

For this repository, the only dependency manifest found during the phase was:

- `pyproject.toml`

There is no lockfile in the repository in this phase.

## Dependabot alerts and security updates boundary

Dependabot alerts and security updates are useful repository-maintenance signals.

They do not prove that dependencies are safe, complete, current, or free of vulnerabilities. They also do not change the runtime product boundary:

- no runtime network access;
- no runtime LLM dependency;
- no execution of commands from analyzed repositories;
- no dependency vulnerability scanning feature in `agent-rules-kit` itself.

Dependabot security updates may open pull requests for vulnerable dependencies with available patches. Those pull requests must follow the normal Always-Green workflow: branch, diff review, checks, PR, CI, and merge by exact head SHA.

## Deferred Dependabot version updates

Dependabot version updates are deliberately deferred in this phase.

Reason: version updates are enabled by committing a `.github/dependabot.yml` file, and they can open normal update PRs even when no vulnerability exists. That is useful, but it is a separate supply-chain maintenance phase, not part of this settings-record phase.

Expected future branch if accepted:

- `supply-chain/add-dependabot-version-updates`

## Deferred automatic dependency submission

Automatic dependency submission remains deferred.

Current rationale:

- simple Python CLI;
- no runtime dependencies;
- no lockfile currently present;
- no complex build-time dependency graph that needs extra submission data.

Re-evaluate this if the project later adds a lockfile, additional build tooling, runtime dependencies, or a release process that needs richer SBOM/dependency evidence.

## Review triggers

Update this record when:

- `.github/dependabot.yml` is added;
- a lockfile is introduced;
- runtime dependencies are added;
- Dependabot malware alerts, grouped security updates, or Dependabot version updates change state;
- Dependabot rules are opened and documented;
- GitHub changes the Advanced Security UI or API fields used as evidence;
- the release process starts relying on SBOM or dependency submission evidence.
