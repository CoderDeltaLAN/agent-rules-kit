<a id="readme-top"></a>

<p align="center">
  <img
    width="100%"
    src="https://capsule-render.vercel.app/api?type=waving&height=220&section=header&color=0:000000,42:111827,72:d4af37,100:000000&text=agent-rules-kit&fontColor=ffffff&fontSize=50&fontAlign=50&fontAlignY=38&desc=Local%20CLI%20%C2%B7%20AI%20agent%20instruction%20diagnostics%20%C2%B7%20read-only%20by%20default&descAlign=50&descAlignY=62&animation=twinkling"
    alt="agent-rules-kit banner"
  />
</p>

<h1 align="center">agent-rules-kit</h1>

<p align="center">
  <strong>Local read-only Python CLI for diagnosing AGENTS.md, CLAUDE.md, GEMINI.md, Cursor rules, GitHub Copilot instructions, and other AI agent instruction files in repositories.</strong>
</p>

<p align="center">
  <a href="https://github.com/CoderDeltaLAN/agent-rules-kit/actions/workflows/ci.yml">
    <img alt="CI" src="https://github.com/CoderDeltaLAN/agent-rules-kit/actions/workflows/ci.yml/badge.svg?branch=main&label=CI" />
  </a>
  <img alt="Python 3.12" src="https://img.shields.io/badge/Python-3.12-111827?logo=python&logoColor=white" />
  <img alt="Local CLI" src="https://img.shields.io/badge/Runtime-local%20CLI-d4af37" />
  <img alt="Read-only by default" src="https://img.shields.io/badge/Default-read--only-0f766e" />
  <img alt="No LLM" src="https://img.shields.io/badge/LLM-none-5a0f0f" />
  <img alt="No network" src="https://img.shields.io/badge/Network-none-111827" />
  <img alt="License MIT" src="https://img.shields.io/badge/License-MIT-d4af37" />
</p>

<p align="center">
  <a href="https://www.paypal.com/donate/?hosted_button_id=YVENCBNCZWVPW">
    <img alt="Support with PayPal" src="https://img.shields.io/badge/Support-PayPal-003087?style=for-the-badge&logo=paypal&logoColor=white&labelColor=050505" />
  </a>
</p>

<p align="center">
  <a href="#screenshots">Screenshots</a>
  ·
  <a href="#overview">Overview</a>
  ·
  <a href="#installation">Installation</a>
  ·
  <a href="#commands">Commands</a>
  ·
  <a href="#governance-findings">Governance Findings</a>
  ·
  <a href="#safety-boundary">Safety Boundary</a>
  ·
  <a href="#quality-gates">Quality Gates</a>
  ·
  <a href="#development-status">Development Status</a>
  ·
  <a href="#maintainer-workflow">Maintainer Workflow</a>
  ·
  <a href="#support">Support</a>
</p>

---

## Screenshots

### Help and repository check

<p align="center">
  <img
    src="docs/screenshots/readme/agent-rules-kit-help-check.png"
    alt="Terminal screenshot showing agent-rules-kit help output and a repository check detecting AGENTS.md"
    width="100%"
  />
</p>

### JSON and Markdown output formats

<p align="center">
  <img
    src="docs/screenshots/readme/agent-rules-kit-output-formats.png"
    alt="Terminal screenshot showing agent-rules-kit check output in JSON and Markdown formats"
    width="100%"
  />
</p>

### Explicit init behavior

<p align="center">
  <img
    src="docs/screenshots/readme/agent-rules-kit-init-safety.png"
    alt="Terminal screenshot showing init dry-run, explicit write, and backup behavior"
    width="100%"
  />
</p>

---

## Overview

`agent-rules-kit` is a local, read-only diagnostic CLI for repositories that use AI coding agents or assistant-specific instruction files.

It helps developers inspect `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Cursor rules, GitHub Copilot instructions, and GitHub instruction files without network calls, LLM calls, or repository command execution.

It focuses on files such as:

- `AGENTS.md`
- `CLAUDE.md`
- `.claude/CLAUDE.md`
- `GEMINI.md`
- `.cursor/rules/*.mdc`
- `.github/copilot-instructions.md`
- `.github/instructions/*`

The project is positioned as a doctor/lint tool for agent instruction files.

It is not:

- a universal instruction generator;
- a security scanner;
- an LLM agent;
- a repository automation bot;
- a CI/CD security auditor;
- a dependency vulnerability scanner.

The default behavior is read-only.

---

## What This Project Does

Current `main` prepares the `v0.2.1` patch release metadata after the published `v0.2.0` baseline and post-release fixes.

The implemented behavior includes:

- discovers supported AI agent instruction files;
- reports repository-relative paths;
- supports console, JSON, and Markdown output;
- provides `init --dry-run` for planning baseline instruction files;
- provides explicit `init --write` behavior for creating or replacing root `AGENTS.md`;
- backs up existing root `AGENTS.md` before replacement;
- redacts supported secret-like values in supported output, including finding messages, paths, and evidence payloads;
- avoids network calls;
- avoids LLM calls;
- avoids executing commands from analyzed repositories.

Governance diagnostics were introduced in `v0.2.0` and have received post-release fixes on `main`.

These diagnostics are heuristic findings for instruction-file governance. They are meant to flag review-worthy instruction patterns, not to prove that a repository is safe.

---

## Governance Findings

Current `main` evaluates the following governance finding rules, in stable evaluation order:

| Rule | Severity | Purpose |
| --- | --- | --- |
| `AIRK-SYS001` | `warning` | Flags supported instruction files that cannot be analyzed as UTF-8. |
| `AIRK-SYS002` | `warning` | Flags supported instruction file paths that are symlinks and are not analyzed. |
| `AIRK-GOV006` | `warning` | Flags unsupported security, production-readiness, or maturity claims. |
| `AIRK-GOV003` | `warning` | Flags guidance that appears to bypass review, CI, PRs, or safe integration. |
| `AIRK-GOV004` | `warning` | Flags unsafe command execution guidance without an explicit confirmation boundary. |
| `AIRK-GOV005` | `warning` | Flags runtime network, LLM, or external API dependency guidance that conflicts with local-first boundaries. |
| `AIRK-GOV002` | `warning` | Flags missing secret-handling boundaries. |
| `AIRK-GOV001` | `warning` | Flags missing instruction scope or authority. |

Governance findings are intentionally conservative and pattern-based. They may produce false positives or false negatives, and they are not a substitute for maintainer review.

The `v0.2.0` GitHub Release introduced this governance rule set. Current `main` may include unreleased fixes and coverage improvements after that tag.

For detailed rule purpose, evidence, limits, and false-positive notes, see `docs/RULES.md`.

For CLI output examples in console, JSON, and Markdown formats, see `docs/OUTPUTS.md`.

---

## What This Project Does Not Do

`agent-rules-kit` does not claim to make a repository secure.

It does not:

- prove that a repository is safe;
- scan dependencies for vulnerabilities;
- execute repository commands;
- inspect private infrastructure;
- call external APIs;
- call an LLM;
- modify files during `check`;
- modify files during `init --dry-run`;
- provide complete secret scanning;
- replace human review.

A clean report means only that the implemented checks did not find a supported issue. It is not proof of safety, completeness, or production readiness.

---

## Installation

`v0.2.1` is the next GitHub Release line being prepared from current `main`.

This project is not published to PyPI yet.

### Normal CLI use

Requirements for using the released CLI:

- Python 3.12 or newer;
- a Python virtual environment;
- the wheel artifact from the GitHub Release.

After the `v0.2.1` GitHub Release is published, download the wheel from that release and install it in a virtual environment:

    python -m venv .venv
    .venv/bin/python -m pip install ./agent_rules_kit-0.2.1-py3-none-any.whl
    .venv/bin/agent-rules-kit --version
    .venv/bin/agent-rules-kit check /path/to/repository --format console

Normal CLI use does not require Ruff or any development dependency.

### Development from source

Requirements for working on the repository and running local checks:

- Python 3.12 or newer;
- a Python virtual environment;
- editable install with development dependencies.

Set up a local development environment from the source tree:

    python -m venv .venv
    .venv/bin/python -m pip install -e '.[dev]'
    PATH="$PWD/.venv/bin:$PATH" ./scripts/check.sh

The development dependency group installs tools used by local checks, including Ruff. Installing only a system `ruff` binary is not enough for `./scripts/check.sh` if the active Python cannot import the `ruff` module.

The source tree can also be used directly for quick CLI inspection:

    PYTHONPATH=src python -m agent_rules_kit.cli --help

---

## Commands

### Check a repository

Installed CLI usage:

    .venv/bin/agent-rules-kit check /path/to/repository --format console

Source-tree development usage:

    PYTHONPATH=src python -m agent_rules_kit.cli check tests/fixtures/repositories/single-agent

Example console output:

    agent-rules-kit check: tests/fixtures/repositories/single-agent
    Found 1 supported instruction file(s):
    - AGENTS.md [agents]

### JSON output

Installed CLI usage:

    .venv/bin/agent-rules-kit check /path/to/repository --format json

Source-tree development usage:

    PYTHONPATH=src python -m agent_rules_kit.cli check tests/fixtures/repositories/single-agent --format json

### Markdown output

Installed CLI usage:

    .venv/bin/agent-rules-kit check /path/to/repository --format markdown

Source-tree development usage:

    PYTHONPATH=src python -m agent_rules_kit.cli check tests/fixtures/repositories/single-agent --format markdown

### Init dry-run

`init --dry-run` shows what would happen without writing files:

    PYTHONPATH=src python -m agent_rules_kit.cli init /path/to/repo --dry-run

Example behavior:

    Mode: dry-run
    No files will be modified.
    Planned file actions:
    - AGENTS.md [create] - baseline agent instruction file would be created

### Init write

`init --write` must be requested explicitly:

    PYTHONPATH=src python -m agent_rules_kit.cli init /path/to/repo --write

If root `AGENTS.md` already exists, it is backed up before replacement:

    AGENTS.md.agent-rules-kit.bak

---

## Output Formats

Supported `check` formats:

| Format | Purpose |
| --- | --- |
| `console` | Human-readable terminal output |
| `json` | Machine-readable output |
| `markdown` | Markdown report output |

The output format is selected with:

    --format console
    --format json
    --format markdown

---

## Safety Boundary

The runtime boundary is intentionally narrow.

The project must preserve these rules:

- read-only by default;
- no network access in runtime behavior;
- no LLM dependency in runtime behavior;
- no execution of commands from analyzed repositories;
- no unsupported security guarantees;
- secret-like values must be redacted;
- write behavior must require explicit user intent;
- generated or overwritten files must be handled conservatively.

Security-sensitive changes must be isolated in their own phase and covered by tests.

See:

- `SECURITY.md`
- `docs/THREAT-MODEL.md`

---

## Repository Layout

    .
    ├── .github/
    │   ├── ISSUE_TEMPLATE/
    │   ├── pull_request_template.md
    │   └── workflows/
    │       └── ci.yml
    ├── docs/
    │   ├── BUILD-PLAN.md
    │   ├── OUTPUTS.md
    │   ├── PRODUCT-STRATEGY.md
    │   ├── RULES.md
    │   ├── THREAT-MODEL.md
    │   ├── V0.2-GOVERNANCE-RULES-SPEC.md
    │   └── screenshots/
    │       └── readme/
    │           ├── agent-rules-kit-help-check.png
    │           ├── agent-rules-kit-init-safety.png
    │           └── agent-rules-kit-output-formats.png
    ├── scripts/
    │   └── check.sh
    ├── src/
    │   └── agent_rules_kit/
    │       ├── __init__.py
    │       ├── cli.py
    │       ├── discovery.py
    │       ├── findings.py
    │       ├── governance.py
    │       ├── init_plan.py
    │       ├── init_write.py
    │       └── redaction.py
    ├── tests/
    ├── AGENTS.md
    ├── CHANGELOG.md
    ├── CONTRIBUTING.md
    ├── LICENSE
    ├── README.md
    ├── SECURITY.md
    ├── SUPPORT.md
    └── pyproject.toml

---

## Quality Gates

Local verification is handled by:

    PATH="$PWD/.venv/bin:$PATH" ./scripts/check.sh

Run this after installing development dependencies with:

    .venv/bin/python -m pip install -e '.[dev]'

The local check suite verifies:

- Python syntax;
- unit tests;
- Ruff lint checks;
- UTF-8 text files;
- LF line endings;
- final newline;
- no trailing whitespace;
- Git whitespace checks.

Current verified local result on `main`:

    ./scripts/check.sh passes

The exact unit test count may change as coverage evolves. The source of truth is the current `./scripts/check.sh` output and the matching GitHub Actions run for `main`.

CI installs project development dependencies and then runs the same local check script through GitHub Actions.

The required status check for `main` is:

    local-checks / Python 3.12

---

## Development Status

Current status:

- `v0.2.0` is published as a GitHub Release;
- `main` is preparing `v0.2.1` patch release metadata from post-`v0.2.0` fixes;
- no stable support or API guarantee yet;
- release tag `v0.2.0` points to the verified release SHA;
- wheel and sdist artifacts are attached to the `v0.2.0` GitHub Release;
- release assets were downloaded, checksum-verified, installed, and smoke-tested;
- local CLI behavior implemented;
- governance diagnostics, structured finding evidence, and evidence redaction are implemented;
- CI active;
- branch protection was documented in prior release-governance evidence and must be re-verified before the next release;
- README distinguishes the published `v0.2.0` release from unreleased `main` state and keeps PyPI marked as not published;
- security boundaries documented;
- threat model documented.

Before claiming the next patch release or final audit-ready state, verify:

- all intended unreleased fixes for the patch release are merged into `main`;
- no known release-blocking audit finding remains open;
- local checks pass from a development virtual environment;
- CI passes for the release SHA;
- sdist and wheel build and install from clean temporary environments;
- release assets can be downloaded, checksum-verified, installed, and smoke-tested;
- output examples are generated from real commands;
- README documents normal CLI use, source-tree development use, virtual environment setup, development dependencies, and local checks;
- README does not claim unsupported maturity;
- SECURITY.md and CHANGELOG.md are current;
- private vulnerability reporting is enabled or its absence is clearly documented;
- tag and GitHub Release point to the verified release SHA;
- no real secrets or private data are present.

---

## Maintainer Workflow

This repository follows a strict Always-Green workflow.

Required discipline:

- never work directly on `main` after Genesis;
- start each phase from clean, synchronized `main`;
- create one branch per logical phase;
- read real files before editing;
- make minimal changes;
- avoid `git add .`;
- stage only expected files;
- inspect staged diff before commit;
- run local checks before push;
- verify remote branch SHA after push;
- open PR;
- verify PR state, diff, and CI;
- merge only after green checks;
- use exact head SHA for merge;
- verify `main` after merge;
- verify CI on `main`;
- delete local and remote phase branches.

A phase is complete only when:

    main is clean
    origin/main is synchronized
    local checks pass
    CI is green
    the PR is merged
    phase branches are deleted

---

## Contributing

See `CONTRIBUTING.md`.

Any contribution must preserve the safety boundary documented in `AGENTS.md`, `SECURITY.md`, and `docs/THREAT-MODEL.md`.

---

## Support

If this project helps you, you can support CDLAN public work here:

<p align="center">
  <a href="https://www.paypal.com/donate/?hosted_button_id=YVENCBNCZWVPW">
    <img
      alt="Support with PayPal"
      src="https://img.shields.io/badge/Support%20CDLAN-PayPal-003087?style=for-the-badge&logo=paypal&logoColor=white&labelColor=050505"
    />
  </a>
</p>

Support is optional. It does not change the license, support policy, or project boundaries.

---

## License

MIT.

See `LICENSE`.

---

## Scope Disclaimer

`agent-rules-kit` is a focused diagnostic tool for AI agent instruction files.

It is not a security product, not a general repository auditor, not a secret scanner, not an autonomous fixer, and not a replacement for maintainer review.

---

<p align="center">
  <strong>CDLAN · Less noise. More system.</strong>
</p>

<p align="center">
  <img
    width="100%"
    src="https://capsule-render.vercel.app/api?type=waving&height=160&section=footer&color=0:000000,55:d4af37,100:111827&animation=twinkling"
    alt="agent-rules-kit footer wave"
  />
</p>
