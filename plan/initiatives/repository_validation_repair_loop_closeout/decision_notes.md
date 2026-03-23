# Repository Validation Repair Loop Closeout Decision Notes

## Summary
Locked execution decisions for the repair loop.

## Locked Decisions
- The loop uses repository-broad validation, not narrow optimistic sampling, as the closeout gate.
- The clean-pass counter resets to zero after any newly surfaced issue or any code or doc fix.
- The initiative stops only after two consecutive clean full passes over the same selected broad command set.
- The minimum broad command set for this initiative is:
  - `./core/python/.venv/bin/python -m pytest tests/unit tests/integration ../../plan/python/tests -q`
  - `./core/python/.venv/bin/ruff check tests ../../plan/python/tests ../../plan/python/src/watchtower_plan/testing`
  - `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json`
- If a fix expands the touched surface materially, the lint scope may broaden, but it must not narrow below the minimum set above.
- The initiative may add targeted validation during debugging, but targeted passes do not count toward the two required clean full passes.
- If a command surfaces only pre-existing long-tail runtime cost without correctness failure, that is not by itself a blocker for this initiative unless the loop reveals an actual correctness or validation defect.
