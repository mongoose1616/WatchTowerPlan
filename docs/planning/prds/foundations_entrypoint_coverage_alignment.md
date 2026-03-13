---
trace_id: trace.foundations_entrypoint_coverage_alignment
id: prd.foundations_entrypoint_coverage_alignment
title: Foundations Entrypoint Coverage Alignment PRD
summary: Align foundations family entrypoints and the foundations context review workflow
  with the machine lookup route and the companion review-context documents already
  advertised by the foundations layer.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-13T00:25:01Z'
audience: shared
authority: authoritative
applies_to:
- docs/foundations/README.md
- docs/foundations/repository_scope.md
- workflows/modules/foundations_context_review.md
- core/control_plane/indexes/foundations/README.md
- core/python/tests/integration/test_control_plane_artifacts.py
---

# Foundations Entrypoint Coverage Alignment PRD

## Record Metadata
- `Trace ID`: `trace.foundations_entrypoint_coverage_alignment`
- `PRD ID`: `prd.foundations_entrypoint_coverage_alignment`
- `Status`: `active`
- `Linked Decisions`: `decision.foundations_entrypoint_coverage_alignment_direction`
- `Linked Designs`: `design.features.foundations_entrypoint_coverage_alignment`
- `Linked Implementation Plans`: `design.implementation.foundations_entrypoint_coverage_alignment`
- `Updated At`: `2026-03-13T00:25:01Z`

## Summary
Align foundations family entrypoints and the foundations context review workflow with the machine lookup route and the companion review-context documents already advertised by the foundations layer.

## Problem Statement
- The foundations family currently routes human reviewers to
  [coordination_tracking.md](/home/j/WatchTowerPlan/docs/planning/coordination_tracking.md)
  and future-state readers to
  [customer_story.md](/home/j/WatchTowerPlan/docs/foundations/customer_story.md),
  but [foundations_context_review.md](/home/j/WatchTowerPlan/workflows/modules/foundations_context_review.md)
  does not load either surface for the review contexts where the family README
  says they matter.
- The foundations family also under-documents its machine entrypoints:
  [docs/foundations/README.md](/home/j/WatchTowerPlan/docs/foundations/README.md),
  [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md),
  and [core/control_plane/indexes/foundations/README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/foundations/README.md)
  do not coherently point readers toward the authoritative
  `watchtower-core query foundations` and `watchtower-core sync foundation-index`
  surfaces.
- That drift does not break validation today, but it does reduce discoverability
  and makes foundations-aware reviews depend on informal repo familiarity
  instead of the documented human and machine routes.

## Goals
- Make the foundations family entrypoints expose both the human read order and
  the machine lookup and rebuild routes for the same family.
- Make the foundations context review workflow load the coordination and
  future-state companion docs when those routes are relevant.
- Add fail-closed regression coverage for the repaired foundations entrypoint
  guidance.

## Non-Goals
- Change `watchtower-core query foundations` or `watchtower-core sync foundation-index`
  runtime behavior.
- Redesign the foundation index schema or the foundations document corpus.
- Expand the slice into unrelated command-doc or standards cleanup outside the
  bounded foundations family entrypoint coverage issue.

## Requirements
- `req.foundations_entrypoint_coverage_alignment.001`: The foundations family
  entrypoints must explicitly expose the machine lookup and rebuild routes that
  serve the governed foundations corpus.
- `req.foundations_entrypoint_coverage_alignment.002`: The foundations context
  review workflow must load the coordination and customer-story companion docs
  when a foundations-aware review or planning task depends on those routes.
- `req.foundations_entrypoint_coverage_alignment.003`: Regression coverage must
  fail closed if the repaired foundations entrypoint guidance drops those human
  or machine routes again.

## Acceptance Criteria
- `ac.foundations_entrypoint_coverage_alignment.001`: The foundations family
  entrypoint docs explicitly point to
  [watchtower_core_query_foundations.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_query_foundations.md)
  and
  [watchtower_core_sync_foundation_index.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_sync_foundation_index.md)
  where machine lookup or rebuild is the right next step.
- `ac.foundations_entrypoint_coverage_alignment.002`:
  [foundations_context_review.md](/home/j/WatchTowerPlan/workflows/modules/foundations_context_review.md)
  loads [customer_story.md](/home/j/WatchTowerPlan/docs/foundations/customer_story.md)
  and [coordination_tracking.md](/home/j/WatchTowerPlan/docs/planning/coordination_tracking.md)
  for the review contexts already described by the foundations layer and
  surfaces `watchtower-core query foundations` as the deterministic discovery
  helper.
- `ac.foundations_entrypoint_coverage_alignment.003`: Targeted integration
  regressions, full repository validation, and repeated foundations-themed
  confirmation passes stay green after the guidance repair lands.

## Risks and Dependencies
- The slice depends on keeping human-facing family guidance and machine-facing
  command/index entrypoints aligned in the same change set so documentation does
  not split into competing routes again.
- The workflow guidance must remain bounded; adding entrypoint coverage should
  not turn the workflow module into a duplicate of the foundations README or the
  command docs.

## References
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md)
- [customer_story.md](/home/j/WatchTowerPlan/docs/foundations/customer_story.md)
