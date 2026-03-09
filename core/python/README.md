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
### Quick Start
1. `cd core/python`
2. `uv python install`
3. `uv sync --extra dev`
4. `uv run watchtower-core doctor`

### Daily Use
- Default path: run commands with `uv run ...` from `core/python/`. This uses the workspace environment without requiring manual activation.
- Interactive shell path: run `./tools/dev_shell.sh` when you want a shell with `.venv` activated for repeated local commands.
- Manual fallback: run `source .venv/bin/activate` if you specifically want to activate the environment in your current shell.

### Common Commands
- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy src`
- `uv run watchtower-core --help`
- `uv run watchtower-core doctor`
- `uv run watchtower-core sync prd-index`
- `uv run watchtower-core sync decision-index`
- `uv run watchtower-core sync design-document-index`

### Commands Inside `./tools/dev_shell.sh`
- `watchtower-core --help`
- `watchtower-core doctor`
- `pytest`
- `ruff check .`
- `mypy src`

### Notes
- `uv run ...` is the default workflow for this repository.
- `source .venv/bin/activate` is optional and mainly useful for interactive shell sessions.
- `./tools/dev_shell.sh` is for interactive use and does not require `uv` once the shell is active.
- If you used `./tools/dev_shell.sh`, leave the activated shell with `exit`.
- If you activated the environment manually, leave it with `deactivate`.

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
- `docs/commands/core_python/watchtower_core_query_prds.md`
- `docs/commands/core_python/watchtower_core_query_decisions.md`
- `docs/commands/core_python/watchtower_core_query_designs.md`
- `docs/commands/core_python/watchtower_core_query_trace.md`
- `docs/commands/core_python/watchtower_core_sync.md`
- `docs/commands/core_python/watchtower_core_sync_command_index.md`
- `docs/commands/core_python/watchtower_core_sync_prd_index.md`
- `docs/commands/core_python/watchtower_core_sync_decision_index.md`
- `docs/commands/core_python/watchtower_core_sync_design_document_index.md`
- `docs/commands/core_python/watchtower_core_sync_traceability_index.md`
- `docs/commands/core_python/watchtower_core_sync_repository_paths.md`
- `docs/commands/core_python/watchtower_core_validate.md`
- `docs/commands/core_python/watchtower_core_validate_artifact.md`
- `docs/commands/core_python/watchtower_core_validate_front_matter.md`
