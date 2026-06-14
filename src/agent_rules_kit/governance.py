"""Instruction governance diagnostics."""

from __future__ import annotations

import re
from pathlib import Path
from re import Pattern

from agent_rules_kit.discovery import InstructionFile
from agent_rules_kit.findings import Finding, Severity

UNSUPPORTED_CLAIM_RULE_ID = "AIRK-GOV006"
UNSUPPORTED_CLAIM_MESSAGE = (
    "Instruction file may contain an unsupported security or maturity claim."
)

UNSUPPORTED_CLAIM_PATTERNS: tuple[Pattern[str], ...] = (
    re.compile(r"\bguarantee[sd]?\s+(security|safety)\b", re.IGNORECASE),
    re.compile(r"\bguaranteed\s+(secure|safe|security|safety)\b", re.IGNORECASE),
    re.compile(
        r"\bmake[s]?\s+(the\s+)?(repository|repo|project|tool)\s+(secure|safe)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bcomplete\s+secret\s+scann(?:er|ing)\b", re.IGNORECASE),
    re.compile(r"\bproduction[- ]ready\b", re.IGNORECASE),
    re.compile(r"\benterprise[- ]grade\b", re.IGNORECASE),
)

NEGATED_UNSUPPORTED_CLAIM_CONTEXT_PATTERNS: tuple[Pattern[str], ...] = (
    re.compile(
        r"\b(do not|don't|must not|should not|never|avoid|forbid|forbidden|no)\b"
        r".{0,120}\b("
        r"claim[s]?|guarantee[sd]?|security|safety|secure|safe|"
        r"production[- ]ready|enterprise[- ]grade|complete secret scann(?:er|ing)"
        r")\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bnot\s+(a\s+)?("
        r"security scanner|secret scanner|production[- ]ready|enterprise[- ]grade|"
        r"secure|safe"
        r")\b",
        re.IGNORECASE,
    ),
)


def find_unsupported_claim_findings(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
) -> tuple[Finding, ...]:
    """Return unsupported security or maturity claim findings.

    The rule is intentionally conservative and deterministic. It scans only
    supported instruction files discovered by agent-rules-kit and does not
    execute repository commands, call the network, or call an LLM.
    """
    findings: list[Finding] = []

    for instruction_file in instruction_files:
        candidate = repository_root / instruction_file.path

        try:
            text = candidate.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for line_number, line in enumerate(text.splitlines(), start=1):
            if _contains_unsupported_claim(line):
                findings.append(
                    Finding(
                        rule_id=UNSUPPORTED_CLAIM_RULE_ID,
                        severity=Severity.WARNING,
                        message=UNSUPPORTED_CLAIM_MESSAGE,
                        path=instruction_file.path,
                        line=line_number,
                    )
                )

    return tuple(findings)


def _contains_unsupported_claim(line: str) -> bool:
    has_claim = any(
        pattern.search(line) is not None for pattern in UNSUPPORTED_CLAIM_PATTERNS
    )
    if not has_claim:
        return False

    return not any(
        pattern.search(line) is not None
        for pattern in NEGATED_UNSUPPORTED_CLAIM_CONTEXT_PATTERNS
    )


__all__ = [
    "NEGATED_UNSUPPORTED_CLAIM_CONTEXT_PATTERNS",
    "UNSUPPORTED_CLAIM_MESSAGE",
    "UNSUPPORTED_CLAIM_PATTERNS",
    "UNSUPPORTED_CLAIM_RULE_ID",
    "find_unsupported_claim_findings",
]
