---
trace_id: trace.design_document_index_relationship_alignment
id: decision.design_document_index_relationship_alignment_direction
title: Design Document Index Relationship Alignment Direction Decision
summary: Records the accepted direction for Design Document Index Relationship
  Alignment.
type: decision_record
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

# Design Document Index Relationship Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.design_document_index_relationship_alignment`
- `Decision ID`: `decision.design_document_index_relationship_alignment_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.design_document_index_relationship_alignment`
- `Linked Designs`: `design.features.design_document_index_relationship_alignment`
- `Linked Implementation Plans`: `design.implementation.design_document_index_relationship_alignment`
- `Updated At`: `2026-03-11T19:24:39Z`

## Summary
Records the accepted direction for Design Document Index Relationship Alignment.

## Decision Statement
Align the design-document index to the authored standards contract by projecting feature-design `Affected Surfaces` into `related_paths`, deriving implementation-plan `source_paths` from traceable design, PRD, and repo-local source surfaces, and updating tracker wording plus companion docs to match the broadened relationship model.

## Trigger or Source Request
- Please do another internal project standards review, be ultra indepth and expansive in coverage, fix all identified issues using the normal task cycle as needed, and continue till every issue is identified, fixed, validated, committed, etc.
- Reproduced defect: feature-design `Affected Surfaces` are missing from machine-readable `related_paths` even though they are required by the feature-design standard.
- Reproduced defect: implementation plans backed by linked PRDs or repo-local source paths fail design-index sync when `Source Designs` is `None`, despite the standards and template allowing that authoring shape.

## Current Context and Constraints
- The design-document index already has fields for `related_paths` and `source_paths`; the defect is that sync populates them too narrowly.
- The live feature-design corpus already shows missing `Affected Surfaces` projection, so this is not just a latent edge case.
- The implementation-plan template explicitly allows `Source Designs: None`, which means the current sync requirement for source-design IDs is stricter than the authored guidance.
- Derived planning and tracking surfaces consume the design-document index, so relationship drift here spreads into multiple downstream views.

## Applied References and Implications
- [design_document_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/design_document_index_standard.md): the index must carry relationship data that matches the design-document family rather than a narrower implementation shortcut.
- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md): the required `Affected Surfaces` section is the authoritative feature-design relationship input and should not be omitted from the index.
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md): implementation plans may be design-, PRD-, or request-driven, so traceable PRD or repo-local source surfaces must be supported in `source_paths`.
- [implementation_plan_template.md](/home/j/WatchTowerPlan/docs/templates/implementation_plan_template.md): the template already signals that `Source Designs` may be `None`, so sync and tracker wording must not force a design-only model.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): relationship fields need normalized repository-relative paths, not raw authored fragments.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): shared parsing seams should drive correctness instead of ad hoc tracker-specific logic.

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

## Options Considered
### Option 1
- Project feature-design `Affected Surfaces` only and leave implementation-plan sources design-only.
- Strength: smaller code delta.
- Tradeoff: leaves the standards and template drift unresolved and still blocks PRD-backed plans.

### Option 2
- Narrow the standards and template so implementation plans must always carry source-design IDs and the design tracker can keep `Source Designs` wording.
- Strength: avoids broadening sync logic.
- Tradeoff: contradicts the current authored contract and throws away useful PRD-backed lineage.

### Option 3
- Align sync, tracker wording, standards, template guidance, and tests around the broader relationship model already documented by the repository.
- Strength: closes both reproduced defects in one bounded relationship-alignment slice.
- Tradeoff: touches code, docs, examples, and derived surfaces together.

## Chosen Outcome
Adopt option 3. The repository should preserve the broader authored relationship contract and make the design-document index plus design tracker conform to it.

## Rationale and Tradeoffs
- The reproduced failures are both relationship-derivation drift, so one bounded fix at the design-index seam is more durable than separate one-off patches.
- Narrowing the standards would resolve the mismatch by weakening the repo contract rather than fixing the implementation defect.
- The aligned fix touches multiple surfaces, but it restores trust in the design-document index as the machine-readable relationship authority for design work.

## Consequences and Follow-Up Impacts
- Feature-design entries will gain more `related_paths` because required `Affected Surfaces` data will finally be projected.
- Implementation-plan `source_paths` and design-tracking output will become more general, so the human tracker should use `Sources` wording instead of `Source Designs`.
- Standards text, template guidance, example artifacts, tests, and derived planning surfaces need to change together or the repository will reintroduce drift in another layer.

## Risks, Dependencies, and Assumptions
- The fix assumes repo-local source paths can be extracted deterministically from `Source Request or Design` when they exist.
- The broadened source model depends on careful deduplication across source designs, linked PRDs, and repo-local source references.
- Final closeout depends on the derived design, planning, task, initiative, and coordination surfaces returning to a clean state after the tasks are closed.

## References
- docs/standards/data_contracts/design_document_index_standard.md
- docs/standards/documentation/feature_design_md_standard.md
- docs/standards/documentation/implementation_plan_md_standard.md
- docs/templates/implementation_plan_template.md
- core/control_plane/examples/valid/indexes/design_document_index.v1.example.json
