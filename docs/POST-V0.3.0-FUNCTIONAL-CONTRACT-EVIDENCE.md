# Post-v0.3.0 Functional Contract Evidence

Status: functional evidence record.
Scope: current post-v0.3.0 main state.
Branch: test/full-cli-functional-contract.
Main baseline SHA before this evidence phase: 6c32d5d4e94cf960b5bfc06d0aa4525bdeab7bf5.

This document records local functional evidence for the current command contract after the published v0.3.0 release and before any later README finalization, external audit, tag, GitHub Release, or PyPI publication.

It is not a release note, version bump, tag decision, GitHub Release approval, PyPI publication, stability guarantee, security guarantee, or public API guarantee.

## Release boundary

No release action is authorized by this document.

Before any future release or PyPI publication, the maintainer must still complete, in separate phases:

- internal audit;
- full functional verification;
- README finalization from verified behavior;
- external audit;
- correction phases for any audit findings;
- packaging dry-run from clean wheel and sdist artifacts;
- release metadata cut;
- GitHub Release;
- PyPI publication through the configured trusted publishing workflow;
- clean install smoke from the published PyPI package;
- post-release verification.

## Verified command surface

The local CLI help exposed the following command surface:

- check;
- init;
- doctor;
- budget;
- dedupe;
- conflicts;
- explain.

The local version command reported:

- agent-rules-kit 0.3.0.

This version string reflects the current package metadata at the time of the evidence run. It does not mean the post-v0.3.0 command additions are already published on PyPI.

## Functional matrix result

The functional matrix passed after correcting the test command to match the real CLI contract.

Verified areas:

- top-level help;
- per-command help for check, init, doctor, budget, dedupe, conflicts, and explain;
- check console output;
- check JSON output parsed by python -m json.tool;
- check Markdown output;
- doctor against tests/fixtures/repositories/multi-agent-overlap;
- budget against tests/fixtures/repositories/multi-agent-overlap;
- dedupe against tests/fixtures/repositories/multi-agent-overlap;
- conflicts against tests/fixtures/repositories/multi-agent-overlap;
- explain AIRK-GOV003;
- explain --list;
- init --dry-run in a temporary sandbox;
- init --write in a temporary sandbox;
- init --write backup-and-replace behavior in a temporary sandbox;
- editable installed console-script smoke;
- scripts/check.sh;
- scripts/post-release-audit.sh.

## Observed functional outputs

Against tests/fixtures/repositories/multi-agent-overlap:

- doctor returned status review with 6 supported instruction files and 8 governance findings;
- budget returned status ok with 6 supported instruction files and deterministic local size metrics;
- dedupe returned status review with 5 duplicate groups and 16 duplicate lines;
- conflicts returned status ok with 0 conflict groups and 0 conflict lines;
- explain AIRK-GOV003 returned the expected review-or-CI-bypass rule explanation.

These outputs are fixture-based functional evidence. They are not a guarantee that the tool detects every possible duplicate, contradiction, governance issue, or unsafe instruction pattern.

## Init contract finding

The functional matrix initially attempted to call:

- init --write --force.

That was incorrect.

The real current init contract is:

- init --dry-run;
- init --write.

The CLI help does not expose --force.

The source and tests show that init --write backs up an existing root AGENTS.md before replacing it. Therefore, --force must not be documented as part of the current contract unless a future explicit product phase adds it intentionally.

Decision:

- do not add --force in this phase;
- do not document --force in README;
- keep init documentation aligned with --dry-run and --write only;
- treat any future --force flag as a separate product and safety decision.

## Sandbox write behavior

The write behavior was verified only inside a temporary directory.

Observed sequence:

- init --dry-run planned AGENTS.md creation and did not create the file;
- init --write created AGENTS.md;
- a second init --write with an existing AGENTS.md performed backup-and-replace;
- AGENTS.md.agent-rules-kit.bak existed after replacement.

No repository files were modified by the init sandbox check.

## Installed editable smoke

A temporary virtual environment installed the project in editable mode with development dependencies.

The installed console script verified:

- --version;
- check JSON output;
- doctor;
- budget;
- dedupe;
- conflicts;
- explain AIRK-GOV003;
- explain --list.

This is not a substitute for final wheel and sdist verification. Future release preparation must still build distributions, install from clean artifacts, and smoke-test the built package.

## Local gates

The final isolated local gates passed:

- python syntax;
- 152 unit tests;
- Ruff;
- text hygiene;
- Git whitespace checks;
- post-release audit.

The post-release audit remained local and did not mutate GitHub, PyPI, tags, releases, or branch protection.

## Known limits

This evidence does not verify:

- final wheel artifact installation;
- final sdist artifact installation;
- PyPI package installation for a future version;
- GitHub Release assets for a future version;
- external audit findings;
- branch protection through a fresh API capture;
- private vulnerability reporting through a fresh UI capture;
- universal semantic duplicate detection;
- universal contradiction detection;
- production readiness;
- repository security.

## Impact on next phases

This evidence supports moving toward README finalization, but only after it is committed, reviewed, merged, and verified on main.

The README final should reflect:

- dedupe and conflicts exist on current main after v0.3.0;
- dedupe and conflicts are not part of the published v0.3.0 package until a later verified release publishes them;
- init supports --dry-run and --write, not --force;
- init --write backs up existing root AGENTS.md before replacement;
- clean reports are not proof of safety;
- all release and PyPI claims require fresh verification during the release phase.
