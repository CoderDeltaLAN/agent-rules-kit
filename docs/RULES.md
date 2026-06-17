# Governance Rules Reference

This document describes the current governance finding rules on `main`.

`v0.2.0` introduced the governance rule set. Current `main` may include unreleased fixes and coverage improvements after that tag.

The rules are conservative, deterministic, pattern-based diagnostics for supported AI agent instruction files. They are designed to flag review-worthy instruction patterns, not to prove that a repository is safe, compliant, production-ready, or free of secrets.

## Scope

These rules apply to supported instruction files discovered by `agent-rules-kit`, such as:

- `AGENTS.md`;
- `CLAUDE.md`;
- `.claude/CLAUDE.md`;
- `GEMINI.md`;
- `.cursor/rules/*.mdc`;
- `.github/copilot-instructions.md`;
- `.github/instructions/*`.

Governance findings do not execute repository commands, call external APIs, call LLMs, inspect private infrastructure, or validate branch protection.

## Stable rule order

Current `main` evaluates governance findings in this order:

1. `AIRK-SYS001` — unreadable supported instruction file.
2. `AIRK-GOV006` — unsupported security or maturity claim.
3. `AIRK-GOV003` — review or CI bypass guidance.
4. `AIRK-GOV004` — unsafe command execution guidance.
5. `AIRK-GOV005` — runtime network or LLM dependency guidance.
6. `AIRK-GOV002` — missing secret-handling boundary.
7. `AIRK-GOV001` — missing instruction scope or authority.

Future rule-order changes must remain deterministic, documented, fixture-backed, and conservative.

## Rule reference

### AIRK-SYS001 — Unreadable instruction file

Flags supported instruction files that cannot be analyzed as UTF-8.

Purpose:

- prevent supported instruction files from being discovered but silently skipped;
- make encoding problems visible in console, JSON, and Markdown output;
- avoid printing raw undecodable bytes as evidence.

This finding reports the repository-relative instruction file path and does not include line, column, or evidence fields.

### AIRK-GOV006 — Unsupported security or maturity claim

Severity: `warning`.

Purpose:
Flags instruction text that appears to claim unsupported safety, security, production readiness, completeness, or maturity.

Examples of risky language:

- guaranteed security;
- guaranteed safety;
- makes the repository secure;
- complete secret scanning;
- production-ready without criteria;
- enterprise-grade as a maturity claim.

Evidence:
Repository-relative path and line number when available.

Why it matters:
Overstated maturity claims can mislead maintainers, users, auditors, or AI assistants into trusting a repository more than the evidence supports.

False positives:
A file may discuss security limits responsibly and still contain words such as security, safe, production, or guarantee. Maintainers should review the surrounding context.

False negatives:
The rule does not understand every possible maturity claim or every form of implied overconfidence.

Non-goals:

- banning all maturity language;
- judging real organizational compliance;
- proving that a claim is false;
- replacing human release review.

### AIRK-GOV003 — Review or CI bypass guidance

Severity: `warning`.

Purpose:
Flags instruction text that appears to encourage bypassing review, CI, PRs, branch protection, or safe integration flow.

Examples of risky language:

- direct push to `main`;
- skip CI;
- ignore failing tests;
- force push as normal workflow;
- merge without review;
- bypass branch protection;
- commit secrets for debugging.

Evidence:
Repository-relative path and line number when available.

Why it matters:
Agent instructions can normalize unsafe integration habits. A repository may look protected while its own instructions tell assistants or maintainers to bypass the protection.

False positives:
Emergency procedures may mention bypass-like language while still requiring explicit human approval and audit evidence.

False negatives:
The rule does not inspect real GitHub settings, CI configuration, or branch protection.

Non-goals:

- auditing GitHub branch protection;
- determining whether CI is actually enforced;
- blocking documented emergency procedures with clear human approval.

### AIRK-GOV004 — Unsafe command execution guidance

Severity: `warning`.

Purpose:
Flags instruction text that appears to ask assistants to run destructive, privileged, broad, or externally fetched commands without an explicit confirmation boundary.

Examples of risky language:

- destructive shell commands;
- broad deletion;
- wide `chmod` or `chown`;
- `sudo` as a normal instruction;
- install or uninstall commands without confirmation;
- executing downloaded scripts;
- treating repository scripts as trusted instructions without review.

Evidence:
Repository-relative path and line number when available.

Why it matters:
Agent instructions are often copied into automated or semi-automated workflows. Unsafe command guidance can turn a documentation problem into local system damage.

False positives:
A safe runbook may mention dangerous commands as examples, warnings, or blocked actions.

False negatives:
The rule is not a full shell safety analyzer and does not evaluate every possible command form.

Non-goals:

- blocking all commands;
- proving whether a command is safe in every environment;
- replacing human confirmation for risky operations.

### AIRK-GOV005 — Runtime network or LLM dependency guidance

Severity: `warning`.

Purpose:
Flags instruction text that appears to require sending repository content to remote services, calling LLMs, using API tokens, or relying on network behavior in a way that conflicts with local-first boundaries.

Examples of risky language:

- upload repository contents to an external service;
- call a remote LLM for validation;
- use an API token to analyze files;
- send instruction files to a third-party endpoint.

Evidence:
Repository-relative path and line number when available.

Why it matters:
`agent-rules-kit` is intentionally local-first. Instructions that normalize remote analysis can create privacy, confidentiality, cost, and reproducibility risks.

False positives:
A repository may legitimately document optional hosted tools while keeping the diagnostic workflow local and explicit.

False negatives:
The rule does not detect every external service, integration, webhook, or hosted assistant workflow.

Non-goals:

- prohibiting developers from using hosted assistants generally;
- enforcing network isolation;
- replacing privacy review.

### AIRK-GOV002 — Missing secret-handling boundary

Severity: `warning`.

Purpose:
Flags instruction files that do not provide visible guidance about secrets, tokens, credentials, private URLs, customer data, or sensitive values.

Examples of missing guidance:

- no mention of secrets;
- no mention of tokens or credentials;
- no instruction to avoid committing sensitive values;
- no instruction to avoid printing sensitive values.

Evidence:
Repository-relative path.

Why it matters:
Agent instruction files often guide tools that read, rewrite, summarize, or execute repository tasks. Missing secret boundaries increase the chance that sensitive data is copied, logged, committed, or exposed.

False positives:
A repository may keep secret policy in another document that the instruction file references indirectly or not at all.

False negatives:
The rule does not prove that secret handling is complete, correct, enforced, or followed.

Non-goals:

- full secret scanning;
- proving that a repository contains no secrets;
- validating actual secret policy compliance.

### AIRK-GOV001 — Missing instruction scope or authority

Severity: `warning`.

Purpose:
Flags instruction files that do not clearly state their scope, authority, or relationship to other project instructions.

Examples of missing guidance:

- no clear statement of what files, directories, assistants, or repository areas the instruction applies to;
- no authority relationship when multiple instruction files exist;
- no mention of higher-priority project instructions.

Evidence:
Repository-relative path.

Why it matters:
Ambiguous instruction scope can cause assistants or maintainers to apply the wrong rules to the wrong files, especially in repositories with more than one agent instruction file.

False positives:
A small repository may have a simple instruction file whose scope is obvious to the maintainer but not explicit in the text.

False negatives:
The rule does not resolve cross-file conflicts or infer the correct authority hierarchy.

Non-goals:

- deciding the correct authority hierarchy automatically;
- rewriting instruction files;
- resolving cross-file conflicts.

## Output behavior

Findings may appear in console, JSON, and Markdown output.

Supported output must keep findings conservative and must not expose raw secret-like values in finding messages, paths, or evidence payloads.

A clean report means only that the implemented checks did not find a supported issue. It is not proof of safety, completeness, maturity, or production readiness.

## Maintainer guidance

Treat findings as review prompts.

Before changing rule behavior, maintainers should update tests, fixtures, documentation, and output examples together. Rule changes should remain deterministic, local-first, read-only by default, and free of unsupported security claims.
