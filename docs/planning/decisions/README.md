# `docs/planning/decisions`

## Description
`This directory holds durable decision records for planning, governance, architecture, and standards choices that need a long-lived written record. Use it when a decision needs clear rationale, status, and downstream links rather than staying implicit in design or implementation docs.`

## Files
| Path | Description |
|---|---|
| `docs/planning/decisions/README.md` | Describes the purpose of the decisions directory, its current contents, and the standards that govern it. |
| `docs/planning/decisions/core_python_workspace_root.md` | Decision record for using core/python as the single Python workspace root. |
| `docs/planning/decisions/decision_tracking.md` | Human-readable tracker for the current decision-record corpus. |

## Notes
- Start with `plan/plan_overview.md` when the main question is the live planning state rather than the decision corpus by itself.
- Use `docs/planning/coordination_tracking.md` and `docs/planning/initiatives/initiative_tracking.md` when you need the deeper traced-planning family view behind a decision-backed change.
- Treat `decision_tracking.md` as an active-first tracker. Use `uv run watchtower-core query initiatives --initiative-status <status> --format json` for terminal trace browsing and `uv run watchtower-core query decisions --trace-id <trace_id>` for one known decision trace.
- Use `uv run watchtower-core query planning --trace-id <trace_id> --format json` when a closed decision trace needs the canonical joined planning record instead of the compact family tracker.
- Treat decision records as durable rationale, not as the only home of active policy. When an accepted rule has already been promoted into standards or other current canonical surfaces, those surviving artifacts stay authoritative.
- Decision records in this directory should follow [decision_record_md_standard.md](/docs/standards/documentation/decision_record_md_standard.md).
- Start new documents from [decision_record_template.md](/docs/templates/decision_record_template.md).
- Keep the machine-readable companion index aligned under `core/control_plane/indexes/decisions/`.
