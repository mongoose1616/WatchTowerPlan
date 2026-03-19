# `plan/tracking`

## Purpose
- Holds the human-readable rendered tracking views for the live `plan/**` workspace.
- Treat these files as derived companions to `plan/.wt/indexes/**`, not as authored sources of truth.

## Contents
| Path | Purpose |
| --- | --- |
| `plan/tracking/coordination_tracking.md` | Rendered coordination start-here view for active initiative and task state. |
| `plan/tracking/initiative_tracking.md` | Rendered initiative-family tracker derived from the live initiative index. |
| `plan/tracking/task_tracking.md` | Rendered task tracker derived from initiative-local live task state. |

## Rules
- Do not hand-edit rendered tracking outputs.
- Rebuild these surfaces through the corresponding `watchtower-core sync` commands or plan-workspace rebuild flows.
- Do not recreate legacy pre-cutover tracker roots; the live tracker family now belongs under `plan/tracking/`.
