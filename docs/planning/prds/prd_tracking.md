# PRD Tracking

## Active PRDs
| Trace ID | PRD | Status | Summary | Linked Designs and Plans |
| --- | --- | --- | --- | --- |
| `trace.core_split_compatibility_wrapper_retirement` | [prd.core_split_compatibility_wrapper_retirement](/home/j/WatchTowerPlan/docs/planning/prds/core_split_compatibility_wrapper_retirement.md) | `active` | Retire repo-specific compatibility wrapper modules from export-safe `watchtower_core` namespaces so a future core split exposes only reusable surfaces. | design.features.core_split_compatibility_wrapper_retirement; design.implementation.core_split_compatibility_wrapper_retirement |
| `trace.planning_artifact_retention_and_purge` | [prd.planning_artifact_retention_and_purge](/home/j/WatchTowerPlan/docs/planning/prds/planning_artifact_retention_and_purge.md) | `active` | Defines a promote-then-purge retention model so closed trace-local planning artifacts do not remain in the repository indefinitely. | design.features.planning_artifact_retention_and_purge; design.implementation.planning_artifact_retention_and_purge |

## Terminal History
- `completed`: 57
- `cancelled`: 1

Use `watchtower-core query initiatives --initiative-status <status> --format json` for terminal trace browse and `watchtower-core query planning --trace-id <trace_id> --format json` for the deep planning record behind one known PRD.

_Updated At: `2026-03-16T02:06:53Z`_
