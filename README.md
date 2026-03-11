# `.`

## Description
`This repository is the planning workspace. Use the root as the entrypoint for repo-wide guidance, routing, and top-level orientation. Place durable documentation in docs/, workflow routing and task procedures in workflows/, and shared implementation assets in core/.`

## Paths
| Path | Description |
|---|---|
| `README.md` | Describes the purpose of the repository root and the main entrypoints stored here. |
| `SUMMARY.md` | Durable whole-repo audit and roadmap report for the current repository state. |
| `AGENTS.md` | Defines the repository-wide wrapper instructions and points task routing to `workflows/ROUTING_TABLE.md`. |
| `.github/` | Holds GitHub-hosted collaboration scaffolding such as issue forms and the pull request template. |
| `docs/` | Holds durable repository documentation, standards, references, and templates. |
| `workflows/` | Holds the routing table and task-execution workflow modules. |
| `core/` | Holds shared implementation assets and the authored control-plane tree. |

## Notes
- Human start-here: `docs/planning/coordination_tracking.md`
- Machine start-here: `cd core/python && uv run watchtower-core query coordination --format json`
- Latest whole-repo review: `SUMMARY.md`
- Use family-specific planning directories only after the coordination surfaces point you to the deeper artifact set you need.
