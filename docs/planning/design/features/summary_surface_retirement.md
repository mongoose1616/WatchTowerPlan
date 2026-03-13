---
trace_id: trace.summary_surface_retirement
id: design.features.summary_surface_retirement
title: Summary Surface Retirement Feature Design
summary: Defines the technical design boundary for Summary Surface Retirement.
type: feature_design
status: draft
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

# Summary Surface Retirement Feature Design

## Record Metadata
- `Trace ID`: `trace.summary_surface_retirement`
- `Design ID`: `design.features.summary_surface_retirement`
- `Design Status`: `draft`
- `Linked PRDs`: `prd.summary_surface_retirement`
- `Linked Decisions`: `decision.summary_surface_retirement_direction`
- `Linked Implementation Plans`: `design.implementation.summary_surface_retirement`
- `Updated At`: `2026-03-13T01:17:32Z`

## Summary
Defines the technical design boundary for Summary Surface Retirement.

## Source Request
- Retire SUMMARY.md as a one-time artifact and purge all associated items.

## Scope and Feature Boundary
- Covers retiring the root `SUMMARY.md` surface, deleting the dedicated
  summary-restoration trace, rewriting the surviving direct dependency chain,
  and repairing the adjacent regression coverage.
- Excludes rerunning the original repository review, changing coordination or
  foundations query behavior, or rewriting unrelated planning history outside
  the direct summary dependency set.

## Current-State Context
- Live repo-review entrypoints already have a governed human current-state route
  in `docs/planning/coordination_tracking.md`.
- The root summary and its dedicated continuity trace now duplicate that role
  and require extra maintenance whenever adjacent foundations or planning docs
  shift.
- Several historical planning, acceptance, and evidence surfaces still contain
  repo-local markdown links to the retired summary path, so the cleanup must
  rewrite them before validation can stay green without `SUMMARY.md`.

## Foundations References Applied
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): live repository-review routing should stay anchored to current repo scope and current planning state.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): human docs, tests, acceptance contracts, and derived indexes must stay aligned in the same change.

## Internal Standards and Canonical References Applied
- [docs/planning/README.md](/home/j/WatchTowerPlan/docs/planning/README.md): current planning state should route through coordination tracking and the machine coordination query.
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): the root README should stay a thin router instead of accumulating one-off historical reports.
- [test_control_plane_artifacts.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_control_plane_artifacts.py): this is the bounded fail-closed regression surface for the repaired entrypoints.

## Design Goals and Constraints
- Remove the redundant root summary surface without degrading current review or
  coordination discoverability.
- Keep the cleanup bounded to the direct dependency chain rather than rewriting
  planning history wholesale.
- Preserve green validation by ensuring no surviving repo-local markdown link
  targets the retired summary path.

## Options Considered
### Option 1
- Keep `SUMMARY.md` and keep the dedicated restoration trace.
- Lowest short-term change volume.
- Preserves a redundant root artifact and an entire trace whose only purpose is
  maintaining that artifact.

### Option 2
- Retire `SUMMARY.md`, delete the dedicated restoration trace, and rewrite the
  surviving dependency chain.
- Removes the redundant route and leaves current-state navigation concentrated
  in the governed coordination surfaces.
- Requires careful cleanup across historical planning, acceptance, and evidence
  records.

## Recommended Design
### Architecture
- Remove the root `SUMMARY.md` artifact and the dedicated
  `trace.foundations_summary_entrypoint_continuity` artifact chain.
- Rewrite live root, foundations, and workflow surfaces to route repo-review
  work through `docs/planning/coordination_tracking.md`.
- Rewrite surviving historical planning, acceptance, and evidence surfaces so
  they keep their rationale without linking to the retired summary path.

### Data and Interface Impacts
- No runtime code or schema behavior changes.
- Human and machine-readable planning surfaces lose the retired summary path
  after sync and closeout.
- The integration artifact regression shifts from asserting summary existence to
  asserting repaired coordination-based entrypoints and the absence of surviving
  summary links in those live surfaces.

### Execution Flow
1. Update the live root, foundations, workflow, and regression surfaces so
   they no longer advertise or require `SUMMARY.md`.
2. Delete the dedicated summary-restoration trace and rewrite the surviving
   historical planning, acceptance, and evidence references that would
   otherwise break validation.
3. Refresh the current retirement trace artifacts, regenerate the derived
   indexes and trackers, and validate the resulting repo state end to end.

### Invariants and Failure Cases
- Live repository-review routes must remain discoverable after the summary
  retirement.
- No surviving repo-local markdown link may target `SUMMARY.md`.
- If the cleanup misses a direct dependency surface, targeted or full
  validation must fail before closeout.

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

## Design Guardrails
- Keep the retirement focused on the direct summary dependency chain.
- Do not weaken validation or the planning trace model to make the deletions
  pass.

## Risks
- The main risk is missing a surviving historical link and reintroducing a
  document-semantics failure after the root summary is removed.

## References
- [README.md](/home/j/WatchTowerPlan/README.md)
- [coordination_tracking.md](/home/j/WatchTowerPlan/docs/planning/coordination_tracking.md)
- [docs/foundations/README.md](/home/j/WatchTowerPlan/docs/foundations/README.md)
- [docs/foundations/repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [workflows/modules/foundations_context_review.md](/home/j/WatchTowerPlan/workflows/modules/foundations_context_review.md)
