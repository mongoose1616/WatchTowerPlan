# Test Suite Efficiency And Redundancy Reduction

## Summary
Reduce the broad Python validation pass from an effectively half-hour workflow into a bounded engineering gate by eliminating redundant high-cost smoke coverage, reusing expensive fixture setup where behavior does not require full rematerialization, and isolating the smallest set of tests that still need full derived-surface rebuilds.

## Identity
- `initiative_id`: `initiative.test_suite_efficiency_and_redundancy_reduction`
- `trace_id`: `trace.test_suite_efficiency_and_redundancy_reduction`
- `scope_type`: `pack_wide`

## Baseline Findings
- The broad suite currently collects `637` tests across `95` files.
- A broad profile run of `./core/python/.venv/bin/pytest core/python/tests/unit core/python/tests/integration --durations=120 -q` was still running after `28` minutes at high CPU and was terminated as a performance defect baseline.
- Measured hotspot files:
- [test_task_lifecycle.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_task_lifecycle.py) took about `2m52s`.
- [test_cli_sync_commands.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_cli_sync_commands.py) took about `2m28s`.
- [test_all_sync.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_all_sync.py) took about `1m54s`.
- [test_cli_planning_query_commands.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_cli_planning_query_commands.py) took about `0m51s`.
- [test_initiative_closeout.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_initiative_closeout.py) took about `0m41s`.
- The dominant cost pattern is repeated full repo-sync or coordination rebuild work inside tests that primarily assert CLI wiring, task document mutation, or error gating rather than sync semantics themselves.

## Scope
- Remove redundant CLI smoke coverage where lower-level service and sync tests already validate the underlying behavior.
- Replace heavy CLI command tests with targeted forwarding tests that stub sync runtimes but still validate parser dispatch, payload shaping, and option handling.
- Reduce task lifecycle test cost by bypassing plan-wide sync rebuilds in scenarios that only need mutation and gating assertions.
- Keep at least one real end-to-end test for each expensive workflow family so the repository still validates the full runtime path.
- Avoid product-code flags that exist only to make tests fast when the same outcome can be achieved through better fixture design or targeted monkeypatching in tests.

## Initial Task Set
- `task.test_suite_efficiency_and_redundancy_reduction.bootstrap_test_suite_efficiency_and_redundancy_reduction`: Bootstrap Test Suite Efficiency And Redundancy Reduction live initiative package.
