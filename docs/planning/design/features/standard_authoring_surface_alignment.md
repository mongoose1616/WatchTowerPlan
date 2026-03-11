---
trace_id: trace.standard_authoring_surface_alignment
id: design.features.standard_authoring_surface_alignment
title: Standard Authoring Surface Alignment Feature Design
summary: Defines the technical design boundary for Standard Authoring Surface Alignment.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-11T20:05:00Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/documentation/standard_md_standard.md
- docs/templates/standard_document_template.md
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/integration/test_control_plane_artifacts.py
- core/control_plane/indexes/standards/standard_index.v1.json
---

# Standard Authoring Surface Alignment Feature Design

## Record Metadata
- `Trace ID`: `trace.standard_authoring_surface_alignment`
- `Design ID`: `design.features.standard_authoring_surface_alignment`
- `Design Status`: `active`
- `Linked PRDs`: `prd.standard_authoring_surface_alignment`
- `Linked Decisions`: `decision.standard_authoring_surface_alignment_direction`
- `Linked Implementation Plans`: `design.implementation.standard_authoring_surface_alignment`
- `Updated At`: `2026-03-11T20:05:00Z`

## Summary
Defines the technical design boundary for Standard Authoring Surface Alignment.

## Source Request
- Please do another internal project standards review, be ultra indepth and expansive in coverage, fix all identified issues using the normal task cycle as needed, and continue till every issue is identified, fixed, validated, committed, etc.
- Reproduced defect: the governed standard-document template omits required sections and marks contract-required sections optional.
- Reproduced defect: querying standards by `docs/templates/standard_document_template.md` returns no results because the Standard Document Standard does not index its own authoring scaffold as an operational surface.

## Scope and Feature Boundary
- Covers the authoring contract for governed standard documents and the standards lookup path from the authoring scaffold to its governing standard.
- Covers the standard template, the governing Standard Document Standard, derived standard-index output, and regression coverage proving the authoring seam stays aligned.
- Does not redesign unrelated document-family templates or change the standard-index schema shape.
- Does not add a new standards query capability when the existing `--operationalization-path` filter already models the required lookup.

## Current-State Context
- [standard_document_template.md](/home/j/WatchTowerPlan/docs/templates/standard_document_template.md) currently omits `Scope`, `Use When`, `Related Standards and Sources`, `Operationalization`, and `Updated At`, even though [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md) and `validator.documentation.standard_semantics` require those sections.
- The template also tells authors those sections are optional, which means the canonical scaffold encodes the wrong contract at the point of authoring.
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md) currently omits [standard_document_template.md](/home/j/WatchTowerPlan/docs/templates/standard_document_template.md) from its `Related Standards and Sources`, `Operationalization`, and `References` surfaces.
- Because standard-index sync derives operationalization data from the standard document itself, `watchtower-core query standards --operationalization-path docs/templates/standard_document_template.md --format json` currently returns zero results.
- No existing automated coverage asserts that the standard template stays aligned with the governed standard-document contract or that the template operationalization path resolves back to `std.documentation.standard_md`.

## Foundations References Applied
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): the repo should keep its authoring entrypoints aligned with the governed standard they operationalize.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): lookup and authoring seams should be explicit, deterministic, and regression-tested rather than inferred from reviewer memory.

## Internal Standards and Canonical References Applied
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): the template and lookup surfaces must reflect the current required section set and operationalization model for standards.
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): the standard index should expose real operational surfaces so query tooling can find the governing standard from the authoring scaffold.
- [documentation_semantics_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/documentation_semantics_standard.md): template guidance should not normalize output that would violate the shared semantic validator once authored as a governed standard.
- [compact_document_authoring_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/compact_document_authoring_standard.md): the template should remain concise, but compactness cannot contradict required contract sections.

## Design Goals and Constraints
- Make the standard template author the live standards-valid shape instead of an outdated minimal subset.
- Keep the template concise enough to satisfy compact-authoring expectations while still surfacing all required governed sections.
- Publish the standard template as a real operational surface of `std.documentation.standard_md` so query and index outputs can answer the authoring-governance lookup directly.
- Add regression coverage at the repo-contract and CLI lookup layers so future drift is caught without relying on manual standards reviews.
- Avoid changing query behavior or schema shape when corrected source data and tests are sufficient.

## Options Considered
### Option 1
- Patch only [standard_document_template.md](/home/j/WatchTowerPlan/docs/templates/standard_document_template.md) and leave the governing standard plus query coverage unchanged.
- Strength: smallest documentation delta.
- Tradeoff: leaves the template-to-governing-standard lookup gap unresolved and does not prevent the same omission from recurring.

### Option 2
- Narrow the Standard Document Standard so the stale template becomes valid again.
- Strength: avoids adding sections back into the template.
- Tradeoff: weakens the live standard contract and validator alignment instead of fixing the authoring seam that drifted.

### Option 3
- Align the template, the governing standard’s companion-surface declarations, the derived standard index, and regression coverage in one bounded slice.
- Strength: restores one coherent contract across authoring, indexing, query, and validation surfaces.
- Tradeoff: touches docs, tests, and derived artifacts together.

## Recommended Design
### Architecture
- Rewrite [standard_document_template.md](/home/j/WatchTowerPlan/docs/templates/standard_document_template.md) so its default scaffold matches the required section set and guidance defined by [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md).
- Update [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md) so it explicitly cites and operationalizes the standard template as a governing authoring surface.
- Let existing standard-index sync rebuild `operationalization_paths` from the corrected standard document instead of adding special-case code.
- Add one repo-contract test for template alignment and one CLI standards-query test for the template operationalization lookup.

### Data and Interface Impacts
- The standard template gains the required governed standard-document sections and corrected authoring notes.
- The Standard Document Standard gains the template in `Related Standards and Sources`, `Operationalization`, and companion references.
- The live standard index gains `docs/templates/standard_document_template.md` in the `operationalization_paths` for `std.documentation.standard_md`.
- The `watchtower-core query standards --operationalization-path ...` surface gains the expected result through corrected indexed data, not through a CLI interface change.

### Execution Flow
1. Rewrite the traced planning artifacts to record the reproduced template-contract and standards-lookup defects.
2. Align the standard template with the governed section contract and companion authoring guidance.
3. Update the Standard Document Standard so its template is a first-class companion and operational surface.
4. Add regression coverage for template alignment and standards query lookup, then refresh derived artifacts and close the trace.

### Invariants and Failure Cases
- The standard template must no longer instruct authors that contract-required sections are optional.
- The governing standard must remain the source of truth for standard-index operationalization data; the fix should not introduce hard-coded query exceptions.
- Querying standards by `docs/templates/standard_document_template.md` must resolve to `std.documentation.standard_md` after the doc fix lands.
- Regression coverage must fail if required standard-template sections disappear or if the template operationalization path drops out of the standard index again.

## Affected Surfaces
- `docs/standards/documentation/standard_md_standard.md`
- `docs/templates/standard_document_template.md`
- `core/control_plane/indexes/standards/standard_index.v1.json`
- `core/python/tests/unit/test_cli_query_commands.py`
- `core/python/tests/integration/test_control_plane_artifacts.py`
- `docs/planning/`

## Design Guardrails
- Do not weaken the Standard Document Standard to match the stale template.
- Do not add query-time special cases when corrected standard-index source data is sufficient.
- Do not add low-value boilerplate back into the template beyond what the governed contract actually requires.

## Risks
- Template changes can become verbose if they overcorrect for the missing sections instead of staying compact and directive.
- Query regression coverage can become brittle if it snapshots unrelated standard-index fields rather than checking the specific template lookup contract.
- If the standard document is updated without refreshing derived standard-index output, the repo will still exhibit lookup drift even though the source doc is fixed.

## References
- docs/standards/documentation/standard_md_standard.md
- docs/standards/data_contracts/standard_index_standard.md
- docs/templates/standard_document_template.md
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/integration/test_control_plane_artifacts.py
