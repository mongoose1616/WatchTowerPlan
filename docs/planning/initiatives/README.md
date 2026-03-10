# `docs/planning/initiatives`

## Description
`This directory holds the cross-family initiative view for the planning corpus. Start here when you need to understand what a traced initiative is, which phase it is in, who is actively working on it, and what should happen next without opening PRDs, designs, plans, tasks, and traceability separately.`

## Paths
| Path | Description |
|---|---|
| `docs/planning/initiatives/README.md` | Describes the purpose of the initiatives directory and how it relates to the family-specific planning surfaces. |
| `docs/planning/initiatives/initiative_tracking.md` | Generated human-readable initiative board for current traced initiatives, their phases, active owners, and next steps. |

## Notes
- Use this directory as the start-here planning surface for cross-family initiative status.
- Use `uv run watchtower-core query coordination --format json` as the machine start-here path for current planning state.
- Treat the family directories under `docs/planning/prds/`, `docs/planning/design/`, `docs/planning/decisions/`, and `docs/planning/tasks/` as the authored source surfaces.
- Treat `initiative_tracking.md` as a derived projection, not as the source of truth for PRD, design, task, or closeout content.
- Keep the machine-readable companion index aligned under `core/control_plane/indexes/initiatives/`.
- Use the current initiative phase model when reading the tracker:
  - `prd`
  - `design`
  - `implementation_planning`
  - `execution`
  - `validation`
  - `closeout`
  - `closed`
