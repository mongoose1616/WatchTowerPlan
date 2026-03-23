# Core Pack Neutrality Followup Implementation Slice

## Summary
Removes remaining donor-style plan assumptions from shared core tests, fixtures, and core-owned standards while keeping legitimate current-repo pack facts scoped to plan-owned boundaries.

## Work Breakdown
- `task.core_pack_neutrality_followup.bootstrap_core_pack_neutrality_followup`
  - confirm authored inputs
  - approve the package
  - close the bootstrap task once execution is ready
- `task.core_pack_neutrality_followup.neutralize_shared_fixture_templates`
  - replace the donor-style `plan` fixture pack with a neutral fixture template
  - update `pack_fixture_support.py` to consume neutral placeholders
  - remove any unnecessary plan-specific helper branches
- `task.core_pack_neutrality_followup.split_live_plan_only_tests_from_core`
  - move plan-owned rebuild, rendered-view, or evidence tests out of `core/python/tests/**`
  - refresh boundary docs and guard tests if needed
  - genericize any remaining shared-core tests that can stay in place
- `task.core_pack_neutrality_followup.generalize_core_owned_guidance`
  - update core-owned references and standards that still use donor `plan/**` operationalization or applies-to metadata for generic hosted-pack behavior
  - keep only deliberate current-repository facts
  - refresh derived surfaces if the touched docs feed governed indexes
- `task.core_pack_neutrality_followup.validate_and_closeout`
  - run targeted validation first
  - run broad validation second
  - close out the initiative and commit the slice

## Commit Boundaries
- Commit 1: shared fixture-template neutralization plus any directly coupled shared-core test updates
- Commit 2: test-boundary moves and maintenance docs
- Commit 3: core-owned reference and standard generalization plus any required derived-surface refresh
- Commit 4: validation-only or closeout adjustments if needed

## Validation Commands
- `cd core/python && ./.venv/bin/ruff check src tests ../../plan/python/tests ../../plan/python/src/watchtower_plan/testing`
- `cd core/python && ./.venv/bin/python -m mypy src ../../plan/python/src/watchtower_plan`
- `cd core/python && ./.venv/bin/python -m pytest tests/unit tests/integration ../../plan/python/tests -q`
- `./core/python/.venv/bin/watchtower-core validate all --skip-acceptance --format json`

## Closeout Criteria
- touched shared-core fixtures and tests are pack-neutral or explicitly plan-owned
- touched core-owned docs validate and no longer use donor `plan/**` operationalization where the intent is generic
- repo coordination returns to `ready_for_bootstrap`
- the worktree is clean after commit

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
