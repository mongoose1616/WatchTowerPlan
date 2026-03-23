# Core Portability Follow-up Root Pack And Query Typing Implementation Slice

## Summary
Cleans up copied-core portability debt in shared help, command docs, tests, and host query typing without changing WatchTowerPlan's current steady-state plan workspace contract.

## Initial Work Breakdown
- `task.core_portability_followup_root_pack_and_query_typing.bootstrap_core_portability_follow_up_root_pack_and_query_typing`: Bootstrap Core Portability Follow-up Root Pack And Query Typing live initiative package.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.

## Execution Tasks
- `task.core_portability_followup_root_pack_and_query_typing.capture_assessment_scope`
  - Reconfirm which copied-core assessment findings are actionable in `WatchTowerPlan/core` versus current-repo facts.
  - Record the bounded scope in the initiative package before code edits begin.
- `task.core_portability_followup_root_pack_and_query_typing.refresh_root_pack_help_and_docs`
  - Update core-owned CLI help, workspace README, command docs, and authoring reference to present first-party root packs as the primary example topology.
- `task.core_portability_followup_root_pack_and_query_typing.align_shared_core_tests_with_root_pack_defaults`
  - Convert the generic shared-core tests touched in this slice from `packs/oversight` assumptions to root-pack defaults where the test is proving generic hosted-pack support.
  - Keep explicit externalization coverage where the externalized topology is the behavior being tested.
- `task.core_portability_followup_root_pack_and_query_typing.clear_host_query_type_backlog`
  - Add explicit typed boundaries in the three host query handler modules and bring targeted `mypy` to green.
- `task.core_portability_followup_root_pack_and_query_typing.validate_and_closeout`
  - Run targeted tests, validation, and closeout updates, then land one bounded commit for the slice.

## Commit Boundary
- One atomic commit is acceptable for this slice because the docs/help/test/typing changes are tightly coupled around the same copied-core portability theme.

## Validation Commands
- `./core/python/.venv/bin/python -m mypy core/python/src/watchtower_host/cli/query_records_handlers.py core/python/src/watchtower_host/cli/query_knowledge_handlers.py core/python/src/watchtower_host/cli/query_discovery_handlers.py`
- `./core/python/.venv/bin/pytest core/python/tests/unit/test_cli.py core/python/tests/unit/test_cli_pack_commands.py core/python/tests/unit/test_schema_store_catalog_validation.py core/python/tests/integration/test_pack_externalization.py -q`
- `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json`
- `./core/python/.venv/bin/ruff check core/python/src/watchtower_host core/python/tests/unit/test_cli.py core/python/tests/unit/test_cli_pack_commands.py core/python/tests/unit/test_schema_store_catalog_validation.py core/python/tests/integration/test_pack_externalization.py`

## Closeout Criteria
- Help and core-owned pack docs no longer imply that `packs/<slug>` is the only supported hosted-pack shape.
- The touched shared-core tests prove first-party root-pack support directly.
- The targeted host query handler mypy baseline is green.
- Repo validation stays green and the initiative can be closed without unresolved discrepancies.
