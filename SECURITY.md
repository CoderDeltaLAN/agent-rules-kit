# Security Policy

agent-rules-kit is a local diagnostic CLI for AI agent instruction files.

It is not a security scanner, provides no security guarantees, and must not be described as making a repository secure.

## Supported versions

There is no stable supported release yet.

| Version | Status |
| --- | --- |
| 0.1.x | Pre-release development |
| < 0.1 | Not supported |

## Security boundaries

The project must preserve these boundaries:

- read-only by default;
- no network access in runtime behavior;
- no LLM dependency in runtime behavior;
- no execution of commands from analyzed repositories;
- no modification of analyzed repositories unless a future explicit write mode is intentionally designed;
- no printing of raw secrets;
- no unsupported security claims.

## Secret handling

Potential secrets must be redacted before being shown in console, JSON, Markdown, logs, or tests.

Do not commit real secrets, tokens, credentials, cookies, private keys, private URLs, or customer data.

Use fake examples only.

## Reporting a vulnerability

This repository is currently in local inception and has no public release.

Before public release, a reporting channel must be defined.

Until then, do not claim that the project has a formal vulnerability disclosure process.

## Non-goals

agent-rules-kit does not aim to:

- prove that a repository is secure;
- replace human security review;
- scan dependencies for vulnerabilities;
- validate CI/CD supply chain security;
- execute repository commands to confirm behavior;
- inspect private services, credentials, or infrastructure.

## Maintainer response

Before a public release, the maintainer must define:

- contact channel;
- expected response time;
- supported versions;
- disclosure handling;
- whether GitHub Security Advisories are enabled.

## Safe development rules

Contributors and AI assistants must follow AGENTS.md.

Any change that touches secret detection, redaction, file traversal, write behavior, symlink handling, or command execution boundaries must be treated as security-sensitive and reviewed carefully.

If a change could expose secrets, execute untrusted code, write outside the intended project root, or make exaggerated security claims, stop and escalate before implementation.
