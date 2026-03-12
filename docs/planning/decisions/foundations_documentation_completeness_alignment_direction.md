---
trace_id: trace.foundations_documentation_completeness_alignment
id: decision.foundations_documentation_completeness_alignment_direction
title: Foundations Documentation Completeness Alignment Direction Decision
summary: Records the initial direction decision for Foundations Documentation Completeness
  Alignment.
type: decision_record
status: active
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

# Foundations Documentation Completeness Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.foundations_documentation_completeness_alignment`
- `Decision ID`: `decision.foundations_documentation_completeness_alignment_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.foundations_documentation_completeness_alignment`
- `Linked Designs`: `design.features.foundations_documentation_completeness_alignment`
- `Linked Implementation Plans`: `design.implementation.foundations_documentation_completeness_alignment`
- `Updated At`: `2026-03-12T21:27:00Z`

## Summary
Use a bounded source-document alignment slice to repair foundations completeness and let the existing foundation index/query machinery project the corrected state.

## Decision Statement
Repair foundations documentation completeness by updating the authoritative foundation source document, foundations-aware workflow guidance, and foundations query help/docs in one slice, while reusing the existing foundation sync and query contract unchanged.

## Trigger or Source Request
- Do a comprehensive internal project review for documentation completeness and cohesiveness with foundations/**.

## Current Context and Constraints
- The current foundations corpus is structurally valid but not fully cohesive with its supporting workflow and command surfaces.
- The foundation index already supports reference metadata for foundation docs; the gap is in authored source content, not in the index contract.
- The repository’s foundations-alignment workflow should foreground current repository scope and standards posture, not only future-product or design-philosophy context.

## Applied References and Implications
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): foundations-aware review must keep current repository ownership explicit, so the workflow context cannot omit scope.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): same-change-set coherence across docs, indexes, and validation is a governing constraint for this repair.
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md): the stack-direction foundation is the right source surface to repair because the index is derived from it.
- [foundation_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/foundation_index_standard.md): the existing index contract already expects reference and external-authority metadata when present in the source docs.
- [repository_maintenance_loop_standard.md](/home/j/WatchTowerPlan/docs/standards/operations/repository_maintenance_loop_standard.md): a maintenance-style review slice should close bounded drift rather than leave partially repaired surfaces behind.

## Affected Surfaces
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

## Options Considered
### Option 1
- Fix only the command docs and workflow wording.
- Faster and lower-touch.
- Leaves the foundation source document and machine-readable foundation index semantically incomplete.

### Option 2
- Repair the source foundation doc, foundations workflow guidance, and query help/docs together, then resync and validate the derived surfaces.
- Produces cohesive human and machine-readable closure without expanding the contract surface.
- Requires a slightly broader bounded slice across docs, CLI help, tests, and synced artifacts.

## Chosen Outcome
Choose Option 2. Treat the issue as source-document incompleteness and workflow/help drift, repair those authoritative surfaces directly, and let the existing foundation sync/query pipeline project the corrected state.

## Rationale and Tradeoffs
- This approach preserves current capability and query semantics while improving documentation completeness.
- It keeps the repair aligned with the repository’s same-change-set governance posture.
- It adds targeted regressions where the current slice had no guardrails, specifically around reference-backed foundation lookup and CLI help examples.

## Consequences and Follow-Up Impacts
- The engineering stack foundation will gain a larger but more useful References section.
- The synced foundation index will expose new reference metadata for that foundation entry.
- Foundations query docs and help text will become more grounded in live corpus behavior.
- The workflow module will load a broader, more authoritative foundation set for review tasks.

## Risks, Dependencies, and Assumptions
- The slice depends on the existing local reference corpus being sufficient for the cited technologies and standards.
- Over-citation would reduce readability, so references should remain limited to material external authorities.
- Future foundation-audience changes could stale examples again if not kept under regression coverage.

## References
- [README.md](/home/j/WatchTowerPlan/docs/foundations/README.md)
- [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md)
- [foundation_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/foundation_index_standard.md)
- [watchtower_core_query_foundations.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_query_foundations.md)
