# `plan/python`

## Description
`This directory holds the plan-domain Python package root. Use it for WatchTowerPlan-specific runtime, query, sync, validation, and authored-document semantics that should not live inside reusable core.`

## Paths
| Path | Description |
|---|---|
| `plan/python/README.md` | Describes the purpose of the plan-owned Python boundary and how it fits into the repo. |
| `plan/python/AGENTS.md` | Adds plan-domain Python instructions on top of the shared Python workspace rules. |
| `plan/python/src/watchtower_plan/` | Holds the plan-domain Python package source tree. |

## Notes
- `core/python/.venv/` remains the current shared local environment for repository work.
- `watchtower_core` may bridge into `watchtower_plan` for repo-local CLI and closeout flows, but reusable-core logic must stay pack-agnostic.
- Keep plan-domain Python aligned with `requirements.md`, `decisions.md`, and the plan-root guidance under `plan/**`.
