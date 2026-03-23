# Core Pack Neutral Portability Cleanup Implementation Slice

## Summary
Removes remaining shared-core plan-specific test and documentation coupling so copied core works with any hosted pack.

## Work Breakdown
- `task.core_pack_neutral_portability_cleanup.bootstrap_core_pack_neutral_portability_cleanup`: Bootstrap, author, confirm, and approve the initiative package.
- `task.core_pack_neutral_portability_cleanup.refresh_core_pack_neutral_docs`: Update shared-core README, standards, and references so they use pack-neutral test guidance where possible.
- `task.core_pack_neutral_portability_cleanup.neutralize_shared_core_test_helpers`: Replace donor-pack defaults in shared-core fixture and helper modules with neutral example values.
- `task.core_pack_neutral_portability_cleanup.move_pack_owned_test_contracts`: Move direct `watchtower_plan` and current live `plan` contract tests out of `core/python/tests/**` into `plan/python/tests/**`.
- `task.core_pack_neutral_portability_cleanup.tighten_boundary_guards`: Update shared test-boundary guards and docs so the moved files do not drift back into the shared-core suite.
- `task.core_pack_neutral_portability_cleanup.validate_and_closeout`: Run targeted and broad validation, fix surfaced drift, close the initiative, and commit the slice.

## Commit Boundaries
- Commit 1: initiative inputs plus shared-core docs and helper neutralization.
- Commit 2: pack-owned test moves plus boundary-guard updates.
- Commit 3: validation fixes, sync, initiative closeout, and final cleanup if needed.

## Validation Commands
- `./core/python/.venv/bin/watchtower-core plan confirm-inputs --initiative-slug core_pack_neutral_portability_cleanup --write --format json`
- `./core/python/.venv/bin/watchtower-core plan approve --initiative-slug core_pack_neutral_portability_cleanup --write --format json`
- `cd core/python && ./.venv/bin/ruff check src tests ../../plan/python/tests ../../plan/python/src/watchtower_plan/testing`
- `cd core/python && ./.venv/bin/python -m mypy src ../../plan/python/src/watchtower_plan`
- `cd core/python && ./.venv/bin/python -m pytest tests/unit tests/integration ../../plan/python/tests -q`
- `cd core/python && ./.venv/bin/watchtower-core validate all --skip-acceptance --format json`

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.
