# Support Policy

agent-rules-kit is currently in local inception and has no public release.

There is no formal support channel yet.

## Current status

This project is pre-release software.

At this stage:

- no public release exists;
- no stability guarantee exists;
- no support response time is promised;
- no production readiness is claimed;
- no security guarantees are provided.

## What this project is

agent-rules-kit is a local Python CLI for diagnosing baseline quality of AI agent instruction files in repositories.

It is not a security scanner.

It is intended to help detect missing, weak, duplicated, or risky instruction patterns.

## What this project is not

agent-rules-kit is not:

- a security scanner;
- a dependency vulnerability scanner;
- a CI/CD security auditor;
- a universal AI agent framework;
- a tool that executes commands from analyzed repositories;
- a guarantee that a repository is safe.

## Before opening an issue

Before reporting a problem, check:

- README.md for project purpose and limits;
- AGENTS.md for workflow and AI assistant rules;
- SECURITY.md for security boundaries and reporting limits;
- CONTRIBUTING.md for contribution rules;
- CHANGELOG.md for unreleased changes.

## Good support requests

Good requests include:

- clear description of the problem;
- expected behavior;
- actual behavior;
- reproduction steps;
- relevant command output;
- operating system and Python version;
- whether the issue affects correctness, safety, documentation, or usability.

## Unsupported requests

The following requests are out of scope unless a maintainer explicitly approves a design change first:

- adding network behavior;
- adding LLM runtime behavior;
- executing commands from analyzed repositories;
- claiming the tool makes repositories secure;
- bypassing checks;
- hiding known failures;
- adding secrets or private data to examples;
- making broad rewrites without a narrow reviewable plan.

## Security reports

Security-sensitive reports should follow SECURITY.md.

Before public release, the maintainer must define whether GitHub Security Advisories are enabled and what contact channel should be used.

Until that is defined, do not claim that this project has a formal vulnerability disclosure process.

## Maintainer note

Support must remain aligned with the project boundaries.

A request should not be accepted just because it is useful. It should be accepted only if it keeps the project local-first, auditable, testable, maintainable, and honest about its limits.
