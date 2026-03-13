---
trace_id: trace.summary_surface_retirement
id: prd.summary_surface_retirement
title: Summary Surface Retirement PRD
summary: Retire SUMMARY.md as a root surface, remove its dedicated restoration artifacts,
  and eliminate remaining repo-local dependencies on the retired summary entrypoint.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-13T01:17:32Z'
audience: shared
authority: authoritative
applies_to:
- README.md
- docs/foundations/README.md
- docs/foundations/repository_scope.md
- workflows/modules/foundations_context_review.md
- docs/planning/prds/
- docs/planning/decisions/
- docs/planning/design/
- docs/planning/tasks/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
- core/python/tests/integration/test_control_plane_artifacts.py
- core/python/tests/unit/test_traceability_index_sync.py
---

# Summary Surface Retirement PRD

## Record Metadata
- `Trace ID`: `trace.summary_surface_retirement`
- `PRD ID`: `prd.summary_surface_retirement`
- `Status`: `active`
- `Linked Decisions`: `decision.summary_surface_retirement_direction`
- `Linked Designs`: `design.features.summary_surface_retirement`
- `Linked Implementation Plans`: `design.implementation.summary_surface_retirement`
- `Updated At`: `2026-03-13T01:17:32Z`

## Summary
Retire SUMMARY.md as a root surface, remove its dedicated restoration artifacts, and eliminate remaining repo-local dependencies on the retired summary entrypoint.

## Problem Statement
- The repository currently carries a one-off root `SUMMARY.md` artifact plus a
  dedicated restoration trace whose only purpose was to keep that retired
  entrypoint alive.
- Active root, foundations, workflow, and regression surfaces can route review
  and remediation work through `docs/planning/coordination_tracking.md`
  without preserving a separate root summary file.
- Several historical planning, acceptance, and evidence documents still
  reference the retired summary path directly, so removing the file without a
  bounded cleanup would reintroduce broken links and stale planning metadata.

## Goals
- Retire the root `SUMMARY.md` surface and the dedicated
  `trace.foundations_summary_entrypoint_continuity` restoration chain.
- Route live repo-review entrypoints through the current coordination and
  foundations surfaces instead of a one-off root report.
- Preserve historical planning coherence by rewriting surviving references to
  generic whole-repo review wording or live current-state entrypoints.

## Non-Goals
- Re-run the original whole-repo review or replace it with a new root report.
- Rewrite unrelated planning history outside the files that would otherwise
  keep broken repo-local summary links alive.
- Change planning coordination behavior, foundations query behavior, or the
  repository authority model outside the bounded retirement cleanup.

## Requirements
- `req.summary_surface_retirement.001`: Active root, foundations, workflow, and
  regression-test entrypoints must stop advertising or depending on the retired
  root summary surface and must use live current-state routes instead.
- `req.summary_surface_retirement.002`: The dedicated summary-restoration trace
  and root `SUMMARY.md` artifact must be removed, while surviving historical
  planning, acceptance, and evidence surfaces must no longer contain broken
  repo-local links to the retired summary path.
- `req.summary_surface_retirement.003`: Sync, targeted validation, full
  validation, and confirmation review passes must stay green after the
  retirement lands.

## Acceptance Criteria
- `ac.summary_surface_retirement.001`: Root and foundations entrypoints plus the
  foundations context review workflow route repository-review and remediation
  work through live coordination surfaces, and the integration regression
  coverage fails closed on the repaired routes.
- `ac.summary_surface_retirement.002`: The root `SUMMARY.md` artifact and the
  dedicated summary-restoration trace are absent from the live planning corpus,
  and the surviving historical docs no longer contain repo-local markdown links
  to the retired summary path.
- `ac.summary_surface_retirement.003`: `watchtower-core sync all --write`,
  targeted regressions, `watchtower-core validate all --format json`, `pytest
  -q`, `python -m mypy src`, and `ruff check .` stay green, and the stop
  condition review finds no remaining actionable `SUMMARY.md` dependency under
  this scope.

## Risks and Dependencies
- Historical planning records still need to preserve their rationale, so the
  cleanup must rewrite direct summary links carefully rather than deleting
  adjacent slices indiscriminately.
- The retirement depends on refreshing derived planning and repository-path
  indexes after the deletions so the machine-readable surfaces do not keep stale
  path references alive.
- The cleanup should stay bounded; broad rewrites outside the direct summary
  dependency chain would add churn without improving the retirement outcome.

## References
- [README.md](/home/j/WatchTowerPlan/README.md)
- [coordination_tracking.md](/home/j/WatchTowerPlan/docs/planning/coordination_tracking.md)
- [docs/foundations/README.md](/home/j/WatchTowerPlan/docs/foundations/README.md)
- [docs/foundations/repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [workflows/modules/foundations_context_review.md](/home/j/WatchTowerPlan/workflows/modules/foundations_context_review.md)
