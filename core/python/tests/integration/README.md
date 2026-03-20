# `core/python/tests/integration`

## Description
`This directory contains integration tests that exercise multiple package surfaces together against authored control-plane artifacts or temporary repo materialization. Repository-aware sync, closeout, bootstrap, workspace, and live query flows belong here instead of in the fast unit suite.`

## Key Local Surfaces
| Path | Description |
|---|---|
| `core/python/tests/integration/README.md` | Describes the purpose of the integration-test directory. |
| `core/python/tests/integration/control_plane_artifact_helpers.py` | Shared JSON and front-matter helpers for the focused integration artifact suites. |
| `core/python/tests/fixture_repo_support.py` | Canonical temporary-repo and pack-materialization helper surface for repository-aware scenarios. |
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

## Notes
- Repo-aware tests that materialize pack state, bootstrap initiatives, copy governed docs, or depend on sync or closeout orchestration should land here by default.
- Use module-scoped baseline repos plus per-test `copytree(...)` isolation when mutation isolation is required and setup cost would otherwise dominate the file.
- Use `materialize_acceptance_and_evidence_paths(..., REPO_ROOT)` when acceptance or evidence fixtures reference governed docs so integration scenarios exercise real Markdown sources instead of placeholder files.
