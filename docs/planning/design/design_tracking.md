# Design Tracking

## Active Feature Designs
| Trace ID | Design | Status | Summary | Linked Plans |
| --- | --- | --- | --- | --- |
| `trace.core_split_compatibility_wrapper_retirement` | [design.features.core_split_compatibility_wrapper_retirement](/home/j/WatchTowerPlan/docs/planning/design/features/core_split_compatibility_wrapper_retirement.md) | `active` | Defines the technical design boundary for retiring repo-specific compatibility wrappers before splitting out reusable core surfaces. | [core_split_compatibility_wrapper_retirement.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/core_split_compatibility_wrapper_retirement.md) |
| `trace.planning_artifact_retention_and_purge` | [design.features.planning_artifact_retention_and_purge](/home/j/WatchTowerPlan/docs/planning/design/features/planning_artifact_retention_and_purge.md) | `active` | Defines the technical design boundary for Planning Artifact Retention and Purge. | [planning_artifact_retention_and_purge.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/planning_artifact_retention_and_purge.md) |

## Active Implementation Plans
| Trace ID | Plan | Status | Summary | Sources | Notes |
| --- | --- | --- | --- | --- | --- |
| `trace.core_split_compatibility_wrapper_retirement` | [design.implementation.core_split_compatibility_wrapper_retirement](/home/j/WatchTowerPlan/docs/planning/design/implementation/core_split_compatibility_wrapper_retirement.md) | `active` | Breaks compatibility-wrapper retirement into a bounded implementation slice that leaves `watchtower_core` cleaner for future extraction. | [core_split_compatibility_wrapper_retirement.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_split_compatibility_wrapper_retirement.md); [core_split_compatibility_wrapper_retirement.md](/home/j/WatchTowerPlan/docs/planning/prds/core_split_compatibility_wrapper_retirement.md); [core_split_compatibility_wrapper_retirement_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/core_split_compatibility_wrapper_retirement_direction.md) | - |
| `trace.planning_artifact_retention_and_purge` | [design.implementation.planning_artifact_retention_and_purge](/home/j/WatchTowerPlan/docs/planning/design/implementation/planning_artifact_retention_and_purge.md) | `active` | Breaks Planning Artifact Retention and Purge into a bounded implementation slice. | [planning_artifact_retention_and_purge.md](/home/j/WatchTowerPlan/docs/planning/design/features/planning_artifact_retention_and_purge.md); [planning_artifact_retention_and_purge.md](/home/j/WatchTowerPlan/docs/planning/prds/planning_artifact_retention_and_purge.md) | - |

## Terminal History
- `completed`: 62
- `cancelled`: 1

Use `watchtower-core query initiatives --initiative-status <status> --format json` for terminal trace browse and `watchtower-core query designs --trace-id <trace_id>` for one known design trace.

_Updated At: `2026-03-16T02:14:43Z`_
