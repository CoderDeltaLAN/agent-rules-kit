# Support Policy

`agent-rules-kit` is a small open source project maintained on a best-effort basis.

There is no commercial SLA, no guaranteed response time, no production-readiness guarantee, and no stable API guarantee yet.

## Current published line

`v0.2.3` remains the current published GitHub Release and PyPI package line.

Current `main` is preparing the `v0.3.0` release candidate and may include command baselines or documentation not yet available from PyPI.

`v0.3.0` must not be described as a published GitHub Release or PyPI package until the dedicated release phase completes and verifies publication.

## Package availability

The current published package is:

    agent-rules-kit==0.2.3

Do not claim `agent-rules-kit==0.3.0` is available on PyPI until the release phase verifies the published package and a clean install smoke test.

## What support means

Best-effort support may include:

- clarifying documented behavior;
- reviewing reproducible bug reports;
- correcting stale documentation;
- considering small fixes that preserve the project safety boundary.

Best-effort support does not include:

- guaranteed fixes;
- private consulting through GitHub issues;
- production incident response;
- security guarantees;
- dependency vulnerability scanning;
- support for behavior outside the documented scope.

## Security and vulnerability handling

Private vulnerability reporting is currently disabled for this repository.

Do not claim GitHub Security Advisories or private vulnerability reporting are enabled unless that setting has been explicitly verified.

Security-relevant reports should avoid posting real secrets, tokens, credentials, private URLs, customer data, or exploit material.

See `SECURITY.md` for the project security boundary and supported-version policy.

## Project boundaries

`agent-rules-kit` is local-first, read-only by default, and does not call an LLM, access the network at runtime, or execute commands from analyzed repositories.

It is not a security product, not a general repository auditor, not a secret scanner, not an autonomous fixer, and not a replacement for maintainer review.
