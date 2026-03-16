---
trace_id: trace.post_rewrite_core_cleanup_and_surface_reduction
id: prd.post_rewrite_core_cleanup_and_surface_reduction
title: Post-Rewrite Core Cleanup and Surface Reduction PRD
summary: Remediates confirmed post-rewrite regressions, pack-boundary defects, and
  retained low-value control-plane surfaces found in the repository review.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-16T06:28:27Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/repo_ops/validation/
- docs/standards/engineering/python_workspace_standard.md
---

# Post-Rewrite Core Cleanup and Surface Reduction PRD

## Record Metadata
- `Trace ID`: `trace.post_rewrite_core_cleanup_and_surface_reduction`
- `PRD ID`: `prd.post_rewrite_core_cleanup_and_surface_reduction`
- `Status`: `active`
- `Linked Decisions`: `decision.post_rewrite_core_cleanup_and_surface_reduction_direction`
- `Linked Designs`: `design.features.post_rewrite_core_cleanup_and_surface_reduction`
- `Linked Implementation Plans`: `design.implementation.post_rewrite_core_cleanup_and_surface_reduction`
- `Updated At`: `2026-03-16T06:28:27Z`

## Summary
Remediates confirmed post-rewrite regressions, pack-boundary defects, and retained low-value control-plane surfaces found in the repository review.

## Problem Statement
- The rewritten core-plus-pack boundary currently claims a reusable startup surface, but `core/python/.venv/bin/pytest -q` fails because the workspace-standard integration test still asserts retired compatibility wording instead of the current guardrail namespace language.
- The new `PackContext` startup path only succeeds when required surfaces stay on this repository's hard-coded paths; relocating a declared required surface in pack settings currently downgrades it to an untyped `dict` and fails startup.
- The control-plane carried inventory-only governed surfaces that added validation, schema, and documentation maintenance without a demonstrated runtime consumer. This trace retires `core/control_plane/manifests/repository_manifest.v1.json` as the first proven-unused family.

## Goals
- Restore a clean full-workspace validation baseline after the rewrite.
- Make required pack-surface startup resolve typed artifacts from declared pack settings rather than repo-specific constants.
- Remove at least one confirmed low-value retained control-plane family when no live consumer exists and repair the remaining references in the same change.

## Non-Goals
- Redesign the entire planning system or replace the broader evidence model in this trace.
- Rename repository terms to mirror STEP1 vocabulary.
- Purge retained control-plane families that have not been proven unused inside this review loop.

## Requirements
- `req.post_rewrite_core_cleanup_and_surface_reduction.001`: The rewrite follow-up trace must capture the confirmed review findings, the bounded cleanup sequence, and the task chain that drives execution.
- `req.post_rewrite_core_cleanup_and_surface_reduction.002`: The Python workspace standard and its integration assertions must describe the same current guardrail and `repo_ops` ownership boundary so the default `pytest` contract is green again.
- `req.post_rewrite_core_cleanup_and_surface_reduction.003`: `PackContext` startup must load required typed surfaces from declared pack-setting paths even when those paths differ from the repository defaults.
- `req.post_rewrite_core_cleanup_and_surface_reduction.004`: At least one confirmed inventory-only control-plane family must either be retired cleanly or be explicitly justified as still required by a live consumer, with validators, schemas, docs, and derived surfaces updated accordingly.
- `req.post_rewrite_core_cleanup_and_surface_reduction.005`: The trace must close only after full validation and one confirmation-pass review loop surface no new concrete issue inside this bounded cleanup scope.

## Acceptance Criteria
- `ac.post_rewrite_core_cleanup_and_surface_reduction.001`: The trace publishes an active PRD, accepted direction decision, active feature design, active implementation plan, aligned acceptance contract, planning-baseline evidence, and bounded execution tasks for the confirmed review findings.

## Risks and Dependencies
- Loader changes can break startup or typed caching if the new pack-surface resolution path diverges from the current default-path behavior.
- Inventory-surface retirement must fail closed if a hidden loader, query, or external consumer still depends on the family under review.
- Derived indexes, trackers, and validation contracts must stay aligned with the repaired docs and retired surfaces in the same cleanup slices.

## References
- [post_rewrite_core_cleanup_and_surface_reduction_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/post_rewrite_core_cleanup_and_surface_reduction_direction.md)
- [post_rewrite_core_cleanup_and_surface_reduction.md](/home/j/WatchTowerPlan/docs/planning/design/features/post_rewrite_core_cleanup_and_surface_reduction.md)
- [post_rewrite_core_cleanup_and_surface_reduction.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/post_rewrite_core_cleanup_and_surface_reduction.md)
