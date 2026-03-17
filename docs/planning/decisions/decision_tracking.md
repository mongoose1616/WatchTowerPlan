# Decision Tracking

## Active Decisions
| Trace ID | Decision | Status | Outcome | Summary |
| --- | --- | --- | --- | --- |
| `trace.capture_first_plan_workspace_bootstrap` | [decision.capture_first_plan_workspace_bootstrap_direction](/docs/planning/decisions/capture_first_plan_workspace_bootstrap_direction.md) | `active` | `accepted` | Records the accepted direction for implementing the requirements-defined `plan/**` workspace through a strict capture-first first tranche. |

## Terminal History
- `completed`: 60
- `cancelled`: 1

Use `watchtower-core query initiatives --initiative-status <status> --format json` for terminal trace browse, and `watchtower-core query decisions --trace-id <trace_id>` for one known decision trace.

_Updated At: `2026-03-17T03:30:21Z`_
