# Product Strategy Roadmap

This document defines the product direction for agent-rules-kit after the published v0.4.0 GitHub Release and PyPI package.

It is a strategy document, not an implementation plan for a specific feature. It must not be used to claim capabilities that are not already implemented.

## Current product truth

agent-rules-kit has a published v0.4.0 GitHub Release and PyPI package line. `v0.3.0` remains the previous published GitHub Release and PyPI package baseline. The v0.4.0 release publishes the compatible `dedupe` and `conflicts` command additions plus maintenance hardening that landed after v0.3.0.

The implemented product currently supports:

- discovering supported instruction files;
- reporting discovered files through the `check` command;
- console, JSON, and Markdown output for `check`;
- explicit `init --dry-run` planning;
- explicit `init --write` behavior for root `AGENTS.md`;
- backup before replacing an existing root `AGENTS.md`;
- conservative governance diagnostics for `AIRK-GOV001` through `AIRK-GOV006`;
- structured evidence for line-based governance findings;
- pattern-based redaction for supported secret-like values in supported output paths;
- read-only `doctor` repository diagnosis output;
- read-only `budget` deterministic local size and context-pressure approximation output;
- read-only `explain` output for known governance rule IDs;
- local tests, Ruff linting, CI, release assets, PyPI publication, and documented safety boundaries.

The implemented product does not yet provide:

- governance scoring;
- cross-file consistency analysis;
- exact tokenizer-specific token accounting;
- policy profiles;
- remediation workflows;
- broad rule generation;
- repository packaging for AI prompts;
- dependency or supply-chain scanning;
- proof that a repository is safe.

The current strength is not feature breadth. The current strength is a narrow local tool with explicit boundaries and a published governance baseline.

## Product hypothesis

agent-rules-kit should evolve toward an AI Agent Instruction Governance Kit.

The product should help maintainers audit, budget, harden, normalize, and verify AI agent instruction files in professional repositories while preserving these runtime boundaries:

- local-first;
- read-only by default;
- no network calls in runtime behavior;
- no LLM calls in runtime behavior;
- no execution of commands from analyzed repositories;
- explicit user intent for any write behavior;
- conservative claims.

The product should focus on the governance quality of instruction files, not on replacing human review or generating universal agent rules.

## Competitive boundary

The product must avoid drifting into adjacent categories that are already better served by other tools.

### Repository-to-context packagers

Tools in this category package or digest a repository into AI-friendly text, context files, or prompt input.

agent-rules-kit should not compete here.

Non-goals:

- packaging a full repository into a prompt;
- producing one large AI context dump;
- optimizing an entire codebase for model ingestion;
- replacing repository summarizers or codebase digest tools.

### Context frameworks and workflow kits

Tools in this category define broader workflows, templates, skills, prompts, specs, and session conventions for AI-assisted development.

agent-rules-kit should not become a full workflow framework.

Non-goals:

- session state;
- agent skills;
- project templates;
- prompt libraries;
- personal AI operating systems;
- workflow orchestration.

### Agent rule generators

Tools in this category generate or manage agent instruction files for specific assistants.

agent-rules-kit may keep explicit init behavior, but it should not become a broad generator.

Non-goals:

- generating long agent rules by default;
- maintaining a catalog of assistant-specific rule packs;
- rewriting every supported instruction file automatically;
- claiming one universal rule format is best.

### Security scanners

agent-rules-kit can detect governance risks in instruction files, but it must not present itself as a security scanner.

Non-goals:

- proving a repository is secure;
- dependency vulnerability scanning;
- malware detection;
- CI/CD security auditing;
- complete secret scanning;
- infrastructure or permission hardening.

## Differentiated wedge

The differentiated product wedge is instruction governance.

agent-rules-kit should answer questions such as:

- Are AI agent instruction files present where expected?
- Are runtime boundaries documented clearly?
- Do instruction files contradict each other?
- Do files ask assistants to bypass review, CI, or security boundaries?
- Do files include risky guidance about secrets, network calls, LLM calls, command execution, or direct pushes?
- Are instructions too fragmented, duplicated, vague, or noisy to maintain?
- Is there a clear authority order between instruction files?
- Is the repository asking AI tools to do things that should require human confirmation?

The product should diagnose these issues with conservative findings and clear evidence. It should not make broad maturity claims.

## Product principles

1. Diagnose before generating.
2. Preserve local-first behavior.
3. Keep read-only behavior as the default.
4. Treat repository content as untrusted input.
5. Avoid network and LLM runtime dependencies.
6. Avoid command execution from analyzed repositories.
7. Prefer transparent findings over magic remediation.
8. Keep output machine-readable where useful.
9. Redact secret-like values in findings and output paths.
10. Document limits as clearly as capabilities.

## Claims policy

Allowed claims:

- local CLI;
- read-only by default;
- no runtime network behavior;
- no runtime LLM dependency;
- no execution of repository commands;
- baseline diagnostics for AI agent instruction files;
- explicit write mode for supported init behavior;
- pattern-based redaction for supported secret-like values;
- best-effort support boundary for the current GitHub Release line.

Forbidden claims:

- security scanner;
- makes a repository secure;
- complete secret scanning;
- guaranteed safety;
- guaranteed token savings;
- exact cost reduction;
- universal best practice generator;
- autonomous remediation agent;
- production maturity without defined release criteria.

Any claim that depends on measured results must be backed by tests, fixtures, benchmarks, or documented evidence.

## Roadmap

### v0.2: Governance baseline

Status: historical baseline published in v0.2.0 and hardened through the v0.2.x patch line.

Implemented scope:

- missing authority or scope diagnostics;
- missing secret-handling boundary diagnostics;
- review or CI bypass diagnostics;
- unsafe command execution diagnostics;
- runtime network, LLM, or external API dependency diagnostics;
- unsupported security or maturity claim diagnostics;
- structured finding evidence for line-based governance findings;
- console, JSON, and Markdown output through the existing `check` command.

Still non-goals for v0.2:

- automatic remediation;
- broad rewriting;
- token savings claims;
- policy profiles;
- repository-wide code analysis;
- LLM-based evaluation.

### v0.3: Local diagnosis toolkit baseline

Status: published in v0.3.0.

Implemented scope:

- read-only `doctor` repository diagnosis output;
- read-only `budget` deterministic local size and context-pressure approximation output;
- read-only `explain` output for known governance rule IDs;
- updated output and release documentation for the v0.3.0 command surface.

Still non-goals for v0.3:

- exact token accounting across providers;
- cost prediction;
- model-specific optimization promises;
- JSON output for `doctor` and `budget`.

### v0.4: Cross-file consistency lint

Goal: detect conflicts between supported instruction files.

Candidate capabilities:

- conflicting branch or PR instructions;
- conflicting test commands;
- conflicting security boundaries;
- duplicated authority statements;
- missing source of truth.

Non-goals for v0.4:

- semantic reasoning through an LLM;
- broad natural-language truth resolution;
- automatic merge of instruction files.

### v0.5: Governance profiles

Goal: provide explicit rule sets only after baseline rules have proven useful.

Candidate capabilities:

- baseline profile;
- strict profile;
- optional rule enablement;
- documented rule ids and severity meanings.

Non-goals for v0.5:

- organization compliance claims;
- external policy enforcement;
- hidden rules.

### v1.0: Defined public maturity

Goal: declare a mature public line only after criteria are met.

Candidate criteria:

- stable documented CLI behavior;
- stable JSON schema for findings;
- documented rule ids and severity semantics;
- tests for representative fixtures;
- repeated release process;
- clear support policy;
- clear compatibility and breaking-change policy;
- private vulnerability reporting path or explicit documented alternative;
- no unsupported security or maturity claims.

## Next implementation direction after v0.4.0

The next implementation phase should be justified against the current repository state, not against older strategy snapshots.

Good next candidates are narrow and evidence-backed:

- release and package smoke hardening;
- README, support, security, and strategy public-truth checks;
- supply-chain workflow additions only after dedicated evaluation phases;
- additional instruction-file discovery only when official tool documentation supports it;
- JSON output for `doctor` and `budget` in a later feature release.

Any next code phase must preserve local-first behavior, read-only default behavior, no runtime network access, no runtime LLM dependency, no execution of repository commands, and conservative claims.

## Decision record

Decision: keep product strategy as the boundary document after v0.2.

Reason:

- v0.4.0 publishes the current local instruction-governance command baseline;
- future post-v0.4.0 work should avoid broadening the tool before machine-readable output and renderer structure are improved;
- adjacent tools still cover repository packaging, context frameworks, and broad rule generation better than this project should;
- the real product wedge remains instruction governance;
- future features must be justified against this document to avoid scope drift.

The next code phase must be justified against the current repo, current docs, current tests, and current external tool behavior.
