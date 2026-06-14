"""Instruction governance diagnostics."""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path
from re import Pattern

from agent_rules_kit.discovery import InstructionFile
from agent_rules_kit.findings import Finding, Severity

REVIEW_CI_BYPASS_RULE_ID = "AIRK-GOV003"
REVIEW_CI_BYPASS_MESSAGE = (
    "Instruction file appears to encourage bypassing review, CI, or safe integration boundaries."
)

UNSUPPORTED_CLAIM_RULE_ID = "AIRK-GOV006"
UNSUPPORTED_CLAIM_MESSAGE = (
    "Instruction file may contain an unsupported security or maturity claim."
)

REVIEW_CI_BYPASS_PATTERNS: tuple[Pattern[str], ...] = (
    re.compile(r"\b(ignore|skip)\s+(failing\s+)?(checks|tests|ci)\b", re.IGNORECASE),
    re.compile(r"\bskip\s+(code\s+)?review\b", re.IGNORECASE),
    re.compile(r"\b(commit|push)\s+directly\s+to\s+main\b", re.IGNORECASE),
    re.compile(r"\bdirect\s+push(?:es)?\s+to\s+main\b", re.IGNORECASE),
    re.compile(r"\bmerge\s+without\s+(review|approval)\b", re.IGNORECASE),
    re.compile(
        r"\bbypass(?:ing)?\s+("
        r"branch protection|review|reviews|pending review gates|ci|checks|safe integration"
        r")\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bforce[- ]push\b.{0,80}\b(normal|default|routine|workflow)\b",
        re.IGNORECASE,
    ),
)

NEGATED_REVIEW_CI_BYPASS_CONTEXT_PATTERNS: tuple[Pattern[str], ...] = (
    re.compile(
        r"\b(do not|don't|must not|should not|never|avoid|forbid|forbidden|no)\b"
        r".{0,120}\b("
        r"bypass(?:ing)?|skip(?:ping)?|ignore|commit(?:ting)?|push(?:ing|es)?|direct push(?:es)?|force[- ]push|merge"
        r")\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bnot\s+("
        r"bypass(?:ing)?|skip(?:ping)?|ignore|commit(?:ting)?|push(?:ing)?|"
        r"merge|force[- ]push"
        r")\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(break[- ]glass|emergency)\b.{0,120}\b(explicit|human|maintainer)\s+approval\b",
        re.IGNORECASE,
    ),
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


LinePredicate = Callable[[str], bool]


def find_governance_findings(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
) -> tuple[Finding, ...]:
    """Return all governance findings in stable rule order."""
    return (
        *find_unsupported_claim_findings(repository_root, instruction_files),
        *find_review_ci_bypass_findings(repository_root, instruction_files),
    )


def find_review_ci_bypass_findings(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
) -> tuple[Finding, ...]:
    """Return review, CI, or safe integration bypass findings."""
    return _find_line_findings(
        repository_root,
        instruction_files,
        rule_id=REVIEW_CI_BYPASS_RULE_ID,
        severity=Severity.WARNING,
        message=REVIEW_CI_BYPASS_MESSAGE,
        predicate=_contains_review_ci_bypass_guidance,
    )


def find_unsupported_claim_findings(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
) -> tuple[Finding, ...]:
    """Return unsupported security or maturity claim findings."""
    return _find_line_findings(
        repository_root,
        instruction_files,
        rule_id=UNSUPPORTED_CLAIM_RULE_ID,
        severity=Severity.WARNING,
        message=UNSUPPORTED_CLAIM_MESSAGE,
        predicate=_contains_unsupported_claim,
    )


def _find_line_findings(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
    *,
    rule_id: str,
    severity: Severity,
    message: str,
    predicate: LinePredicate,
) -> tuple[Finding, ...]:
    findings: list[Finding] = []

    for instruction_file in instruction_files:
        candidate = repository_root / instruction_file.path

        try:
            text = candidate.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for line_number, line in enumerate(text.splitlines(), start=1):
            if predicate(line):
                findings.append(
                    Finding(
                        rule_id=rule_id,
                        severity=severity,
                        message=message,
                        path=instruction_file.path,
                        line=line_number,
                    )
                )

    return tuple(findings)


def _contains_review_ci_bypass_guidance(line: str) -> bool:
    has_bypass_guidance = any(
        pattern.search(line) is not None for pattern in REVIEW_CI_BYPASS_PATTERNS
    )
    if not has_bypass_guidance:
        return False

    return not any(
        pattern.search(line) is not None
        for pattern in NEGATED_REVIEW_CI_BYPASS_CONTEXT_PATTERNS
    )


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
    "NEGATED_REVIEW_CI_BYPASS_CONTEXT_PATTERNS",
    "NEGATED_UNSUPPORTED_CLAIM_CONTEXT_PATTERNS",
    "REVIEW_CI_BYPASS_MESSAGE",
    "REVIEW_CI_BYPASS_PATTERNS",
    "REVIEW_CI_BYPASS_RULE_ID",
    "UNSUPPORTED_CLAIM_MESSAGE",
    "UNSUPPORTED_CLAIM_PATTERNS",
    "UNSUPPORTED_CLAIM_RULE_ID",
    "find_governance_findings",
    "find_review_ci_bypass_findings",
    "find_unsupported_claim_findings",
]
