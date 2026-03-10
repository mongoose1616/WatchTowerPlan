# `core/control_plane/indexes/initiatives`

## Description
`This directory holds machine-readable initiative indexes that project the current traced planning corpus into one coordination view for queries, workflows, and local tracking surfaces.`

## Paths
| Path | Description |
|---|---|
| `core/control_plane/indexes/initiatives/README.md` | Describes the purpose of the initiative-index directory and its current artifacts. |
| `core/control_plane/indexes/initiatives/initiative_index.v1.json` | Machine-readable initiative index for current traced initiatives, their phases, active owners, and next actions. |

## Notes
- Treat this directory as a derived lookup surface, not as the source of truth for planning or task content.
- Build the initiative index from traceability plus the current planning and task indexes.
- Keep the human-readable companion tracker aligned at `docs/planning/initiatives/initiative_tracking.md`.
