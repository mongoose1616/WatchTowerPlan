---
trace_id: trace.foundation_index_family_contract_alignment
id: decision.foundation_index_family_contract_alignment_direction
title: Foundation Index Family Contract Alignment Direction Decision
summary: Records the initial direction decision for Foundation Index Family Contract
  Alignment.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-12T23:12:00Z'
audience: shared
authority: supporting
applies_to:
- docs/standards/data_contracts/foundation_index_standard.md
- core/python/src/watchtower_core/repo_ops/sync/foundation_index.py
- core/python/src/watchtower_core/repo_ops/query/foundations.py
- docs/commands/core_python/watchtower_core_query_foundations.md
- docs/commands/core_python/watchtower_core_sync_foundation_index.md
- core/control_plane/indexes/foundations/
---

# Foundation Index Family Contract Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.foundation_index_family_contract_alignment`
- `Decision ID`: `decision.foundation_index_family_contract_alignment_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.foundation_index_family_contract_alignment`
- `Linked Designs`: `design.features.foundation_index_family_contract_alignment`
- `Linked Implementation Plans`: `design.implementation.foundation_index_family_contract_alignment`
- `Updated At`: `2026-03-12T23:12:00Z`

## Summary
Records the initial direction decision for Foundation Index Family Contract Alignment.

## Decision Statement
Repair the foundation-index family contract by publishing the missing authoritative sync/query and foundations-command operationalization surfaces in the governing standard, then lock the restored lookup behavior with targeted regressions instead of changing standards-query runtime behavior.

## Trigger or Source Request
- Comprehensive internal project review for documentation coverage, standards alignment, and cohesiveness with foundations/**.

## Current Context and Constraints
- The current review reproduced a real lookup gap: [watchtower-core query standards](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_query_standards.md) does not return [std.data_contracts.foundation_index](/home/j/WatchTowerPlan/docs/standards/data_contracts/foundation_index_standard.md) for [foundation_index.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/repo_ops/sync/foundation_index.py), [foundations.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/repo_ops/query/foundations.py), or the foundations-specific command pages because the standard never operationalized those surfaces.
- The same standard explicitly says command docs and query or sync surfaces must stay aligned when the family changes structurally, so the governing contract and the live lookup behavior are currently inconsistent.
- The foundations document-family standard and broader engineering standards already resolve from some of those surfaces; the fix must add the missing data-contract match without removing other legitimate standards.

## Applied References and Implications
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): keeps the repair inside current repository-owned standards, command docs, indexes, and tests.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): favors explicit contract publication over implicit family membership or inferred runtime behavior.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): requires the authored standard, derived standard index, command docs, and regressions to move together in one slice.
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md): preserves deterministic local standards lookup instead of introducing new heuristics.
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): establishes the peer pattern for index-family operationalization coverage across sync/query/family-readme surfaces.

## Affected Surfaces
- docs/standards/data_contracts/foundation_index_standard.md
- core/python/src/watchtower_core/repo_ops/sync/foundation_index.py
- core/python/src/watchtower_core/repo_ops/query/foundations.py
- docs/commands/core_python/watchtower_core_query_foundations.md
- docs/commands/core_python/watchtower_core_sync_foundation_index.md
- core/control_plane/indexes/foundations/
- core/control_plane/indexes/foundations/README.md

## Options Considered
### Option 1
- Add only the missing `repo_ops` sync and query module paths to the foundation-index standard.
- Smallest possible authored contract change.
- Leaves the foundations command pages outside the explicit family contract and under-protects the documentation completeness goal of the review.

### Option 2
- Align the full bounded family contract by adding the authoritative sync/query modules, the foundations-specific command pages, and the family README, then protect the resulting lookup behavior with targeted regressions.
- Restores one coherent human-readable and machine-readable family contract without touching runtime code.
- Slightly larger documentation and regression surface than the minimum code-path-only change.

## Chosen Outcome
Apply the broader bounded contract alignment in Option 2 and keep standards-query runtime behavior unchanged.

## Rationale and Tradeoffs
- The reproduced defect lives in the authored family contract, not in the query engine, so the lowest-risk fix is to correct the governing standard and regenerate the machine-readable standard index.
- Including the foundations command pages and family README keeps the family contract explicit and cohesive instead of repairing only the internal code-path symptom.
- The main tradeoff is a wider documentation diff, but that is preferable to leaving operator-facing surfaces outside the stated family boundary.

## Consequences and Follow-Up Impacts
- The foundation-index standard will become discoverable from the authoritative foundations sync/query modules and the two foundations command pages.
- The standard index and standards-query surface will expose the repaired data-contract match after sync refresh.
- Targeted regressions will be added so future contract drift fails closed before full validation can pass.

## Risks, Dependencies, and Assumptions
- Assumes the current standards-query exact, directory, and descendant matching semantics remain authoritative.
- Risks incomplete regression coverage if one repaired surface is omitted from the targeted tests.
- Depends on refreshing derived indexes and planning trackers after the standard changes.

## References
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md)
