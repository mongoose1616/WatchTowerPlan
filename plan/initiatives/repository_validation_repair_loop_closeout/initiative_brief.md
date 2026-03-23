# Repository Validation Repair Loop Closeout

## Summary
Runs repeated broad validation and review loops, fixes newly surfaced issues, and closes only after two consecutive clean full passes.

## Identity
- `initiative_id`: `initiative.repository_validation_repair_loop_closeout`
- `trace_id`: `trace.repository_validation_repair_loop_closeout`
- `scope_type`: `pack_wide`

## Problem
- Repository changes have accumulated across shared core, host composition, and the current internal pack.
- A clean worktree and a recent passing tranche do not prove the repository is free of newly surfaced validation, lint, test, or derived-surface drift issues.
- The repository needs one explicit repair loop that keeps running broad review and validation passes, fixes anything newly found, and only stops after two consecutive clean full passes.

## Desired Outcome
- The repository completes one bounded repair cycle with no remaining issues found by the selected broad validation loop.
- The final state is supported by two consecutive clean full passes over the same validation set without intermediate fixes.
- The initiative captures enough authored detail that a later operator or agent can resume the loop without reconstructing the stop condition.

## In Scope
- Shared-core and host validation under `core/python/**`.
- Plan-owned validation under `plan/python/**`.
- Repository-wide governed validation through `watchtower-core validate all --skip-acceptance --format json`.
- Review and repair of issues surfaced by the selected broad loop, including code, tests, docs, or derived surfaces when they are directly implicated by the failing pass.
- Initiative-task tracking and closeout for the loop itself.

## Out Of Scope
- New feature work that is not required to resolve a surfaced validation or review failure.
- Broad architectural refactors that are not justified by a failing loop result.
- Changing the stop condition mid-run without recording the reason in the initiative package.

## Operator Requirements
- Run from the shared environment rooted at `core/python/.venv`.
- Prefer repository-broad checks over narrow slices when deciding whether the loop can close.
- If a validation pass fails, fix the issue first and then restart the clean-pass count from zero.
- Do not close the initiative after one clean pass; require two consecutive clean passes over the same broad set.

## Acceptance Criteria
- `./core/python/.venv/bin/python -m pytest tests/unit tests/integration ../../plan/python/tests -q` passes twice in a row.
- `./core/python/.venv/bin/ruff check tests ../../plan/python/tests ../../plan/python/src/watchtower_plan/testing` passes twice in a row, or the broader touched-surface variant if more files need repair.
- `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json` passes twice in a row.
- Any newly surfaced issue encountered during the loop is either fixed in the tranche or explicitly recorded as a bounded follow-up with a reason that it does not block closeout.
- Repo coordination returns to `ready_for_bootstrap` after initiative closeout.

## Non-Goals
- Proving the repository has no theoretical defects beyond the selected review and validation surfaces.
- Redesigning the entire validation program.
- Replacing the existing initiative workflow with ad hoc local notes.

## Planned Task Set
- `task.repository_validation_repair_loop_closeout.bootstrap_repository_validation_repair_loop_closeout`: Bootstrap and approve the live initiative package.
- `task.repository_validation_repair_loop_closeout.run_broad_validation_pass_01`: Run the first broad repository validation and review pass and capture all surfaced issues.
- `task.repository_validation_repair_loop_closeout.fix_newly_surfaced_issues`: Repair each issue surfaced by the first failing or non-clean pass and keep docs and derived surfaces aligned.
- `task.repository_validation_repair_loop_closeout.run_clean_validation_pass_01`: Run the first clean candidate pass after fixes and verify no new issues are found.
- `task.repository_validation_repair_loop_closeout.run_clean_validation_pass_02`: Repeat the same broad validation set and require a second consecutive clean result.
- `task.repository_validation_repair_loop_closeout.closeout_repository_validation_repair_loop_closeout`: Record validation evidence, summarize fixes, close the initiative, and return coordination to `ready_for_bootstrap`.
