---
trace_id: trace.data_contract_index_family_baseline_alignment
id: decision.data_contract_index_family_baseline_alignment_direction
title: Data-Contract Index Family Baseline Alignment Direction Decision
summary: Records the initial direction decision for Data-Contract Index Family Baseline
  Alignment.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-13T19:55:04Z'
audience: shared
authority: supporting
applies_to:
- docs/standards/data_contracts/
- core/control_plane/indexes/standards/standard_index.v1.json
- docs/commands/core_python/watchtower_core_query_standards.md
- core/python/tests/unit/
---

# Data-Contract Index Family Baseline Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.data_contract_index_family_baseline_alignment`
- `Decision ID`: `decision.data_contract_index_family_baseline_alignment_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.data_contract_index_family_baseline_alignment`
- `Linked Designs`: `design.features.data_contract_index_family_baseline_alignment`
- `Linked Implementation Plans`: `design.implementation.data_contract_index_family_baseline_alignment`
- `Updated At`: `2026-03-13T19:55:04Z`

## Summary
Records the initial direction decision for Data-Contract Index Family Baseline Alignment.

## Decision Statement
Introduce one narrow shared planning-index-family baseline standard, refactor the targeted planning-related data-contract index standards to keep only family-specific deltas after applying that baseline, and use authored tags plus navigation updates to make the family discoverable without changing query or sync runtime behavior.

## Trigger or Source Request
- Another comprehensive internal refactor review was requested using the March 13, 2026 refactor audit, with instructions to keep reviewing under one stable theme until repeated confirmation passes found no new actionable issue.
- The discovery pass confirmed that `RF-STD-001` is best addressed through a bounded data-contract standards slice rather than a whole-corpus rewrite or a deferred runtime hotspot.

## Current Context and Constraints
- The targeted family repeats the same derived-index baseline across several member standards while exposing only per-document tags in the standard index.
- The member standards must remain explicit about their specific fields and invariants; the refactor cannot collapse them into a generic template that weakens reviewability.
- The runtime `query standards` and `sync standard-index` surfaces already support authored tags, so the preferred path is better authored metadata and documentation rather than new code unless the loop finds a direct behavior gap.

## Applied References and Implications
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): favors a small explicit family baseline over hidden macros or broad templating.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): requires the human guidance, machine index, and validation surfaces to move together in one change set.
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): keeps operationalization, validation, and change-control sections mandatory, so the chosen design must standardize repeated content without deleting those contracts.
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): means discoverability improvements should flow through governed tags and index output instead of ad hoc notes.

## Affected Surfaces
- docs/standards/data_contracts/
- docs/standards/README.md
- docs/standards/data_contracts/README.md
- core/control_plane/indexes/standards/standard_index.v1.json
- docs/commands/core_python/watchtower_core_query_standards.md
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/unit/test_cli_knowledge_query_commands.py

## Options Considered
### Option 1
- Add only shared tags and README grouping while leaving the member-standard prose largely unchanged.
- Low risk to runtime-adjacent surfaces.
- Rejected because it leaves the repeated-baseline maintenance cost substantially intact.

### Option 2
- Add one shared planning-index-family baseline standard, refactor the member standards down to their family-specific deltas, and align README, index, query-doc, and test surfaces around the new family tag.
- Addresses both the repeated-prose problem and the discoverability gap while keeping runtime behavior stable.
- Requires coordinated documentation, index, test, and closeout updates across several governed surfaces.

### Option 3
- Apply a broad templating rewrite across a much larger portion of the standards corpus.
- Could shrink more boilerplate immediately.
- Rejected because it exceeds the bounded audit slice and risks reducing explicitness across standards that were not part of the confirmed hotspot.

## Chosen Outcome
Accept Option 2. The trace will add one narrow planning-index-family baseline standard, refactor the targeted member standards to reference it while preserving explicit family-specific contracts, add a stable shared tag for machine discoverability, and refresh the adjacent README, standard-index, command-doc, and test surfaces in the same change set.

## Rationale and Tradeoffs
- The confirmed problem is repeated family boilerplate plus weak discoverability, not missing runtime filter capability.
- A shared family baseline preserves explicit governance while moving repeated derived-index rules into one authoritative place.
- The main tradeoff is one additional standard document, but that cost is justified because it absorbs repeated prose from several member standards and gives the family a stable documented identity.

## Consequences and Follow-Up Impacts
- The data-contract standards directory will gain one new family baseline standard.
- The targeted member standards, standards READMEs, standard-index output, command docs, and direct tests will all change together.
- Acceptance, evidence, and closeout surfaces will need to record the repeated confirmation passes that prove the family is clean after the refactor.

## Risks, Dependencies, and Assumptions
- Assumes the existing standard query and sync runtime surfaces are already sufficient once the authored metadata and docs improve.
- Risks adding an abstraction layer that does not pay for itself if the member standards are not actually shortened and clarified.
- Depends on targeted validation and repeated confirmation passes to prove the family baseline did not create drift across the standard index or its query consumers.

## References
- March 13, 2026 refactor audit
- [data_contract_index_family_baseline_alignment.md](/home/j/WatchTowerPlan/docs/planning/prds/data_contract_index_family_baseline_alignment.md)
