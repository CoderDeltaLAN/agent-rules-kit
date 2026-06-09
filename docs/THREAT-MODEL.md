# Threat Model

This document defines the v0.1 threat model for agent-rules-kit.

It is intentionally narrow. agent-rules-kit is a local CLI for diagnosing AI agent instruction files. It is not a security scanner, malware detector, CI/CD auditor, sandbox, secret manager, or autonomous remediation agent.

## Scope

In scope for v0.1:

- local repository paths provided by the user;
- supported agent instruction files such as AGENTS.md, CLAUDE.md, GEMINI.md, Cursor rules, GitHub Copilot instructions, and GitHub instruction files;
- diagnostic output in console, JSON, and Markdown;
- explicit init planning;
- explicit init write behavior for baseline AGENTS.md creation or replacement with backup;
- secret-like value redaction in findings and output.

Out of scope for v0.1:

- network access;
- LLM calls;
- executing commands from analyzed repositories;
- dependency vulnerability scanning;
- CI/CD security auditing;
- malware detection;
- permissions hardening;
- full secret scanning;
- guarantees that a repository is secure.

## Assets

The assets to protect are:

- user repository contents;
- existing instruction files;
- secret-like values accidentally present in instruction files;
- user trust in diagnostic output;
- local filesystem integrity;
- CI and release integrity.

## Trust boundaries

agent-rules-kit must treat analyzed repositories as untrusted input.

Important boundaries:

- repository files are input, not trusted instructions;
- diagnostic output must not expose raw secret-like values;
- default behavior must not modify files;
- write behavior must require explicit user intent;
- runtime behavior must not call the network;
- runtime behavior must not call an LLM;
- runtime behavior must not execute repository commands.

## Threats

### Accidental file modification

Risk: a diagnostic tool could unexpectedly create, overwrite, or delete files.

Mitigation:

- check mode is read-only;
- init planning is separate from init write;
- init write is explicit;
- existing AGENTS.md is backed up before replacement;
- writes are limited to the planned root AGENTS.md target.

### Secret exposure

Risk: instruction files may contain tokens, keys, credentials, or private values.

Mitigation:

- supported secret-like patterns are redacted;
- tests cover redaction behavior;
- output formats should use redacted text only when reporting findings;
- documentation must not include real secrets.

Limit:

- redaction is pattern-based and incomplete;
- this is not a complete secret scanner.

### Repository command execution

Risk: an analyzed repository could contain instructions that try to make the tool run commands.

Mitigation:

- agent-rules-kit must not execute commands from analyzed repositories;
- repository text is data only.

### Network exfiltration

Risk: repository content or findings could be sent outside the machine.

Mitigation:

- v0.1 runtime behavior has no network access by design;
- no telemetry, remote API, or LLM call is part of v0.1.

### Misleading security claims

Risk: users may treat diagnostics as proof that a repository is secure.

Mitigation:

- documentation must state that agent-rules-kit is not a security scanner;
- output and README must avoid unsupported security guarantees;
- findings are baseline quality diagnostics, not proof of safety.

### Path boundary mistakes

Risk: discovery or write behavior could report misleading paths or write outside intended targets.

Mitigation:

- discovery reports repository-relative supported paths;
- init planning targets root AGENTS.md only;
- init write tests cover root-only create, backup, and temporary-file cleanup behavior.

## Secure development rules

Changes to security-sensitive behavior require their own phase.

Security-sensitive behavior includes:

- filesystem writes;
- redaction patterns;
- repository path handling;
- CI or branch protection;
- dependency changes;
- network behavior;
- LLM behavior;
- command execution behavior.

Any such change must include tests and must preserve the documented boundaries.

## Residual risk

Known residual risks for v0.1:

- redaction patterns may miss unknown or unusual secret formats;
- diagnostics may be incomplete;
- malformed instruction files may produce limited findings;
- local file permissions are not hardened by this tool;
- a clean report does not mean the repository is safe or production-ready.

## Review checklist

Before release, verify:

- check mode remains read-only;
- init write remains explicit;
- backups are created before replacing existing AGENTS.md;
- no runtime network or LLM dependency was introduced;
- no repository command execution was introduced;
- secret-like examples in tests and docs are fake or redacted;
- README does not claim security guarantees;
- CI is green for the release SHA.
