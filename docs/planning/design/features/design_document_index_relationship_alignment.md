---
trace_id: trace.design_document_index_relationship_alignment
id: design.features.design_document_index_relationship_alignment
title: Design Document Index Relationship Alignment Feature Design
summary: Defines the technical design boundary for Design Document Index Relationship
  Alignment.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-11T19:24:39Z'
audience: shared
authority: authoritative
applies_to:
- docs/planning/design/
- docs/standards/data_contracts/design_document_index_standard.md
- docs/standards/documentation/feature_design_md_standard.md
- docs/standards/documentation/implementation_plan_md_standard.md
- docs/templates/implementation_plan_template.md
- core/control_plane/examples/valid/indexes/design_document_index.v1.example.json
- core/python/src/watchtower_core/repo_ops/sync/design_document_index.py
- core/python/src/watchtower_core/repo_ops/sync/design_tracking.py
- core/python/tests/
---

# Design Document Index Relationship Alignment Feature Design

## Record Metadata
- `Trace ID`: `trace.design_document_index_relationship_alignment`
- `Design ID`: `design.features.design_document_index_relationship_alignment`
- `Design Status`: `active`
- `Linked PRDs`: `prd.design_document_index_relationship_alignment`
- `Linked Decisions`: `decision.design_document_index_relationship_alignment_direction`
- `Linked Implementation Plans`: `design.implementation.design_document_index_relationship_alignment`
- `Updated At`: `2026-03-11T19:24:39Z`

## Summary
Defines the technical design boundary for Design Document Index Relationship Alignment.

## Source Request
- Please do another internal project standards review, be ultra indepth and expansive in coverage, fix all identified issues using the normal task cycle as needed, and continue till every issue is identified, fixed, validated, committed, etc.
- Reproduced defect: feature-design `Affected Surfaces` paths are absent from design-index `related_paths` even though `Affected Surfaces` is a required standards-governed section.
- Reproduced defect: implementation plans that rely on linked PRDs or repo-local source paths fail design-index sync when `Source Designs` is `None`, despite the standards and template allowing that authoring shape.

## Scope and Feature Boundary
- Covers relationship derivation for feature-design `related_paths` and implementation-plan `source_paths` in the machine-readable design-document index.
- Covers the companion design-tracking output, design-document index example artifact, implementation-plan template guidance, and related standards text that describe those relationship fields.
- Covers regression tests and planning artifacts needed to keep the design-document family aligned after the fix.
- Does not redesign broader planning catalog semantics or invent new design-document schema fields when the existing fields can carry the corrected relationship data.
- Does not relax the requirement that implementation plans carry traceable source lineage.

## Current-State Context
- `DesignDocumentIndexSyncService` currently builds feature-design `related_paths` from linked implementation-plan IDs, front matter `applies_to`, and existing notes only; it never reads the required `Affected Surfaces` section.
- A live corpus audit shows many feature designs publishing repo-local affected surfaces that are missing from the generated design-document index, which means downstream query and planning surfaces cannot rely on the index to understand the full design footprint.
- The design-document index standard defines implementation-plan `source_paths` as driving feature-design, PRD, or other source-surface paths, while the implementation-plan template explicitly allows `Source Designs: None`.
- Despite that authored contract, sync currently requires mapped `Source Designs` IDs and raises when an implementation plan instead points to a linked PRD or repo-local source path in `Source Request or Design`.
- `DesignTrackingSyncService` labels implementation-plan sources as `Source Designs`, which reinforces the narrower implementation model even when the governing standards describe broader source lineage.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): shared parsing and relationship-derivation helpers should be explicit and composable so trackers and indexes do not encode different semantics.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): fail-closed repository governance requires derived planning surfaces to reflect the standards-valid authored relationship model.

## Internal Standards and Canonical References Applied
- [design_document_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/design_document_index_standard.md): the machine-readable design-document index must capture `related_paths` and `source_paths` consistently with the governed design corpus.
- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md): feature designs must publish `Affected Surfaces`, so the index should not drop that required relationship data.
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md): implementation plans may be driven by a feature design, PRD, or user request, so source-lineage derivation must support the traceable repo-local sources that contract already allows.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): relationship fields should carry normalized repository-relative paths rather than raw authored fragments.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): planning docs, task state, acceptance artifacts, and derived indexes must move in one traced change set.

## Design Goals and Constraints
- Project feature-design `Affected Surfaces` into machine-readable `related_paths` without dropping existing linked-plan or front-matter path relationships.
- Broaden implementation-plan `source_paths` derivation to match the existing standards contract without allowing untraceable free-text requests to satisfy the field.
- Preserve normalized repository-relative paths across all derived relationship fields, including document-relative authored links.
- Keep tracker wording and standards guidance aligned with the corrected source model so the repo does not continue to say `Source Designs` when the data now carries broader `Sources`.
- Fail closed when an implementation plan still lacks any traceable source surface after checking `Source Designs`, linked PRDs, and repo-local source references.

## Options Considered
### Option 1
- Patch only feature-design `related_paths` and leave implementation-plan source derivation unchanged.
- Strength: smallest change in the most obviously missing live-corpus field.
- Tradeoff: keeps the standards and template drift unresolved and still blocks PRD-backed plans from indexing correctly.

### Option 2
- Narrow the design-document index standard and implementation-plan guidance to require feature-design sources only.
- Strength: avoids broadening sync behavior.
- Tradeoff: contradicts the current implementation-plan standard and template, and discards a useful PRD-backed source model that the repo already documents.

### Option 3
- Align the index to the documented contract by deriving feature-design `related_paths` from `Affected Surfaces`, deriving implementation-plan `source_paths` from traceable design, PRD, and repo-local source surfaces, and updating tracker wording plus companion docs together.
- Strength: closes both reproduced defects at the relationship-derivation seam and preserves the authored standards contract.
- Tradeoff: touches sync, tracker wording, standards docs, template guidance, example artifacts, and tests in one slice.

## Recommended Design
### Architecture
- Add feature-design relationship derivation that normalizes repo-local paths from `Affected Surfaces` and merges them into `related_paths` alongside existing linked-plan and front-matter relationships.
- Add implementation-plan source derivation that merges mapped `Source Designs`, linked PRD document paths, and normalized repo-local paths cited in `Source Request or Design`.
- Keep both derivation paths inside the design-document index sync service so the index remains the canonical machine-readable relationship builder for design-family artifacts.
- Update design-tracking output to use neutral `Sources` wording for implementation-plan rows because the corrected source model is broader than feature designs only.

### Data and Interface Impacts
- `core/python/src/watchtower_core/repo_ops/sync/design_document_index.py` gains explicit feature-design `related_paths` and broadened implementation-plan `source_paths` derivation.
- `core/python/src/watchtower_core/repo_ops/sync/design_tracking.py` updates its implementation-plan table label and renders the broadened source set without implying all sources are designs.
- Standards and templates under `docs/standards/**` and `docs/templates/implementation_plan_template.md` clarify the corrected relationship semantics.
- The design-document index example artifact can demonstrate the supported relationship model without changing schema shape.

### Execution Flow
1. Rewrite the traced planning chain around the two reproduced relationship defects and split execution into feature-design related-path alignment and implementation-plan source-path alignment tasks.
2. Implement feature-design `Affected Surfaces` projection and implementation-plan source-surface derivation inside the design-document index sync path, then refresh the design tracker to use aligned source wording.
3. Update standards, template guidance, and companion example artifacts so the human and machine surfaces describe the same relationship contract.
4. Add regression coverage for both defects, rerun the repository validation stack, and close the trace with refreshed derived planning surfaces.

### Invariants and Failure Cases
- Feature-design `related_paths` must remain normalized repository-relative paths and must preserve existing linked-plan relationships instead of replacing them.
- Implementation-plan `source_paths` must prefer traceable repo-local sources only; free-text user-request prose without a repo-local source path must not silently satisfy the field.
- Document-relative authored links in `Affected Surfaces` or `Source Request or Design` must normalize to the same repository-relative paths that repository-absolute links would produce.
- Design-index sync must still fail clearly when an implementation plan has no traceable source surface after all supported derivation paths are considered.

## Affected Surfaces
- `docs/planning/design/`
- `docs/planning/design/design_tracking.md`
- `docs/standards/data_contracts/design_document_index_standard.md`
- `docs/standards/documentation/feature_design_md_standard.md`
- `docs/standards/documentation/implementation_plan_md_standard.md`
- `docs/templates/implementation_plan_template.md`
- `core/control_plane/examples/valid/indexes/design_document_index.v1.example.json`
- `core/python/src/watchtower_core/repo_ops/sync/design_document_index.py`
- `core/python/src/watchtower_core/repo_ops/sync/design_tracking.py`
- `core/python/tests/`

## Design Guardrails
- Do not encode one relationship model in standards and a narrower one in sync or tracker output.
- Do not weaken the requirement that implementation plans surface at least one traceable repo-local source when they are indexed.
- Do not introduce raw document-relative strings into machine-readable relationship fields; normalize them before publishing.

## Risks
- The feature-design change will add many new `related_paths` into the live index, so tests and validation need to prove downstream consumers still behave deterministically.
- Broadening implementation-plan `source_paths` without a clear precedence order could create duplicate or noisy source lists if the derivation does not deduplicate carefully.
- Tracker wording and standards text can drift again if the code fix lands without companion documentation updates in the same slice.

## References
- docs/standards/data_contracts/design_document_index_standard.md
- docs/standards/documentation/feature_design_md_standard.md
- docs/standards/documentation/implementation_plan_md_standard.md
- docs/templates/implementation_plan_template.md
- core/control_plane/examples/valid/indexes/design_document_index.v1.example.json
