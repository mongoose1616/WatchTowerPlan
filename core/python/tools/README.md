# `core/python/tools`

## Description
`This directory holds small workspace-local helper scripts and notes for the Python workspace when the behavior does not belong in the package itself or cannot be expressed cleanly through uv commands.`

## Boundaries
`Do not create a second source tree here. Prefer package modules and CLI entrypoints for long-lived behavior.`

## Files
| Path | Description |
|---|---|
| `core/python/tools/README.md` | Describes the purpose and limits of the Python workspace tools directory. |
| `core/python/tools/dev_shell.sh` | Opens an interactive shell rooted at `core/python/` with `.venv` activated when the local environment already exists. |
| `core/python/tools/verify.sh` | Runs the canonical local verification flow for fast and broad shared-core validation, with optional hosted-pack coverage. |
| `core/python/tools/install_git_hooks.sh` | Installs the optional repository-local pre-push hook path and configures which verification mode it should run. |
