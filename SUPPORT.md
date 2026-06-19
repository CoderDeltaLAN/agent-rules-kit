# Support Policy

`agent-rules-kit` is a small open source project maintained on a best-effort basis.

There is no commercial SLA, no guaranteed response time, no production-readiness guarantee, and no stable API guarantee yet.

## Current published line

`v0.3.0` is the current published GitHub Release and PyPI package line.

`v0.2.3` remains the previous published GitHub Release and PyPI package baseline.

## Package availability

The current published package is:

    agent-rules-kit==0.3.0

Future PyPI availability claims must be verified per release before updating this policy.

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

Private vulnerability reporting is enabled for this repository after manual GitHub UI verification.

Use GitHub private vulnerability reporting for sensitive vulnerability reports when available. This disclosure channel does not change the best-effort support boundary and is not a security guarantee.

Security-relevant reports should avoid posting real secrets, tokens, credentials, private URLs, customer data, or exploit material.

See `SECURITY.md` and `docs/PRIVATE-VULNERABILITY-REPORTING.md` for the project security boundary, supported-version policy, verification record, and limits of this disclosure channel.

## Project boundaries

`agent-rules-kit` is local-first, read-only by default, and does not call an LLM, access the network at runtime, or execute commands from analyzed repositories.

It is not a security product, not a general repository auditor, not a secret scanner, not an autonomous fixer, and not a replacement for maintainer review.
