---
trace_id: trace.standard_authoring_surface_alignment
id: decision.standard_authoring_surface_alignment_direction
title: Standard Authoring Surface Alignment Direction Decision
summary: Records the accepted direction for Standard Authoring Surface Alignment.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-11T20:05:00Z'
audience: shared
authority: supporting
applies_to:
- docs/standards/documentation/standard_md_standard.md
- docs/templates/standard_document_template.md
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/integration/test_control_plane_artifacts.py
- core/control_plane/indexes/standards/standard_index.v1.json
---

# Standard Authoring Surface Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.standard_authoring_surface_alignment`
- `Decision ID`: `decision.standard_authoring_surface_alignment_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.standard_authoring_surface_alignment`
- `Linked Designs`: `design.features.standard_authoring_surface_alignment`
- `Linked Implementation Plans`: `design.implementation.standard_authoring_surface_alignment`
- `Updated At`: `2026-03-11T20:05:00Z`

## Summary
Records the accepted direction for Standard Authoring Surface Alignment.

## Decision Statement
Align the standard-authoring scaffold, the governing Standard Document Standard, and regression coverage around one live contract by fixing the template itself, operationalizing that template in the governing standard, and testing the standards lookup path that depends on it.

## Trigger or Source Request
- Please do another internal project standards review, be ultra indepth and expansive in coverage, fix all identified issues using the normal task cycle as needed, and continue till every issue is identified, fixed, validated, committed, etc.
- Reproduced defect: the standard-document template omits contract-required sections and tells authors some of those sections are optional.
- Reproduced defect: querying standards by `docs/templates/standard_document_template.md` returns zero results because the governing standard does not index its own authoring scaffold as an operational surface.

## Current Context and Constraints
- The repo already has a live Standard Document Standard, a semantic validator, a standard index, and a standards query path; the defect is misalignment among those surfaces.
- The standard index already supports `operationalization_paths`, so the missing query result is driven by stale source documentation rather than a missing query feature.
- The template should stay compact, but compactness cannot override the live required section set for governed standard documents.
- No automated regression currently checks this authoring seam, so any fix should add durable test coverage rather than relying on future reviews to spot the same drift.

## Applied References and Implications
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): the governing standard should remain the source of truth for both template shape and standard-index operationalization.
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): operationalization metadata should expose the real authoring and enforcement surfaces that standards query relies on.
- [documentation_semantics_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/documentation_semantics_standard.md): the authoring scaffold should not instruct maintainers toward outputs that would violate current semantic validation.
- [compact_document_authoring_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/compact_document_authoring_standard.md): the repaired template should restore required sections without reintroducing gratuitous boilerplate.

## Affected Surfaces
- `docs/standards/documentation/standard_md_standard.md`
- `docs/templates/standard_document_template.md`
- `core/control_plane/indexes/standards/standard_index.v1.json`
- `core/python/tests/unit/test_cli_query_commands.py`
- `core/python/tests/integration/test_control_plane_artifacts.py`
- `docs/planning/`

## Options Considered
### Option 1
- Patch only the standard template.
- Strength: smallest initial change.
- Tradeoff: leaves the template-to-standard lookup gap and regression gap unresolved.

### Option 2
- Narrow the Standard Document Standard to fit the stale template.
- Strength: avoids expanding the template.
- Tradeoff: weakens the governed contract and contradicts the live validator behavior.

### Option 3
- Align the template, the governing standard’s operationalization metadata, and regression coverage in one bounded change.
- Strength: restores one coherent contract across authoring, indexing, query, and validation surfaces.
- Tradeoff: requires coordinated updates across docs, tests, and derived artifacts.

## Chosen Outcome
Adopt option 3. The repository should preserve the current standard-document contract, repair the canonical authoring scaffold to match it, and make the template discoverable through the existing standards lookup path.

## Rationale and Tradeoffs
- The live defect is contract drift at the authoring seam, not an over-strict validator. Weakening the contract would hide the defect rather than solve it.
- The standards query failure is downstream of stale source documentation, so correcting the source standard is more durable than adding code-side exceptions.
- Adding regression coverage keeps the fix small but durable by exercising both the template contract and the user-visible query lookup that depends on it.

## Consequences and Follow-Up Impacts
- The standard template will grow slightly to restore the required sections and guidance needed for compliant standard authoring.
- The Standard Document Standard and derived standard index will expose the standard template as a first-class operational surface.
- Querying standards by `docs/templates/standard_document_template.md` will become a supported lookup path backed by source data and tests.

## Risks, Dependencies, and Assumptions
- The fix assumes the repo wants the existing Standard Document Standard and validator contract to remain authoritative.
- The repaired template must stay concise enough that maintainers continue using it instead of treating it as overly ceremonial.
- Final closeout depends on refreshing the standard index and planning surfaces after the standard doc and tests change.

## References
- docs/standards/documentation/standard_md_standard.md
- docs/standards/data_contracts/standard_index_standard.md
- docs/templates/standard_document_template.md
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/integration/test_control_plane_artifacts.py
