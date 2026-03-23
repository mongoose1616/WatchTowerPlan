# `plan/python/tests`

## Description
`This directory contains the plan-owned Python test suite. Keep tests here when they import or exercise watchtower_plan directly, including plan-native workspace, initiative, query, task, sync, closeout, and semantic-validation behavior.`

## Boundaries
- `plan/python/tests/` owns direct `watchtower_plan` coverage.
- `core/python/tests/` remains the shared pack-neutral suite for `watchtower_core` and `watchtower_host`.
- Shared synthetic pack-fixture tests stay in `core/python/tests/`; plan tests do not need to preserve pack neutrality.
- Run this suite from the shared environment under `core/python/.venv/`.

## Paths
| Path | Description |
|---|---|
| `plan/python/tests/README.md` | Describes the purpose of the plan-owned test root. |
| `plan/python/tests/unit/` | Holds plan-owned unit tests that import `watchtower_plan` directly without repo materialization. |
| `plan/python/tests/integration/` | Holds plan-owned integration tests for live workspace, initiative, task, sync, and closeout flows. |
| `plan/python/src/watchtower_plan/testing/` | Holds reusable plan-owned test-support helpers and shared case modules. |

## Notes
- Prefer `./core/python/.venv/bin/python -m pytest ../../plan/python/tests -q` from `core/python/` for the broad plan-owned Python pass.
- Keep pack-specific test helpers under `watchtower_plan.testing` or near the tests that use them; do not move them back into `core/python/tests/`.
