# `core/python/tests`

## Description
`This directory contains the pack-neutral Python tests and fixtures for the shared core helper and harness packages. Keep tests here aligned with reusable-core and host boundaries plus the authored control-plane artifacts they exercise. Pack-owned tests that import or exercise a hosted pack directly belong under the owning pack root such as plan/python/tests/. The default local pytest -q loop collects only tests/unit/; use the explicit tests/unit tests/integration command when you need the full shared-core suite.`

## Paths
| Path | Description |
|---|---|
| `core/python/tests/README.md` | Describes the purpose of the Python test directory. |
| `core/python/tests/cli_command_helpers.py` | Shared JSON command-runner helper used by parser-level CLI tests in both suites. |
| `core/python/tests/pack_fixture_support.py` | Reusable synthetic pack-fixture materialization helpers for shared-core validation scenarios. |
| `core/python/tests/unit/` | Holds fast unit tests for package-local behavior. |
| `core/python/tests/integration/` | Holds integration tests that exercise multiple package surfaces together. |
| `core/python/tests/fixtures/` | Holds shared fixture data for tests when authored examples are not sufficient. |
| `plan/python/tests/` | Holds plan-owned tests that import or exercise `watchtower_plan` directly. |

## Notes
- Shared-core tests must stay pack-neutral even when they need pack context. Prefer synthetic fixture packs, temporary copied pack roots, or typed loader seams instead of direct live-pack imports.
- Pack-owned tests that exercise `watchtower_plan` behavior, repo-local workspace state, or plan-native orchestration belong under `plan/python/tests/`.
