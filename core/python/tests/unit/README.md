# `core/python/tests/unit`

## Description
`This directory contains fast unit tests for package-local behavior in the core helper and harness workspace.`

## Files
| Path | Description |
|---|---|
| `core/python/tests/unit/README.md` | Describes the purpose of the unit-test directory. |
| `core/python/tests/unit/test_all_validation.py` | Unit tests for the registry-backed validate-all orchestration service. |
| `core/python/tests/unit/test_artifact_validation.py` | Unit tests for registry-backed JSON artifact validation. |
| `core/python/tests/unit/test_acceptance_reconciliation.py` | Unit tests for acceptance-contract lookup, evidence lookup, and semantic acceptance reconciliation. |
| `core/python/tests/unit/test_all_sync.py` | Unit tests for the registry-backed all-sync orchestration service. |
| `core/python/tests/unit/test_cli.py` | Unit tests for the watchtower-core CLI command surfaces. |
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
