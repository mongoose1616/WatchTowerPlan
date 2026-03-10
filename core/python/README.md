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
| `core/python/src/` | Holds the `watchtower_core` package source tree, including CLI, repo-ops, and control-plane runtime code. |
| `core/python/tests/` | Holds Python tests and fixtures for package behavior, validation, and sync/query flows. |
| `core/python/tools/` | Holds small workspace-local helper scripts such as `dev_shell.sh` when they are warranted. |

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
- `uv run watchtower-core route preview --request "review code and commit"`
- `uv run watchtower-core plan scaffold --kind prd --trace-id trace.example --document-id prd.example --title "Example PRD" --summary "Frames the example initiative." --format json`
- `uv run watchtower-core query coordination --format json`
- `uv run watchtower-core query commands --query coordination --format json`
- `uv run watchtower-core query foundations --query philosophy`
- `uv run watchtower-core query workflows --query validation`
- `uv run watchtower-core query references --query uv`
- `uv run watchtower-core query standards --category governance --format json`
- `uv run watchtower-core query tasks --task-status backlog`
- `uv run watchtower-core query tasks --blocked-only --include-dependency-details`
- `uv run watchtower-core task transition --task-id task.example.001 --task-status done --format json`
- `uv run watchtower-core query acceptance --trace-id trace.core_python_foundation`
- `uv run watchtower-core query evidence --trace-id trace.core_python_foundation --format json`
- `uv run watchtower-core query initiatives --current-phase execution`
- `uv run watchtower-core sync prd-index`
- `uv run watchtower-core sync all`
- `uv run watchtower-core sync coordination`
- `uv run watchtower-core sync route-index`
- `uv run watchtower-core sync initiative-index`
- `uv run watchtower-core sync task-index`
- `uv run watchtower-core sync github-tasks --repo owner/repo`
- `uv run watchtower-core sync github-tasks --repo owner/repo --no-label-sync`
- `uv run watchtower-core closeout initiative --trace-id trace.example --initiative-status completed --closure-reason "Delivered and validated"`
- `uv run watchtower-core validate all --skip-acceptance`
- `uv run watchtower-core validate document-semantics --path workflows/modules/code_validation.md`
- `uv run watchtower-core validate acceptance --trace-id trace.core_python_foundation --format json`
- `uv run watchtower-core validate artifact --path /tmp/pack_note.json --schema-id urn:watchtower:schema:external:pack-note:v1 --supplemental-schema-path /tmp/pack_schemas --format json`

## Command Docs
- Start with [README.md](/home/j/WatchTowerPlan/docs/commands/core_python/README.md) for command-doc navigation.
- Open [watchtower_core.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core.md) for the root command and shared options.
- Open [watchtower_core_route.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_route.md) when you need a route preview for a request or explicit task type.
- Open [watchtower_core_plan.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_plan.md) when you need one-step planning scaffolds or traced bootstrap chains.
- Use the group pages for deeper browsing:
  - [watchtower_core_plan.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_plan.md)
  - [watchtower_core_query.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_query.md)
  - [watchtower_core_task.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_task.md)
  - [watchtower_core_sync.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_sync.md)
  - [watchtower_core_validate.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_validate.md)
  - [watchtower_core_closeout.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_closeout.md)
- Prefer `uv run watchtower-core query commands --query <term> --format json` when you want the machine-readable command lookup surface.

### Commands Inside `./tools/dev_shell.sh`
- `watchtower-core --help`
- `watchtower-core doctor`
- `pytest`
- `ruff check .`
- `mypy src`

### Notes
- `uv run ...` is the default workflow for this repository.
- `uv run watchtower-core doctor` is the fastest non-mutating baseline health snapshot before a full `sync all` or `validate all` run.
- `uv run watchtower-core route preview --request "<text>"` is the fastest advisory check for how the current routing surfaces map a request onto workflow modules.
- `uv run watchtower-core query coordination --format json` is the default machine-readable current-state entrypoint and stays useful even when no initiative is active.
- `uv run watchtower-core sync coordination` now refreshes the derived coordination index in the same deterministic slice as task, traceability, and initiative surfaces.
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

## Programmatic Use
- `watchtower_core.control_plane.WorkspaceConfig` and `ControlPlaneLoader` support alternate workspace layouts instead of hard-wiring callers to this repo shape.
- `watchtower_core.control_plane.SupplementalSchemaDocument` lets external consumers register additional schemas in-memory for validation without modifying this repository's canonical schema catalog.
- `ControlPlaneLoader(... supplemental_schema_paths=...)` and `SchemaStore.from_workspace(... supplemental_schema_paths=...)` let callers load supplemental schemas from explicit files or directories for bounded external artifact validation.
