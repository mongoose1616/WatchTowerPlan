# Design Tracking

## Active Feature Designs
| Trace ID | Design | Status | Summary | Linked Plans |
| --- | --- | --- | --- | --- |
| `trace.core_split_compatibility_wrapper_retirement` | [design.features.core_split_compatibility_wrapper_retirement](/home/j/WatchTowerPlan/docs/planning/design/features/core_split_compatibility_wrapper_retirement.md) | `active` | Defines the technical design boundary for retiring repo-specific compatibility wrappers before splitting out reusable core surfaces. | [core_split_compatibility_wrapper_retirement.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/core_split_compatibility_wrapper_retirement.md) |

## Active Implementation Plans
| Trace ID | Plan | Status | Summary | Sources | Notes |
| --- | --- | --- | --- | --- | --- |
| `trace.core_split_compatibility_wrapper_retirement` | [design.implementation.core_split_compatibility_wrapper_retirement](/home/j/WatchTowerPlan/docs/planning/design/implementation/core_split_compatibility_wrapper_retirement.md) | `active` | Breaks compatibility-wrapper retirement into a bounded implementation slice that leaves `watchtower_core` cleaner for future extraction. | [core_split_compatibility_wrapper_retirement.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_split_compatibility_wrapper_retirement.md); [core_split_compatibility_wrapper_retirement.md](/home/j/WatchTowerPlan/docs/planning/prds/core_split_compatibility_wrapper_retirement.md); [core_split_compatibility_wrapper_retirement_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/core_split_compatibility_wrapper_retirement_direction.md) | - |

## Terminal History
- `completed`: 62
- `cancelled`: 1

Use `watchtower-core query initiatives --initiative-status <status> --format json` for terminal trace browse and `watchtower-core query designs --trace-id <trace_id>` for one known design trace.

_Updated At: `2026-03-16T03:31:47Z`_
