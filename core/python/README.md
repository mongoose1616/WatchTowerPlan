# `core/python`

## Description
`This directory contains the consolidated Python workspace for the core helper and harness layer. Keep package code, tests, tool configuration, lockfiles, and local Python environment surfaces here, and keep authored control-plane artifacts in core/control_plane/.`

## Boundaries
`Use one local virtual environment at core/python/.venv/. Keep caches, wheels, build outputs, and egg-info directories ignored. Do not place canonical schemas, registries, contracts, policies, or indexes in this subtree.`

## Paths
| Path | Description |
|---|---|
| `core/python/AGENTS.md` | Defines Python-workspace-specific instructions for agents working under this subtree. |
| `core/python/README.md` | Describes the purpose of the Python workspace and the standard onboarding flow. |
| `core/python/.python-version` | Pins the expected Python interpreter version for the workspace. |
| `core/python/.gitignore` | Ignores the local virtual environment, caches, and build outputs. |
| `core/python/pyproject.toml` | Canonical Python project and tool configuration for the core helper and harness package. |
| `core/python/uv.lock` | Locked dependency graph used for repeatable local onboarding. |
| `core/python/src/` | Holds the `watchtower_core` package source tree. |
| `core/python/tests/` | Holds Python tests and fixtures for the package. |
| `core/python/tools/` | Holds small workspace-local helper scripts and notes when they are warranted. |

## Onboarding
1. `cd core/python`
2. `uv python install`
3. `uv sync --extra dev`
4. `source .venv/bin/activate`
5. `uv run pytest`
6. `uv run ruff check .`
7. `uv run mypy src`
8. `uv run watchtower-core doctor`

## Agent Use
- Read `core/python/AGENTS.md` before making changes under this workspace.
- Run Python package commands from `core/python/`.
- Prefer `uv run` for tests, linting, typing, and CLI execution.
- When a command supports structured output, prefer `--format json` for agent or workflow consumption instead of parsing human-readable text.
- Keep `pyproject.toml`, `uv.lock`, and command docs aligned when the Python execution contract changes.

## Command Docs
- `docs/commands/core_python/README.md`
- `docs/commands/core_python/watchtower_core.md`
- `docs/commands/core_python/watchtower_core_doctor.md`
- `docs/commands/core_python/watchtower_core_query.md`
- `docs/commands/core_python/watchtower_core_query_paths.md`
- `docs/commands/core_python/watchtower_core_query_commands.md`
- `docs/commands/core_python/watchtower_core_query_trace.md`
- `docs/commands/core_python/watchtower_core_sync.md`
- `docs/commands/core_python/watchtower_core_sync_repository_paths.md`
