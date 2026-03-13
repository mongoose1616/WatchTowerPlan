---
trace_id: trace.summary_surface_retirement
id: design.implementation.summary_surface_retirement
title: Summary Surface Retirement Implementation Plan
summary: Breaks Summary Surface Retirement into a bounded implementation slice.
type: implementation_plan
status: draft
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

# Summary Surface Retirement Implementation Plan

## Record Metadata
- `Trace ID`: `trace.summary_surface_retirement`
- `Plan ID`: `design.implementation.summary_surface_retirement`
- `Plan Status`: `draft`
- `Linked PRDs`: `prd.summary_surface_retirement`
- `Linked Decisions`: `decision.summary_surface_retirement_direction`
- `Source Designs`: `design.features.summary_surface_retirement`
- `Linked Acceptance Contracts`: `contract.acceptance.summary_surface_retirement`
- `Updated At`: `2026-03-13T01:17:32Z`

## Summary
Breaks Summary Surface Retirement into a bounded implementation slice.

## Source Request or Design
- Retire SUMMARY.md as a one-time artifact and purge all associated items.

## Scope Summary
- Retire the root summary surface, rewrite the direct dependency chain, delete
  the dedicated summary-restoration trace, and close the retirement initiative
  with refreshed planning evidence.
- Excludes broad repository-review reruns and unrelated planning-history edits
  outside the direct summary dependency chain.

## Assumptions and Constraints
- The repository already has a governed current-state entrypoint in
  `docs/planning/coordination_tracking.md`.
- Any surviving repo-local markdown link to `SUMMARY.md` will fail validation
  once the root artifact is deleted.

## Internal Standards and Canonical References Applied
- [docs/planning/README.md](/home/j/WatchTowerPlan/docs/planning/README.md): the work should reinforce coordination tracking and query coordination as the live planning entrypoints.
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): root surfaces should remain compact routers.
- [test_control_plane_artifacts.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_control_plane_artifacts.py): this provides the targeted regression boundary for the retired summary route.

## Proposed Technical Approach
- Rewrite active root, foundations, workflow, and regression-test surfaces to
  point to live coordination routes instead of `SUMMARY.md`.
- Delete the dedicated summary-restoration trace and rewrite the surviving
  historical planning, acceptance-contract, and evidence references that would
  otherwise keep a broken local summary path alive.
- Refresh the retirement slice artifacts, run sync, validate the resulting
  state, and close the initiative with fresh evidence and trackers.

## Work Breakdown
1. Update the live entrypoint docs, workflow module, and integration regression
   so no active surface depends on `SUMMARY.md`.
2. Delete the root summary and the dedicated summary-restoration trace, and
   rewrite the direct historical dependency chain to remove repo-local summary
   links.
3. Refresh the retirement PRD, decision, design, acceptance contract, and
   validation evidence; sync derived artifacts; run targeted and full
   validation; and close the initiative.

## Risks
- Missing one historical dependency surface would leave the repo with stale
  planning metadata or broken links after the delete.

## Validation Plan
- Run targeted integration coverage for
  [test_control_plane_artifacts.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_control_plane_artifacts.py).
- Run `watchtower-core sync all --write --format json`,
  `watchtower-core validate all --skip-acceptance --format json`,
  `python -m mypy src`, `ruff check .`, `watchtower-core validate acceptance
  --trace-id trace.summary_surface_retirement --format json`,
  final `watchtower-core validate all --format json`, and `pytest -q`.
- Run confirmation passes that audit the touched surfaces and the remaining
  repo-local `SUMMARY.md` mentions after the cleanup.

## References
- [README.md](/home/j/WatchTowerPlan/README.md)
- [coordination_tracking.md](/home/j/WatchTowerPlan/docs/planning/coordination_tracking.md)
- [docs/foundations/README.md](/home/j/WatchTowerPlan/docs/foundations/README.md)
- [docs/foundations/repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [workflows/modules/foundations_context_review.md](/home/j/WatchTowerPlan/workflows/modules/foundations_context_review.md)
