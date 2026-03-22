# `watchtower_plan.workspace`

## Summary
Feature-owned pack workspace services for live `plan/**` aggregation. This package owns the cross-initiative workspace orchestration and artifact-index surfaces that are specific to the WatchTowerPlan pack layout.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Responsibilities`: pack-wide workspace rebuilds, rendered overview shaping, coordination/task/readiness aggregate loading, and pack-local artifact index generation.
- `Non-Goals`: generic rebuild/query helpers that already belong in `watchtower_core`, or new infra-family mirrors under `watchtower_plan`.

## Governing Foundations
- [repository_scope.md](/home/j/WatchTowerPlan/core/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/core/docs/foundations/engineering_design_principles.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/core/docs/foundations/repository_standards_posture.md)

## Governing Standards
- [python_code_design_standard.md](/home/j/WatchTowerPlan/core/docs/standards/engineering/python_code_design_standard.md)
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/core/docs/standards/engineering/engineering_best_practices_standard.md)
- [planning_index_family_standard.md](/home/j/WatchTowerPlan/plan/docs/standards/data_contracts/planning_index_family_standard.md)
- [coordination_tracking_standard.md](/home/j/WatchTowerPlan/plan/docs/standards/governance/coordination_tracking_standard.md)

## Key Modules
- `service.py`: `PlanWorkspaceService` orchestration façade and compatibility re-exports for existing callers.
- `constants.py`, `models.py`, `search.py`, and `snapshots.py`: package-local constants, public index/search dataclasses, query filters, and initiative snapshot loading.
- `builders.py` and `rendering.py`: aggregate document construction plus rendered overview and initiative surface generation.
- `artifacts.py`: `ArtifactIndexService`, artifact-index persistence, and artifact search helpers.

## Shrink Rules
- Keep new pack-wide workspace logic here instead of adding more top-level `watchtower_plan` modules.
- When logic becomes generic across packs, move it into `watchtower_core` rather than growing this package.

## Runtime Telemetry
- Workspace sync and rebuild flows should emit nested telemetry through the active `watchtower_core.telemetry` session when they are invoked from CLI command paths.
- Keep telemetry-specific file handling out of this package. Sink resolution, JSONL writing, and stderr summaries belong to reusable core.
