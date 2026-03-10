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
- Start with `docs/planning/initiatives/initiative_tracking.md` when the main question is cross-family initiative state rather than the decision corpus by itself.
- Decision records in this directory should follow [decision_record_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/decision_record_md_standard.md).
- Start new documents from [decision_record_template.md](/home/j/WatchTowerPlan/docs/templates/decision_record_template.md).
- Keep the machine-readable companion index aligned under `core/control_plane/indexes/decisions/`.
