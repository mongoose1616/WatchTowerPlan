---
trace_id: trace.foundations_documentation_completeness_alignment
id: design.features.foundations_documentation_completeness_alignment
title: Foundations Documentation Completeness Alignment Feature Design
summary: Defines the technical design boundary for Foundations Documentation Completeness
  Alignment.
type: feature_design
status: draft
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

# Foundations Documentation Completeness Alignment Feature Design

## Record Metadata
- `Trace ID`: `trace.foundations_documentation_completeness_alignment`
- `Design ID`: `design.features.foundations_documentation_completeness_alignment`
- `Design Status`: `draft`
- `Linked PRDs`: `prd.foundations_documentation_completeness_alignment`
- `Linked Decisions`: `decision.foundations_documentation_completeness_alignment_direction`
- `Linked Implementation Plans`: `design.implementation.foundations_documentation_completeness_alignment`
- `Updated At`: `2026-03-12T21:27:00Z`

## Summary
This slice is a documentation-completeness and retrieval-cohesion repair for the governed foundations corpus. The design intentionally reuses the existing foundation index, query service, and reference-resolution logic instead of changing foundation schemas or query semantics.

## Source Request
- Do a comprehensive internal project review for documentation completeness and cohesiveness with foundations/**.

## Scope and Feature Boundary
- Refresh the foundations-aware workflow module so it loads the authoritative current-scope, standards-posture, and stack-direction foundation context required for review work.
- Refresh the foundations query help/doc examples so they reflect the live foundation corpus and highlight at least one meaningful retrieval path.
- Add governed local reference citations to the engineering stack foundation so existing sync/query machinery can project richer foundation reference metadata.
- Exclude query-contract changes, schema changes, or new foundation artifact families.

## Current-State Context
- The live foundation index already carries `reference_doc_paths`, `internal_reference_paths`, and `external_reference_urls`, but the engineering stack foundation does not currently cite any governed reference docs, so those fields stay empty for one of the most outward-facing foundations.
- The foundations-alignment workflow exists and is routed correctly, but its own context-loading guidance omits repository scope, standards posture, and engineering stack direction even though those are part of the authoritative foundations backbone.
- The foundations query command already supports useful filters such as `--reference-path`, `--related-path`, and `--applied-by-path`, but the published examples do not fully reflect the current corpus.

## Foundations References Applied
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): foundations-aware review has to foreground current repository ownership before future-product narrative, so the workflow context cannot omit repository scope.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): same-change-set alignment between docs, machine-readable indexes, and validation surfaces is part of the governing standards posture for this repair.
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md): the design must improve the engineering stack foundation's reference completeness without changing its substantive direction.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): future-product context remains relevant, but it must stay explicitly subordinate to current repository scope in foundations-aware review.

## Internal Standards and Canonical References Applied
- [foundation_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md): foundation docs must remain indexable, auditable, and explicit about material references.
- [foundation_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/foundation_index_standard.md): the foundation index should carry reference and external-authority metadata when the source foundation doc publishes it.
- [repository_maintenance_loop_standard.md](/home/j/WatchTowerPlan/docs/standards/operations/repository_maintenance_loop_standard.md): maintenance and review work should close drift in one bounded change and re-check the foundations intent layer before closeout.
- [watchtower_core_query_foundations.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_query_foundations.md): command docs must stay aligned with actual help text and current queryable surfaces.

## Design Goals and Constraints
- Improve foundations completeness by editing the authoritative source docs rather than patching the derived index directly.
- Keep the fix bounded to documentation, help text, and regression coverage; do not invent new query behavior.
- Preserve deterministic sync: all machine-readable changes must come from resyncing the existing foundation index after source docs change.

## Options Considered
### Option 1
- Patch only the command docs and workflow module.
- Low implementation cost.
- Leaves the engineering stack foundation and foundation index semantically incomplete.

### Option 2
- Repair the source foundation document, foundations-aware workflow guidance, and query help/docs together while adding targeted regression coverage.
- Restores completeness across human and machine surfaces in one slice without expanding the contract surface.
- Requires touching documentation, CLI help text, tests, and derived index outputs together.

## Recommended Design
### Architecture
- `docs/foundations/engineering_stack_direction.md` becomes the corrected source authority for stack-direction references.
- `workflows/modules/foundations_context_review.md` becomes the corrected review-context loader for foundations-aware work.
- `core/python/src/watchtower_core/cli/query_knowledge_family.py` and the companion command doc publish examples grounded in live corpus behavior.
- `core/python/tests/**` add regression coverage for the refreshed reference-path lookup and help text.
- `core/control_plane/indexes/foundations/foundation_index.v1.json` is regenerated from the updated foundation source docs.

### Data and Interface Impacts
- No schema changes.
- No query payload shape changes.
- The live foundation index entry for `foundation.engineering_stack_direction` gains `reference_doc_paths` and `external_reference_urls`.
- CLI help text and command docs change to use live examples and current audience wording.

### Execution Flow
1. Update the traced planning/decision/acceptance surfaces to record the confirmed findings and closure criteria.
2. Repair the foundations-aware workflow, engineering stack foundation, and foundations query help/docs in the authoritative source surfaces.
3. Add targeted regression tests, rebuild the derived foundation/planning outputs, validate the repo baseline, and perform two post-fix review passes.

### Invariants and Failure Cases
- The foundation index remains a derived artifact; fixes must land in source Markdown and then resync.
- Foundations query behavior stays read-only and contract-stable.
- If the refreshed reference links do not appear in the synced foundation index, the slice is incomplete and must not close.
- If the refreshed help/docs examples still return zero results, the slice is incomplete and must not close.

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

## Design Guardrails
- Prefer governed local reference docs over raw external URLs in the engineering stack foundation where the reference corpus already exists.
- Do not turn the foundations-alignment workflow into a complete foundations summary; it should load the authoritative files, not duplicate them.

## Risks
- The engineering stack foundation may become link-heavy if the references are not curated carefully.
- A help-text example can drift again later if future foundation audiences change and there is no regression coverage.

## References
- [README.md](/home/j/WatchTowerPlan/docs/foundations/README.md)
- [watchtower_core_query_foundations.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_query_foundations.md)
- [foundation_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/foundations/foundation_index.v1.json)
