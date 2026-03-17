# `watchtower_core.repo_ops`

## Summary
WatchTowerPlan-specific planning, task, query, sync, and validation behavior that depends on the repository’s governed document and control-plane layout.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: Explicit repo-ops modules and subpackages such as `query`, `sync`, `validation`, `planning_documents`, and `task_lifecycle`.
- `Non-Goals`: Stable export-safe namespace for downstream consumers outside this repository.

## Key Surfaces
- `planning_documents.py` and `task_documents.py`: Repo-native document parsing and validation helpers.
- `planning_scaffolds.py` and `task_lifecycle.py`: Stable planning and task authoring or transition service entrypoints.
- `initiative_packages.py`: Plan-workspace initiative package bootstrap, authored-input confirmation, and readiness-gate helpers for live `plan/**` state.
- `project_context.py`: Machine-first project-context loading on top of always-loaded pack context for project-scoped runtime work.
- `plan_workspace.py`: Plan-workspace aggregate index builders, rendered-view generators, derived-surface drift checks, and pack-local query helpers for live `plan/**` state.
- `project_workspace.py`: Project-container bootstrap, project-context loading, project rendered-view generation, and project-local query helpers for live `plan/projects/**` state.
- `planning_scaffold_specs.py`, `planning_scaffold_rendering.py`, and `planning_bootstrap_support.py`: Declarative scaffold contracts, section rendering, bootstrap artifact builders, and planning-surface refresh helpers behind `planning_scaffolds.py`.
- `planning_rendered_snapshot.py`, `planning_rendered_source_assembly.py`, `planning_rendered_policy.py`, `planning_rendered_task_selection.py`, `planning_rendered_serialization.py`, and `planning_rendered_catalog_composition.py`: Private planning-rendered helpers behind the initiative and planning sync entrypoints.
- `task_companion_path_repair.py`: Governed acceptance-contract and validation-evidence task-path repair isolated from `task_lifecycle.py`.
- `query/`, `sync/`, and `validation/`: Repo-local planning and orchestration implementations behind the reusable-core query, sync, and validation boundaries.

## Related Surfaces
- `core/python/src/watchtower_core/query/README.md`
- `core/python/src/watchtower_core/sync/README.md`
- `core/python/src/watchtower_core/validation/README.md`
