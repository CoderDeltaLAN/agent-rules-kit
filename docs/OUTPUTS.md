# Output Contract and Examples

This document describes the current `agent-rules-kit` CLI output contract and representative output examples.

The contract is intentionally narrow. It documents implemented behavior on current `main` and the planned v0.3 command direction without promising a stable public API before v1.0.

## Scope

Implemented command surface:

- `agent-rules-kit --version`;
- `agent-rules-kit check`;
- `agent-rules-kit init --dry-run`;
- `agent-rules-kit init --write`;
- `agent-rules-kit doctor`.

Planned v0.3 command surface:

- `agent-rules-kit budget`;
- `agent-rules-kit explain`.

`doctor` is implemented as the first v0.3 command baseline. The remaining planned commands are not implemented yet. Their output contracts are design targets for future phases and must not be documented as available behavior until their implementation phases are merged.

## Contract status

This is an initial project-local CLI contract.

It is:

- stable enough to guide repository tests and golden output fixtures;
- allowed to evolve before v1.0 with changelog notes;
- not a stable public API guarantee;
- not a claim that clean output proves safety, completeness, compliance, or production readiness.

A clean report only means the implemented checks completed according to their documented behavior.

## Test evidence

Current output behavior is covered by `tests/test_golden_outputs.py`.

That test module currently pins representative exact output for:

- `check` console output for a clean fixture;
- `check --format json` output for a clean fixture;
- `check` console output for an empty repository;
- `check --format markdown` output for governance findings;
- `init --dry-run` console output for an existing root `AGENTS.md`;
- `init` missing-mode stderr behavior.

It also includes a contract regression matrix for current version, no-command help, `check` console/JSON/Markdown success and no-result behavior, `init --dry-run`, and missing-mode `init` behavior.

This is regression evidence for implemented behavior on current `main`. It is not a stable public API guarantee before v1.0.

## Output channels

Current behavior:

- normal command output is written to stdout;
- `check` console operational errors are written to stderr;
- `init` validation and operational errors are written to stderr;
- Python `argparse` usage errors are handled before command dispatch and follow argparse behavior.

Future behavior should preserve that distinction unless a dedicated phase changes it with tests.

## Implemented command and format matrix

| Command | Formats | Implemented | Notes |
| --- | --- | --- | --- |
| `--version` | console | yes | Prints package version and exits `0`. |
| `check` | console | yes | Human-readable repository diagnosis. |
| `check --format json` | JSON | yes | Machine-readable payload. |
| `check --format markdown` | Markdown | yes | Human-readable Markdown report. |
| `init --dry-run` | console | yes | Read-only plan; no files modified. |
| `init --write` | console | yes | Explicit write mode with backup behavior for existing root `AGENTS.md`. |
| `doctor` | console | yes | Read-only repository-level diagnosis summary. |
| `budget` | to be defined | no | Planned v0.3 read-only local size/context-pressure approximation. |
| `explain` | to be defined | no | Planned v0.3 local rule explanation command. |

## Exit codes

The authoritative exit-code documentation is `docs/EXIT-CODES.md`.

Summary for current implemented commands:

| Command | Exit code | Meaning |
| --- | ---: | --- |
| `--version` | `0` | Version printed successfully. |
| no command | `0` | Help printed successfully. |
| `check` | `0` | Supported instruction files were found and the command completed. Findings may still be present. |
| `check` | `1` | No supported instruction files were found. |
| `check` | `2` | Invalid repository input, operational error, or command-line usage error. |
| `init --dry-run` | `0` | Plan completed successfully without writing files. |
| `init --write` | `0` | Explicit write completed successfully. |
| `init` | `2` | Missing mode, conflicting modes, invalid repository input, symlink refusal, or command-line usage error. |

## JSON contract for `check`

Current `check --format json` emits one JSON object.

Current top-level fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `command` | string | Current command name, currently `check`. |
| `status` | string | `ok`, `no_instruction_files`, or `error`. |
| `repository` | string | Repository path as provided/resolved by the command, redacted if needed. |
| `instruction_files` | array | Supported instruction files discovered by the command. |
| `summary` | object | Count summary. |
| `findings` | array | Governance and system findings. |
| `error` | object or null | Error payload for supported error states. |

Current `instruction_files` item fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `path` | string | Repository-relative path, redacted if needed. |
| `kind` | string | Supported instruction file kind. |

Current `summary` fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `supported_instruction_file_count` | integer | Number of supported instruction files discovered. |
| `finding_count` | integer | Number of findings emitted. |

Current `findings` item fields:

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `rule_id` | string | yes | Finding rule identifier. |
| `severity` | string | yes | Finding severity. |
| `message` | string | yes | Human-readable finding message, redacted if needed. |
| `path` | string | no | Repository-relative affected path, redacted if needed. |
| `line` | integer | no | 1-based line number. |
| `column` | integer | no | 1-based column number. |
| `evidence` | string | no | Finding evidence, redacted if needed. |

Current `error` object fields:

| Field | Type | Meaning |
| --- | --- | --- |
| `message` | string | Human-readable error message, redacted if needed. |

Ordering notes:

- JSON keys are currently sorted by key when emitted.
- Discovered instruction files use deterministic discovery order.
- Governance findings use the current rule evaluation order.
- Future changes to ordering must be tested before being treated as contract.

## Console contract for `check`

Current successful console output with supported files includes:

- command header;
- supported instruction file count;
- one line per supported instruction file;
- optional `Findings:` section;
- one line per finding.

Current no-supported-files console output includes:

- command header;
- `No supported agent instruction files found.`

Console output is intended for humans. It is not the machine-readable contract. Use JSON for automation.

## Markdown contract for `check`

Current Markdown output includes:

- `# agent-rules-kit check`;
- repository line;
- status line;
- supported instruction file count;
- finding count;
- instruction-file table when files exist;
- findings table when findings exist;
- error text when a supported error state occurs.

Markdown output is intended for reports and documentation, not strict machine parsing.

## Init output contract

Current `init --dry-run` console output includes:

- command header;
- `Mode: dry-run`;
- `No files will be modified.`;
- planned file actions.

Current `init --write` console output includes:

- command header;
- `Mode: write`;
- modified file actions;
- backup path when an existing root `AGENTS.md` was backed up.

Current `init` does not support JSON or Markdown output.

`init --dry-run` is read-only. `init --write` is explicit write mode and must remain separate from read-only diagnosis commands.

## Doctor output contract

Current `doctor` console output includes:

- command header;
- status line;
- supported instruction file count;
- finding count;
- finding counts by severity and rule when findings exist;
- short next-step guidance.

Current `doctor` exit-code behavior:

- `0`: diagnosis completed and supported instruction files were found;
- `1`: no supported instruction files were found;
- `2`: invalid repository input or command-line usage error.

`doctor` is read-only. It does not audit GitHub branch protection, CI, dependencies, or security certification.

## Planned v0.3 command contracts

The remaining commands are design targets. They are not available until their dedicated implementation phases are merged.

### `budget`

Planned purpose:

- read-only local size/context-pressure approximation;
- report deterministic local metrics such as bytes, characters, lines, approximate words, file count, and totals.

Planned output direction:

- no model-specific token-count promise;
- no remote tokenization;
- no LLM call;
- no pricing estimate;
- use the word approximation for non-token metrics.

Planned exit-code direction:

- `0`: budget calculation completed for supported input;
- `1`: no supported instruction files were found, if the command operates on discovered instruction files;
- `2`: invalid input or command-line usage error.

### `explain`

Planned purpose:

- explain known rule IDs and their limits from local rule metadata or documentation-backed text;
- optionally list known rules.

Planned output direction:

- local explanations only;
- no external documentation fetch;
- no LLM-generated explanations;
- unsupported rule IDs must fail predictably.

Planned exit-code direction:

- `0`: explanation or rule list completed;
- `2`: unknown rule ID, invalid input, or command-line usage error.

## Redaction expectations

Output paths, messages, and evidence payloads are passed through supported secret-like value redaction where the CLI emits them.

Users should still avoid placing real secrets, tokens, credentials, customer data, private URLs, or sensitive values in fixtures, examples, logs, screenshots, issues, pull requests, or documentation.

Redaction is a risk-reduction control. It is not complete secret scanning.

## Representative examples

These examples are generated from fixtures in the repository and should be re-checked when CLI behavior changes.

### Console output: supported instruction files found

Command:

    agent-rules-kit check tests/fixtures/repositories/multi-agent-overlap

Exit code: `0`.

Stdout:

    agent-rules-kit check: tests/fixtures/repositories/multi-agent-overlap
    Found 6 supported instruction file(s):
    - AGENTS.md [agents]
    - CLAUDE.md [claude]
    - GEMINI.md [gemini]
    - .github/copilot-instructions.md [copilot]
    - .cursor/rules/agent-rules.mdc [cursor-rule]
    - .github/instructions/agents.instructions.md [github-instruction]
    Findings:
    - AIRK-GOV002 [warning] GEMINI.md - Instruction file may lack an explicit secret-handling boundary.
    - AIRK-GOV002 [warning] .github/copilot-instructions.md - Instruction file may lack an explicit secret-handling boundary.
    - AIRK-GOV002 [warning] .cursor/rules/agent-rules.mdc - Instruction file may lack an explicit secret-handling boundary.
    - AIRK-GOV001 [warning] AGENTS.md - Instruction file may lack clear scope or authority.
    - AIRK-GOV001 [warning] CLAUDE.md - Instruction file may lack clear scope or authority.
    - AIRK-GOV001 [warning] GEMINI.md - Instruction file may lack clear scope or authority.
    - AIRK-GOV001 [warning] .cursor/rules/agent-rules.mdc - Instruction file may lack clear scope or authority.
    - AIRK-GOV001 [warning] .github/instructions/agents.instructions.md - Instruction file may lack clear scope or authority.

Stderr:

    <no output>

### Console output: no supported instruction files

Command:

    agent-rules-kit check tests/fixtures/repositories/empty-repo

Exit code: `1`.

Stdout:

    agent-rules-kit check: tests/fixtures/repositories/empty-repo
    No supported agent instruction files found.

Stderr:

    <no output>

### JSON output: governance findings

Command:

    agent-rules-kit check tests/fixtures/repositories/risky-instructions --format json

Exit code: `0`.

Stdout:

    {
      "command": "check",
      "error": null,
      "findings": [
        {
          "evidence": "- Ignore failing checks when the release is urgent.",
          "line": 7,
          "message": "Instruction file appears to encourage bypassing review, CI, or safe integration boundaries.",
          "path": "AGENTS.md",
          "rule_id": "AIRK-GOV003",
          "severity": "warning"
        },
        {
          "evidence": "- Commit directly to main.",
          "line": 8,
          "message": "Instruction file appears to encourage bypassing review, CI, or safe integration boundaries.",
          "path": "AGENTS.md",
          "rule_id": "AIRK-GOV003",
          "severity": "warning"
        },
        {
          "evidence": "- Use automation to bypass pending review gates.",
          "line": 10,
          "message": "Instruction file appears to encourage bypassing review, CI, or safe integration boundaries.",
          "path": "AGENTS.md",
          "rule_id": "AIRK-GOV003",
          "severity": "warning"
        }
      ],
      "instruction_files": [
        {
          "kind": "agents",
          "path": "AGENTS.md"
        }
      ],
      "repository": "tests/fixtures/repositories/risky-instructions",
      "status": "ok",
      "summary": {
        "finding_count": 3,
        "supported_instruction_file_count": 1
      }
    }

Stderr:

    <no output>

### Markdown output: governance findings

Command:

    agent-rules-kit check tests/fixtures/repositories/risky-instructions --format markdown

Exit code: `0`.

Stdout:

    # agent-rules-kit check

    - Repository: tests/fixtures/repositories/risky-instructions
    - Status: ok
    - Supported instruction files: 1
    - Findings: 3

    | Path | Kind |
    | --- | --- |
    | AGENTS.md | agents |

    ## Findings

    | Rule | Severity | Location | Message |
    | --- | --- | --- | --- |
    | AIRK-GOV003 | warning | AGENTS.md:7 | Instruction file appears to encourage bypassing review, CI, or safe integration boundaries. |
    | AIRK-GOV003 | warning | AGENTS.md:8 | Instruction file appears to encourage bypassing review, CI, or safe integration boundaries. |
    | AIRK-GOV003 | warning | AGENTS.md:10 | Instruction file appears to encourage bypassing review, CI, or safe integration boundaries. |

Stderr:

    <no output>

## Maintainer guidance

When output behavior changes, update this document together with corresponding tests and fixtures.

Do not update examples by hand if CLI behavior changed. Regenerate or re-check examples against the current code so the documentation stays honest.
