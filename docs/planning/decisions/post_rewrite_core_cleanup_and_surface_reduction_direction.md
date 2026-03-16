---
trace_id: trace.post_rewrite_core_cleanup_and_surface_reduction
id: decision.post_rewrite_core_cleanup_and_surface_reduction_direction
title: Post-Rewrite Core Cleanup and Surface Reduction Direction Decision
summary: Records the accepted cleanup direction for the confirmed post-rewrite
  review findings.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-16T07:00:01Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/repo_ops/validation/
- docs/standards/engineering/python_workspace_standard.md
---

# Post-Rewrite Core Cleanup and Surface Reduction Direction Decision

## Record Metadata
- `Trace ID`: `trace.post_rewrite_core_cleanup_and_surface_reduction`
- `Decision ID`: `decision.post_rewrite_core_cleanup_and_surface_reduction_direction`
- `Record Status`: `active`
- `Decision Status`: `proposed`
- `Linked PRDs`: `prd.post_rewrite_core_cleanup_and_surface_reduction`
- `Linked Designs`: `design.features.post_rewrite_core_cleanup_and_surface_reduction`
- `Linked Implementation Plans`: `design.implementation.post_rewrite_core_cleanup_and_surface_reduction`
- `Updated At`: `2026-03-16T07:00:01Z`

## Summary
Records the accepted cleanup direction for the confirmed post-rewrite review findings.

## Decision Statement
Prefer direct cleanup of confirmed rewrite regressions and proven-unused control-plane surfaces over compatibility-preserving shims or inventory-only retention.

## Trigger or Source Request
- Full repository review focused on code and rewrite leftovers after the core-pack restructuring.

## Current Context and Constraints
- `core/python/.venv/bin/pytest -q` currently fails because the workspace-standard integration test still expects retired compatibility wording.
- `PackContext` startup fails when a required declared surface moves away from the repository-default path because `load_known_surface()` only returns typed artifacts for hard-coded locations.
- The control-plane can validate and document inventory-only surfaces such as `repository_manifest.v1.json`, so rewrite leftovers can remain governed even when they no longer participate in runtime behavior.
- The current validation and standards baseline still treats the rewrite-era example corpus as active enforcement even though those fixtures are not part of the reusable-core load root or a live pack boundary.

## Applied References and Implications
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): compatibility aids should be temporary and cleanup should prefer explicit boundaries once migration help is no longer needed.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): `pytest`, `ruff`, and `mypy` remain the default workspace validation contract, so a failing full `pytest` run is a release-blocking regression.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/README.md): pack settings are the reusable-core startup root, so required-surface loading must follow declarations rather than hidden repo-specific assumptions.

## Affected Surfaces
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/repo_ops/validation/
- docs/standards/engineering/python_workspace_standard.md

## Options Considered
### Option 1
- Patch the broken integration test only and leave the rest of the review findings for later.
- Restores one failing validation quickly.
- Leaves the pack startup defect and the inventory-only governed surfaces untouched, so the reusable-core claim and maintenance burden both remain weak.

### Option 2
- Treat the review as a bounded cleanup trace: repair the failing validation contract, generalize pack startup, and retire proven-unused governed families plus the example-driven validation path.
- Aligns code, docs, validation, and the control-plane boundary with the rewrite direction in one trace.
- Requires multiple focused slices and a confirmation-pass review instead of one narrow patch.

## Chosen Outcome
Option 2 is accepted. The trace will first repair the failing workspace-standard contract, then generalize pack-surface loading so declared required paths stay typed, then remove proven-unused inventory-only governed families and the example-driven validation path, repairing the remaining references before closeout.

## Rationale and Tradeoffs
- A green test suite alone is not enough if the new reusable-core startup surface still only works for this repository's path layout.
- Removing proven-unused governed families is preferable to keeping them as documentation-only inventory because they still cost validation time, docs upkeep, and mental overhead.
- Removing example-driven validation is preferable once live artifact validation and direct schema checks already cover the same contracts, because fixtures otherwise create drift-heavy maintenance without affecting the real startup boundary.
- The cleanup stays bounded by requiring concrete evidence before retiring any family and by running a confirmation-pass review before closeout.

## Consequences and Follow-Up Impacts
- Planning docs, task records, acceptance contracts, and evidence will track the bounded cleanup sequence.
- Control-plane loader code and tests will change to make required-surface loading declaration-driven.
- The repository-manifest family is the first retired family in this trace, and later retirement candidates should use the same consumer-audit standard before removal.
- Compatibility or intake contracts, example-fixture coverage, and retained repo-local artifact catalogs are the next review targets because the current code audit shows no live reusable-core consumer for them.

## Risks, Dependencies, and Assumptions
- Assumption confirmed in this trace: `repository_manifest.v1.json` was inventory-only and not required by a live runtime or external consumer.
- Risk: pack-loading changes could break current default-path behavior if typed caching is not preserved.
- Dependency: validator registries, schema catalog entries, docs, and derived indexes must be repaired in the same slice as any governed-family retirement.

## References
- [post_rewrite_core_cleanup_and_surface_reduction.md](/home/j/WatchTowerPlan/docs/planning/prds/post_rewrite_core_cleanup_and_surface_reduction.md)
- [post_rewrite_core_cleanup_and_surface_reduction.md](/home/j/WatchTowerPlan/docs/planning/design/features/post_rewrite_core_cleanup_and_surface_reduction.md)
