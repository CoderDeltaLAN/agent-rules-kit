# Output Examples

This document shows representative `agent-rules-kit` CLI outputs generated from fixtures in the current repository state.

`v0.2.0` release artifacts may differ from unreleased `main` if post-release fixes have not yet been cut into a new release.

The examples document output shape, exit codes, and redaction expectations. They are not a claim that the analyzed repository is safe, complete, production-ready, compliant, or free of secrets.

## Scope

Covered commands and formats:

- `agent-rules-kit check` console output;
- `agent-rules-kit check --format json`;
- `agent-rules-kit check --format markdown`.

These examples do not document `init --write` side effects. Write-mode behavior remains explicit, local, and backup-oriented.

## Exit codes

`check` uses these documented exit codes:

- `0`: supported instruction files were found;
- `1`: no supported instruction files were found;
- `2`: invalid input or operational error.

A successful exit code does not mean that the repository is safe or production-ready. It only means that the command completed according to its documented behavior.

## Console output: supported instruction files found

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

## Console output: no supported instruction files

Command:

    agent-rules-kit check tests/fixtures/repositories/empty-repo

Exit code: `1`.

Stdout:

    agent-rules-kit check: tests/fixtures/repositories/empty-repo
    No supported agent instruction files found.

Stderr:

    <no output>

## JSON output: governance findings

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

## Markdown output: governance findings

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

## Redaction expectations

Output paths, messages, and evidence payloads are passed through secret-like value redaction where the CLI emits them.

Users should still avoid placing real secrets, tokens, credentials, customer data, or private URLs in fixtures, examples, logs, screenshots, issues, or pull requests.

## Maintainer guidance

When output behavior changes, update this document together with the corresponding tests and fixtures.

Do not update examples by hand if the CLI behavior changed. Regenerate or re-check examples against the current code so the documentation stays honest.
