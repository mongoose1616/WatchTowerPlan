---
trace_id: trace.foundation_document_standard_boundary_alignment
id: design.implementation.foundation_document_standard_boundary_alignment
title: Foundation Document Standard Boundary Alignment Implementation Plan
summary: Breaks Foundation Document Standard Boundary Alignment into a bounded implementation
  slice.
type: implementation_plan
status: draft
owner: repository_maintainer
updated_at: '2026-03-12T23:43:00Z'
audience: shared
authority: supporting
applies_to:
- docs/standards/documentation/foundation_md_standard.md
- docs/foundations/README.md
- core/control_plane/indexes/standards/standard_index.v1.json
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/integration/test_control_plane_artifacts.py
---

# Foundation Document Standard Boundary Alignment Implementation Plan

## Record Metadata
- `Trace ID`: `trace.foundation_document_standard_boundary_alignment`
- `Plan ID`: `design.implementation.foundation_document_standard_boundary_alignment`
- `Plan Status`: `draft`
- `Linked PRDs`: `prd.foundation_document_standard_boundary_alignment`
- `Linked Decisions`: `decision.foundation_document_standard_boundary_alignment_direction`
- `Source Designs`: `design.features.foundation_document_standard_boundary_alignment`
- `Linked Acceptance Contracts`: `contract.acceptance.foundation_document_standard_boundary_alignment`
- `Updated At`: `2026-03-12T23:43:00Z`

## Summary
Breaks Foundation Document Standard Boundary Alignment into a bounded implementation slice.

## Source Request or Design
- [foundation_document_standard_boundary_alignment.md](/home/j/WatchTowerPlan/docs/planning/design/features/foundation_document_standard_boundary_alignment.md)
- Comprehensive internal project review for documentation coverage, standards alignment, and cohesiveness with foundations/**.

## Scope Summary
- Update the authored foundation-document standard so its published operationalization surfaces match the documented family boundary.
- Regenerate the standard index and dependent planning surfaces after the authored contract changes.
- Add targeted regressions covering positive governed-foundation lookups and the negative README exclusion.
- Exclude broad standards-query runtime changes or unrelated foundations documentation refresh work.

## Assumptions and Constraints
- Standards lookup for the foundations family should keep working through the existing `--operationalization-path` filter; the slice should not add new CLI flags or matching semantics.
- The explicit operationalization list in [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md) can be treated as fail-closed maintenance overhead when the governed foundations corpus changes.

## Internal Standards and Canonical References Applied
- [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md): is the authored contract being repaired.
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): constrains the expected governance boundary for `docs/foundations/README.md`.
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): requires published operationalization metadata to stay concrete and reviewable.
- [watchtower_core_query_standards.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_query_standards.md): defines the live lookup behavior the regressions will verify.

## Proposed Technical Approach
- Replace the directory-level operationalization path in the foundation-document standard with the current governed foundation-document file set.
- Add one authored guidance and validation note explaining that the family README is governed by the README standard instead of the foundation-document standard.
- Extend targeted tests so:
  - CLI lookup proves positive coverage for governed foundation docs.
  - CLI lookup proves negative coverage for `docs/foundations/README.md`.
  - Standard-index sync proves the derived entry publishes the exact current governed foundation-document file set.
  - Integration artifact checks prove the authored operationalization section stays aligned with the live foundations corpus.

## Work Breakdown
1. Rewrite the traced PRD, design, implementation plan, decision, and acceptance contract around the confirmed foundations-family boundary issue.
2. Update [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md) to publish the current governed foundation docs explicitly and describe the README exclusion.
3. Add CLI, sync, and integration regressions for the repaired boundary.
4. Refresh the derived standard index and coordination/planning trackers.
5. Run targeted validation, full repository validation, and repeated themed confirmation passes before closeout.

## Risks
- If the explicit operationalization list misses one governed foundation doc, standards lookup will under-report the family until the tests catch it.
- If tests only check the README exclusion and not complete positive coverage, future doc additions could drift silently.

## Validation Plan
- Run targeted pytest coverage for [test_cli_query_commands.py](/home/j/WatchTowerPlan/core/python/tests/unit/test_cli_query_commands.py), [test_standard_index_sync.py](/home/j/WatchTowerPlan/core/python/tests/unit/test_standard_index_sync.py), and [test_control_plane_artifacts.py](/home/j/WatchTowerPlan/core/python/tests/integration/test_control_plane_artifacts.py).
- Run `watchtower-core validate document-semantics --path docs/standards/documentation/foundation_md_standard.md --format json`.
- Run full repository validation, type checking, and linting after the targeted checks pass.
- Re-run themed confirmation passes over the touched docs, standard index, standards-query behavior, and adjacent foundations surfaces to confirm no new actionable issues remain.

## References
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
- [foundation_document_standard_boundary_alignment.md](/home/j/WatchTowerPlan/docs/planning/design/features/foundation_document_standard_boundary_alignment.md)
