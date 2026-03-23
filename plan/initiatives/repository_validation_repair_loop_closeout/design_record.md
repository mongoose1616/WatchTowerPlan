# Repository Validation Repair Loop Closeout Design Record

## Summary
Runs repeated broad validation and review loops, fixes newly surfaced issues, and closes only after two consecutive clean full passes.

## Execution Model
- The initiative uses one explicit loop:
  1. run the broad command set
  2. capture surfaced failures or review issues
  3. fix everything found in that pass
  4. rerun the same broad command set
  5. require two consecutive clean results before closeout
- Targeted debugging commands may be inserted between broad passes, but only the broad set advances the clean-pass counter.

## Broad Validation Set
- `./core/python/.venv/bin/python -m pytest tests/unit tests/integration ../../plan/python/tests -q`
- `./core/python/.venv/bin/ruff check tests ../../plan/python/tests ../../plan/python/src/watchtower_plan/testing`
- `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json`

## Failure Handling
- Any non-zero exit code, surfaced validation issue, or newly identified review defect counts as a failed pass.
- After any fix, the next broad run becomes clean pass `1`, not clean pass `2`.
- If the same broad pass remains clean twice in a row with no intervening code changes, the stop condition is satisfied.

## Repair Scope Boundary
- Fixes may land in shared core, host, plan-owned Python, or adjacent docs when those surfaces are directly implicated by a failing loop result.
- The initiative should not grow into unrelated feature work.
- If a discovered issue would require a separate architectural tranche, capture it explicitly and leave the loop focused on closing the current repository health gap.

## Tracking Boundary
- The initiative package is machine-first and local to `plan/initiatives/repository_validation_repair_loop_closeout/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.
