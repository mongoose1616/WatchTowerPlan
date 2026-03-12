---
trace_id: trace.documentation_family_lookup_and_readme_template_alignment
id: design.implementation.documentation_family_lookup_and_readme_template_alignment
title: Documentation Family Lookup and README Template Alignment Implementation Plan
summary: Breaks Documentation Family Lookup and README Template Alignment into a bounded
  implementation slice.
type: implementation_plan
status: draft
owner: repository_maintainer
updated_at: '2026-03-12T00:58:00Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/repo_ops/standards.py
- core/python/src/watchtower_core/repo_ops/query/standards.py
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/integration/test_control_plane_artifacts.py
- docs/commands/core_python/watchtower_core_query_standards.md
- docs/standards/data_contracts/standard_index_standard.md
- docs/standards/documentation/standard_md_standard.md
- docs/standards/documentation/readme_md_standard.md
- docs/standards/documentation/agents_md_standard.md
- docs/standards/documentation/reference_md_standard.md
- docs/templates/readme_template.md
---

# Documentation Family Lookup and README Template Alignment Implementation Plan

## Record Metadata
- `Trace ID`: `trace.documentation_family_lookup_and_readme_template_alignment`
- `Plan ID`: `design.implementation.documentation_family_lookup_and_readme_template_alignment`
- `Plan Status`: `draft`
- `Linked PRDs`: `prd.documentation_family_lookup_and_readme_template_alignment`
- `Linked Decisions`: `decision.documentation_family_lookup_and_readme_template_alignment_direction`
- `Source Designs`: `design.features.documentation_family_lookup_and_readme_template_alignment`
- `Linked Acceptance Contracts`: `None`
- `Updated At`: `2026-03-12T00:58:00Z`

## Summary
Breaks Documentation Family Lookup and README Template Alignment into a bounded implementation slice.

## Source Request or Design
- Another expansive internal standards review confirmed two live issues: standards lookup cannot reliably resolve several concrete governed docs because operationalization metadata cannot represent repeating filename families or some family-document surfaces, and the README template still drifts from the governed README title contract.

## Scope Summary
- Covers operationalization glob support in the standards parser and query service, live standard-document metadata updates, standards-query command docs, and README template/test alignment.
- Excludes unrelated document-family changes and any new generic README or AGENTS validation framework.

## Assumptions and Constraints
- The standard-index schema remains structurally unchanged; only the allowed operationalization string semantics expand.
- The implementation must preserve existing exact and directory-descendant standards lookup behavior for current callers.

## Internal Standards and Canonical References Applied
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): the index must stay compact and auditable while gaining enough expressiveness for repeating file families.
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): operationalization metadata changes must remain explicit in the standards corpus itself.
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): the README template update must follow the governed title and inventory contract.
- [compact_document_authoring_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/compact_document_authoring_standard.md): the template should stay compact and avoid low-value pre-inventory scaffolding.

## Proposed Technical Approach
- Add glob-aware operationalization parsing and matching helpers in the standards repo-ops layer, then reuse them from standard-index sync, document semantics, and standards query behavior.
- Update the affected standards to publish precise family-document operationalization surfaces, then align the standards query docs/help text and README template with the new contract.

## Work Breakdown
1. Implement bounded glob-pattern support for standard operationalization surfaces and add unit coverage for sync, validation, and standards-query matching.
2. Update the AGENTS, README, reference, and standard document-family standards plus the standards-query docs/help text to use the corrected operationalization model.
3. Align the README template with the governed README title and inventory ordering contract, then add integration coverage for the live artifact wording.

## Risks
- Overly broad patterns could create noisy lookup results, so the live standards should use the narrowest patterns that cover the governed family.

## Validation Plan
- Run targeted unit coverage for standards query, standard-index sync, and document-semantics validation.
- Run artifact integration coverage for the updated live standards and README template.
- Re-run `watchtower-core validate acceptance --trace-id trace.documentation_family_lookup_and_readme_template_alignment --format json`, `watchtower-core validate all --format json`, `pytest -q`, `python -m mypy src/watchtower_core`, and `ruff check .`.

## References
- docs/standards/data_contracts/standard_index_standard.md
- docs/standards/documentation/standard_md_standard.md
- docs/standards/documentation/readme_md_standard.md
- docs/standards/documentation/agents_md_standard.md
- docs/standards/documentation/reference_md_standard.md
- docs/standards/documentation/compact_document_authoring_standard.md
