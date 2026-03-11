# `core/python/tests/unit`

## Description
`This directory contains a hybrid unit and repository-contract test suite for the core helper and harness workspace. The fastest tests still exercise small functions directly, but many tests intentionally run against authored repository state, generated control-plane artifacts, and command outputs.`

## Files
| Path | Description |
|---|---|
| `core/python/tests/unit/README.md` | Describes the purpose of the unit-test directory. |
| `core/python/tests/unit/conftest.py` | Shared pytest fixtures for common JSON-writing and future unit-suite helpers. |
| `core/python/tests/unit/test_all_validation.py` | Unit tests for the registry-backed validate-all orchestration service. |
| `core/python/tests/unit/test_artifact_validation.py` | Unit tests for registry-backed JSON artifact validation. |
| `core/python/tests/unit/test_acceptance_reconciliation.py` | Unit tests for acceptance-contract lookup, evidence lookup, and semantic acceptance reconciliation. |
| `core/python/tests/unit/test_all_sync.py` | Unit tests for the registry-backed all-sync orchestration service. |
| `core/python/tests/unit/test_cli.py` | Thin smoke tests for the watchtower-core entrypoint, help output, and compatibility facades. |
| `core/python/tests/unit/test_cli_query_commands.py` | Parser-level JSON contract tests for query, route, task-create, and plan-scaffold CLI families. |
| `core/python/tests/unit/test_cli_sync_commands.py` | Parser-level JSON and output-path tests for the sync command family. |
| `core/python/tests/unit/test_cli_validate_commands.py` | Parser-level JSON and evidence-recording tests for the validation command family. |
| `core/python/tests/unit/test_command_index_sync.py` | Unit tests for rebuilding the command index from registry-backed CLI metadata with companion command docs. |
| `core/python/tests/unit/test_control_plane_loader.py` | Unit tests for the high-level governed artifact loaders. |
| `core/python/tests/unit/test_decision_index_sync.py` | Unit tests for rebuilding the decision index from governed decision records. |
| `core/python/tests/unit/test_design_document_index_sync.py` | Unit tests for rebuilding the design-document index from governed design docs. |
| `core/python/tests/unit/test_front_matter_validation.py` | Unit tests for registry-backed front-matter validation. |
| `core/python/tests/unit/test_github_task_sync.py` | Unit tests for push-only GitHub task sync planning behavior. |
| `core/python/tests/unit/test_repo_ops_compatibility.py` | Unit tests for the explicit repo-ops boundary and its compatibility shims. |
| `core/python/tests/unit/test_prd_index_sync.py` | Unit tests for rebuilding the PRD index from governed PRD documents. |
| `core/python/tests/unit/test_reference_index_sync.py` | Unit tests for rebuilding the reference index from governed reference docs. |
| `core/python/tests/unit/test_standard_index_sync.py` | Unit tests for rebuilding the standard index from governed standards docs. |
| `core/python/tests/unit/test_schema_store.py` | Unit tests for schema-catalog-backed schema resolution and validation. |
| `core/python/tests/unit/test_traceability_index_sync.py` | Unit tests for rebuilding the traceability index from governed source artifacts. |
| `core/python/tests/unit/test_validation_evidence.py` | Unit tests for durable validation-evidence document building and write flows. |
| `core/python/tests/unit/test_workspace_injection.py` | Unit tests for injected workspace mappings, logical artifact paths, and default artifact writes outside the fixed repo layout. |

## Notes
- This suite is not a pure isolated unit-test corpus. Many tests are intentionally repository-aware because the package governs authored docs, schemas, indexes, and trackers.
- Keep broad parser or help assertions in the dedicated CLI family files and prefer direct handler or service tests when behavior can be validated below the top-level parser.
- Use the shared fixtures in `conftest.py` for repeated JSON-writing or similar small helper patterns instead of duplicating one-off utilities.
