---
trace_id: trace.foundation_document_standard_boundary_alignment
id: decision.foundation_document_standard_boundary_alignment_direction
title: Foundation Document Standard Boundary Alignment Direction Decision
summary: Records the initial direction decision for Foundation Document Standard Boundary
  Alignment.
type: decision_record
status: active
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

# Foundation Document Standard Boundary Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.foundation_document_standard_boundary_alignment`
- `Decision ID`: `decision.foundation_document_standard_boundary_alignment_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.foundation_document_standard_boundary_alignment`
- `Linked Designs`: `design.features.foundation_document_standard_boundary_alignment`
- `Linked Implementation Plans`: `design.implementation.foundation_document_standard_boundary_alignment`
- `Updated At`: `2026-03-12T23:43:00Z`

## Summary
Records the initial direction decision for Foundation Document Standard Boundary Alignment.

## Decision Statement
Repair the foundations-family boundary by narrowing the authored foundation document standard to the current governed foundation documents, excluding the family README from its operationalization coverage, and locking that boundary with targeted regressions instead of changing standards-query runtime semantics.

## Trigger or Source Request
- Comprehensive internal project review for documentation coverage, standards alignment, and cohesiveness with foundations/**.

## Current Context and Constraints
- The current review reproduced a real mismatch between the authored standard and live machine lookup: `watchtower-core query standards --operationalization-path docs/foundations/README.md` returns `std.documentation.foundation_md` even though [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md) explicitly excludes the family README from scope.
- The foundations README is already covered by [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md), so the extra foundation-document match is incorrect rather than simply redundant.
- Current regressions do not fail closed on complete governed foundation-doc coverage plus README exclusion, so the same drift can recur silently.

## Applied References and Implications
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): keeps the fix inside the repo-owned docs, standards, indexes, and test surfaces.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): favors explicit, deterministic published contracts over hidden heuristics.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): requires the authored standard, derived standard index, and regressions to move together in one slice.
- [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md): is the contract whose scope and operationalization need to agree again.
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): confirms that the family README belongs to the README-document family rather than the governed foundation-document family.

## Affected Surfaces
- docs/standards/documentation/foundation_md_standard.md
- docs/foundations/README.md
- core/control_plane/indexes/standards/standard_index.v1.json
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/integration/test_control_plane_artifacts.py

## Options Considered
### Option 1
- Change standards-query matching behavior so directory operationalization paths exclude nested `README.md` surfaces automatically.
- Would avoid explicit file maintenance in the foundation-document standard.
- Changes repository-wide runtime semantics for all directory-backed standards and risks unrelated lookup regressions.

### Option 2
- Repair the authored foundation-document standard by publishing the current governed foundation docs explicitly, excluding the family README, and adding targeted regressions.
- Fixes the confirmed defect at its source while leaving broader runtime behavior unchanged.
- Requires future same-change updates when the governed foundation-doc corpus changes.

## Chosen Outcome
Apply Option 2 and keep standards-query runtime behavior unchanged.

## Rationale and Tradeoffs
- The defect lives in the authored family contract, not in the query engine, so the lowest-risk fix is to narrow the published operationalization boundary.
- Explicit governed-document coverage makes the foundations-family boundary reviewable in the standard itself and fail-closed under targeted tests.
- The main tradeoff is extra maintenance when the foundation-doc corpus changes, but that is preferable to silently overmatching the family README.

## Consequences and Follow-Up Impacts
- The foundation-document standard will stop resolving from `docs/foundations/README.md`.
- The standard will continue resolving from each governed foundation document under `docs/foundations/`.
- Targeted regressions will force same-change updates if the governed foundation-document corpus changes later.

## Risks, Dependencies, and Assumptions
- Depends on regenerating the standard index after the standard changes so the machine-readable lookup surface reflects the new boundary.
- Assumes the current six governed foundation documents are the intended foundation-document family and that the family README remains governed by the README standard.
- Risks incomplete coverage if the tests do not verify both positive governed doc matches and the negative README case.

## References
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
- [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md)
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md)
