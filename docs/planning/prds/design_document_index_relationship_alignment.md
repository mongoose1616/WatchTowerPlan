---
trace_id: trace.design_document_index_relationship_alignment
id: prd.design_document_index_relationship_alignment
title: Design Document Index Relationship Alignment PRD
summary: Closes reproduced design-document index drift by projecting feature-design
  affected surfaces into related_paths and deriving implementation-plan source_paths
  from traceable PRD or repo-local sources instead of requiring Source Designs only.
type: prd
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

# Design Document Index Relationship Alignment PRD

## Record Metadata
- `Trace ID`: `trace.design_document_index_relationship_alignment`
- `PRD ID`: `prd.design_document_index_relationship_alignment`
- `Status`: `active`
- `Linked Decisions`: `decision.design_document_index_relationship_alignment_direction`
- `Linked Designs`: `design.features.design_document_index_relationship_alignment`
- `Linked Implementation Plans`: `design.implementation.design_document_index_relationship_alignment`
- `Updated At`: `2026-03-11T19:24:39Z`

## Summary
Closes reproduced design-document index drift by projecting feature-design affected surfaces into `related_paths` and deriving implementation-plan `source_paths` from traceable PRD or repo-local sources instead of requiring `Source Designs` only.

## Problem Statement
The standards review reproduced two live defects in the design-document indexing boundary. First, `DesignDocumentIndexSyncService` does not project the required `Affected Surfaces` section from feature designs into the index `related_paths` field. The live repository already shows this drift: many feature-design documents publish repo-local affected surfaces that are absent from the machine-readable design index because sync only preserves linked implementation-plan paths, front matter `applies_to`, and previously stored notes. As a result, design queries, planning catalog projections, and design-tracking surfaces underreport the repository paths those designs actually target.

Second, implementation-plan `source_paths` are currently derived from `Source Designs` only. That is stricter than the governed contract. The design-document index standard defines `source_paths` as paths to the driving feature design, PRD, or other source surfaces, and the implementation-plan template explicitly allows `Source Designs: None`. A reproduced temp-repo fixture with a linked PRD and a repo-local source path in `Source Request or Design` fails index generation today because sync raises an error when no source-design ID exists. This means durable, standards-valid implementation plans cannot currently rely on PRD- or repo-path-driven source lineage even though the standards and template say they can.

Together these defects make the design-document index less trustworthy as the machine-readable relationship surface for design work. Feature designs lose machine-visible affected-path lineage, implementation plans are forced into an unnecessarily narrow source model, and the human-readable design tracker compounds that drift by labeling all implementation-plan sources as `Source Designs` even when the standard allows broader source surfaces.

## Goals
- Make feature-design `related_paths` reflect the actual repo-local `Affected Surfaces` published in governed feature-design documents.
- Make implementation-plan `source_paths` derive from traceable source surfaces including `Source Designs`, linked PRDs, and repo-local paths cited in `Source Request or Design`.
- Keep the design-document index, design tracker, standards docs, template guidance, tests, and planning evidence aligned in one bounded trace.
- Return the repository to a green validation baseline after the fixes land.

## Non-Goals
- Redesigning the broader planning-document model outside the design-document relationship fields reproduced here.
- Changing the schema shape of the design-document index unless a structural change becomes necessary to close the reproduced defects.
- Reworking unrelated query or tracking families that already consume the design-document index correctly once its fields are fixed.
- Replacing the existing feature-design or implementation-plan document families.

## Requirements
- `req.design_document_index_relationship_alignment.001`: This trace must publish a real PRD, accepted direction decision, feature design, implementation plan, updated acceptance contract, refreshed planning-baseline evidence, a closed bootstrap task, and bounded execution tasks for each confirmed relationship-alignment defect.
- `req.design_document_index_relationship_alignment.002`: Feature-design index entries must project repo-local paths from the required `Affected Surfaces` section into `related_paths`, preserving normalized repository-relative paths.
- `req.design_document_index_relationship_alignment.003`: Implementation-plan index entries must derive `source_paths` from the traceable design and planning surfaces the standards already allow, including `Source Designs`, linked PRDs, and repo-local source paths cited in `Source Request or Design`.
- `req.design_document_index_relationship_alignment.004`: Companion standards, template guidance, machine-readable examples, design-tracking output, and regression coverage must stay aligned with the updated relationship semantics.
- `req.design_document_index_relationship_alignment.005`: The repository must return to a green baseline on `./.venv/bin/watchtower-core validate acceptance --trace-id trace.design_document_index_relationship_alignment --format json`, `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/python -m mypy src/watchtower_core`, and `./.venv/bin/ruff check`.

## Acceptance Criteria
- `ac.design_document_index_relationship_alignment.001`: The trace publishes the full planning chain, the accepted decision, the refreshed acceptance contract and planning-baseline evidence, the closed bootstrap task, and two bounded execution tasks covering feature-design related-path projection and implementation-plan source-path derivation.
- `ac.design_document_index_relationship_alignment.002`: Regression coverage proves feature designs now project normalized repo-local `Affected Surfaces` into design-index `related_paths` and derived design-tracking or planning surfaces preserve that relationship data.
- `ac.design_document_index_relationship_alignment.003`: Regression coverage proves implementation plans can build valid `source_paths` from linked PRDs or repo-local source paths without requiring `Source Designs`, while still failing closed when no traceable source surface exists.
- `ac.design_document_index_relationship_alignment.004`: The design-document index standard, implementation-plan guidance, example artifact, tracker wording, and affected runtime helpers describe the updated relationship semantics accurately enough that future contributors do not restore the narrower source model or omit feature-design affected surfaces.
- `ac.design_document_index_relationship_alignment.005`: The repository passes `./.venv/bin/watchtower-core validate acceptance --trace-id trace.design_document_index_relationship_alignment --format json`, `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/python -m mypy src/watchtower_core`, and `./.venv/bin/ruff check` after the trace closes.

## Risks and Dependencies
- The feature-design fix touches a broad machine-readable relationship surface, so regression coverage needs to prove the additional `related_paths` do not regress existing linked-plan or front-matter behavior.
- The implementation-plan source fix needs to broaden accepted source derivation without allowing untraceable free-text requests to masquerade as governed source paths.
- Companion standards, template guidance, generated tracker wording, and machine-readable examples must move with the code change or the repository will reintroduce standards drift in a different layer.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): relationship derivation should come from explicit, shared parsing seams instead of ad hoc tracker-specific logic.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): machine-readable planning surfaces should conform to the governed document contract instead of silently narrowing it.

## References
- docs/standards/data_contracts/design_document_index_standard.md
- docs/standards/documentation/feature_design_md_standard.md
- docs/standards/documentation/implementation_plan_md_standard.md
- docs/templates/implementation_plan_template.md
- core/control_plane/examples/valid/indexes/design_document_index.v1.example.json
