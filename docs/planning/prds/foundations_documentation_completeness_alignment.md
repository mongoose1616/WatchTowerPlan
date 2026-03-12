---
trace_id: trace.foundations_documentation_completeness_alignment
id: prd.foundations_documentation_completeness_alignment
title: Foundations Documentation Completeness Alignment PRD
summary: Close documentation and workflow drift around the governed foundations corpus
  by restoring complete foundations-aware review context, aligning live query/help
  examples with the current foundation index, and making the engineering stack foundation
  cite the governed reference corpus it materially depends on so index and query surfaces
  remain cohesive.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-12T21:27:00Z'
audience: shared
authority: authoritative
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

# Foundations Documentation Completeness Alignment PRD

## Record Metadata
- `Trace ID`: `trace.foundations_documentation_completeness_alignment`
- `PRD ID`: `prd.foundations_documentation_completeness_alignment`
- `Status`: `active`
- `Linked Decisions`: `decision.foundations_documentation_completeness_alignment_direction`
- `Linked Designs`: `design.features.foundations_documentation_completeness_alignment`
- `Linked Implementation Plans`: `design.implementation.foundations_documentation_completeness_alignment`
- `Updated At`: `2026-03-12T21:27:00Z`

## Summary
Close documentation and workflow drift around the governed foundations corpus by restoring complete foundations-aware review context, aligning live query/help examples with the current foundation index, and making the engineering stack foundation cite the governed reference corpus it materially depends on so index and query surfaces remain cohesive.

## Problem Statement
The governed foundations corpus is structurally valid, but it is not fully cohesive across its companion workflow, query, and reference surfaces.

Three concrete gaps currently reduce documentation completeness:

1. `workflows/modules/foundations_context_review.md` under-specifies the authoritative foundation set for foundations-aware review work. Its `Additional Files to Load` section lists only engineering design principles and product direction even though the workflow purpose explicitly covers current repository scope, standards posture, and technology direction.
2. `watchtower-core query foundations` publishes at least one stale example. The documented and help-text example `--audience maintainers` currently returns zero results because the live foundations corpus only publishes `shared` audience entries.
3. `docs/foundations/engineering_stack_direction.md` materially discusses repository-chosen or candidate external technologies and standards, but it cites no governed local reference docs for them. As a result the live foundation index cannot expose the reference relationships or external authority metadata for that foundation entry.

These gaps make the foundations layer less complete for humans and less useful for machine-backed lookup, even though the underlying sync and query machinery is already capable of carrying the missing metadata.

## Goals
- Restore foundations-aware review guidance so it loads the correct authoritative context for scope, standards posture, and stack direction.
- Align foundations query documentation and CLI help examples with the live foundation corpus rather than hypothetical values.
- Make the engineering stack foundation cite the governed reference corpus it materially depends on so the foundation index and query surfaces expose complete reference metadata.
- Preserve existing query behavior, validation strictness, and deterministic sync behavior while improving documentation cohesion.

## Non-Goals
- Change the meaning of foundation audiences, authorities, or related-path matching.
- Introduce new foundation schemas, new foundation artifact families, or new query filters.
- Require every foundation document to cite external references when the document is primarily repository-internal and does not materially depend on external authority.

## Requirements
- `req.foundations_documentation_completeness_alignment.001`: Foundations-aware workflow guidance must name the authoritative foundation documents needed for review and documentation-alignment work, including current repository scope, engineering design principles, standards posture, and technology direction, while still distinguishing future-product context from current repo ownership.
- `req.foundations_documentation_completeness_alignment.002`: Foundations query help and command documentation must use examples and filter wording that remain truthful against the current live foundations corpus and must highlight at least one live index-backed lookup path.
- `req.foundations_documentation_completeness_alignment.003`: The engineering stack foundation must cite the governed local reference docs for the external technologies and standards it materially names so the foundation index and query surfaces expose reference-doc and external-authority relationships without changing the query contract.

## Acceptance Criteria
- `ac.foundations_documentation_completeness_alignment.001`: The traced planning chain, decision record, acceptance contract, evidence ledger, and closed task set all reconcile for `trace.foundations_documentation_completeness_alignment`.
- `ac.foundations_documentation_completeness_alignment.002`: `workflows/modules/foundations_context_review.md` explicitly loads the authoritative foundation set needed for foundations-aware review, and the guidance remains aligned with `docs/foundations/README.md`.
- `ac.foundations_documentation_completeness_alignment.003`: `docs/foundations/engineering_stack_direction.md` cites governed local reference docs for its material external technologies and the rebuilt `foundation_index.v1.json` records non-empty `reference_doc_paths` and `external_reference_urls` for `foundation.engineering_stack_direction`.
- `ac.foundations_documentation_completeness_alignment.004`: The CLI help and command doc for `watchtower-core query foundations` publish live examples that return real results against the current foundation corpus, with targeted regression coverage for the refreshed lookup path.
- `ac.foundations_documentation_completeness_alignment.005`: Targeted and full validation pass, and two post-fix review passes find no additional actionable issues in the touched foundations/documentation/query area.

## Risks and Dependencies
- Adding too many reference links to the engineering stack foundation would make the document noisy instead of clearer. The implementation should cite the technologies and standards that materially shape repository stack direction, not every adjacent concept.
- Updating workflow guidance without keeping the foundation README aligned would trade one drift boundary for another.
- Help-text and command-doc examples must remain grounded in current corpus reality; otherwise the repository will keep publishing examples that are technically valid commands but operationally misleading.

## References
- [README.md](/home/j/WatchTowerPlan/docs/foundations/README.md)
- [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md)
- [foundation_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/foundation_index_standard.md)
- [foundations_context_review.md](/home/j/WatchTowerPlan/workflows/modules/foundations_context_review.md)
