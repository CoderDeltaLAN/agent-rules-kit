"""Deterministic conflicting instruction detection."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from agent_rules_kit.discovery import InstructionFile


@dataclass(frozen=True, slots=True)
class ConflictLocation:
    """One occurrence of guidance participating in a conflict."""

    path: str
    line: int
    evidence: str


@dataclass(frozen=True, slots=True)
class ConflictGroup:
    """Opposing guidance detected for one instruction topic."""

    topic: str
    summary: str
    allow_locations: tuple[ConflictLocation, ...]
    block_locations: tuple[ConflictLocation, ...]


@dataclass(frozen=True, slots=True)
class ConflictReport:
    """Conflict report for supported instruction files."""

    groups: tuple[ConflictGroup, ...]

    @property
    def conflict_group_count(self) -> int:
        return len(self.groups)

    @property
    def conflict_line_count(self) -> int:
        return sum(
            len(group.allow_locations) + len(group.block_locations)
            for group in self.groups
        )


@dataclass(frozen=True, slots=True)
class _ConflictRule:
    topic: str
    polarity: str
    summary: str
    patterns: tuple[re.Pattern[str], ...]


_CONFLICT_RULES: tuple[_ConflictRule, ...] = (
    _ConflictRule(
        topic="main integration",
        polarity="allow",
        summary="direct-main guidance conflicts with PR/review boundaries",
        patterns=(
            re.compile(r"\b(commit|push)\s+directly\s+to\s+main\b", re.IGNORECASE),
            re.compile(r"\bdirect\s+push(?:es)?\s+to\s+main\s+(are\s+)?(allowed|ok|fine)\b", re.IGNORECASE),  # noqa: E501
            re.compile(r"\bmerge\s+without\s+(review|approval)\b", re.IGNORECASE),
            re.compile(r"\b(do not|don't|never|avoid)\b.{0,80}\buse\s+pull\s+requests?\b", re.IGNORECASE),  # noqa: E501
            re.compile(r"\b(no\s+PR|PR\s+is\s+not|required\s+PR\s+is\s+not|pull\s+requests?\s+are\s+not)\b.{0,80}\b(required|needed|mandatory)\b", re.IGNORECASE),  # noqa: E501
        ),
    ),
    _ConflictRule(
        topic="main integration",
        polarity="block",
        summary="direct-main guidance conflicts with PR/review boundaries",
        patterns=(
            re.compile(r"\b(do not|don't|never|avoid|no)\b.{0,80}\b(commit|push|merge)\b.{0,80}\bmain\b", re.IGNORECASE),  # noqa: E501
            re.compile(r"\buse\s+pull\s+requests?\b", re.IGNORECASE),
            re.compile(r"\bPR\s+(is\s+)?required\b", re.IGNORECASE),
        ),
    ),
    _ConflictRule(
        topic="checks",
        polarity="allow",
        summary="skip-check guidance conflicts with mandatory validation guidance",
        patterns=(
            re.compile(r"\b(ignore|skip)\s+(failing\s+)?(checks|tests|ci)\b", re.IGNORECASE),
            re.compile(r"\btests?\s+can\s+be\s+skipped\b", re.IGNORECASE),
            re.compile(r"\bCI\s+can\s+be\s+ignored\b", re.IGNORECASE),
        ),
    ),
    _ConflictRule(
        topic="checks",
        polarity="block",
        summary="skip-check guidance conflicts with mandatory validation guidance",
        patterns=(
            re.compile(r"\b(run|execute)\b.{0,80}\b(checks|tests|ci)\b", re.IGNORECASE),
            re.compile(r"\b(checks|tests|ci)\b.{0,80}\b(must|required|before\s+(commit|push|merge))\b", re.IGNORECASE),  # noqa: E501
            re.compile(r"\bdo\s+not\s+(ignore|skip)\s+(checks|tests|ci)\b", re.IGNORECASE),
        ),
    ),
    _ConflictRule(
        topic="runtime network or LLM",
        polarity="allow",
        summary="runtime network or LLM guidance conflicts with local-first boundaries",
        patterns=(
            re.compile(r"\b(use|call|query|invoke)\b.{0,80}\b(OpenAI|Anthropic|Claude|Gemini|ChatGPT|LLM|external API|remote API)\b", re.IGNORECASE),  # noqa: E501
            re.compile(r"\b(runtime|check|scan|audit|validate)\b.{0,80}\b(requires?|needs?|depends on|must use)\b.{0,80}\b(network|internet|LLM|external API)\b", re.IGNORECASE),  # noqa: E501
        ),
    ),
    _ConflictRule(
        topic="runtime network or LLM",
        polarity="block",
        summary="runtime network or LLM guidance conflicts with local-first boundaries",
        patterns=(
            re.compile(r"\b(no|without|do not|don't|never|avoid)\b.{0,100}\b(network|internet|LLM|OpenAI|Anthropic|Claude|Gemini|ChatGPT|external API|remote API)\b", re.IGNORECASE),  # noqa: E501
            re.compile(r"\b(local-first|local first|read-only local)\b", re.IGNORECASE),
        ),
    ),
    _ConflictRule(
        topic="secrets",
        polarity="allow",
        summary="secret-handling guidance conflicts with no-secret boundaries",
        patterns=(
            re.compile(r"\b(commit|store|check in|include)\b.{0,80}\b(secrets?|tokens?|credentials?|api[-_ ]?keys?)\b", re.IGNORECASE),  # noqa: E501
            re.compile(r"\bsecrets?\b.{0,80}\b(allowed|ok|fine)\b", re.IGNORECASE),
        ),
    ),
    _ConflictRule(
        topic="secrets",
        polarity="block",
        summary="secret-handling guidance conflicts with no-secret boundaries",
        patterns=(
            re.compile(r"\b(do not|don't|never|avoid|no)\b.{0,100}\b(commit|store|check in|include)\b.{0,100}\b(secrets?|tokens?|credentials?|api[-_ ]?keys?)\b", re.IGNORECASE),  # noqa: E501
            re.compile(r"\bno\s+secrets?\b", re.IGNORECASE),
        ),
    ),
    _ConflictRule(
        topic="unsafe commands",
        polarity="allow",
        summary="automatic unsafe-command guidance conflicts with confirmation boundaries",
        patterns=(
            re.compile(r"\brun\b.{0,80}\brm\s+-[A-Za-z]*r[A-Za-z]*f\b.{0,80}\b(without asking|automatically|always)\b", re.IGNORECASE),  # noqa: E501
            re.compile(r"\buse\s+sudo\b.{0,80}\b(default|normal|routine|always)\b", re.IGNORECASE),
            re.compile(r"\brun\b.{0,80}\brepository\s+scripts?\b.{0,80}\b(automatically|without asking)\b", re.IGNORECASE),  # noqa: E501
        ),
    ),
    _ConflictRule(
        topic="unsafe commands",
        polarity="block",
        summary="automatic unsafe-command guidance conflicts with confirmation boundaries",
        patterns=(
            re.compile(r"\b(do not|don't|never|avoid)\b.{0,100}\b(rm\s+-[A-Za-z]*r[A-Za-z]*f|sudo|repository\s+scripts?)\b", re.IGNORECASE),  # noqa: E501
            re.compile(r"\bask\b.{0,80}\bbefore\b.{0,100}\b(rm\s+-[A-Za-z]*r[A-Za-z]*f|sudo|repository\s+scripts?)\b", re.IGNORECASE),  # noqa: E501
            re.compile(r"\b(explicit|human|maintainer|user)\b.{0,80}\b(approval|confirmation|permission)\b", re.IGNORECASE),  # noqa: E501
        ),
    ),
)


def build_conflict_report(
    repository_root: Path,
    instruction_files: tuple[InstructionFile, ...],
) -> ConflictReport:
    """Build a conservative report of opposite instruction guidance."""
    matches: dict[str, dict[str, list[ConflictLocation]]] = {
        rule.topic: {"allow": [], "block": []} for rule in _CONFLICT_RULES
    }
    summaries = {rule.topic: rule.summary for rule in _CONFLICT_RULES}

    for instruction_file in instruction_files:
        file_path = repository_root / instruction_file.path

        if file_path.is_symlink():
            raise ValueError(
                "instruction file path is a symlink and cannot be checked for conflicts: "
                f"{instruction_file.path}"
            )

        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            raise ValueError(
                "instruction file is not valid UTF-8 and cannot be checked for conflicts: "
                f"{instruction_file.path}"
            ) from error

        for line_number, line_text in enumerate(text.splitlines(), start=1):
            stripped = line_text.strip()
            if not _is_scannable_instruction_line(stripped):
                continue

            for rule in _CONFLICT_RULES:
                if not _matches_conflict_rule(stripped, rule):
                    continue

                matches[rule.topic][rule.polarity].append(
                        ConflictLocation(
                            path=instruction_file.path,
                            line=line_number,
                            evidence=stripped,
                        )
                    )

    groups = [
        ConflictGroup(
            topic=topic,
            summary=summaries[topic],
            allow_locations=tuple(polarities["allow"]),
            block_locations=tuple(polarities["block"]),
        )
        for topic, polarities in matches.items()
        if polarities["allow"] and polarities["block"]
    ]

    return ConflictReport(groups=tuple(groups))


def _matches_conflict_rule(stripped: str, rule: _ConflictRule) -> bool:
    matched = any(pattern.search(stripped) for pattern in rule.patterns)
    if not matched:
        return False

    if rule.topic == "main integration" and _has_negated_pr_boundary(stripped):
        return rule.polarity == "allow"

    return not (rule.polarity == "allow" and _has_negated_guidance(stripped))


def _has_negated_pr_boundary(stripped: str) -> bool:
    return bool(
        re.search(
            r"\b(do not|don't|never|avoid)\b.{0,80}\buse\s+pull\s+requests?\b",
            stripped,
            re.IGNORECASE,
        )
        or re.search(
            r"\b(no\s+PR|PR\s+is\s+not|required\s+PR\s+is\s+not|pull\s+requests?\s+are\s+not)\b.{0,80}\b(required|needed|mandatory)\b",
            stripped,
            re.IGNORECASE,
        )
    )


def _has_negated_guidance(stripped: str) -> bool:
    return bool(
        re.search(
            r"\b(do not|don't|never|avoid|no|must not|should not)\b",
            stripped,
            re.IGNORECASE,
        )
    )


def _is_scannable_instruction_line(stripped: str) -> bool:
    if not stripped:
        return False

    if stripped.startswith(("```", "---", "<!--")):
        return False

    if len(stripped) < 12:
        return False

    return any(character.isalpha() for character in stripped)


__all__ = [
    "ConflictGroup",
    "ConflictLocation",
    "ConflictReport",
    "build_conflict_report",
]
