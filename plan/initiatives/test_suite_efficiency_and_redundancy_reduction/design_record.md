# Test Suite Efficiency And Redundancy Reduction Design Record

## Summary
The slowest tests are not dominated by assertion logic; they are dominated by expensive setup and sync orchestration that is repeatedly exercised in places where cheaper boundary tests would preserve the same contract.

## Measured Hotspots
- [test_cli_sync_commands.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_cli_sync_commands.py) pays the full cost of `plan sync all`, `plan sync coordination`, and several index rebuilds mainly to assert CLI JSON envelopes and output-path plumbing.
- [test_all_sync.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_all_sync.py) performs real full syncs in dry-run fixtures where some assertions only need target ordering, dependency reuse, or output-shape validation.
- [test_task_lifecycle.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_task_lifecycle.py) invokes full `PlanWorkspaceService.sync(write=True)` and `CoordinationSyncService.run(write=True)` on nearly every mutation path even when the test assertion only inspects task documents, closeout recommendation flags, or lifecycle gating errors.
- Secondary hotspots such as [test_cli_planning_query_commands.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_cli_planning_query_commands.py) and [test_initiative_closeout.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_initiative_closeout.py) also show expensive fixture setup but are not the first tranche.

## Decisions
- Prefer removing or collapsing redundant wrapper tests over adding broad test-only bypass flags to production code.
- Keep heavy end-to-end coverage only where it proves cross-surface materialization that lower-level tests cannot replace.
- For CLI tests, validate dispatch and payload shaping with monkeypatched sync services when the underlying sync behavior is already covered elsewhere.
- For task lifecycle tests, monkeypatch expensive workspace or coordination sync calls in scenarios that do not assert sync outputs.
- Defer parallel test execution tooling changes unless structural reductions still leave the broad validation gate unreasonably slow.

## First Tranche
- Rework [test_cli_sync_commands.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_cli_sync_commands.py) so full sync commands are covered once end-to-end and otherwise validated through lightweight forwarding doubles.
- Rework [test_all_sync.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_all_sync.py) so order and reuse assertions do not require repeated full sync runs over the live repository.
- Rework [test_task_lifecycle.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_task_lifecycle.py) so non-sync assertions bypass redundant coordination rebuilds.

## Follow-on Tranche
- Revisit [test_cli_planning_query_commands.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_cli_planning_query_commands.py) and [test_initiative_closeout.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_initiative_closeout.py) if the first tranche does not cut the broad suite enough.
