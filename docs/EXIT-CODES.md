# Exit Codes

This document defines the initial `agent-rules-kit` CLI exit-code contract.

The contract is project-local and pre-v1.0. It is meant to guide tests, documentation, and future command implementation. It is not a stable public API guarantee before v1.0.

## General rules

- `0` means the command completed successfully according to its command-specific rules.
- `1` is reserved for supported no-result or review-needed states when documented by the command.
- `2` means invalid command-line usage, invalid repository input, unsupported command input, or another documented operational error.
- Findings do not currently make `check` fail.
- A successful exit code does not prove that a repository is safe, complete, compliant, production-ready, or free of secrets.

## Current implemented exit codes

### Global options

| Invocation | Exit code | Meaning |
| --- | ---: | --- |
| `agent-rules-kit --version` | `0` | Version printed successfully. |
| `agent-rules-kit` | `0` | Help printed successfully because no subcommand was provided. |
| invalid option or invalid subcommand | `2` | Command-line usage error handled by argparse. |

### `check`

| Condition | Exit code | Stdout | Stderr |
| --- | ---: | --- | --- |
| Supported instruction files found | `0` | Console, JSON, or Markdown report | Empty unless lower-level runtime fails unexpectedly |
| No supported instruction files found | `1` | Console, JSON, or Markdown no-result report | Empty unless lower-level runtime fails unexpectedly |
| Invalid repository input or supported operational error | `2` | JSON/Markdown error payload when those formats were requested; empty console stdout | Console error message on stderr |
| Invalid `--format` value or command-line usage | `2` | Argparse-dependent | Argparse-dependent |

Notes:

- `check` returns `0` even when warning findings are present.
- `check` returns `1` only for the supported no-instruction-files state.
- `check` returns `2` for repository validation errors raised by discovery and for argparse usage errors.

### `doctor`

| Condition | Exit code | Stdout | Stderr |
| --- | ---: | --- | --- |
| Supported instruction files found | `0` | Console diagnosis summary | Empty unless lower-level runtime fails unexpectedly |
| No supported instruction files found | `1` | Console no-result diagnosis summary | Empty unless lower-level runtime fails unexpectedly |
| Invalid repository input or command-line usage error | `2` | Empty | Error message or argparse-dependent |

Notes:

- `doctor` is read-only.
- `doctor` reuses the existing discovery and governance diagnostics.
- `doctor` findings do not currently make the command fail.
- `doctor` does not audit GitHub branch protection, CI, dependencies, or security certification.

### `budget`

| Condition | Exit code | Stdout | Stderr |
| --- | ---: | --- | --- |
| Supported instruction files found | `0` | Console budget approximation | Empty unless lower-level runtime fails unexpectedly |
| No supported instruction files found | `1` | Console no-result budget summary | Empty unless lower-level runtime fails unexpectedly |
| Invalid repository input, unsupported instruction-file input, or command-line usage error | `2` | Empty | Error message or argparse-dependent |

Notes:

- `budget` is read-only.
- `budget` uses deterministic local metrics only.
- `budget` does not perform tokenizer-specific counting, remote tokenization, LLM calls, pricing estimates, or optimization claims.
- `Approximate words` is not a model token count.
- Symlinked supported instruction-file paths fail hard with exit code `2` instead of being followed or silently skipped.

### `dedupe`

| Condition | Exit code | Stdout | Stderr |
| --- | ---: | --- | --- |
| Supported instruction files found | `0` | Console duplicate-line report | Empty unless lower-level runtime fails unexpectedly |
| No supported instruction files found | `1` | Console no-result duplicate-line summary | Empty unless lower-level runtime fails unexpectedly |
| Invalid repository input, unsupported instruction-file input, or command-line usage error | `2` | Empty | Error message or argparse-dependent |

Notes:

- `dedupe` is read-only.
- `dedupe` uses deterministic local normalization only.
- `dedupe` detects repeated normalized lines across supported instruction files, not broad semantic duplication.
- Symlinked supported instruction-file paths fail hard with exit code `2` instead of being followed or silently skipped.

### `conflicts`

| Condition | Exit code | Stdout | Stderr |
| --- | ---: | --- | --- |
| Supported instruction files found | `0` | Console contradictory-guidance report | Empty unless lower-level runtime fails unexpectedly |
| No supported instruction files found | `1` | Console no-result conflict summary | Empty unless lower-level runtime fails unexpectedly |
| Invalid repository input, unsupported instruction-file input, or command-line usage error | `2` | Empty | Error message or argparse-dependent |

Notes:

- `conflicts` is read-only.
- `conflicts` uses deterministic local pattern families only.
- `conflicts` detects implemented opposite-guidance patterns, not broad semantic contradiction.
- Symlinked supported instruction-file paths fail hard with exit code `2` instead of being followed or silently skipped.

### `explain`

| Condition | Exit code | Stdout | Stderr |
| --- | ---: | --- | --- |
| Known rules listed or known rule explained | `0` | Console rule explanation output | Empty unless lower-level runtime fails unexpectedly |
| Unknown rule ID, conflicting input, missing input, or command-line usage error | `2` | Empty or argparse-dependent | Error message or argparse-dependent |

Notes:

- `explain` is read-only.
- `explain` uses local rule metadata only.
- `explain` does not fetch external documentation, call an LLM, infer new rules, or generate free-form policy advice.
- Unknown rule IDs fail predictably.

### `init --dry-run`

| Condition | Exit code | Stdout | Stderr |
| --- | ---: | --- | --- |
| Plan completed | `0` | Dry-run plan | Empty unless lower-level runtime fails unexpectedly |
| Invalid repository input or symlink refusal | `2` | Empty | Error message |
| Missing mode, conflicting modes, or command-line usage error | `2` | Argparse-dependent or empty | Error message or argparse-dependent |

Notes:

- `init --dry-run` is read-only.
- It must not modify repository files.

### `init --write`

| Condition | Exit code | Stdout | Stderr |
| --- | ---: | --- | --- |
| Explicit write completed | `0` | Write summary | Empty unless lower-level runtime fails unexpectedly |
| Invalid repository input or symlink refusal | `2` | Empty | Error message |
| Missing mode, conflicting modes, or command-line usage error | `2` | Argparse-dependent or empty | Error message or argparse-dependent |

Notes:

- `init --write` is the only current write mode.
- It backs up an existing root `AGENTS.md` before replacement.
- It must remain explicit and separate from read-only diagnosis commands.

## Planned command exit-code direction

No remaining planned command exit-code target is documented here. Future release or documentation phases must update this file only from verified behavior.

## Test evidence

Current implemented exit-code behavior is covered by `tests/test_golden_outputs.py`.

The contract regression matrix currently checks:

- `agent-rules-kit --version` exits `0`;
- `agent-rules-kit` without a subcommand exits `0` and prints help;
- `check` exits `0` when supported instruction files are found;
- `check` exits `1` when no supported instruction files are found;
- `check --format json` and `check --format markdown` preserve the same success and no-result exit-code behavior;
- `doctor` exits `0` when supported instruction files are found;
- `doctor` exits `1` when no supported instruction files are found;
- `budget` exits `0` when supported instruction files are found;
- `budget` exits `1` when no supported instruction files are found;
- `dedupe` exits `0` when supported instruction files are found;
- `dedupe` exits `1` when no supported instruction files are found;
- `conflicts` exits `0` when supported instruction files are found;
- `conflicts` exits `1` when no supported instruction files are found;
- `explain --list` exits `0`;
- `explain RULE_ID` exits `0` for known rule IDs;
- `explain RULE_ID` exits `2` for unknown rule IDs;
- `init --dry-run` exits `0`;
- `init` without `--dry-run` or `--write` exits `2` and writes the supported error to stderr.

These tests are evidence for current implemented behavior. They do not turn this pre-v1.0 contract into a stable public API guarantee.

## Maintenance rules

Update this document when:

- a command changes exit-code behavior;
- a new command is added;
- a new supported no-result state is introduced;
- command-line usage handling changes;
- JSON/Markdown error payload behavior changes.

Do not update this document after code changes by guesswork. Verify behavior with real commands, tests, or fixtures before changing the contract.
