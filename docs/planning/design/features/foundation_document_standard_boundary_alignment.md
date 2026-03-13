---
trace_id: trace.foundation_document_standard_boundary_alignment
id: design.features.foundation_document_standard_boundary_alignment
title: Foundation Document Standard Boundary Alignment Feature Design
summary: Defines the technical design boundary for Foundation Document Standard Boundary
  Alignment.
type: feature_design
status: draft
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

# Foundation Document Standard Boundary Alignment Feature Design

## Record Metadata
- `Trace ID`: `trace.foundation_document_standard_boundary_alignment`
- `Design ID`: `design.features.foundation_document_standard_boundary_alignment`
- `Design Status`: `draft`
- `Linked PRDs`: `prd.foundation_document_standard_boundary_alignment`
- `Linked Decisions`: `decision.foundation_document_standard_boundary_alignment_direction`
- `Linked Implementation Plans`: `design.implementation.foundation_document_standard_boundary_alignment`
- `Updated At`: `2026-03-12T23:43:00Z`

## Summary
Defines the technical design boundary for Foundation Document Standard Boundary Alignment.

## Source Request
- Comprehensive internal project review for documentation coverage, standards alignment, and cohesiveness with foundations/**.

## Scope and Feature Boundary
- Covers the authored operationalization contract in [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md), the derived standard index, and the targeted regressions that prove the repaired lookup boundary.
- Covers the lookup relationship between the governed foundation documents under `docs/foundations/` and the family [README.md](/home/j/WatchTowerPlan/docs/foundations/README.md).
- Excludes broad changes to `watchtower-core query standards` matching semantics for unrelated documentation families.
- Excludes content rewrites to the governed foundation documents themselves beyond the published family-boundary contract.

## Current-State Context
- The live standards query currently resolves `std.documentation.foundation_md` for `docs/foundations/README.md` because the standard operationalizes the whole `docs/foundations/` directory even though its documented scope excludes the family README.
- The foundations README is already governed by [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md), so the extra foundation-document match is both redundant and incorrect.
- Current tests prove positive foundations-family coverage in adjacent areas but do not fail closed on the README exclusion or on complete governed-doc coverage for `std.documentation.foundation_md`.

## Foundations References Applied
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): keeps the slice bounded to the standards, docs, indexes, and tests owned by this repository.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): favors explicit, deterministic published boundaries over implicit lookup behavior.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): requires the authored standard, derived indexes, and regressions to move in the same change set.

## Internal Standards and Canonical References Applied
- [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md): is the governing contract whose published scope and operationalization must be brought back into alignment.
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): confirms that `docs/foundations/README.md` is a directory-orientation surface, not a governed foundation document.
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): requires operationalization metadata to point to real repository surfaces and stay reviewable without code spelunking.
- [watchtower_core_query_standards.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_query_standards.md): defines the live lookup behavior the fix must preserve for the governed foundation documents.

## Design Goals and Constraints
- Restore one coherent human-readable and machine-readable boundary for the foundations documentation family.
- Keep the repair localized to the authored contract and derived indexes rather than changing repository-wide standards-query semantics.
- Preserve existing legitimate standards matches for the foundations README, especially `std.documentation.readme_md`.
- Fail closed when the governed foundation-document set changes in the future.

## Options Considered
### Option 1
- Change standards-query matching semantics so directory operationalization entries automatically exclude family README descendants.
- Would avoid listing the current governed foundation documents explicitly in the foundation standard.
- Changes runtime behavior for every standard that operationalizes directories and risks unintended lookup regressions outside the foundations slice.

### Option 2
- Narrow the authored foundation-document standard so it publishes the current governed foundation docs explicitly, keeps the README out of its operationalization list, and adds fail-closed regressions.
- Repairs the confirmed defect at its source without broadening runtime semantics.
- Requires same-change updates when the governed foundation-document corpus gains, renames, or removes a file.

## Recommended Design
### Architecture
- Keep standards-query runtime code unchanged and repair the boundary at the authored standard level.
- Publish the current governed foundation documents explicitly in the `Operational Surfaces` list for [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md).
- Lock the repaired contract through one CLI lookup regression, one standard-index sync regression, and one integration artifact check.

### Data and Interface Impacts
- [standard_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/standards/standard_index.v1.json) will change because the foundation-document standard’s published operationalization paths change.
- `watchtower-core query standards --operationalization-path` will return one fewer match for `docs/foundations/README.md` and continue returning `std.documentation.foundation_md` for the governed foundation documents.
- No schema, loader, or query-interface shape changes are required.

### Execution Flow
1. Replace the over-broad `docs/foundations/` directory operationalization entry with the current governed foundation-document file list and README exclusion guidance.
2. Regenerate the standard index so the machine-readable lookup surface matches the authored contract.
3. Add regressions that prove positive coverage for all governed foundation docs and a negative lookup result for `docs/foundations/README.md`.

### Invariants and Failure Cases
- `docs/foundations/README.md` must remain governed by the README standard, not the foundation-document standard.
- Every governed foundation document under `docs/foundations/` must resolve `std.documentation.foundation_md`.
- If a new governed foundation document is added without updating the standard’s operationalization list, targeted tests must fail.

## Affected Surfaces
- docs/standards/documentation/foundation_md_standard.md
- docs/foundations/README.md
- core/control_plane/indexes/standards/standard_index.v1.json
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/integration/test_control_plane_artifacts.py

## Design Guardrails
- Do not change the public CLI contract or repository-wide standards-query matching behavior to solve this slice.
- Do not remove legitimate complementary matches such as `std.documentation.readme_md` for `docs/foundations/README.md`.
- Keep the published operationalization list specific enough that drift fails closed on future foundations-family changes.

## Risks
- Explicit file coverage adds maintenance overhead when the foundations corpus changes, but that tradeoff is preferable to silently overmatching the family README.
- The repaired tests must distinguish the standard’s authored contract from broader standards such as `std.data_contracts.format_selection` so the slice does not over-constrain legitimate multi-standard matches.

## References
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
- [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md)
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md)
