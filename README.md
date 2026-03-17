# `.`

## Description
`This repository is the reusable WatchTower core plus the first internal planning-and-implementation pack workspace. Use the root as the entrypoint for repository scope, routing, current-state orientation, and top-level review. Keep the root thin: durable documentation belongs in docs/, workflow routing and task procedures belong in workflows/, and shared implementation assets belong in core/.`

## Paths
| Path | Description |
|---|---|
| `README.md` | Describes the purpose of the repository root and the main entrypoints stored here. |
| `AGENTS.md` | Defines the repository-wide wrapper instructions and points task routing to `workflows/ROUTING_TABLE.md`. |
| `.github/` | Holds GitHub-hosted collaboration scaffolding such as issue forms and the pull request template. |
| `plan/` | Holds the live plan-domain workspace, machine authority root, and scoped initiative or project containers. |
| `docs/` | Holds durable repository documentation, standards, references, and templates. |
| `workflows/` | Holds the routing table and task-execution workflow modules. |
| `core/` | Holds shared implementation assets and the authored control-plane tree. |

## Notes
- Current repository scope: `docs/foundations/repository_scope.md`
- Human current-state start-here: `plan/README.md`, then `plan/plan_overview.md`
- Human plan workflow start-here: `plan/workflows/README.md`
- Machine current-state start-here: `plan/.wt/indexes/coordination_index.json`
- Machine project lookup start-here: `plan/.wt/indexes/project_index.json`
- Machine canonical-surface lookup: `cd core/python && ./.venv/bin/watchtower-core query authority --domain planning --format json`
- Use `docs/planning/**` after the live `plan/**` surfaces point you to the deeper traced planning artifacts you need.
