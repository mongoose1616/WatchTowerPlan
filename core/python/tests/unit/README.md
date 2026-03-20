# `core/python/tests/unit`

## Description
`This directory contains the fast unit suite for the core helper and harness workspace. Tests here stay below repo-materialization and multi-surface orchestration: they exercise parser-level CLI wiring, pure helpers, registry builders, schema services, render/query helpers, boundary guards, and other narrow behaviors that can run in the default local loop.`

## Key Local Surfaces
| Path | Description |
|---|---|
| `core/python/tests/unit/README.md` | Describes the purpose of the unit-test directory. |
| `core/python/tests/unit/conftest.py` | Shared pytest fixtures for small unit-only helper patterns. |
| `core/python/tests/unit/document_semantics_fixtures.py` | Focused temporary-document writers for document-semantics rule tests. |
| `core/python/tests/unit/test_unit_suite_boundary.py` | Fail-closed guard that blocks repo-fixture helper imports from the unit suite. |

## Suite Families
- CLI parser and handler tests stay here when they can validate behavior without bootstrapping a temp repo. See `test_cli.py`, `test_cli_knowledge_query_commands.py`, `test_cli_route_and_path_commands.py`, `test_cli_validate_commands.py`, `test_plan_and_task_handlers.py`, and `test_route_and_query_handlers.py`.
- Reusable-core service tests stay here when they operate directly on governed artifacts or in-memory data, such as `test_artifact_validation.py`, `test_control_plane_loader.py`, `test_rebuild_harness.py`, `test_schema_store.py`, `test_validation_evidence.py`, and `test_validation_suite_service.py`.
- Boundary and policy guards stay here when they are pure import, export, vocabulary, or contract checks, such as `test_plan_python_boundary.py`, `test_python_tooling_contracts.py`, `test_planning_vocabulary.py`, `test_retention_policy.py`, and `test_sync_harness.py`.

## Notes
- This suite is now a true fast unit corpus.
- Keep broad parser or help assertions in the dedicated CLI family files and prefer direct handler or service tests when behavior can be validated below the top-level parser.
- Use the shared fixtures in `conftest.py` for repeated JSON-writing or similar small helper patterns instead of duplicating one-off utilities.
- Do not import `tests.fixture_repo_support` from `tests/unit/`. Any test that needs pack materialization, repo bootstrap, sync orchestration, closeout flows, or governed-doc copying belongs in `tests/integration/`.
- Keep `pytest -q` fast by moving repo-aware scenarios out of this directory instead of adding more helper shortcuts here.
