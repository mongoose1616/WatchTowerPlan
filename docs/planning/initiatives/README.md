# `docs/planning/initiatives`

## Description
`This directory holds the cross-family initiative view for the planning corpus. Start here when you need to understand what a traced initiative is, which phase it is in, who is actively working on it, and what should happen next without opening PRDs, designs, plans, tasks, and traceability separately.`

## Paths
| Path | Description |
|---|---|
| `docs/planning/initiatives/README.md` | Describes the purpose of the initiatives directory and how it relates to the family-specific planning surfaces. |
| `docs/planning/initiatives/initiative_tracking.md` | Generated human-readable initiative board for current traced initiatives, their phases, active owners, and next steps. |

## Notes
- Use `plan/plan_overview.md` and `plan/.wt/indexes/coordination_index.json` as the live planning start-here surfaces.
- Use this directory for the deeper human initiative-family view beneath the live `plan/**` entrypoints when you need traced-planning context, broader artifact-family browsing, or explicit terminal-history lookup.
- Use `uv run watchtower-core query initiatives --format json` when you need the machine-readable live initiative-family view from `plan/.wt/indexes/initiative_index.json`.
- Filterless `uv run watchtower-core query initiatives --format json` now defaults to active initiatives only; use `--initiative-status <status>` when you need completed, cancelled, or superseded history instead of the current active family view.
- Use `uv run watchtower-core query initiatives --initiative-status <status> --format json` when you need completed, cancelled, or superseded initiative lookup without opening the full deep planning record.
- Treat the family directories under `docs/planning/prds/`, `docs/planning/design/`, and `docs/planning/decisions/` as the authored source surfaces for traced planning context.
- Treat `docs/planning/tasks/` as a derived human companion plus retained historical task corpus, not as the live source of task execution state.
- Treat `initiative_tracking.md` as a derived projection, not as the source of truth for PRD, design, live task, or closeout content.
- Keep the machine-readable companion index aligned under `plan/.wt/indexes/initiative_index.json`.
- Initiative-family projections use explicit lifecycle and outcome fields; read `artifact_status` separately from `initiative_status` when a trace is already terminal.
- Use the current initiative phase model when reading the tracker:
  - `implementation_planning`
  - `execution`
  - `closeout`
  - `closed`
