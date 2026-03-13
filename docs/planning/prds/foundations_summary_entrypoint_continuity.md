---
trace_id: trace.foundations_summary_entrypoint_continuity
id: prd.foundations_summary_entrypoint_continuity
title: Foundations Summary Entrypoint Continuity PRD
summary: Restore the root SUMMARY.md surface referenced by foundations-adjacent docs
  and guard that entrypoint against future drift.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-12T23:50:46Z'
audience: shared
authority: authoritative
applies_to:
- SUMMARY.md
- README.md
- docs/foundations/README.md
- docs/foundations/repository_scope.md
- core/python/tests/integration/test_control_plane_artifacts.py
---

# Foundations Summary Entrypoint Continuity PRD

## Record Metadata
- `Trace ID`: `trace.foundations_summary_entrypoint_continuity`
- `PRD ID`: `prd.foundations_summary_entrypoint_continuity`
- `Status`: `active`
- `Linked Decisions`: `decision.foundations_summary_entrypoint_continuity_direction`
- `Linked Designs`: `design.features.foundations_summary_entrypoint_continuity`
- `Linked Implementation Plans`: `design.implementation.foundations_summary_entrypoint_continuity`
- `Updated At`: `2026-03-12T23:50:46Z`

## Summary
Restore the root SUMMARY.md surface referenced by foundations-adjacent docs and guard that entrypoint against future drift.

## Problem Statement
- Full repository validation for the foundations documentation review surfaced a
  second real issue: the root [SUMMARY.md](/home/j/WatchTowerPlan/SUMMARY.md)
  document referenced by
  [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
  and several planning follow-up slices was missing entirely.
- That removal left the foundations review route pointing to a broken entrypoint
  and caused document-semantics validation to fail across the foundations layer
  and the historical planning slices that cite the whole-repo review.
- The root [README.md](/home/j/WatchTowerPlan/README.md) still inventories
  `SUMMARY.md`, so the repository entrypoint contract and the filesystem had
  drifted out of alignment.

## Goals
- Restore a durable root `SUMMARY.md` document so the foundations entrypoints
  and historical planning references resolve again.
- Preserve the historical whole-repo review context that existing planning
  slices cite without forcing a broad rewrite of those records.
- Add fail-closed coverage so the root summary entrypoint cannot disappear again
  while root and foundations docs still depend on it.

## Non-Goals
- Re-run or replace the full whole-repo assessment itself.
- Rewrite the many historical planning documents that already cite
  `SUMMARY.md` when restoring the missing target is sufficient.
- Expand the slice into unrelated foundations or standards cleanup beyond the
  missing summary entrypoint.

## Requirements
- `req.foundations_summary_entrypoint_continuity.001`: A root
  `SUMMARY.md` document must exist and provide durable whole-repo review context
  compatible with the existing root and foundations entrypoints.
- `req.foundations_summary_entrypoint_continuity.002`: The restored summary
  entrypoint must resolve the broken links from
  [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
  and the historical planning slices that cite it.
- `req.foundations_summary_entrypoint_continuity.003`: Regression coverage must
  fail closed if the root summary entrypoint disappears again while repo
  entrypoints still reference it.

## Acceptance Criteria
- `ac.foundations_summary_entrypoint_continuity.001`: A durable
  [SUMMARY.md](/home/j/WatchTowerPlan/SUMMARY.md) exists at the repository root
  and preserves the historical whole-repo review findings referenced by the
  foundations and planning docs.
- `ac.foundations_summary_entrypoint_continuity.002`: Document-semantics
  validation no longer reports broken `SUMMARY.md` links from the foundations
  layer or the historical planning slices that cite the root summary.
- `ac.foundations_summary_entrypoint_continuity.003`: Targeted integration
  coverage plus full repository validation stay green after the root summary
  entrypoint is restored.

## Risks and Dependencies
- The restored summary should stay durable and concise; over-expanding it into a
  new living handbook would recreate the root-entrypoint sprawl that the
  foundations layer is trying to avoid.
- The fix depends on preserving enough historical context that the existing
  planning documents still cite a meaningful review artifact.
- Regression coverage should verify the existence of the entrypoint, not the
  full prose contents of the summary, so the document can evolve without brittle
  text-locking tests.

## References
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
