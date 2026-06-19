#!/usr/bin/env sh
set -eu

require_file() {
    if [ ! -f "$1" ]; then
        printf 'ERROR missing required file: %s\n' "$1"
        return 1
    fi
}

require_contains() {
    file_name="$1"
    pattern="$2"
    if ! grep -Eq "$pattern" "$file_name"; then
        printf 'ERROR expected pattern not found in %s: %s\n' "$file_name" "$pattern"
        return 1
    fi
}

require_absent() {
    file_name="$1"
    pattern="$2"
    if grep -Eq "$pattern" "$file_name"; then
        printf 'ERROR unexpected stale pattern found in %s: %s\n' "$file_name" "$pattern"
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
require_file docs/PRODUCT-STRATEGY.md
require_file docs/THREAT-MODEL.md
require_file docs/V0.3.0-POST-RELEASE-AUDIT.md
require_file scripts/check.sh
printf 'OK: required files present.\n'

printf '\n== git state ==\n'
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

printf '\n== v0.3.0 documentation sanity ==\n'
require_absent README.md 'doctor\.py'
require_absent docs/THREAT-MODEL.md 'v0\.2\.0 release line|post-v0\.2\.0 main state'
require_absent docs/PRODUCT-STRATEGY.md 'published v0\.2\.0 GitHub Release and current post-v0\.2\.0 main fixes|published v0\.2\.0 GitHub Release line|unreleased post-v0\.2\.0 fixes|Status: published in v0\.2\.0, with unreleased post-v0\.2\.0 fixes on main|current main contains post-v0\.2\.0 fixes'
require_absent SUPPORT.md 'Private vulnerability reporting is currently disabled'
require_contains docs/THREAT-MODEL.md 'v0\.3\.0 doctor, budget, and explain command surface'
require_contains docs/PRODUCT-STRATEGY.md 'published v0\.3\.0 GitHub Release and PyPI package line'
require_contains docs/PRODUCT-STRATEGY.md 'Status: published in v0\.3\.0'
require_contains SUPPORT.md 'Private vulnerability reporting is enabled'
require_contains docs/V0.3.0-POST-RELEASE-AUDIT.md 'v0\.3\.0'
printf 'OK: v0.3.0 documentation sanity checks passed.\n'

printf '\nOK: post-release audit passed.\n'
