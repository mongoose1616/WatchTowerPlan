# AGENTS.md

## Role
- This file applies to the [core/python](/home/j/WatchTowerPlan/core/python) subtree.
- Use it for Python-workspace-specific instructions that should guide agent behavior under this workspace.
- Keep durable policy in standards and keep task execution detail in workflow modules rather than expanding this file into a workflow.

## Scope
- Applies to `core/python/**`.
- Inherit the root [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md) first.
- This file adds Python-workspace execution rules and must not weaken repository-wide safety or documentation rules.

## Local Rules
- Treat [core/python](/home/j/WatchTowerPlan/core/python) as the only canonical Python workspace in this repository.
- Run Python package commands from `core/python/` unless a narrower subpath is explicitly required.
- Prefer `uv run <command>` for tests, linting, typechecking, CLI execution, and ad hoc package-local Python invocations.
- Use the workspace-local environment at `core/python/.venv/`; do not create alternate virtual environments under `core/` or elsewhere in the repo.
- Keep Python dependency and tool changes aligned across `pyproject.toml`, `uv.lock`, and [core/python/README.md](/home/j/WatchTowerPlan/core/python/README.md) in the same change set.
- When Python command behavior changes, update the relevant command pages under [docs/commands/core_python](/home/j/WatchTowerPlan/docs/commands/core_python/), the command index, and the workspace README in the same change set.
- Keep authored schemas, registries, contracts, policies, and indexes in [core/control_plane](/home/j/WatchTowerPlan/core/control_plane), not in the Python workspace.

## Do
- Use [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md) as the governing standard for workspace layout and tooling.
- Use [core/python/README.md](/home/j/WatchTowerPlan/core/python/README.md) as the quick-reference onboarding and command surface.
- Use `uv run watchtower-core ...` or `uv run python -m watchtower_core...` for package-local execution.

## Do Not
- Do not install Python packages globally for repository work when the workspace can manage them locally.
- Do not add parallel Python roots such as `core/src/`, `core/tests/`, or top-level CLI source trees outside `core/python/src/watchtower_core/`.
- Do not commit `.venv`, caches, wheels, or build outputs.
