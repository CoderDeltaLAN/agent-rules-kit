#!/usr/bin/env sh
set -eu

printf '\n== python syntax ==\n'
python -m compileall -q src tests

printf '\n== unit tests ==\n'
PYTHONPATH=src python -m unittest discover -s tests -p 'test_*.py'

printf '\n== ruff ==\n'
python -m ruff check .

printf '\n== text hygiene ==\n'
python - <<'PY'
from __future__ import annotations

from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
}

CHECK_SUFFIXES = {
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".txt",
    ".yml",
    ".yaml",
}

failed = False

for file_item in sorted(Path(".").rglob("*")):
    if not file_item.is_file():
        continue
    if any(part in SKIP_DIRS for part in file_item.parts):
        continue
    if file_item.suffix not in CHECK_SUFFIXES and file_item.name not in {"LICENSE", ".gitignore"}:
        continue

    data = file_item.read_bytes()

    if b"\r\n" in data:
        print(f"ERROR CRLF: {file_item}")
        failed = True

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        print(f"ERROR non-UTF-8: {file_item}")
        failed = True
        continue

    if text and not text.endswith("\n"):
        print(f"ERROR missing final newline: {file_item}")
        failed = True

    for line_number, line_text in enumerate(text.splitlines(), start=1):
        if line_text.rstrip(" \t") != line_text:
            print(f"ERROR trailing whitespace: {file_item}:{line_number}")
            failed = True

if failed:
    raise SystemExit(1)

print("OK: text files are UTF-8/LF with final newline and no trailing whitespace.")
PY

printf '\n== git whitespace checks ==\n'
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git diff --check
    git diff --cached --check
else
    printf 'skip: not inside a git work tree\n'
fi

printf '\nOK: local checks passed.\n'
