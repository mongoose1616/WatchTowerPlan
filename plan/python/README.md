# `plan/python`

## Description
`This directory holds the plan-domain Python package project root. Use it only for narrow WatchTowerPlan-specific repo-local orchestration that should not live inside reusable core.`

## Boundaries
- `plan/python/**` is the approved plan-owned Python boundary.
- Keep this tree narrow. New generic loaders, validators, adapters, query helpers, sync helpers, and utilities belong in `core/python/src/watchtower_core/**`.
- `plan/.wt/**` is live plan machine state only, not a place for Python source or hand-maintained implementation logic.
- Use the shared environment under `core/python/.venv/`; do not create a second local Python workspace here.

## Paths
| Path | Description |
|---|---|
| `plan/python/README.md` | Describes the purpose of the plan-owned Python boundary and how it fits into the repo. |
| `plan/python/AGENTS.md` | Adds plan-domain Python instructions on top of the shared Python workspace rules. |
| `plan/python/pyproject.toml` | Declares the installable package metadata for the plan-owned Python project. |
| `plan/python/src/watchtower_plan/` | Holds the plan-domain Python package source tree. |
| `plan/python/src/watchtower_plan/testing/` | Holds plan-owned test-support helpers used by the plan test suite. |
| `plan/python/tests/` | Holds plan-owned tests that import or exercise `watchtower_plan` directly. |

## Notes
- `core/python/.venv/` remains the current shared local environment for repository work.
- The shared `core/python` workspace installs `watchtower-plan` as an editable local package; do not fall back to repo-local `sys.path` mutation to reach this source tree.
- Keep plan-owned tests under `plan/python/tests/` instead of `core/python/tests/`.
- Keep pack-specific test helpers under `watchtower_plan.testing` or `plan/python/tests/`; do not reintroduce direct `watchtower_plan` imports into the shared `core/python/tests/` suite.
- `watchtower_host` may compose `watchtower_plan` into the shared `watchtower-core` CLI, but reusable-core logic in `watchtower_core` must stay pack-agnostic.
- Repo-shared governed-document helpers now live under `core/python/src/watchtower_core/documentation/`; do not duplicate them back into `watchtower_plan`.
- `watchtower_plan` is not a plan-flavored mirror of `watchtower_core`; keep only repo-local plan behavior here.
- Keep plan-domain Python aligned with `requirements.md`, `decisions.md`, and the plan-root guidance under `plan/**`.
