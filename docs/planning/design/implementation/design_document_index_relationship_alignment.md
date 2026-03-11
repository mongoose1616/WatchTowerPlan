---
trace_id: trace.design_document_index_relationship_alignment
id: design.implementation.design_document_index_relationship_alignment
title: Design Document Index Relationship Alignment Implementation Plan
summary: Breaks Design Document Index Relationship Alignment into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-11T19:24:39Z'
audience: shared
authority: supporting
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

# Design Document Index Relationship Alignment Implementation Plan

## Record Metadata
- `Trace ID`: `trace.design_document_index_relationship_alignment`
- `Plan ID`: `design.implementation.design_document_index_relationship_alignment`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.design_document_index_relationship_alignment`
- `Linked Decisions`: `decision.design_document_index_relationship_alignment_direction`
- `Source Designs`: `design.features.design_document_index_relationship_alignment`
- `Linked Acceptance Contracts`: `contract.acceptance.design_document_index_relationship_alignment`
- `Updated At`: `2026-03-11T19:24:39Z`

## Summary
Breaks Design Document Index Relationship Alignment into a bounded implementation slice.

## Source Request or Design
- design.features.design_document_index_relationship_alignment

## Scope Summary
- Align feature-design `related_paths` with the standards-required `Affected Surfaces` section.
- Broaden implementation-plan `source_paths` derivation to support mapped source designs, linked PRDs, and repo-local source surfaces cited in `Source Request or Design`.
- Update the design tracker, companion standards and template guidance, example artifact, tests, and trace artifacts in the same change set.
- Do not redesign unrelated planning or query families outside the design-document relationship seam.

## Assumptions and Constraints
- The design-document index schema can remain structurally stable; the issue is the correctness of populated relationship fields, not the field names themselves.
- Feature-design `Affected Surfaces` and implementation-plan `Source Request or Design` may contain document-relative repo-local references, so the fix should reuse normalized repo-path extraction rather than inventing another parser.
- The implementation should fail closed when an implementation plan still lacks any traceable source surface after all supported derivation paths are checked.

## Internal Standards and Canonical References Applied
- [design_document_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/design_document_index_standard.md): the machine-readable design-document index should publish relationship data that matches the governed design-document family.
- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md): feature designs must publish `Affected Surfaces`, so the index should treat that section as authoritative relationship input.
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md): implementation plans may be driven by a design, PRD, or user request, which means source derivation must support the traceable repo-local source surfaces already allowed by the standard.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): relationship paths should remain normalized repository-relative values.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): planning docs, task records, acceptance artifacts, and derived indexes need to stay aligned through the full task cycle.

## Proposed Technical Approach
- Extend the design-document index sync service with explicit helper logic for feature-design `related_paths` and implementation-plan `source_paths` so both relationship fields come from standards-governed document sections or metadata instead of partially inferred prior state.
- Use repo-path extraction for feature-design `Affected Surfaces` and implementation-plan `Source Request or Design` so document-relative authored links normalize correctly.
- Add a PRD ID to path map inside design-index sync so linked PRDs can participate in `source_paths` without requiring a source-design ID.
- Update design-tracking output to label implementation-plan origins as `Sources` instead of `Source Designs`.
- Refresh companion standards, implementation-plan template guidance, and the design-document index example to match the corrected relationship model.

## Work Breakdown
1. Rewrite the traced planning artifacts to capture the confirmed relationship defects and split execution into feature-design related-path alignment and implementation-plan source-path alignment tasks.
2. Implement feature-design `Affected Surfaces` projection and broadened implementation-plan source-path derivation in design-index sync, then align design-tracking wording with the corrected source model.
3. Update standards, template guidance, and example artifacts so the human-readable contract matches the machine-readable relationship behavior.
4. Add regression coverage for both defects, rerun validation, close the tasks and initiative, refresh derived surfaces, and commit the bounded slice.

## Risks
- Deriving more feature-design `related_paths` can materially expand the live index, which raises regression risk in downstream derived planning surfaces.
- Implementation-plan source derivation needs careful deduplication so a source design, linked PRD, and source-section path do not create noisy duplicates.
- If the documentation changes land without code or test updates, the repo will continue to advertise a relationship contract it cannot actually fulfill.

## Validation Plan
- `./.venv/bin/pytest -q tests/unit/test_design_document_index_sync.py`
- `./.venv/bin/pytest -q tests/unit/test_tracking_output_compaction.py`
- `./.venv/bin/python -m mypy src/watchtower_core`
- `./.venv/bin/ruff check`
- `./.venv/bin/watchtower-core validate acceptance --trace-id trace.design_document_index_relationship_alignment --format json`
- `./.venv/bin/watchtower-core validate all --format json`
- `./.venv/bin/pytest -q`
- Final refreshed planning evidence under `core/control_plane/ledgers/validation_evidence/design_document_index_relationship_alignment_planning_baseline.v1.json`

## References
- docs/standards/data_contracts/design_document_index_standard.md
- docs/standards/documentation/feature_design_md_standard.md
- docs/standards/documentation/implementation_plan_md_standard.md
- docs/templates/implementation_plan_template.md
- core/control_plane/examples/valid/indexes/design_document_index.v1.example.json
