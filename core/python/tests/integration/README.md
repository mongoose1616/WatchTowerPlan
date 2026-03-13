# `core/python/tests/integration`

## Description
`This directory contains integration tests that exercise multiple package surfaces together against authored control-plane artifacts. The suites are grouped by validation family so repository-aware checks stay broad while failures remain local enough to review and extend safely.`

## Files
| Path | Description |
|---|---|
| `core/python/tests/integration/README.md` | Describes the purpose of the integration-test directory. |
| `core/python/tests/integration/test_control_plane_artifacts.py` | Compatibility marker that preserves the historical hotspot path and points to the focused integration suites. |
| `core/python/tests/integration/control_plane_artifact_helpers.py` | Shared JSON and front-matter helpers for the focused integration artifact suites. |
| `core/python/tests/integration/test_control_plane_loader_and_foundation_contracts.py` | Integration tests for loader-backed artifact materialization plus foundation and entrypoint contract coverage. |
| `core/python/tests/integration/test_control_plane_artifact_schema_contracts.py` | Integration tests for schema-backed governed artifacts, examples, front-matter profiles, and canonical path contracts. |
| `core/python/tests/integration/test_standard_and_template_authoring_contracts.py` | Integration tests for standards, templates, and authored operationalization contract coverage. |
| `core/python/tests/integration/test_planning_and_workflow_authoring_contracts.py` | Integration tests for planning-document authoring contracts and workflow additional-load semantics. |
