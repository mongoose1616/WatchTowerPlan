# `core/control_plane/indexes/coordination`

## Description
`This directory holds the machine-readable coordination index that projects one always-useful current-state view above the initiative, task, and traceability families.`

## Paths
| Path | Description |
|---|---|
| `core/control_plane/indexes/coordination/README.md` | Describes the purpose of the coordination-index directory and its current artifacts. |
| `core/control_plane/indexes/coordination/coordination_index.v1.json` | Machine-readable coordination index for current planning mode, recommended next action, actionable work, and recent closeouts. |

## Notes
- Treat this directory as a derived start-here surface, not as the source of truth for planning or task content.
- Build the coordination index from the initiative index and the task-backed active-task projection it already carries.
- Use `watchtower-core query coordination` as the default machine entrypoint for current planning state.
