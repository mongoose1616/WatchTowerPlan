# `watchtower_plan.workspace`

## Summary
Feature-owned pack workspace services for live `plan/**` aggregation. This package owns the cross-initiative workspace orchestration and artifact-index surfaces that are specific to the WatchTowerPlan pack layout.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Responsibilities`: pack-wide workspace rebuilds, rendered overview shaping, coordination/task/readiness aggregate loading, and pack-local artifact index generation.
- `Compatibility`: top-level [plan_workspace.py](/home/j/WatchTowerPlan/plan/python/src/watchtower_plan/plan_workspace.py) and [artifact_index.py](/home/j/WatchTowerPlan/plan/python/src/watchtower_plan/artifact_index.py) remain thin forwarding shims for callers that still import the legacy paths.
- `Non-Goals`: generic rebuild/query helpers that already belong in `watchtower_core`, or new infra-family mirrors under `watchtower_plan`.

## Key Modules
- `service.py`: `PlanWorkspaceService`, plan index constants, rendered views, and coordination/readiness/task aggregation.
- `artifacts.py`: `ArtifactIndexService`, artifact-index persistence, and artifact search helpers.

## Shrink Rules
- Keep new pack-wide workspace logic here instead of adding more top-level `watchtower_plan` modules.
- When logic becomes generic across packs, move it into `watchtower_core` rather than growing this package.
