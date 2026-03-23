# `core/python/tests/unit`

## Description
`This directory contains the fast pack-neutral unit suite for the shared core helper and harness workspace. Tests here stay below repo-materialization and multi-surface orchestration: they exercise parser-level CLI wiring, pure helpers, registry builders, schema services, render/query helpers, boundary guards, and other narrow behaviors that can run in the default local loop.`

## Key Local Surfaces
| Path | Description |
|---|---|
| `core/python/tests/unit/README.md` | Describes the purpose of the unit-test directory. |
| `core/python/tests/unit/conftest.py` | Shared pytest fixtures for small unit-only helper patterns. |
| `core/python/tests/unit/document_semantics_fixtures.py` | Focused temporary-document writers for document-semantics rule tests. |
| `core/python/tests/unit/test_unit_suite_boundary.py` | Fail-closed guard that blocks repo-fixture helper imports and direct hosted-pack imports from the shared unit suite. |

## Suite Families
- CLI parser and handler tests stay here when they can validate shared behavior without bootstrapping a temp repo or importing a hosted pack directly. See `test_cli_route_and_path_commands.py`, `test_cli_validate_commands.py`, and `test_route_preview_handlers.py`.
- Reusable-core service tests stay here when they operate directly on governed artifacts, synthetic fixture packs, or in-memory data, such as `test_artifact_validation.py`, `test_control_plane_loader_pack_settings.py`, `test_rebuild_harness.py`, `test_schema_store_catalog_validation.py`, and `test_validation_evidence.py`.
- Boundary and policy guards stay here when they are pure import, export, or contract checks over shared surfaces, such as `test_python_tooling_contracts.py` and `test_sync_harness.py`.

## Notes
- This suite is now a true fast unit corpus.
- Keep broad parser or help assertions in the dedicated CLI family files and prefer direct handler or service tests when behavior can be validated below the top-level parser.
- Use the shared fixtures in `conftest.py` for repeated JSON-writing or similar small helper patterns instead of duplicating one-off utilities.
- Do not import `tests.fixture_repo_support` from `tests/unit/`. Any test that needs pack materialization, repo bootstrap, sync orchestration, closeout flows, or governed-doc copying belongs in `tests/integration/`.
- Do not import `watchtower_<pack>` directly from `tests/unit/`. Shared unit tests that need pack context must use synthetic fixture packs or typed loader/runtime seams instead of the live hosted pack package.
- Do not treat the current internal pack as a hidden unit-test dependency. If a shared unit test only passes because the live `plan/` workspace exists, move it to the owning pack root or replace it with synthetic fixture-pack setup.
- Keep `pytest -q` fast by moving repo-aware scenarios out of this directory instead of adding more helper shortcuts here.
