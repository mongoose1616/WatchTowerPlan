# `core/python/tests`

## Description
`This directory contains the pack-neutral Python tests and fixtures for the shared core helper and harness packages. Keep tests here aligned with reusable-core and host boundaries plus the authored control-plane artifacts they exercise. Pack-owned tests that import or exercise a hosted pack directly belong under the owning pack root such as <pack-root>/python/tests/. The default local pytest -q loop collects only tests/unit/; use the explicit tests/unit tests/integration command when you need the full shared-core suite.`

## Paths
| Path | Description |
|---|---|
| `core/python/tests/README.md` | Describes the purpose of the Python test directory. |
| `core/python/tests/cli_command_helpers.py` | Shared JSON command-runner helper used by parser-level CLI tests in both suites. |
| `core/python/tests/pack_fixture_support.py` | Reusable synthetic pack-fixture materialization helpers for shared-core validation scenarios. |
| `core/python/tests/unit/` | Holds fast unit tests for package-local behavior. |
| `core/python/tests/integration/` | Holds integration tests that exercise multiple package surfaces together. |
| `core/python/tests/fixtures/` | Holds shared fixture data for tests when authored examples are not sufficient. |
| `<pack-root>/python/tests/` | Holds pack-owned tests that import or exercise `watchtower_<pack>` directly. |

## Notes
- Shared-core tests must stay pack-neutral even when they need pack context. Prefer synthetic fixture packs, temporary copied pack roots, or typed loader seams instead of direct live-pack imports.
- When using `tests/pack_fixture_support.py`, let the helper derive pack identity from the temporary pack root unless the test is explicitly proving override behavior.
- Pack-owned tests that exercise `watchtower_<pack>` behavior, repo-local workspace state, or pack-native orchestration belong under the owning pack root.
- Tests that require live pack-owned rendered surface IDs, initiative indexes, or pack-owned evidence/tracking state do not belong here even if they only import `watchtower_core`.
- Use `cd core/python && ./tools/verify.sh <fast|all> --fail-fast` when you want pytest-driven validation to stop on the first failure during remediation work.
