# `plan/python`

## Description
`This directory holds the plan-domain Python package project root. Use it for WatchTowerPlan-specific runtime, live planning queries, sync, validation, and authored-document semantics that should not live inside reusable core.`

## Paths
| Path | Description |
|---|---|
| `plan/python/README.md` | Describes the purpose of the plan-owned Python boundary and how it fits into the repo. |
| `plan/python/AGENTS.md` | Adds plan-domain Python instructions on top of the shared Python workspace rules. |
| `plan/python/pyproject.toml` | Declares the installable package metadata for the plan-owned Python project. |
| `plan/python/src/watchtower_plan/` | Holds the plan-domain Python package source tree. |

## Notes
- `core/python/.venv/` remains the current shared local environment for repository work.
- The shared `core/python` workspace installs `watchtower-plan` as an editable local package; do not fall back to repo-local `sys.path` mutation to reach this source tree.
- `watchtower_core` may bridge into `watchtower_plan` for repo-local CLI and closeout flows, but reusable-core logic must stay pack-agnostic.
- Keep plan-domain Python aligned with `requirements.md`, `decisions.md`, and the plan-root guidance under `plan/**`.
