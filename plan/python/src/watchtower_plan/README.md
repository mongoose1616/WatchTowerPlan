# `watchtower_plan`

## Summary
WatchTowerPlan-specific plan-domain runtime that depends on this repository's current plan-workspace layout, live plan indexes, and pack-local orchestration seams. This namespace is the approved plan-owned Python boundary under `plan/**`, and it is installed into the shared `core/python` environment as a local editable package.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: Explicit plan-owned services and subpackages such as `initiatives`, `projects`, `tasks`, `promotion`, `rendering`, `workspace`, `query`, `sync`, `validation`, and `closeout`, plus thin compatibility shims for legacy top-level imports.
- `Non-Goals`: Stable export-safe namespace for downstream consumers outside this repository, a mirror of `watchtower_core`, or a catch-all home for helpers that now fit in `control_plane`, `query`, `sync`, `rebuild`, `routing`, `workflow_execution`, `evidence`, `documentation`, or `utils`.
- `Packaging Contract`: Reach this package through the shared workspace installation path, not through repo-local `sys.path` mutation inside `watchtower_core`.
- `Machine-State Boundary`: Keep live plan machine state in `plan/.wt/**`, not in this package tree.

## Governing Foundations
- [repository_scope.md](/home/j/WatchTowerPlan/core/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/core/docs/foundations/engineering_design_principles.md)
- [product_direction.md](/home/j/WatchTowerPlan/core/docs/foundations/product_direction.md)

## Governing Standards
- [python_code_design_standard.md](/home/j/WatchTowerPlan/core/docs/standards/engineering/python_code_design_standard.md)
- [core_host_pack_python_boundary_standard.md](/home/j/WatchTowerPlan/core/docs/standards/engineering/core_host_pack_python_boundary_standard.md)
- [domain_pack_authoring_standard.md](/home/j/WatchTowerPlan/core/docs/standards/engineering/domain_pack_authoring_standard.md)
- [planning_retention_and_purge_standard.md](/home/j/WatchTowerPlan/plan/docs/standards/governance/planning_retention_and_purge_standard.md)

## Responsibilities
- Feature-owned lifecycle orchestration: `initiatives/`, `projects/`, and `tasks/` own live `plan/**` bootstrap, project-container state, task mutation, and readiness-gate behavior that depends on plan-local workspace rules.
- Workspace aggregation: `workspace/` owns pack-wide derived surfaces, rendered views, overview shaping, and artifact-index generation across live `plan/**` initiative state.
- Pack-local aggregate services: `promotion/` and `rendering/` still coordinate durable guidance promotion and rendered initiative payload shaping that remain specific to the current pack.
- Plan-domain closeout: `closeout/` owns retained trace closeout, initiative-package terminal closeout helpers, and guarded purge orchestration because those flows depend on live plan workspace state and repo-local purge policy.
- Plan-owned subpackages: `query/`, `sync/`, and `validation/` remain the pack-local integrations behind reusable-core boundaries, but generic governed-surface rebuild, validation, and documentation helpers should move back into `watchtower_core`.

## Key Surfaces
- `initiatives/`: Initiative package bootstrap, authored-input confirmation, and readiness-gate helpers for live `plan/**` state.
- `projects/`: Project context loading, project-container bootstrap, and project-local rendered/query surfaces.
- `tasks/`: Live task-state loading, event writes, and lifecycle mutation support over initiative-local plan task state.
- `workspace/`: Pack-wide orchestration over live initiative state, rendered views, artifact indexes, and derived-surface drift checks. Legacy `plan_workspace.py` and `artifact_index.py` remain thin forwarding shims.
- `promotion/`: Governed initiative-to-guidance promotion flow with an explicit extraction stage before durable `plan/docs/**` outputs and initiative-local promotion records.
- `rendering/`: Shared serializers for compact and human-facing initiative payloads that support CLI, query, and rendered-surface output.
- `closeout/`: Plan-domain closeout services for retained traces, live initiative packages, and guarded trace purges.
- `query/`, `sync/`, and `validation/`: Pack-local planning integrations behind the reusable-core query, sync, validation, and documentation boundaries, with generic governed-index or document-semantics helpers expected to live back under `watchtower_core`.

## Shrink Rules
- Prefer moving new generic helpers into explicit reusable-core packages rather than growing this plan-owned namespace unnecessarily.
- Keep `watchtower_plan` additions tightly scoped to plan-workspace state or other feature-owned pack behavior that cannot move cleanly into reusable core.
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
- `plan/python/src/watchtower_plan/workspace/README.md`
- `plan/python/src/watchtower_plan/closeout/README.md`
- `core/python/src/watchtower_core/validation/README.md`
