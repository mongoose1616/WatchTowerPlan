# Remaining Dirty Tranche Closeout Design Record

## Summary
Inventories the remaining dirty worktree, lands the validated slices as coherent commits, and returns the repository to a clean state.

## Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/remaining_dirty_tranche_closeout/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.

## Slice Strategy
- Slice 1 is retained-record conversion. It owns the `core/control_plane/ledgers/**` retirement, `core/control_plane/records/**` additions, schema and registry alignment, retention-policy and validation updates, plan closeout and purge behavior, and the committed retained initiative package that documents the change.
- Slice 2 is foundations and governance refresh. It owns `foundations_review.md`, authored and mirrored foundations, README governance pointers, root and subtree orientation docs, and derived indexes that directly depend on those surfaces.
- Slice 3 is reusable-core concentration reduction. It owns the control-plane loader split, catalog model split, reusable-core typing and helper alignment, and the unit or integration test rebalancing tied to those shared runtime surfaces.
- Slice 4 is plan-runtime concentration reduction. It owns the workspace, initiatives, tasks, and promotion splits, plan-owned typing adjustments, plan sync and query helper alignment, and the rebalanced plan integration tests.

## Conflict-Control Rules
- Do not mix the retained-records conversion with later refactor slices. That slice changes artifact-family ownership and historical records.
- Land the foundations slice before relying on refreshed foundation indexes or README governance pointers in later commits.
- Keep reusable-core and plan-runtime refactors separate unless a minimal compatibility touch is required to preserve package boundaries.
- Rebuild and validate derived indexes and rendered views in the same slice as their governing inputs.
- Use repository-root validation at the end of the initiative even if slice-local validation passes earlier.
