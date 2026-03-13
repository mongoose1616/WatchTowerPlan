# `docs/planning/initiatives`

## Description
`This directory holds the cross-family initiative view for the planning corpus. Start here when you need to understand what a traced initiative is, which phase it is in, who is actively working on it, and what should happen next without opening PRDs, designs, plans, tasks, and traceability separately.`

## Paths
| Path | Description |
|---|---|
| `docs/planning/initiatives/README.md` | Describes the purpose of the initiatives directory and how it relates to the family-specific planning surfaces. |
| `docs/planning/initiatives/initiative_tracking.md` | Generated human-readable initiative board for current traced initiatives, their phases, active owners, and next steps. |

## Notes
- Use `docs/planning/coordination_tracking.md` as the root planning start-here surface.
- Use this directory for the deeper initiative-family view beneath the root coordination tracker, including broader active context and explicit terminal-history browsing.
- Use `uv run watchtower-core query coordination --format json` as the machine start-here path for active current planning state.
- Filterless `uv run watchtower-core query initiatives --format json` now defaults to active initiatives only; use `--initiative-status <status>` when you need completed, cancelled, or superseded history instead of the current active family view.
- Use `uv run watchtower-core query initiatives --initiative-status <status> --format json` when you need completed, cancelled, or superseded initiative lookup without opening the full deep planning record.
- Treat the family directories under `docs/planning/prds/`, `docs/planning/design/`, `docs/planning/decisions/`, and `docs/planning/tasks/` as the authored source surfaces.
- Treat `initiative_tracking.md` as a derived projection, not as the source of truth for PRD, design, task, or closeout content.
- Keep the machine-readable companion index aligned under `core/control_plane/indexes/initiatives/`.
- Initiative-family projections use explicit lifecycle and outcome fields; read `artifact_status` separately from `initiative_status` when a trace is already terminal.
- Use the current initiative phase model when reading the tracker:
  - `prd`
  - `design`
  - `implementation_planning`
  - `execution`
  - `validation`
  - `closeout`
  - `closed`
