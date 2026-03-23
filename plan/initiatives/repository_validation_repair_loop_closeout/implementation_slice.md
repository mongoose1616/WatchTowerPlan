# Repository Validation Repair Loop Closeout Implementation Slice

## Summary
Runs repeated broad validation and review loops, fixes newly surfaced issues, and closes only after two consecutive clean full passes.

## Work Breakdown
- `task.repository_validation_repair_loop_closeout.bootstrap_repository_validation_repair_loop_closeout`
  - Approve the initiative package and prepare it for execution.
- `task.repository_validation_repair_loop_closeout.run_broad_validation_pass_01`
  - Run the selected broad command set once.
  - Record all surfaced failures before making fixes.
- `task.repository_validation_repair_loop_closeout.fix_newly_surfaced_issues`
  - Repair each surfaced issue.
  - Keep code, tests, docs, and derived surfaces aligned in the same tranche when required.
- `task.repository_validation_repair_loop_closeout.run_clean_validation_pass_01`
  - Rerun the exact same broad command set.
  - Treat the result as clean pass `1` only if no new issues appear.
- `task.repository_validation_repair_loop_closeout.run_clean_validation_pass_02`
  - Rerun the exact same broad command set again without additional changes.
  - Treat the result as clean pass `2` only if no new issues appear.
- `task.repository_validation_repair_loop_closeout.closeout_repository_validation_repair_loop_closeout`
  - Summarize fixes, record the two clean passes, close the initiative, and verify `ready_for_bootstrap` repo coordination.

## Broad Command Set
- `cd /home/j/WatchTowerPlan/core/python && ./.venv/bin/python -m pytest tests/unit tests/integration ../../plan/python/tests -q`
- `cd /home/j/WatchTowerPlan/core/python && ./.venv/bin/ruff check tests ../../plan/python/tests ../../plan/python/src/watchtower_plan/testing`
- `cd /home/j/WatchTowerPlan/core/python && ./.venv/bin/watchtower-core validate all --skip-acceptance --format json`

## Reset Rule
- Any failing pass or any repair commit resets the clean-pass counter to zero.

## Commit Boundary
- If no issues are surfaced, one closeout commit is sufficient.
- If issues are surfaced and fixed, commit each coherent repair tranche after targeted verification and before restarting the clean-pass count when that improves traceability.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
