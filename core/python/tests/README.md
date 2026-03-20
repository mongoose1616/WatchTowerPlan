# `core/python/tests`

## Description
`This directory contains Python tests and fixtures for the core helper and harness package. Keep tests aligned with the package boundaries and the authored control-plane artifacts they exercise. The default local `pytest -q` loop collects only `tests/unit/`; use the explicit `tests/unit tests/integration` command when you need the full Python suite.`

## Paths
| Path | Description |
|---|---|
| `core/python/tests/README.md` | Describes the purpose of the Python test directory. |
| `core/python/tests/unit/` | Holds fast unit tests for package-local behavior. |
| `core/python/tests/integration/` | Holds integration tests that exercise multiple package surfaces together. |
| `core/python/tests/fixtures/` | Holds shared fixture data for tests when authored examples are not sufficient. |
