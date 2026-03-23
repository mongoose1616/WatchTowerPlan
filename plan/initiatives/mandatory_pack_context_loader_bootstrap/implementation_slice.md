# Mandatory Pack Context Loader Bootstrap Implementation Slice

## Summary
Makes effective pack resolution the required first phase for pack-aware loader, host, validation, and runtime operations, with full `PackContext` loading reserved for callers that actually consume pack-governed surfaces.

## Work Breakdown
- `task.mandatory_pack_context_loader_bootstrap.bootstrap_mandatory_pack_context_loader_bootstrap`
  - confirm and approve the authored initiative inputs
  - keep initiative/task/coordination surfaces aligned as the tranche progresses
- `task.mandatory_pack_context_loader_bootstrap.centralize_effective_pack_context_bootstrap`
  - add the canonical loader-owned effective pack activation path and cached full-context path
  - consolidate or remove duplicated default-pack activation helpers that no longer belong at caller sites
- `task.mandatory_pack_context_loader_bootstrap.rewire_pack_aware_runtime_neighbors`
  - switch runtime integration loading, validation context loading, doctor/default-pack helpers, and sync harness runtime loader creation to the shared bootstrap path
  - keep runtime registry default selection aligned with the same effective pack identity
- `task.mandatory_pack_context_loader_bootstrap.refresh_pack_context_invariant_docs`
  - update core-owned engineering, command, and pack-authoring docs to state the Phase 0 effective-pack activation invariant and the narrower full-context rule
  - update pack-boundary tests and fixture guidance where stale module-identity assumptions were masking the bug
- `task.mandatory_pack_context_loader_bootstrap.validate_and_closeout`
  - run targeted validation while iterating
  - finish with broad repo validation
  - close the initiative and return coordination to `ready_for_bootstrap`

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.

## Commit Boundaries
- Commit 1: loader-owned effective pack bootstrap plus reusable-core regression coverage
- Commit 2: pack-aware host/runtime/validation rewiring plus pack-boundary test hardening
- Commit 3: docs refresh, final sync, validation, and initiative closeout

## Validation Commands
- `cd core/python && ./.venv/bin/ruff check src tests ../../plan/python/tests ../../plan/python/src/watchtower_plan/testing`
- `cd core/python && ./.venv/bin/python -m mypy src ../../plan/python/src/watchtower_plan`
- `cd core/python && ./.venv/bin/python -m pytest tests/unit tests/integration ../../plan/python/tests -q`
- `cd core/python && ./.venv/bin/watchtower-core validate all --skip-acceptance --format json`

## Closeout Criteria
- Effective pack activation is centralized behind the loader and reused by pack-aware neighbors.
- Full `PackContext` loading is cached and limited to seams that actually need pack-governed surfaces.
- Copied-core regressions remain green.
- Broad validation passes on the closed state.
