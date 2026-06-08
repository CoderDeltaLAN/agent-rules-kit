# AGENTS.md — agent-rules-kit

This file is mandatory for every AI assistant, coding agent, or chat working on this repository.

The repository must be handled with strict CDLAN discipline. Do not improvise a new workflow.

## Current project

agent-rules-kit is a local Python CLI that diagnoses baseline quality of AI agent instruction files in repositories.

Core boundaries:

- Local-first.
- Read-only by default.
- No network access in runtime behavior.
- No LLM dependency in runtime behavior.
- No execution of commands from analyzed repositories.
- No security guarantees or exaggerated claims.
- Secret-like findings must be redacted.

## Operating modes

There are two different work modes.

### Mode 1 — Genesis / Inception

Genesis is only for creating the project from zero before remote GitHub protection exists.

During Genesis, work on main is temporarily allowed, but only under these rules:

- main must start clean before every mutation.
- Create one file at a time whenever possible.
- Before stage, the prompt/status should show exactly one untracked or modified item.
- Stage exactly one file.
- Review the staged diff visibly.
- Commit that one file.
- Return main to clean state.
- Repeat.

Genesis pattern:

- main clean.
- create one file.
- validate that file.
- status shows one change.
- stage exact file only.
- staged shows one file.
- diff staged is visible.
- no unstaged changes.
- commit.
- main clean.

Allowed exception:

- The first identity baseline may include README.md, LICENSE, and .gitignore together because they form the repository identity baseline.

### Mode 2 — Always-Green

Always-Green begins only after Genesis is closed.

Genesis is closed when:

- local main is clean;
- local checks pass;
- AGENTS.md exists;
- scripts/check.sh exists and passes;
- tests exist and pass;
- CI exists or a documented reason explains why it does not yet exist;
- remote is created intentionally;
- initial push is verified;
- main protection/ruleset is applied or explicitly tracked as a blocker.

After Genesis closes:

- Do not work directly on main.
- Create a specific branch for every logical phase.
- Read real files before editing.
- Make minimal changes.
- Run checks before stage.
- Stage exact files only.
- Never use git add .
- Review staged diff fully.
- Commit small.
- Push branch only after local gates pass.
- Open PR.
- Merge only after checks are green.
- Return main to clean synchronized state.

## Absolute prohibitions

Do not:

- use git add .;
- commit without staged review;
- push just to see if CI passes;
- create or push a remote before local Genesis gates pass;
- work on main after Genesis is closed;
- hide failing checks;
- invent unsupported claims;
- add secrets, tokens, credentials, cookies, keys, or private URLs;
- add network behavior without explicit approval;
- add LLM behavior without explicit approval;
- execute commands from repositories being analyzed;
- overwrite files without reading existing state first.

## Zsh and terminal safety

The user works in zsh.

Never use `path` as a shell variable name in zsh commands.

Reason: in zsh, `path` is tied to `PATH`. Using `path` as a variable can break PATH and make basic commands unavailable.

Use these names instead:

- item
- entry
- target
- target_dir
- file_item
- file_name
- repo_dir
- repo_root

If basic commands such as git, mkdir, chmod, cat, or python suddenly return command not found, check PATH first.

Safe temporary PATH repair:

export PATH="/usr/local/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

## Required checks

Before every commit:

- git status --short --branch
- git diff --name-status
- git diff --cached --name-status
- git diff --cached --check
- visible staged diff with git --no-pager diff --cached --no-ext-diff
- file-specific validation
- scripts/check.sh when it exists and applies

For Python files:

- compile the file;
- run related tests;
- ensure UTF-8, LF, final newline, and no trailing whitespace.

For shell files:

- sh -n file;
- executable bit must be intentional and verified when needed.

For documentation:

- no internal secrets;
- no fake claims;
- no unsupported production/security promises.

## Commit discipline

Commit messages must be small and specific.

Examples:

- chore: add repository identity baseline
- chore: add python project metadata
- chore: add package version module
- feat: add initial cli entrypoint
- test: add cli smoke tests
- chore: add local check script

Do not combine unrelated changes.

## If anything fails

Stop immediately.

Do not continue building on a failed step.

Required recovery sequence:

- inspect status;
- inspect changed files;
- identify the exact failure;
- clean or revert explicitly;
- return to the last clean commit;
- retry with smaller granularity.

Do not guess.
Do not patch blindly.
Do not keep going after a broken command.
