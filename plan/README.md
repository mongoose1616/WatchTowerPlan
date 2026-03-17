# `plan/`

## Description
`This directory is the live plan-domain workspace for capture-first initiative and project state. Stage 1 seeds the root, machine authority entrypoint, and scoped containers that future WatchTower-targeted implementation work will use.`

## Paths
| Path | Description |
|---|---|
| `plan/README.md` | Describes the purpose of the plan root and the main surfaces seeded here. |
| `plan/.wt/` | Holds the authoritative machine-readable plan-pack root and Stage 1 bootstrap record. |
| `plan/initiatives/` | Holds pack-wide initiative containers for live work. |
| `plan/projects/` | Holds project containers and project-scoped initiative roots. |

## Notes
- `plan/.wt/` is the authoritative machine root for new live plan-pack state.
- Use `plan/initiatives/<initiative_slug>/` for pack-wide work and `plan/projects/<project_slug>/initiatives/<initiative_slug>/` for project-scoped work.
- `plan/plan_overview.md` and the initiative-local rendered views are derived from the live machine state and must stay current with the indexes under `plan/.wt/indexes/`.
- Project containers publish their own rendered `project.md`, `repositories.md`, and `summary.md` views after bootstrap, with pack-level project lookup stored in `plan/.wt/indexes/project_index.json`.
- Do not start new live work under `docs/planning/**`; the retained bootstrap trace there exists only until later cutover slices replace the old entrypoints.
