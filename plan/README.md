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
- Rendered overview, initiative, and project views land in later tasks; this slice seeds only the live roots and tracked bootstrap state.
- Do not start new live work under `docs/planning/**`; the retained bootstrap trace there exists only until later cutover slices replace the old entrypoints.
