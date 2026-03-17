# PRD Tracking

## Active PRDs
| Trace ID | PRD | Status | Summary | Linked Designs and Plans |
| --- | --- | --- | --- | --- |
| `trace.capture_first_plan_workspace_bootstrap` | [prd.capture_first_plan_workspace_bootstrap](/docs/planning/prds/capture_first_plan_workspace_bootstrap.md) | `active` | Bootstraps the new plan workspace, initiative-local machine state, and strict capture-before-execution gating for pack-wide and project-scoped initiatives. | design.features.capture_first_plan_workspace_bootstrap; design.implementation.capture_first_plan_workspace_bootstrap |

## Terminal History
- `completed`: 65
- `cancelled`: 1

Use `watchtower-core query initiatives --initiative-status <status> --format json` for terminal trace browse and `watchtower-core query planning --trace-id <trace_id> --format json` for the deep planning record behind one known PRD.

_Updated At: `2026-03-17T03:30:21Z`_
