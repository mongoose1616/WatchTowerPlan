---
trace_id: trace.foundations_documentation_completeness_alignment
id: design.implementation.foundations_documentation_completeness_alignment
title: Foundations Documentation Completeness Alignment Implementation Plan
summary: Breaks Foundations Documentation Completeness Alignment into a bounded implementation
  slice.
type: implementation_plan
status: draft
owner: repository_maintainer
updated_at: '2026-03-12T21:27:00Z'
audience: shared
authority: supporting
applies_to:
- docs/foundations/
- workflows/modules/foundations_context_review.md
- docs/commands/core_python/watchtower_core_query_foundations.md
- core/python/src/watchtower_core/cli/query_knowledge_family.py
- core/python/src/watchtower_core/cli/query_knowledge_handlers.py
- core/control_plane/indexes/foundations/
- core/python/tests/
- docs/planning/
- core/control_plane/contracts/acceptance/
- core/control_plane/ledgers/validation_evidence/
---

# Foundations Documentation Completeness Alignment Implementation Plan

## Record Metadata
- `Trace ID`: `trace.foundations_documentation_completeness_alignment`
- `Plan ID`: `design.implementation.foundations_documentation_completeness_alignment`
- `Plan Status`: `draft`
- `Linked PRDs`: `prd.foundations_documentation_completeness_alignment`
- `Linked Decisions`: `decision.foundations_documentation_completeness_alignment_direction`
- `Source Designs`: `design.features.foundations_documentation_completeness_alignment`
- `Linked Acceptance Contracts`: `None`
- `Updated At`: `2026-03-12T21:27:00Z`

## Summary
Implement the confirmed documentation and workflow alignment fixes without changing foundation query semantics or contracts.

## Source Request or Design
- Do a comprehensive internal project review for documentation completeness and cohesiveness with foundations/**.

## Scope Summary
- Update the authoritative foundations-aware workflow guidance.
- Update the engineering stack foundation references so the synced foundation index carries complete reference metadata.
- Update foundations query help/docs to use live corpus-backed examples and wording.
- Add targeted regression coverage and sync/validation evidence for the repaired surfaces.

## Assumptions and Constraints
- Preserve the existing foundation query contract and payload shape.
- Preserve the current foundation index schema and derive all machine-readable changes from source Markdown plus normal sync commands.
- Assume the existing local reference corpus already contains the technologies and standards named by the engineering stack foundation.

## Internal Standards and Canonical References Applied
- [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md): constrains the minimum structure and reference visibility expected from foundation docs.
- [foundation_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/foundation_index_standard.md): constrains what the synced foundation index should expose once the source foundation doc is complete.
- [repository_maintenance_loop_standard.md](/home/j/WatchTowerPlan/docs/standards/operations/repository_maintenance_loop_standard.md): constrains same-change-set drift closure and the required validation loop.

## Proposed Technical Approach
- Edit `docs/foundations/engineering_stack_direction.md` to cite the governed local references for the technologies and standards it materially names.
- Expand `workflows/modules/foundations_context_review.md` so its load guidance matches the authoritative foundations backbone for review work.
- Refresh `core/python/src/watchtower_core/cli/query_knowledge_family.py` and `docs/commands/core_python/watchtower_core_query_foundations.md` to use live examples and wording that match the current foundation corpus.
- Add tests that prove the engineering stack foundation is queryable by a governed reference path and that CLI help advertises a live example path.

## Work Breakdown
1. Author the traced planning, decision, and acceptance surfaces for the confirmed findings and close the bootstrap task.
2. Create and execute an implementation task covering the foundation doc, workflow module, CLI help/doc refresh, and regression tests.
3. Create and execute a validation task covering targeted tests, `sync all`, `validate acceptance`, `validate all`, and two post-fix no-new-issues review passes.

## Risks
- Reference additions could introduce noisy or redundant citations if not kept scoped to material technologies.
- The foundations query doc could drift from CLI help again if only one surface is updated.

## Validation Plan
- Run targeted tests for foundations query and control-plane artifact coverage.
- Rebuild synced surfaces with `watchtower-core sync all --write --format json`.
- Validate the acceptance contract for `trace.foundations_documentation_completeness_alignment`.
- Run final `watchtower-core validate all --format json`.
- Complete two post-fix review passes from different angles and record that neither found additional actionable issues.

## References
- [foundation_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/foundations/foundation_index.v1.json)
- [foundations_context_review.md](/home/j/WatchTowerPlan/workflows/modules/foundations_context_review.md)
- [watchtower_core_query_foundations.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_query_foundations.md)
