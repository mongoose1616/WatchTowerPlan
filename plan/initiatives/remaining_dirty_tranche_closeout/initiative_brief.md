# Remaining Dirty Tranche Closeout

## Summary
Inventories the remaining dirty worktree, lands the validated slices as coherent commits, and returns the repository to a clean state.

## Identity
- `initiative_id`: `initiative.remaining_dirty_tranche_closeout`
- `trace_id`: `trace.remaining_dirty_tranche_closeout`
- `scope_type`: `pack_wide`

## Problem
- The repository contains a large mixed worktree that bundles already-validated architectural changes, control-plane artifact retirement, foundations refresh work, runtime refactors, and test rebalancing into one uncommitted surface.
- Leaving the tree mixed makes validation difficult to trust, obscures which changes belong together, and raises the risk of accidental conflicts or partial closeout.
- The next bounded need is not new feature development. It is to convert the current dirty tree into a sequence of coherent, validated commits while preserving the already-completed functional changes.

## Scope
- Inventory the remaining modified, deleted, and untracked files across `core/**`, `plan/**`, and repository-root governance surfaces.
- Group the worktree into conflict-safe slices that can be validated and committed independently.
- Land the retained-records retirement slice that removes `core/control_plane/ledgers/**`, promotes `core/control_plane/records/**`, and aligns the governing schemas, docs, loaders, validators, and closeout behavior.
- Land the foundations and governance refresh slice that updates the authored and mirrored foundation corpus, README governance pointers, indexes, and the review artifact.
- Land the reusable-core runtime slice that keeps public import surfaces stable while splitting hotspots such as the control-plane loader, catalog models, and related tests.
- Land the plan-runtime slice that keeps public pack behavior stable while splitting the workspace, initiatives, tasks, and promotion hotspots and rebalancing the large test files.
- Close the initiative only after repository validation passes and the worktree is clean except for intentionally deferred unrelated changes, if any remain.

## Out Of Scope
- New product-facing features unrelated to the current dirty worktree.
- Fresh architectural direction changes beyond what is already implemented in the worktree.
- Reopening ledger-retirement design decisions beyond completing and safely landing the already-authored retained-records conversion.

## Initial Task Set
- `task.remaining_dirty_tranche_closeout.bootstrap_remaining_dirty_tranche_closeout`: Bootstrap Remaining Dirty Tranche Closeout live initiative package.
