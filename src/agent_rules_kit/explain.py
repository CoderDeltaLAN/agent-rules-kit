"""Local governance rule explanations."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuleExplanation:
    """Human-readable explanation for one known rule."""

    rule_id: str
    title: str
    category: str
    summary: str
    limits: str


RULE_EXPLANATIONS: tuple[RuleExplanation, ...] = (
    RuleExplanation(
        rule_id="AIRK-SYS001",
        title="Unreadable instruction file",
        category="system",
        summary=(
            "Flags supported instruction files that cannot be analyzed as UTF-8."
        ),
        limits="Does not print raw undecodable bytes and does not repair encoding.",
    ),
    RuleExplanation(
        rule_id="AIRK-SYS002",
        title="Symlinked instruction file",
        category="system",
        summary=(
            "Flags supported instruction file paths that are symlinks and are not "
            "analyzed."
        ),
        limits="Does not follow symlinked instruction files or wildcard directories.",
    ),
    RuleExplanation(
        rule_id="AIRK-GOV006",
        title="Unsupported security or maturity claim",
        category="governance",
        summary=(
            "Flags instruction text that appears to claim unsupported safety, "
            "security, production readiness, completeness, or maturity."
        ),
        limits=(
            "Does not prove a claim false and does not replace human release "
            "review."
        ),
    ),
    RuleExplanation(
        rule_id="AIRK-GOV003",
        title="Review or CI bypass guidance",
        category="governance",
        summary=(
            "Flags instruction text that appears to encourage bypassing review, "
            "CI, PRs, branch protection, or safe integration flow."
        ),
        limits=(
            "Does not audit real GitHub settings, CI configuration, or branch "
            "protection."
        ),
    ),
    RuleExplanation(
        rule_id="AIRK-GOV004",
        title="Unsafe command execution guidance",
        category="governance",
        summary=(
            "Flags instruction text that appears to ask assistants to run "
            "destructive, privileged, broad, or externally fetched commands "
            "without an explicit confirmation boundary."
        ),
        limits=(
            "Is not a full shell safety analyzer and does not evaluate every "
            "possible command form."
        ),
    ),
    RuleExplanation(
        rule_id="AIRK-GOV005",
        title="Runtime network or LLM dependency guidance",
        category="governance",
        summary=(
            "Flags instruction text that appears to require remote services, LLMs, "
            "API tokens, or network behavior that conflicts with local-first "
            "boundaries."
        ),
        limits=(
            "Does not inspect real runtime behavior or external service "
            "configuration."
        ),
    ),
    RuleExplanation(
        rule_id="AIRK-GOV002",
        title="Missing secret-handling boundary",
        category="governance",
        summary=(
            "Flags supported instruction files that may lack explicit guidance "
            "for handling secrets, tokens, credentials, or sensitive data."
        ),
        limits=(
            "Is not complete secret scanning and does not prove that a repository "
            "is free of secrets."
        ),
    ),
    RuleExplanation(
        rule_id="AIRK-GOV001",
        title="Missing instruction scope or authority",
        category="governance",
        summary=(
            "Flags supported instruction files that may lack clear scope, "
            "authority, or precedence boundaries."
        ),
        limits=(
            "Does not resolve organizational policy or prove that instructions "
            "are complete."
        ),
    ),
)

_RULE_INDEX = {explanation.rule_id: explanation for explanation in RULE_EXPLANATIONS}


def list_rule_explanations() -> tuple[RuleExplanation, ...]:
    """Return known rule explanations in stable order."""
    return RULE_EXPLANATIONS


def get_rule_explanation(rule_id: str) -> RuleExplanation | None:
    """Return a known rule explanation by ID."""
    return _RULE_INDEX.get(rule_id.strip().upper())


__all__ = [
    "RULE_EXPLANATIONS",
    "RuleExplanation",
    "get_rule_explanation",
    "list_rule_explanations",
]
