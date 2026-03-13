---
trace_id: trace.summary_surface_retirement
id: decision.summary_surface_retirement_direction
title: Summary Surface Retirement Direction Decision
summary: Records the initial direction decision for Summary Surface Retirement.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-13T01:17:32Z'
audience: shared
authority: supporting
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

# Summary Surface Retirement Direction Decision

## Record Metadata
- `Trace ID`: `trace.summary_surface_retirement`
- `Decision ID`: `decision.summary_surface_retirement_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.summary_surface_retirement`
- `Linked Designs`: `design.features.summary_surface_retirement`
- `Linked Implementation Plans`: `design.implementation.summary_surface_retirement`
- `Updated At`: `2026-03-13T01:17:32Z`

## Summary
Records the initial direction decision for Summary Surface Retirement.

## Decision Statement
Retire the root `SUMMARY.md` surface and its dedicated restoration trace,
rewrite surviving historical references to generic whole-repo review wording or
live coordination routes, and keep the repaired behavior fail-closed through
the touched entrypoint and validation surfaces.

## Trigger or Source Request
- Retire SUMMARY.md as a one-time artifact and purge all associated items.

## Current Context and Constraints
- `SUMMARY.md` duplicates repo-review and next-step routing that already exists
  in `docs/planning/coordination_tracking.md` and the foundations layer.
- The dedicated `trace.foundations_summary_entrypoint_continuity` slice exists
  only to keep the retired root summary entrypoint alive.
- Removing the summary without rewriting the surviving historical references
  would reintroduce document-semantics failures across planning and acceptance
  surfaces.

## Applied References and Implications
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): live repo-review entrypoints should route through current repository scope and coordination rather than through a one-off root report.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): retiring the root summary requires the adjacent docs, tests, and derived machine-readable surfaces to move together.
- [coordination_tracking.md](/home/j/WatchTowerPlan/docs/planning/coordination_tracking.md): this already serves as the durable human current-state entrypoint for repository review, active work, and next remediation decisions.

## Affected Surfaces
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

## Options Considered
### Option 1
- Keep `SUMMARY.md` as a durable root artifact and preserve the dedicated
  summary-restoration trace.
- Minimizes historical doc churn.
- Retains a one-off root report and a dedicated maintenance slice whose only
  purpose is continuity for a retired route.

### Option 2
- Retire `SUMMARY.md`, delete the dedicated restoration trace, and rewrite the
  surviving historical references to generic review wording or live
  coordination routes.
- Removes the redundant root artifact and aligns live review entrypoints with
  the current coordination model.
- Requires a bounded but real rewrite across historical planning,
  acceptance-contract, and evidence surfaces.

## Chosen Outcome
Apply option 2.

## Rationale and Tradeoffs
- The root summary is no longer the right current-state entrypoint because the
  repo already has a governed coordination surface for review and next-step
  routing.
- Deleting the dedicated continuity slice removes maintenance overhead and
  prevents future drift around a surface the user no longer wants to keep.
- The tradeoff is touching more historical planning records, but the rewrite is
  bounded to the direct dependency chain and leaves the underlying rationale
  intact.

## Consequences and Follow-Up Impacts
- Live root and foundations entrypoints will route whole-repo review context to
  `docs/planning/coordination_tracking.md`.
- The repository-path index and planning trackers will drop the retired summary
  and continuity-trace surfaces after sync.
- The surviving historical planning docs will preserve their context without
  keeping a broken or stale local summary path alive.

## Risks, Dependencies, and Assumptions
- Assumes the repo should keep one canonical human current-state entrypoint
  rather than both coordination tracking and a separate root summary.
- Depends on updating the current slice docs, tests, and generated surfaces in
  the same change set so the retirement does not leave stale machine-readable
  references behind.
- Risks over-broad cleanup if the rewrite strays beyond the direct
  `SUMMARY.md` dependency chain.

## References
- [README.md](/home/j/WatchTowerPlan/README.md)
- [coordination_tracking.md](/home/j/WatchTowerPlan/docs/planning/coordination_tracking.md)
- [docs/foundations/README.md](/home/j/WatchTowerPlan/docs/foundations/README.md)
- [docs/foundations/repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [workflows/modules/foundations_context_review.md](/home/j/WatchTowerPlan/workflows/modules/foundations_context_review.md)
