# `watchtower_plan`

## Summary
WatchTowerPlan-specific plan-domain runtime that depends on this repository's current plan-workspace layout, live plan indexes, and pack-local orchestration seams. This namespace is the approved plan-owned Python boundary under `plan/**`, and it is installed into the shared `core/python` environment as a local editable package.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: Explicit residual services and subpackages such as `plan_workspace`, `project_workspace`, `initiative_packages`, `task_lifecycle`, `query`, `sync`, `validation`, and `closeout`.
- `Non-Goals`: Stable export-safe namespace for downstream consumers outside this repository, a mirror of `watchtower_core`, or a catch-all home for helpers that now fit in `control_plane`, `query`, `sync`, `rebuild`, `routing`, `workflow_execution`, `evidence`, `documentation`, or `utils`.
- `Packaging Contract`: Reach this package through the shared workspace installation path, not through repo-local `sys.path` mutation inside `watchtower_core`.
- `Machine-State Boundary`: Keep live plan machine state in `plan/.wt/**`, not in this package tree.

## Responsibilities
- Workspace orchestration: `initiative_packages.py`, `plan_workspace.py`, and `project_workspace.py` still own live `plan/**` and `plan/projects/**` package bootstrap, rendered-surface shaping, and readiness-gate behavior that has not been extracted behind narrower reusable-core seams.
- Authored-document orchestration: `reference_resolution.py` still bridges plan-owned sync services into reusable documentation helpers when plan-domain sync or validation needs a freshly rebuilt reference map.
- Planning lifecycle: `plan_task_state.py`, `task_lifecycle.py`, and `task_lifecycle_support.py` still own repo-local task state mutation, task-event recording, and lifecycle guardrails over live plan state.
- Pack-local aggregate services: `artifact_index.py`, `guidance_promotion.py`, and `project_context.py` still coordinate plan-pack artifacts, promotion, and project-scoped runtime loading that remain specific to the current pack.
- Plan-domain closeout: `closeout/` owns retained trace closeout, initiative-package terminal closeout helpers, and guarded purge orchestration because those flows depend on live plan workspace state and repo-local purge policy.
- Plan-owned subpackages: `query/`, `sync/`, and `validation/` remain the repo-local planning implementations that sit behind the reusable-core package boundaries, but only for live plan-runtime behavior that cannot already live under reusable core.

## Key Surfaces
- `initiative_packages.py`: Plan-workspace initiative package bootstrap, authored-input confirmation, and readiness-gate helpers for live `plan/**` state.
- `plan_workspace.py` and `project_workspace.py`: Pack-wide and project-scoped workspace orchestration over live initiative state, rendered views, and derived-surface drift checks.
- `reference_resolution.py`: Plan-owned bridge from plan sync services into reusable documentation helper data such as rebuilt reference URL maps.
- `plan_task_state.py`, `task_lifecycle.py`, and `task_lifecycle_support.py`: Live task-state loading, event writes, and lifecycle mutation support over initiative-local plan task state.
- `guidance_promotion.py`: Governed initiative-to-guidance promotion flow with an explicit extraction stage before durable `plan/docs/**` outputs and initiative-local promotion records.
- `closeout/`: Plan-domain closeout services for retained traces, live initiative packages, and guarded trace purges.
- `query/`, `sync/`, and `validation/`: Repo-local planning and orchestration implementations behind the reusable-core query, sync, validation, and documentation boundaries, with generic governed-index or document-semantics helpers expected to live back under `watchtower_core`.

## Shrink Rules
- Prefer moving new generic helpers into explicit reusable-core packages rather than growing this plan-owned namespace unnecessarily.
- Keep `watchtower_plan` additions tightly scoped to plan-workspace state, plan-owned reference-resolution bridges, or other current-pack behavior that cannot move cleanly into reusable core.
- Do not let live plan behavior drift back into catch-all repo-local modules when a narrower reusable boundary is available.
- Do not mirror reusable-core package structure here just to create plan-flavored duplicates.

## Related Surfaces
- `core/docs/standards/engineering/python_code_design_standard.md`
- `core/python/src/watchtower_core/query/README.md`
- `core/python/src/watchtower_core/documentation/README.md`
- `core/python/src/watchtower_core/sync/README.md`
- `core/python/src/watchtower_core/rebuild/README.md`
- `core/python/src/watchtower_core/routing/README.md`
- `core/python/src/watchtower_core/workflow_execution/README.md`
- `plan/python/src/watchtower_plan/closeout/README.md`
- `core/python/src/watchtower_core/validation/README.md`
