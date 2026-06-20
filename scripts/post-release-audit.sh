#!/usr/bin/env sh
set -eu

require_file() {
    if [ ! -f "$1" ]; then
        printf 'ERROR missing required file: %s\n' "$1"
        return 1
    fi
}

require_executable() {
    if [ ! -x "$1" ]; then
        printf 'ERROR expected executable file: %s\n' "$1"
        return 1
    fi
}

require_contains() {
    file_name="$1"
    pattern="$2"
    if ! grep -Eq -- "$pattern" "$file_name"; then
        printf 'ERROR expected pattern not found in %s: %s\n' "$file_name" "$pattern"
        return 1
    fi
}

require_absent() {
    file_name="$1"
    pattern="$2"
    if grep -Eq -- "$pattern" "$file_name"; then
        printf 'ERROR unexpected stale pattern found in %s: %s\n' "$file_name" "$pattern"
        return 1
    fi
}

require_absent_in_files() {
    pattern="$1"
    shift

    if grep -REn -- "$pattern" "$@"; then
        printf 'ERROR unexpected pattern found: %s\n' "$pattern"
        return 1
    fi
}

printf '\n== post-release audit ==\n'
printf 'mode: local tracked-file audit; no GitHub, PyPI, tag, release, or branch mutation\n'

printf '\n== required files ==\n'
require_file pyproject.toml
require_file README.md
require_file CHANGELOG.md
require_file SECURITY.md
require_file SUPPORT.md
require_file LICENSE
require_file docs/PRODUCT-STRATEGY.md
require_file docs/THREAT-MODEL.md
require_file docs/V0.3.0-POST-RELEASE-AUDIT.md
require_file docs/V0.3.0-RELEASE-NOTES.md
require_file docs/DEPENDABOT-DEPENDENCY-GRAPH.md
require_file docs/SECURITY-SUPPLY-CHAIN-EVALUATION.md
require_file docs/OPENSSF-SCORECARD-EVALUATION.md
require_file docs/PRIVATE-VULNERABILITY-REPORTING.md
require_file .github/dependabot.yml
require_file .github/workflows/ci.yml
require_file .github/workflows/codeql.yml
require_file .github/workflows/publish-pypi.yml
require_file scripts/check.sh
require_file scripts/post-release-audit.sh
require_executable scripts/check.sh
require_executable scripts/post-release-audit.sh
printf 'OK: required files present.\n'

printf '
== forbidden local artifacts ==
'
python - <<'PY_FORBIDDEN_ARTIFACTS'
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
    "env",
    "venv",
}

failed = False

for item in sorted(Path(".").rglob("*")):
    if any(part in SKIP_DIRS for part in item.parts):
        continue

    if item.is_file() and (item.name == ".env" or item.name.startswith(".env.")):
        if item.name != ".env.example":
            print(f"ERROR forbidden environment file found: {item}")
            failed = True

    if item.is_dir() and (item.name in {"build", "dist"} or item.name.endswith(".egg-info")):
        print(f"ERROR forbidden build artifact directory found: {item}")
        failed = True

if failed:
    raise SystemExit(1)

print("OK: no forbidden local artifacts found outside ignored tool/build directories.")
PY_FORBIDDEN_ARTIFACTS

printf '
== git state ==
'
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    printf 'branch: %s\n' "$(git branch --show-current)"
    printf 'head: %s\n' "$(git rev-parse HEAD)"
    git status --short --branch
    if [ -n "$(git status --short --untracked-files=all)" ]; then
        printf 'ERROR working tree is not clean.\n'
        false
    fi
else
    printf 'ERROR not inside a git work tree.\n'
    false
fi

printf '\n== local checks ==\n'
./scripts/check.sh

printf '\n== package metadata and version parity ==\n'
python - <<'PY_METADATA'
from __future__ import annotations

import re
import tomllib
from pathlib import Path

pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
project = pyproject["project"]
pyproject_version = project["version"]

init_text = Path("src/agent_rules_kit/__init__.py").read_text(encoding="utf-8")
match = re.search(r'^__version__ = "([^"]+)"$', init_text, re.MULTILINE)

if match is None:
    raise SystemExit("ERROR package __version__ not found")

package_version = match.group(1)

if pyproject_version != package_version:
    raise SystemExit(
        f"ERROR version mismatch: pyproject={pyproject_version} package={package_version}"
    )

expected = {
    "name": "agent-rules-kit",
    "requires-python": ">=3.12",
    "dependencies": [],
}

for key, expected_value in expected.items():
    actual_value = project.get(key)
    if actual_value != expected_value:
        raise SystemExit(f"ERROR unexpected project.{key}: {actual_value!r}")

if "ruff>=0.8,<1" not in project.get("optional-dependencies", {}).get("dev", []):
    raise SystemExit("ERROR dev dependency on Ruff is missing or changed")

urls = project.get("urls", {})
required_urls = {
    "Homepage",
    "Documentation",
    "Repository",
    "Issues",
    "Changelog",
    "Security",
    "Release",
}

missing_urls = sorted(required_urls.difference(urls))
if missing_urls:
    raise SystemExit(f"ERROR missing project URLs: {missing_urls}")

expected_release_url = (
    "https://github.com/CoderDeltaLAN/agent-rules-kit/releases/tag/"
    f"v{pyproject_version}"
)
if urls["Release"] != expected_release_url:
    raise SystemExit(f"ERROR release URL does not match v{pyproject_version}")

if "License :: OSI Approved :: MIT License" not in project.get("classifiers", []):
    raise SystemExit("ERROR MIT classifier is missing")

print(f"OK: package metadata and version parity {pyproject_version}")
PY_METADATA

printf '\n== local CLI smoke ==\n'
PACKAGE_VERSION="$(python - <<'PY_VERSION'
from __future__ import annotations

import tomllib
from pathlib import Path

project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))["project"]
print(project["version"])
PY_VERSION
)"
PYTHONPATH=src python -m agent_rules_kit.cli --version | grep -Fx "agent-rules-kit ${PACKAGE_VERSION}"
PYTHONPATH=src python -m agent_rules_kit.cli check tests/fixtures/repositories/single-agent --format json | python -m json.tool >/dev/null
PYTHONPATH=src python -m agent_rules_kit.cli doctor tests/fixtures/repositories/single-agent >/dev/null
PYTHONPATH=src python -m agent_rules_kit.cli budget tests/fixtures/repositories/single-agent >/dev/null
PYTHONPATH=src python -m agent_rules_kit.cli dedupe tests/fixtures/repositories/multi-agent-overlap >/dev/null
PYTHONPATH=src python -m agent_rules_kit.cli conflicts tests/fixtures/repositories/multi-agent-overlap >/dev/null
PYTHONPATH=src python -m agent_rules_kit.cli explain AIRK-GOV003 >/dev/null
PYTHONPATH=src python -m agent_rules_kit.cli explain --list >/dev/null
printf 'OK: local CLI smoke checks passed.\n'

printf '\n== workflow action inventory ==\n'
python - <<'PY_WORKFLOWS'
from __future__ import annotations

import re
from pathlib import Path

expected_workflows = {
    ".github/workflows/ci.yml",
    ".github/workflows/codeql.yml",
    ".github/workflows/publish-pypi.yml",
}

workflow_paths = {item.as_posix() for item in Path(".github/workflows").glob("*.yml")}
if workflow_paths != expected_workflows:
    raise SystemExit(f"ERROR unexpected workflow inventory: {sorted(workflow_paths)}")

allowed_uses = {
    "actions/checkout@v7",
    "actions/setup-python@v6",
    "actions/upload-artifact@v4",
    "actions/download-artifact@v8",
    "github/codeql-action/init@v4",
    "github/codeql-action/analyze@v4",
    "pypa/gh-action-pypi-publish@release/v1",
}

observed_uses: list[str] = []

for workflow_path in sorted(Path(".github/workflows").glob("*.yml")):
    for line_number, line in enumerate(workflow_path.read_text(encoding="utf-8").splitlines(), start=1):
        match = re.match(r"\s*uses:\s*['\"]?([^'\"\s]+)['\"]?\s*$", line)
        if match is None:
            continue

        value = match.group(1)
        observed_uses.append(value)

        if "${{" in value:
            raise SystemExit(f"ERROR dynamic action reference in {workflow_path}:{line_number}: {value}")

        if value not in allowed_uses:
            raise SystemExit(f"ERROR unapproved action reference in {workflow_path}:{line_number}: {value}")

missing_uses = sorted(allowed_uses.difference(observed_uses))
if missing_uses:
    raise SystemExit(f"ERROR expected action reference not observed: {missing_uses}")

print("OK: workflow action inventory is explicit and approved.")
PY_WORKFLOWS

printf '\n== workflow permission and trigger sanity ==\n'
require_absent_in_files 'pull_request_target|workflow_run|schedule:' .github/workflows/ci.yml .github/workflows/codeql.yml .github/workflows/publish-pypi.yml
require_absent_in_files 'write-all|contents: write|packages: write|actions: write|pull-requests: write|issues: write|deployments: write' .github/workflows/ci.yml .github/workflows/codeql.yml .github/workflows/publish-pypi.yml
require_absent_in_files '\$\{\{[[:space:]]*secrets\.|PYPI_TOKEN|TWINE_PASSWORD|__token__|password:|username:' .github/workflows/ci.yml .github/workflows/codeql.yml .github/workflows/publish-pypi.yml
require_contains .github/workflows/ci.yml '^permissions:$'
require_contains .github/workflows/ci.yml '^  contents: read$'
require_contains .github/workflows/ci.yml 'name: local-checks / Python 3\.12'
require_contains .github/workflows/ci.yml 'name: compatibility / Python \$\{\{ matrix\.python-version \}\}'
require_contains .github/workflows/ci.yml 'python-version: "3\.12"'
require_contains .github/workflows/ci.yml '- "3\.13"'
require_contains .github/workflows/ci.yml 'agent-rules-kit doctor tests/fixtures/repositories/single-agent'
require_contains .github/workflows/ci.yml 'agent-rules-kit budget tests/fixtures/repositories/single-agent'
require_contains .github/workflows/ci.yml 'agent-rules-kit explain AIRK-GOV003'
require_contains .github/workflows/ci.yml 'agent-rules-kit explain --list'
require_contains .github/workflows/codeql.yml '^permissions:$'
require_contains .github/workflows/codeql.yml '^  contents: read$'
require_contains .github/workflows/codeql.yml '^  security-events: write$'
require_contains .github/workflows/codeql.yml 'queries: security-and-quality'
require_contains .github/workflows/publish-pypi.yml 'types:'
require_contains .github/workflows/publish-pypi.yml '^[[:space:]]+- published$'
require_contains .github/workflows/publish-pypi.yml '^permissions:$'
require_contains .github/workflows/publish-pypi.yml '^  contents: read$'
require_contains .github/workflows/publish-pypi.yml '^  publish:$'
require_contains .github/workflows/publish-pypi.yml 'environment: pypi'
require_contains .github/workflows/publish-pypi.yml 'id-token: write'
require_contains .github/workflows/publish-pypi.yml 'retention-days: 7'
require_contains .github/workflows/publish-pypi.yml 'Verify release ref matches package version'
require_contains .github/workflows/publish-pypi.yml 'Smoke test wheel'
printf 'OK: workflow permission and trigger sanity checks passed.\n'

printf '\n== Dependabot sanity ==\n'
require_contains .github/dependabot.yml '^version: 2$'
require_contains .github/dependabot.yml 'package-ecosystem: "pip"'
require_contains .github/dependabot.yml 'package-ecosystem: "github-actions"'
require_contains .github/dependabot.yml 'interval: "monthly"'
require_contains .github/dependabot.yml 'open-pull-requests-limit: 2'
require_absent .github/dependabot.yml 'registries:|username:|password:|token:|insecure-external-code-execution'
require_contains docs/DEPENDABOT-DEPENDENCY-GRAPH.md 'Dependabot version updates | Configured'
require_contains docs/DEPENDABOT-DEPENDENCY-GRAPH.md 'Dependabot malware alerts | Enabled'
require_contains docs/DEPENDABOT-DEPENDENCY-GRAPH.md 'Grouped security updates | Enabled'
require_contains docs/SECURITY-SUPPLY-CHAIN-EVALUATION.md 'Dependabot-created PRs still require normal Always-Green review'
printf 'OK: Dependabot sanity checks passed.\n'

printf '\n== public truth and claim boundaries ==\n'
require_contains README.md '`v0\.3\.0` is the current published GitHub Release and PyPI package for `agent-rules-kit`'
require_contains README.md 'agent-rules-kit==0\.3\.0'
require_contains README.md 'PyPI Trusted Publishing'
require_contains README.md 'not a security product, not a general repository auditor, not a secret scanner'
require_contains SECURITY.md '`v0\.3\.0` is the current published GitHub Release and PyPI package'
require_contains SECURITY.md 'Private vulnerability reporting is enabled'
require_contains SECURITY.md 'not a security scanner, provides no security guarantees'
require_contains SUPPORT.md '`v0\.3\.0` is the current published GitHub Release and PyPI package line'
require_contains SUPPORT.md 'Private vulnerability reporting is enabled'
require_contains docs/PRIVATE-VULNERABILITY-REPORTING.md 'private vulnerability reporting was enabled manually'
require_contains docs/OPENSSF-SCORECARD-EVALUATION.md 'Do not add a Scorecard workflow in this phase'
require_contains docs/V0.3.0-POST-RELEASE-AUDIT.md 'v0\.3\.0 remains published and should not be modified'
require_absent README.md 'enterprise-grade|production-ready|guarantees security|guaranteed secure|complete secret scanner'
require_absent SECURITY.md 'enterprise-grade|production-ready|guarantees security|guaranteed secure|complete secret scanner'
require_absent SUPPORT.md 'enterprise-grade|production-ready|guarantees security|guaranteed secure|complete secret scanner'
printf 'OK: public truth and claim boundary checks passed.\n'

printf '\n== v0.3.0 documentation sanity ==\n'
require_absent README.md 'doctor\.py'
require_absent docs/THREAT-MODEL.md 'v0\.2\.0 release line|post-v0\.2\.0 main state'
require_absent docs/PRODUCT-STRATEGY.md 'published v0\.2\.0 GitHub Release and current post-v0\.2\.0 main fixes|published v0\.2\.0 GitHub Release line|unreleased post-v0\.2\.0 fixes|Status: published in v0\.2\.0, with unreleased post-v0\.2\.0 fixes on main|current main contains post-v0\.2\.0 fixes'
require_absent SUPPORT.md 'Private vulnerability reporting is currently disabled'
require_contains docs/THREAT-MODEL.md 'v0\.3\.0 doctor, budget, and explain command surface'
require_contains docs/PRODUCT-STRATEGY.md 'published v0\.3\.0 GitHub Release and PyPI package line'
require_contains docs/PRODUCT-STRATEGY.md 'Status: published in v0\.3\.0'
require_contains SUPPORT.md 'Private vulnerability reporting is enabled'
require_contains docs/DEPENDABOT-DEPENDENCY-GRAPH.md 'Evidence is ranked in this record as follows'
require_contains docs/DEPENDABOT-DEPENDENCY-GRAPH.md 'vulnerability-alerts` returned HTTP `204`'
require_contains docs/DEPENDABOT-DEPENDENCY-GRAPH.md 'private-vulnerability-reporting` returned `enabled: true`'
require_contains docs/SECURITY-SUPPLY-CHAIN-EVALUATION.md 'Dependabot malware alerts and grouped security updates are manually verified as enabled'
require_contains docs/V0.3.0-POST-RELEASE-AUDIT.md 'v0\.3\.0'
printf 'OK: v0.3.0 documentation sanity checks passed.\n'

printf '\nOK: post-release audit passed.\n'
