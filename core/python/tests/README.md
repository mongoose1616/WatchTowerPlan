# `core/python/tests`

## Description
`This directory contains Python tests and fixtures for the core helper and harness package. Keep tests aligned with the package boundaries and the authored control-plane artifacts they exercise. The default local `pytest -q` loop collects only `tests/unit/`; use the explicit `tests/unit tests/integration` command when you need the full Python suite.`

## Paths
| Path | Description |
|---|---|
| `core/python/tests/README.md` | Describes the purpose of the Python test directory. |
| `core/python/tests/cli_command_helpers.py` | Shared JSON command-runner helper used by parser-level CLI tests in both suites. |
| `core/python/tests/fixture_repo_support.py` | Canonical temporary-repo and pack-materialization helper surface for repository-aware integration tests. |
| `core/python/tests/pack_fixture_support.py` | Reusable static pack-fixture materialization helpers for validation-pack scenarios. |
| `core/python/tests/unit/` | Holds fast unit tests for package-local behavior. |
| `core/python/tests/integration/` | Holds integration tests that exercise multiple package surfaces together. |
| `core/python/tests/fixtures/` | Holds shared fixture data for tests when authored examples are not sufficient. |
