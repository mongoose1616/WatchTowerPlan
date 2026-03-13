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
| `core/python/tests/unit/test_cli_query_commands.py` | Compatibility marker that redirects historical references to the focused CLI family suites. |
| `core/python/tests/unit/test_cli_route_and_path_commands.py` | Parser-level JSON contract tests for the `query paths` and `route preview` CLI surfaces. |
| `core/python/tests/unit/test_cli_dry_run_authoring_commands.py` | Parser-level JSON contract tests for dry-run `task create` and `plan scaffold` behavior. |
| `core/python/tests/unit/test_cli_knowledge_query_commands.py` | Parser-level JSON contract tests for command, reference, foundation, standard, and workflow query families. |
| `core/python/tests/unit/test_cli_planning_query_commands.py` | Parser-level JSON contract tests for PRD, decision, design, task, initiative, coordination, authority, acceptance, evidence, and trace query families. |
| `core/python/tests/unit/test_cli_sync_commands.py` | Parser-level JSON and output-path tests for the sync command family. |
| `core/python/tests/unit/test_cli_validate_commands.py` | Parser-level JSON and evidence-recording tests for the validation command family. |
| `core/python/tests/unit/test_command_index_sync.py` | Unit tests for rebuilding the command index from registry-backed CLI metadata with companion command docs. |
| `core/python/tests/unit/test_control_plane_loader.py` | Unit tests for the high-level governed artifact loaders. |
| `core/python/tests/unit/test_decision_index_sync.py` | Unit tests for rebuilding the decision index from governed decision records, including normalized affected-surface path projection. |
| `core/python/tests/unit/document_semantics_fixtures.py` | Shared temporary-repo and fixture writers for the focused document-semantics validation suites. |
| `core/python/tests/unit/test_document_semantics_validation.py` | Compatibility marker that preserves the historical document-semantics hotspot path and points to the focused suites. |
| `core/python/tests/unit/test_document_semantics_validator_selection.py` | Unit tests for semantic validator selection plus workflow and standard heading/link entrypoint rules. |
| `core/python/tests/unit/test_document_semantics_reference_rules.py` | Unit tests for governed reference-document semantic requirements and allowed maturity wording. |
| `core/python/tests/unit/test_document_semantics_standard_rules.py` | Unit tests for standard-document link accounting and canonical path semantics. |
| `core/python/tests/unit/test_document_semantics_planning_rules.py` | Unit tests for planning-document semantic requirements around applied references and heading spacing. |
| `core/python/tests/unit/test_design_document_index_sync.py` | Unit tests for rebuilding the design-document index from governed design docs, including affected-surface and source-path relationship derivation. |
| `core/python/tests/unit/test_front_matter_validation.py` | Unit tests for registry-backed front-matter validation. |
| `core/python/tests/unit/test_github_task_sync.py` | Unit tests for push-only GitHub task sync planning behavior. |
| `core/python/tests/unit/test_governed_markdown_reference_resolution.py` | Unit tests for source-aware governed Markdown repo-path extraction across adapters, planning helpers, and derived sync services. |
| `core/python/tests/unit/test_planning_catalog_sync.py` | Unit tests for rebuilding the planning catalog and validating the deep planning query behavior against the governed artifact. |
| `core/python/tests/unit/test_projection_search_common.py` | Unit tests for the shared projection-search helper that planning, initiative, and coordination queries now share. |
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
