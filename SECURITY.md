# Security Policy

agent-rules-kit is a local diagnostic CLI for AI agent instruction files.

It is not a security scanner, provides no security guarantees, and must not be described as making a repository secure.

## Supported versions

There is no stable supported release yet. The `0.1.x` line is a pre-release support boundary, not a stability guarantee.

| Version | Status |
| --- | --- |
| 0.1.x | Pre-release / best-effort security fixes |
| < 0.1 | Not supported |

## Security boundaries

The project must preserve these boundaries:

- read-only by default;
- no network access in runtime behavior;
- no LLM dependency in runtime behavior;
- no execution of commands from analyzed repositories;
- no unsupported security claims;
- no printing of raw secrets;
- no file modification during `check`;
- no file modification during `init --dry-run`;
- file modification only through explicit `init --write` user intent;
- existing root `AGENTS.md` must be backed up before replacement.

## Secret handling

Potential secrets must be redacted before being shown in console, JSON, Markdown, logs, or tests.

Do not commit real secrets, tokens, credentials, cookies, private keys, private URLs, or customer data.

Use fake examples only.

## Reporting a vulnerability

This repository is public and has no stable release yet.

Preferred sensitive-reporting path: use GitHub Security Advisories or GitHub private vulnerability reporting when available to the maintainer.

If a sensitive issue cannot be reported privately through GitHub, do not publish secrets, exploit details, private URLs, customer data, or sensitive repository contents. Open only a minimal public issue requesting a private contact path.

For non-sensitive security boundary issues, open a GitHub issue with a minimal reproduction.

## Non-goals

agent-rules-kit does not aim to:

- prove that a repository is secure;
- replace human security review;
- scan dependencies for vulnerabilities;
- validate CI/CD supply chain security;
- execute repository commands to confirm behavior;
- inspect private services, credentials, or infrastructure;
- provide complete secret scanning.

## Maintainer response

Security response is best-effort for pre-release `0.1.x`. There is no commercial SLA or guaranteed response time.

Before any stable release, the maintainer must define:

- supported versions;
- expected response time;
- disclosure handling;
- whether GitHub Security Advisories or private vulnerability reporting are enabled.

## Safe development rules

Contributors and AI assistants must follow AGENTS.md.

Any change that touches secret detection, redaction, file traversal, write behavior, symlink handling, or command execution boundaries must be treated as security-sensitive and reviewed carefully.

If a change could expose secrets, execute untrusted code, write outside the intended project root, or make exaggerated security claims, stop and escalate before implementation.
