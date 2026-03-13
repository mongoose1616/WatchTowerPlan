# `.`

## Description
`This repository is the governed core and planning workspace for WatchTower. Use the root as the entrypoint for repository scope, routing, current-state orientation, and top-level review. Keep the root thin: durable documentation belongs in docs/, workflow routing and task procedures belong in workflows/, and shared implementation assets belong in core/.`

## Paths
| Path | Description |
|---|---|
| `README.md` | Describes the purpose of the repository root and the main entrypoints stored here. |
| `AGENTS.md` | Defines the repository-wide wrapper instructions and points task routing to `workflows/ROUTING_TABLE.md`. |
| `.github/` | Holds GitHub-hosted collaboration scaffolding such as issue forms and the pull request template. |
| `docs/` | Holds durable repository documentation, standards, references, and templates. |
| `workflows/` | Holds the routing table and task-execution workflow modules. |
| `core/` | Holds shared implementation assets and the authored control-plane tree. |

## Notes
- Current repository scope: `docs/foundations/repository_scope.md`
- Human current-state start-here: `docs/planning/coordination_tracking.md`
- Machine current-state start-here (preferred): `cd core/python && uv run watchtower-core query coordination --format json`
- Machine current-state start-here (fallback): `cd core/python && ./.venv/bin/watchtower-core query coordination --format json`
- Machine canonical-surface lookup: `cd core/python && ./.venv/bin/watchtower-core query authority --domain planning --format json`
- Use family-specific planning directories only after the coordination surfaces point you to the deeper artifact set you need.
