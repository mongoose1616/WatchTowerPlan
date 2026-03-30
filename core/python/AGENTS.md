# AGENTS.md

## Role
- This file applies to the [core/python](/core/python) subtree.
- Use it for Python-workspace-specific instructions that should guide agent behavior under this workspace.
- Keep durable policy in standards and keep task execution detail in workflow modules rather than expanding this file into a workflow.

## Scope
- Applies to `core/python/**`.
- Inherit the root [AGENTS.md](/AGENTS.md) first.
- This file adds Python-workspace execution rules and must not weaken repository-wide safety or documentation rules.

## Local Rules
- Treat the current foundations, shared Python standards, and active control-plane pack and runtime surfaces as the authoritative implementation contract for workspace, routing, and hosted-pack runtime behavior.
- Use existing standards, references, and helper docs only where they stay consistent with those current authority surfaces.
- Treat [core/python](/core/python) as the canonical shared Python tooling, tests, and local virtual-environment workspace in this repository. Pack-owned Python source boundaries live under the owning pack roots such as `<pack>/python/**`.
- Treat `watchtower_core/**` as the reusable-core Python namespace. Keep pack-specific orchestration and pack-local lifecycle behavior in the owning `watchtower_<pack>/**` package when that behavior is truly repo-local.
- Run Python package commands from `core/python/` unless a narrower subpath is explicitly required.
- Prefer `uv run <command>` for tests, linting, typechecking, CLI execution, and ad hoc package-local Python invocations.
- When a command supports structured output, prefer `--format json` for agent or workflow use instead of scraping human-readable text.
- Use the workspace-local environment at `core/python/.venv/`; do not create alternate virtual environments under `core/` or elsewhere in the repo.
- Keep Python dependency and tool changes aligned across `pyproject.toml`, `uv.lock`, and [core/python/README.md](/core/python/README.md) in the same change set.
- When Python command behavior changes, update the relevant command pages under [core/docs/commands/core_python](/core/docs/commands/core_python/), the command index, the workspace README, and any impacted pack-owned Python boundary docs in the same change set.
- Keep authored schemas, registries, contracts, policies, and indexes in [core/control_plane](/core/control_plane), and keep live pack machine state under the owning pack `.wt/**` roots rather than in the Python workspace.

## Do
- Use [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md) as the governing standard for workspace layout and tooling.
- Use [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md) as the governing standard for Python naming, module shape, typed boundaries, docstrings, and consolidation decisions.
- Use [core/python/README.md](/core/python/README.md) as the quick-reference onboarding and command surface.
- Use `uv run watchtower-core ...` or `uv run python -m watchtower_core...` for package-local execution.
- Keep reusable-core packages such as `adapters`, `validation`, `control_plane`, `query`, `sync`, `rebuild`, `routing`, `workflow_execution`, `evidence`, and `utils` clean under the stricter `mypy` override and `ruff` comprehension rules declared in `core/python/pyproject.toml`.
- Push generic loaders, validators, adapters, and utility logic back into reusable-core packages when they stop being pack-specific.

## Do Not
- Do not install Python packages globally for repository work when the workspace can manage them locally.
- Do not add ad hoc parallel Python roots such as `core/src/`, `core/tests/`, or top-level CLI source trees outside `core/python/src/watchtower_core/`. Pack-owned Python boundaries belong under the owning pack roots; any additional shared Python root still requires explicit approval plus companion updates to the current foundations or standards, workspace READMEs, validation coverage, and routing or command guidance.
- Do not pull repo-local pack behavior into `watchtower_core/**` just to keep nearby callers in one package.
- Do not commit `.venv`, caches, wheels, or build outputs.
