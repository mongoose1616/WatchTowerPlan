# `core/python/tests/integration`

## Description
`This directory contains the pack-neutral integration tests that exercise multiple shared package surfaces together against authored control-plane artifacts or temporary repo materialization. Repository-aware sync, validation, loader, and host-composition flows belong here instead of in the fast unit suite. Pack-owned orchestration, closeout, workspace, and live query flows that import a hosted pack directly belong under that pack's python/tests/ root instead of here.`

## Key Local Surfaces
| Path | Description |
|---|---|
| `core/python/tests/integration/README.md` | Describes the purpose of the integration-test directory. |
| `core/python/tests/integration/control_plane_artifact_helpers.py` | Shared JSON and front-matter helpers for the focused integration artifact suites. |
| `core/python/tests/integration/test_release_commands.py` | Integration tests for the local release-gate flow, dirty-worktree protection, and recipient bootstrap smoke coverage. |
| `core/python/tests/integration/test_standard_and_template_authoring_contracts.py` | Integration tests for standards, templates, and authored operationalization contract coverage. |
| `core/python/tests/integration/test_validate_all_cli.py` | CLI integration tests for the aggregate validation entrypoint. |
| `core/python/tests/integration/test_validation_pack_commands.py` | Integration tests for pack-scoped validation suite command execution. |
| `<pack-root>/python/tests/integration/` | Pack-owned integration tests for one hosted pack's direct runtime, workspace, orchestration, and current-repository contract behavior. |

## Notes
- Repo-aware tests that materialize synthetic or copied pack state for shared-core validation should land here by default.
- Tests that import `watchtower_<pack>` directly or exercise pack-native workspace, task, closeout, or query behavior belong under the owning pack's `python/tests/` root instead of in the shared integration suite.
- Shared integration tests that need pack context should load synthetic fixture packs or copied pack roots through helpers such as `pack_fixture_support.py`; they should not import the live hosted pack package directly.
- Use module-scoped baseline repos plus per-test `copytree(...)` isolation when mutation isolation is required and setup cost would otherwise dominate the file.
- Use `materialize_acceptance_and_evidence_paths(..., REPO_ROOT)` when acceptance or evidence fixtures reference governed docs so integration scenarios exercise real Markdown sources instead of placeholder files.
