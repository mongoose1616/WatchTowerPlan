# `core/python/tests/integration`

## Description
`This directory contains integration tests that exercise multiple package surfaces together against authored control-plane artifacts. The suites are grouped by validation family so repository-aware checks stay broad while failures remain local enough to review and extend safely.`

## Files
| Path | Description |
|---|---|
| `core/python/tests/integration/README.md` | Describes the purpose of the integration-test directory. |
| `core/python/tests/integration/control_plane_artifact_helpers.py` | Shared JSON and front-matter helpers for the focused integration artifact suites. |
| `core/python/tests/integration/test_control_plane_loader_and_foundation_contracts.py` | Integration tests for loader-backed artifact materialization plus foundation and entrypoint contract coverage. |
| `core/python/tests/integration/test_control_plane_artifact_schema_contracts.py` | Integration tests for schema-backed governed artifacts, examples, front-matter profiles, and canonical path contracts. |
| `core/python/tests/integration/test_endstate_cutover_guards.py` | Repository-level hard-cutover guards for root path removal and retired planning-model residue on active surfaces. |
| `core/python/tests/integration/test_initiative_package_service.py` | Integration tests for live initiative-package bootstrap, confirmation, approval, and closeout-adjacent state transitions. |
| `core/python/tests/integration/test_plan_workspace_service.py` | Integration tests for pack-wide plan workspace indexes, rendered views, promotions, and coordination projections. |
| `core/python/tests/integration/test_project_workspace_service.py` | Integration tests for project-scoped workspace surfaces layered on top of the pack context. |
| `core/python/tests/integration/test_standard_and_template_authoring_contracts.py` | Integration tests for standards, templates, and authored operationalization contract coverage. |
| `core/python/tests/integration/test_task_lifecycle_service.py` | Integration tests for initiative-local live task creation, updates, transitions, and dependent surface refreshes. |
| `core/python/tests/integration/test_task_workflow_end_to_end.py` | End-to-end integration tests for live task workflows, queries, tracking, and initiative projections. |
| `core/python/tests/integration/test_validate_all_cli.py` | CLI integration tests for the aggregate validation entrypoint. |
| `core/python/tests/integration/test_validation_pack_commands.py` | Integration tests for pack-scoped validation suite command execution. |
