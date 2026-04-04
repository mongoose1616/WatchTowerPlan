# `core/python/tools`

## Description
`This directory holds small workspace-local helper scripts and notes for the Python workspace when the behavior does not belong in the package itself or cannot be expressed cleanly through uv commands.`

## Boundaries
`Do not create a second source tree here. Prefer package modules and CLI entrypoints for long-lived behavior.`

## Usage
- Run `./tools/setup_dev_env.sh` from `core/python/` for the standard first-run or repair bootstrap. The script runs the documented workspace setup flow and a `watchtower-core doctor` smoke check when the required tooling is available.
- Use `./tools/dev_shell.sh` after `core/python/.venv` already exists when you want an activated interactive shell for repeated local commands.

## Files
| Path | Description |
|---|---|
| `core/python/tools/README.md` | Describes the purpose and limits of the Python workspace tools directory. |
| `core/python/tools/dev_shell.sh` | Opens an interactive shell rooted at `core/python/` with `.venv` activated when the local environment already exists. |
| `core/python/tools/git_hooks/` | Holds the shared templates used to materialize one repository-local `.githooks/` guard path. |
| `core/python/tools/verify.sh` | Runs the canonical local verification flow for fast and broad shared-core validation, with optional hosted-pack mypy, Ruff, and pytest coverage plus optional fail-fast pytest behavior. |
| `core/python/tools/install_git_hooks.sh` | Materializes the repository-local `.githooks/` path from shared templates and configures which verification mode, hosted-pack target, and optional fail-fast behavior it should run. |
