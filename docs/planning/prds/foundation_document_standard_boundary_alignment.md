---
trace_id: trace.foundation_document_standard_boundary_alignment
id: prd.foundation_document_standard_boundary_alignment
title: Foundation Document Standard Boundary Alignment PRD
summary: Align foundation-document lookup coverage with the governed foundations-doc
  boundary and exclude the family README from the foundation-doc standard.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-12T23:43:00Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/documentation/foundation_md_standard.md
- docs/foundations/README.md
- core/control_plane/indexes/standards/standard_index.v1.json
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/integration/test_control_plane_artifacts.py
---

# Foundation Document Standard Boundary Alignment PRD

## Record Metadata
- `Trace ID`: `trace.foundation_document_standard_boundary_alignment`
- `PRD ID`: `prd.foundation_document_standard_boundary_alignment`
- `Status`: `active`
- `Linked Decisions`: `decision.foundation_document_standard_boundary_alignment_direction`
- `Linked Designs`: `design.features.foundation_document_standard_boundary_alignment`
- `Linked Implementation Plans`: `design.implementation.foundation_document_standard_boundary_alignment`
- `Updated At`: `2026-03-12T23:43:00Z`

## Summary
Align foundation-document lookup coverage with the governed foundations-doc boundary and exclude the family README from the foundation-doc standard.

## Problem Statement
- The current foundations review reproduced a real standards-lookup drift:
  `watchtower-core query standards --operationalization-path docs/foundations/README.md`
  returns `std.documentation.foundation_md` even though
  [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md)
  explicitly scopes itself to governed foundation documents other than the
  family `README.md`.
- That machine-readable overmatch blurs the authored boundary between governed
  foundation documents and the directory-orientation README, reducing trust in
  standards lookup for `docs/foundations/**`.
- Current regression coverage does not fail closed on that boundary, so future
  edits to the foundation-document standard can silently reintroduce the same
  mismatch.

## Goals
- Make the foundation-document standard resolve from every governed foundation
  document under `docs/foundations/` while excluding
  `docs/foundations/README.md`.
- Keep the repair in the authored standard and derived lookup surfaces rather
  than changing broader standards-query runtime behavior.
- Add fail-closed regression coverage for the repaired foundations-family
  boundary.

## Non-Goals
- Redesign directory, glob, or exclusion semantics for standards lookup across
  the full repository.
- Change the content or ownership of
  [docs/foundations/README.md](/home/j/WatchTowerPlan/docs/foundations/README.md)
  beyond its lookup-boundary relationship to the foundation-document standard.
- Expand the slice into unrelated foundations, command-doc, or workflow
  cleanup beyond the confirmed lookup-boundary issue.

## Requirements
- `req.foundation_document_standard_boundary_alignment.001`: [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md) must publish operationalization coverage that aligns with its documented scope by covering the current governed foundation documents and excluding the family README.
- `req.foundation_document_standard_boundary_alignment.002`: The live standard index and standards-query surface must resolve `std.documentation.foundation_md` for the governed foundation documents while excluding `docs/foundations/README.md`.
- `req.foundation_document_standard_boundary_alignment.003`: Targeted regression coverage must fail closed if the foundation-document standard regresses back to an over-broad family boundary or drops a governed foundation document from operationalization coverage.

## Acceptance Criteria
- `ac.foundation_document_standard_boundary_alignment.001`: [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md) publishes the six current governed foundation documents as operational surfaces, does not operationalize `docs/foundations/README.md`, and explains that README governance belongs to the README standard.
- `ac.foundation_document_standard_boundary_alignment.002`: `watchtower-core query standards --operationalization-path` resolves `std.documentation.foundation_md` for each governed foundation document under `docs/foundations/` and does not resolve it for `docs/foundations/README.md`.
- `ac.foundation_document_standard_boundary_alignment.003`: Targeted CLI, standard-index sync, and integration regressions plus full repository validation stay green after the repaired boundary lands.

## Risks and Dependencies
- The repair depends on the derived [standard_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/standards/standard_index.v1.json) being refreshed in the same slice so machine-readable lookup matches the authored standard.
- Publishing explicit governed-document operationalization paths trades some convenience for fail-closed coverage; future additions or renames in `docs/foundations/` must update this standard in the same change set.
- The slice must preserve legitimate matches from `std.documentation.readme_md` and other broader standards such as `std.data_contracts.format_selection`.

## References
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
