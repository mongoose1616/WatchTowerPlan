# `watchtower_core.plan_runtime`

## Summary
Residual WatchTowerPlan-specific orchestration that still depends on this repository's current plan-workspace layout, live plan indexes, and pack-local authored-document semantics. This namespace is a transitional staging boundary, not the clean-endstate home for plan-domain Python.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: Explicit residual services and subpackages such as `plan_workspace`, `project_workspace`, `initiative_packages`, `task_lifecycle`, `query`, `sync`, and `validation`.
- `Non-Goals`: Stable export-safe namespace for downstream consumers outside this repository, a catch-all home for helpers that now fit in `control_plane`, `query`, `sync`, `rebuild`, `routing`, `workflow_execution`, `evidence`, `closeout`, or `utils`, or the permanent home for plan-domain Python once the plan-owned boundary under `plan/**` lands.

## Residual Responsibilities
- Workspace orchestration: `initiative_packages.py`, `plan_workspace.py`, and `project_workspace.py` still own live `plan/**` and `plan/projects/**` package bootstrap, rendered-surface shaping, and readiness-gate behavior that has not been extracted behind narrower reusable-core seams.
- Authored-document semantics: `front_matter_paths.py`, `markdown_semantics.py`, `reference_resolution.py`, `reference_semantics.py`, and `standards.py` still interpret this repository's governed Markdown corpus and related repo-native path rules.
- Planning lifecycle: `plan_task_state.py`, `task_lifecycle.py`, and `task_lifecycle_support.py` still own repo-local task state mutation, task-event recording, and lifecycle guardrails over live plan state.
- Pack-local aggregate services: `artifact_index.py`, `guidance_promotion.py`, and `project_context.py` still coordinate plan-pack artifacts, promotion, and project-scoped runtime loading that remain specific to the current pack.
- Residual subpackages: `query/`, `sync/`, and `validation/` remain the repo-local planning implementations that sit behind the reusable-core package boundaries.

## Key Surfaces
- `initiative_packages.py`: Plan-workspace initiative package bootstrap, authored-input confirmation, and readiness-gate helpers for live `plan/**` state.
- `plan_workspace.py` and `project_workspace.py`: Pack-wide and project-scoped workspace orchestration over live initiative state, rendered views, and derived-surface drift checks.
- `front_matter_paths.py`, `markdown_semantics.py`, `reference_resolution.py`, `reference_semantics.py`, and `standards.py`: Repo-native document parsing, normalization, and reference-resolution helpers for governed Markdown surfaces that still live in this repository.
- `plan_task_state.py`, `task_lifecycle.py`, and `task_lifecycle_support.py`: Live task-state loading, event writes, and lifecycle mutation support over initiative-local plan task state.
- `task_lifecycle.py` and `task_lifecycle_support.py`: Live task transition support over initiative-local plan task state.
- `guidance_promotion.py`: Governed initiative-to-guidance promotion flow with an explicit extraction stage before durable `plan/docs/**` outputs and initiative-local promotion records.
- `query/`, `sync/`, and `validation/`: Repo-local planning and orchestration implementations behind the reusable-core query, sync, and validation boundaries.

## Shrink Rules
- Prefer moving new generic helpers into explicit reusable-core packages rather than adding new top-level `plan_runtime` modules.
- Keep `plan_runtime` additions tightly scoped to plan-workspace state, repo-native authored-document semantics, or other current-pack behavior that cannot yet move behind narrower boundaries.
- Treat this namespace as transitional, keep shrinking it, and do not let live plan behavior drift back into catch-all repo-local modules when a narrower reusable boundary or the future plan-owned Python boundary is available.

## Related Surfaces
- `core/docs/standards/engineering/python_code_design_standard.md`
- `core/python/src/watchtower_core/query/README.md`
- `core/python/src/watchtower_core/sync/README.md`
- `core/python/src/watchtower_core/rebuild/README.md`
- `core/python/src/watchtower_core/routing/README.md`
- `core/python/src/watchtower_core/workflow_execution/README.md`
- `core/python/src/watchtower_core/closeout/README.md`
- `core/python/src/watchtower_core/validation/README.md`
