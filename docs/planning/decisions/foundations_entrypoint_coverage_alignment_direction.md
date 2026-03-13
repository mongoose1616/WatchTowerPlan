---
trace_id: trace.foundations_entrypoint_coverage_alignment
id: decision.foundations_entrypoint_coverage_alignment_direction
title: Foundations Entrypoint Coverage Alignment Direction Decision
summary: Records the initial direction decision for Foundations Entrypoint Coverage
  Alignment.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-13T00:26:44Z'
audience: shared
authority: supporting
applies_to:
- docs/foundations/README.md
- docs/foundations/repository_scope.md
- workflows/modules/foundations_context_review.md
- core/control_plane/indexes/foundations/README.md
- core/python/tests/integration/test_control_plane_artifacts.py
---

# Foundations Entrypoint Coverage Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.foundations_entrypoint_coverage_alignment`
- `Decision ID`: `decision.foundations_entrypoint_coverage_alignment_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.foundations_entrypoint_coverage_alignment`
- `Linked Designs`: `design.features.foundations_entrypoint_coverage_alignment`
- `Linked Implementation Plans`: `design.implementation.foundations_entrypoint_coverage_alignment`
- `Updated At`: `2026-03-13T00:26:44Z`

## Summary
Records the initial direction decision for Foundations Entrypoint Coverage Alignment.

## Decision Statement
Align the existing foundations family entrypoint docs and the foundations
context review workflow so they explicitly route readers to the machine
foundations lookup and rebuild surfaces and load the summary and customer-story
companions for the review contexts the foundations layer already advertises.

## Trigger or Source Request
- Comprehensive internal project review for documentation coverage, standards alignment, and cohesiveness with foundations/**.

## Current Context and Constraints
- The foundations family README already describes review paths that depend on
  `SUMMARY.md` and future-state paths that depend on `customer_story.md`, but
  the foundations context review workflow does not load those surfaces.
- The family entrypoint docs and the machine foundations README do not
  currently expose a coherent machine route to `watchtower-core query foundations`
  and `watchtower-core sync foundation-index`.
- The slice must preserve current query and sync behavior and stay bounded to
  documentation and workflow alignment.

## Applied References and Implications
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): the current repository boundary should stay easy to resolve from both human and machine entrypoints.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): adjacent human and machine guidance should land in the same change set.
- [customer_story.md](/home/j/WatchTowerPlan/docs/foundations/customer_story.md): the foundations family already treats this document as supporting future-state context, so the review workflow should load it when that route matters.
- [foundation_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/foundation_index_standard.md): the machine-readable foundation family needs clear query and rebuild entrypoints alongside the published artifact.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): the workflow update should stay procedural and focused on execution.

## Affected Surfaces
- docs/foundations/README.md
- docs/foundations/repository_scope.md
- workflows/modules/foundations_context_review.md
- core/control_plane/indexes/foundations/README.md
- core/python/tests/integration/test_control_plane_artifacts.py

## Options Considered
### Option 1
- Patch only the workflow module.
- Minimal documentation touch surface.
- Leaves the foundations family entrypoint docs and the machine foundations
  README under-documented.

### Option 2
- Align the foundations family entrypoints, the review workflow, and targeted
  regression coverage together.
- Repairs the documented routes end to end and keeps the family coherent from
  whichever entrypoint opens first.
- Touches more docs and planning metadata than a workflow-only patch.

## Chosen Outcome
Choose option 2. Repair the foundations family entrypoint docs, the review
workflow module, and the targeted integration regression in one bounded slice.

## Rationale and Tradeoffs
- This keeps the fix aligned with the repository standards posture: human docs,
  workflow guidance, machine index entrypoints, and regression coverage all move
  together.
- The tradeoff is a slightly broader documentation slice, but it avoids leaving
  the repaired workflow dependent on still-stale family entrypoint docs.

## Consequences and Follow-Up Impacts
- Foundations reviewers and agents can discover the correct human and machine
  routes from the family entrypoints without relying on prior repo familiarity.
- The integration artifact suite gains fail-closed coverage for the repaired
  foundations route guidance.

## Risks, Dependencies, and Assumptions
- The workflow must not become a command reference; the added guidance should
  stay limited to route selection and context loading.

## References
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md)
- [customer_story.md](/home/j/WatchTowerPlan/docs/foundations/customer_story.md)
