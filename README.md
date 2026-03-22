# `.`

## Description
`This repository is the reusable WatchTower core plus the first internal plan-domain workspace. Use the root only for repository scope, routing, current-state orientation, and top-level review. Keep the root thin: live plan state belongs under plan/, shared implementation assets belong under core/, authored shared foundations live under core/docs/foundations/, and the mirrored plan-facing foundations view lives under plan/docs/foundations/.`

## Paths
| Path | Description |
|---|---|
| `README.md` | Describes the purpose of the repository root and the main entrypoints stored here. |
| `AGENTS.md` | Defines the repository-wide wrapper instructions and routes work into `core/workflows/` and `plan/workflows/`. |
| `.github/` | Holds GitHub-hosted collaboration scaffolding such as issue forms and the pull request template. |
| `plan/` | Holds the live plan-domain workspace, machine authority root, and scoped initiative or project containers. |
| `core/docs/` | Holds shared command docs, references, templates, shared standards, and the authored foundations source. |
| `plan/docs/` | Holds durable plan-domain guidance plus the mirrored foundations family. |
| `core/` | Holds shared implementation assets and the authored control-plane tree. |

## Notes
- Current repository scope: `core/docs/foundations/repository_scope.md`
- Authoritative implementation contract: `requirements.md` and `decisions.md`.
- Treat standards, references, and older supporting docs as secondary guidance that must conform to those two files.
- Human current-state start-here: `plan/README.md`, then `plan/plan_overview.md`
- Shared workflow start-here: `core/workflows/README.md`
- Human plan workflow start-here: `plan/workflows/README.md`
- Authored foundations start-here: `core/docs/foundations/README.md`
- Mirrored plan foundations start-here: `plan/docs/foundations/README.md`
- Authored machine authority start-here: `core/control_plane/README.md`
- Machine current-state start-here: `plan/.wt/indexes/coordination_index.json`
- Machine project lookup start-here: `plan/.wt/indexes/project_index.json`
- Shared Python workspace start-here: `core/python/README.md`
- Plan-owned Python boundary start-here: `plan/python/README.md`
- Machine canonical-surface lookup: `cd core/python && ./.venv/bin/watchtower-core plan query authority --domain planning --format json`
- Legacy docs-backed planning has been purged. Use `plan/initiatives/**`, `plan/projects/**`, `plan/tracking/**`, and `core/control_plane/records/purges/**` instead.
