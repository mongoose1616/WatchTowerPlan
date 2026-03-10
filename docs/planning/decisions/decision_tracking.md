# Decision Tracking

## Summary
This document provides the human-readable tracking view for durable decision records under `docs/planning/decisions/`.

## Current Decision Records
| Trace ID | Decision ID | Initiative Status | Path | Decision Status | Summary |
|---|---|---|---|---|---|
| `trace.core_python_foundation` | `decision.core_python_workspace_root` | `completed` | `docs/planning/decisions/core_python_workspace_root.md` | `accepted` | Records the decision to use core/python as the single Python workspace root alongside the versioned control plane. |

## Update Rules
- Rebuild this tracker in the same change set when a decision record is added, renamed, removed, materially retargeted, or when a trace initiative changes closeout state.
- Keep the machine-readable companion index at [decision_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/decisions/decision_index.v1.json) aligned with this tracker.
- Treat the unified traceability index at [traceability_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/traceability/traceability_index.v1.json) as the source for initiative closeout status.

## References
- [README.md](/home/j/WatchTowerPlan/docs/planning/decisions/README.md)
- [decision_record_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/decision_record_md_standard.md)
- [decision_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/decision_index_standard.md)

## Updated At
- `2026-03-09T23:02:08Z`
