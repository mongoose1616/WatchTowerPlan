---
trace_id: trace.standard_authoring_surface_alignment
id: design.implementation.standard_authoring_surface_alignment
title: Standard Authoring Surface Alignment Implementation Plan
summary: Breaks Standard Authoring Surface Alignment into a bounded implementation
  slice.
type: implementation_plan
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

# Standard Authoring Surface Alignment Implementation Plan

## Record Metadata
- `Trace ID`: `trace.standard_authoring_surface_alignment`
- `Plan ID`: `design.implementation.standard_authoring_surface_alignment`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.standard_authoring_surface_alignment`
- `Linked Decisions`: `decision.standard_authoring_surface_alignment_direction`
- `Source Designs`: `design.features.standard_authoring_surface_alignment`
- `Linked Acceptance Contracts`: `contract.acceptance.standard_authoring_surface_alignment`
- `Updated At`: `2026-03-11T20:05:00Z`

## Summary
Breaks Standard Authoring Surface Alignment into a bounded implementation slice.

## Source Request or Design
- design.features.standard_authoring_surface_alignment

## Scope Summary
- Align the governed standard-document template with the current Standard Document Standard and validator contract.
- Update the Standard Document Standard so the standard template is indexed and queryable as an operational surface.
- Add regression coverage for template alignment and standards-query operationalization lookup.
- Refresh trace artifacts, derived indexes, and trackers in the same change set.

## Assumptions and Constraints
- No standard-index schema change is needed; correcting the source standard document is sufficient for the derived lookup behavior.
- The existing `watchtower-core query standards --operationalization-path` filter already models the desired lookup and should remain unchanged.
- The fix should remain compact and documentation-first; introducing special-case runtime code for one template path would be the wrong layer.

## Internal Standards and Canonical References Applied
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): the template must match the required section contract for governed standard docs.
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): operationalization metadata should expose the real authoring and enforcement surfaces used by a standard.
- [documentation_semantics_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/documentation_semantics_standard.md): the authoring scaffold should not direct maintainers toward outputs that violate the live semantic validator.
- [compact_document_authoring_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/compact_document_authoring_standard.md): the repaired template should stay compact even while restoring required sections.

## Proposed Technical Approach
- Rewrite [standard_document_template.md](/home/j/WatchTowerPlan/docs/templates/standard_document_template.md) to include the required standard-document sections, correct explained-bullet guidance, `Operationalization`, and `Updated At`.
- Update [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md) so its related sources, operationalization metadata, and companion references explicitly include the standard template.
- Add an integration test that checks the standard template remains aligned with the required section contract.
- Add a CLI query test that asserts querying by `docs/templates/standard_document_template.md` returns `std.documentation.standard_md`.
- Refresh the standard index and traced planning artifacts through the normal sync and closeout flows.

## Work Breakdown
1. Rewrite the traced planning chain and split the work into template-contract alignment and standards-lookup alignment tasks.
2. Update the standard template and the governing Standard Document Standard to publish one coherent authoring contract.
3. Add regression coverage for template alignment and template-path standards lookup.
4. Refresh acceptance and validation evidence, close the tasks and initiative, rerun validation, and commit the completed slice.

## Risks
- If the template update is too terse, it could still leave out guidance authors need to satisfy explained-bullet requirements for `Related Standards and Sources`.
- If the standard document is updated but the standard index is not refreshed, the query reproduction will remain broken despite the source fix.
- Template-focused tests need to check contract shape rather than exact prose so future wording improvements do not create noisy failures.

## Validation Plan
- `./.venv/bin/pytest -q core/python/tests/unit/test_cli_query_commands.py`
- `./.venv/bin/pytest -q core/python/tests/integration/test_control_plane_artifacts.py`
- `./.venv/bin/python -m mypy src/watchtower_core`
- `./.venv/bin/ruff check`
- `./.venv/bin/watchtower-core validate acceptance --trace-id trace.standard_authoring_surface_alignment --format json`
- `./.venv/bin/watchtower-core validate all --format json`
- `./.venv/bin/pytest -q`

## References
- docs/standards/documentation/standard_md_standard.md
- docs/templates/standard_document_template.md
- core/python/tests/unit/test_cli_query_commands.py
- core/python/tests/integration/test_control_plane_artifacts.py
