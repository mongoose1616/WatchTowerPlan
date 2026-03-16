---
trace_id: trace.post_rewrite_core_cleanup_and_surface_reduction
id: design.implementation.post_rewrite_core_cleanup_and_surface_reduction
title: Post-Rewrite Core Cleanup and Surface Reduction Implementation Plan
summary: Breaks Post-Rewrite Core Cleanup and Surface Reduction into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-16T06:28:27Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/repo_ops/validation/
- docs/standards/engineering/python_workspace_standard.md
---

# Post-Rewrite Core Cleanup and Surface Reduction Implementation Plan

## Record Metadata
- `Trace ID`: `trace.post_rewrite_core_cleanup_and_surface_reduction`
- `Plan ID`: `design.implementation.post_rewrite_core_cleanup_and_surface_reduction`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.post_rewrite_core_cleanup_and_surface_reduction`
- `Linked Decisions`: `decision.post_rewrite_core_cleanup_and_surface_reduction_direction`
- `Source Designs`: `design.features.post_rewrite_core_cleanup_and_surface_reduction`
- `Linked Acceptance Contracts`: `None`
- `Updated At`: `2026-03-16T06:28:27Z`

## Summary
Breaks Post-Rewrite Core Cleanup and Surface Reduction into a bounded implementation slice.

## Source Request or Design
- Full repository review focused on code and rewrite leftovers after the core-pack restructuring.

## Scope Summary
- Covers three execution slices: the broken workspace-standard validation contract, the generic pack-context loading defect, and retirement of the first proven-unused inventory-only governed family.
- Excludes broader planning-system replacement, large-scale ledger retirement, and opportunistic cleanup that is not backed by this review loop.

## Assumptions and Constraints
- Preserve the current repository-default pack behavior while making required-surface loading generic for alternate declared paths.
- The consumer audit for `repository_manifest.v1.json` must stay empty before this slice deletes the family and repairs its companion surfaces.

## Internal Standards and Canonical References Applied
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): full workspace validation remains the default completion contract for the Python boundary.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/README.md): pack settings remain the reusable-core startup root throughout the cleanup.
- [all.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/repo_ops/validation/all.py): aggregate validation must stay deterministic while dead governed surfaces are removed.

## Proposed Technical Approach
- Land each confirmed review finding in its own small slice so code, docs, tests, and governed surfaces can be committed independently.
- Use targeted regression tests for each repaired boundary, then rerun the full validation suite before deciding whether another cleanup pass is needed inside this trace.

## Work Breakdown
1. Repair the workspace-standard integration contract, rerun targeted `pytest`, and commit the slice.
2. Generalize pack-context loading for relocated declared paths, add regression coverage, rerun targeted validation, and commit the slice.
3. Audit and retire the repository-manifest family if no live consumer exists, repair companion surfaces, rerun validation, and commit the slice.
4. Run full validation plus a confirmation-pass review loop, create follow-on tasks only if a new concrete issue remains, otherwise close the trace.

## Risks
- The repository-manifest retirement slice could uncover hidden documentation or query dependencies outside the initial audit set.
- The pack-context fix could expose additional hard-coded surface assumptions in other reusable-core startup helpers.

## Validation Plan
- Use targeted `pytest` runs for the repaired workspace-standard and pack-context boundaries as each slice lands.
- Run `core/python/.venv/bin/ruff check .`, `core/python/.venv/bin/python -m mypy src`, and `core/python/.venv/bin/watchtower-core validate all --format json` before closeout.
- Perform one final review pass focused on rewrite leftovers after the last code slice lands and only close the trace if that pass surfaces no new concrete issue.

## References
- [post_rewrite_core_cleanup_and_surface_reduction.md](/home/j/WatchTowerPlan/docs/planning/prds/post_rewrite_core_cleanup_and_surface_reduction.md)
- [post_rewrite_core_cleanup_and_surface_reduction_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/post_rewrite_core_cleanup_and_surface_reduction_direction.md)
