# Design Tracking

## Active Feature Designs
| Trace ID | Design | Status | Summary | Linked Plans |
| --- | --- | --- | --- | --- |
| `trace.capture_first_plan_workspace_bootstrap` | [design.features.capture_first_plan_workspace_bootstrap](/docs/planning/design/features/capture_first_plan_workspace_bootstrap.md) | `active` | Defines the machine-first `plan/**` workspace design and the first-tranche runtime needed to enforce capture-before-execution. | [capture_first_plan_workspace_bootstrap.md](/docs/planning/design/implementation/capture_first_plan_workspace_bootstrap.md) |

## Active Implementation Plans
| Trace ID | Plan | Status | Summary | Sources | Notes |
| --- | --- | --- | --- | --- | --- |
| `trace.capture_first_plan_workspace_bootstrap` | [design.implementation.capture_first_plan_workspace_bootstrap](/docs/planning/design/implementation/capture_first_plan_workspace_bootstrap.md) | `active` | Breaks Capture-First Plan Workspace Bootstrap into a bounded implementation slice. | [capture_first_plan_workspace_bootstrap.md](/docs/planning/design/features/capture_first_plan_workspace_bootstrap.md); [capture_first_plan_workspace_bootstrap.md](/docs/planning/prds/capture_first_plan_workspace_bootstrap.md); [capture_first_plan_workspace_bootstrap_direction.md](/docs/planning/decisions/capture_first_plan_workspace_bootstrap_direction.md) | - |

## Terminal History
- `completed`: 70
- `cancelled`: 1

Use `watchtower-core query initiatives --initiative-status <status> --format json` for terminal trace browse and `watchtower-core query designs --trace-id <trace_id>` for one known design trace.

_Updated At: `2026-03-17T03:30:21Z`_
