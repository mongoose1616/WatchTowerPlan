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
- `uv run watchtower-core query foundations --query philosophy`
- `uv run watchtower-core query workflows --query validation`
- `uv run watchtower-core query references --query uv`
- `uv run watchtower-core query standards --category governance --format json`
- `uv run watchtower-core query tasks --task-status backlog`
- `uv run watchtower-core query tasks --blocked-only --include-dependency-details`
- `uv run watchtower-core query acceptance --trace-id trace.core_python_foundation`
- `uv run watchtower-core query evidence --trace-id trace.core_python_foundation --format json`
- `uv run watchtower-core sync prd-index`
- `uv run watchtower-core sync all`
- `uv run watchtower-core sync foundation-index`
- `uv run watchtower-core sync standard-index`
- `uv run watchtower-core sync workflow-index`
- `uv run watchtower-core sync reference-index`
- `uv run watchtower-core sync prd-tracking`
- `uv run watchtower-core sync task-index`
- `uv run watchtower-core sync task-tracking`
- `uv run watchtower-core sync github-tasks --repo owner/repo`
- `uv run watchtower-core sync github-tasks --repo owner/repo --no-label-sync`
- `uv run watchtower-core sync decision-index`
- `uv run watchtower-core sync decision-tracking`
- `uv run watchtower-core sync design-document-index`
- `uv run watchtower-core sync design-tracking`
- `uv run watchtower-core closeout initiative --trace-id trace.example --initiative-status completed --closure-reason "Delivered and validated"`
- `uv run watchtower-core validate all --skip-acceptance`
- `uv run watchtower-core validate document-semantics --path workflows/modules/code_validation.md`
- `uv run watchtower-core validate acceptance --trace-id trace.core_python_foundation --format json`

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
- `docs/commands/core_python/watchtower_core_query_foundations.md`
- `docs/commands/core_python/watchtower_core_query_workflows.md`
- `docs/commands/core_python/watchtower_core_query_references.md`
- `docs/commands/core_python/watchtower_core_query_standards.md`
- `docs/commands/core_python/watchtower_core_query_prds.md`
- `docs/commands/core_python/watchtower_core_query_decisions.md`
- `docs/commands/core_python/watchtower_core_query_designs.md`
- `docs/commands/core_python/watchtower_core_query_acceptance.md`
- `docs/commands/core_python/watchtower_core_query_evidence.md`
- `docs/commands/core_python/watchtower_core_query_tasks.md`
- `docs/commands/core_python/watchtower_core_query_trace.md`
- `docs/commands/core_python/watchtower_core_closeout.md`
- `docs/commands/core_python/watchtower_core_closeout_initiative.md`
- `docs/commands/core_python/watchtower_core_sync.md`
- `docs/commands/core_python/watchtower_core_sync_all.md`
- `docs/commands/core_python/watchtower_core_sync_command_index.md`
- `docs/commands/core_python/watchtower_core_sync_foundation_index.md`
- `docs/commands/core_python/watchtower_core_sync_reference_index.md`
- `docs/commands/core_python/watchtower_core_sync_standard_index.md`
- `docs/commands/core_python/watchtower_core_sync_workflow_index.md`
- `docs/commands/core_python/watchtower_core_sync_prd_index.md`
- `docs/commands/core_python/watchtower_core_sync_prd_tracking.md`
- `docs/commands/core_python/watchtower_core_sync_decision_index.md`
- `docs/commands/core_python/watchtower_core_sync_decision_tracking.md`
- `docs/commands/core_python/watchtower_core_sync_design_document_index.md`
- `docs/commands/core_python/watchtower_core_sync_design_tracking.md`
- `docs/commands/core_python/watchtower_core_sync_task_index.md`
- `docs/commands/core_python/watchtower_core_sync_task_tracking.md`
- `docs/commands/core_python/watchtower_core_sync_github_tasks.md`
- `docs/commands/core_python/watchtower_core_sync_traceability_index.md`
- `docs/commands/core_python/watchtower_core_sync_repository_paths.md`
- `docs/commands/core_python/watchtower_core_validate.md`
- `docs/commands/core_python/watchtower_core_validate_all.md`
- `docs/commands/core_python/watchtower_core_validate_acceptance.md`
- `docs/commands/core_python/watchtower_core_validate_artifact.md`
- `docs/commands/core_python/watchtower_core_validate_document_semantics.md`
- `docs/commands/core_python/watchtower_core_validate_front_matter.md`
