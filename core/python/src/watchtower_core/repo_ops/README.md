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
- `planning_scaffold_specs.py`, `planning_scaffold_rendering.py`, and `planning_bootstrap_support.py`: Declarative scaffold contracts, section rendering, bootstrap artifact builders, and planning-surface refresh helpers behind `planning_scaffolds.py`.
- `task_companion_path_repair.py`: Governed acceptance-contract and validation-evidence task-path repair isolated from `task_lifecycle.py`.
- `query/`, `sync/`, and `validation/`: Repo-local authoritative implementations behind the compatibility wrappers.

## Related Surfaces
- `core/python/src/watchtower_core/query/README.md`
- `core/python/src/watchtower_core/sync/README.md`
- `core/python/src/watchtower_core/validation/README.md`
