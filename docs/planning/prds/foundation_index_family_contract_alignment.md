---
trace_id: trace.foundation_index_family_contract_alignment
id: prd.foundation_index_family_contract_alignment
title: Foundation Index Family Contract Alignment PRD
summary: Align the foundation-index standard and lookup coverage with the full foundations
  index family surfaces.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-12T23:12:00Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/data_contracts/foundation_index_standard.md
- core/python/src/watchtower_core/repo_ops/sync/foundation_index.py
- core/python/src/watchtower_core/repo_ops/query/foundations.py
- docs/commands/core_python/watchtower_core_query_foundations.md
- docs/commands/core_python/watchtower_core_sync_foundation_index.md
- core/control_plane/indexes/foundations/
---

# Foundation Index Family Contract Alignment PRD

## Record Metadata
- `Trace ID`: `trace.foundation_index_family_contract_alignment`
- `PRD ID`: `prd.foundation_index_family_contract_alignment`
- `Status`: `active`
- `Linked Decisions`: `decision.foundation_index_family_contract_alignment_direction`
- `Linked Designs`: `design.features.foundation_index_family_contract_alignment`
- `Linked Implementation Plans`: `design.implementation.foundation_index_family_contract_alignment`
- `Updated At`: `2026-03-12T23:12:00Z`

## Summary
Align the foundation-index standard and lookup coverage with the full foundations index family surfaces.

## Problem Statement
- The foundations-focused documentation and standards review reproduced a standards-lookup gap in [foundation_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/foundation_index_standard.md): the governing data-contract standard only operationalizes the artifact directory and example/schema surfaces, so [watchtower-core query standards](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_query_standards.md) does not resolve `std.data_contracts.foundation_index` from the authoritative foundations sync and query modules.
- The same operationalization gap leaves the foundations-specific command pages outside the foundation-index family contract even though the standard's change-control language says command docs and query or sync surfaces must stay aligned in the same change set.
- Current regression coverage does not fail closed on those lookup expectations, so the contract can drift without a targeted test catching it.

## Goals
- Make the foundation-index data-contract standard discoverable from the authoritative foundations sync and query implementation surfaces.
- Bring the bounded foundations command and family-documentation surfaces into the same published family contract the standard already claims to govern.
- Add durable regression coverage for the repaired lookup behavior and documentation contract.

## Non-Goals
- Change the runtime behavior of [foundation_index.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/repo_ops/sync/foundation_index.py) or [foundations.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/repo_ops/query/foundations.py).
- Redesign standards lookup semantics, directory matching, or glob support beyond the already-governed current behavior.
- Expand the slice into unrelated foundations content edits outside the foundation-index family contract.

## Requirements
- `req.foundation_index_family_contract_alignment.001`: [foundation_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/foundation_index_standard.md) must operationalize the bounded foundations index family surfaces that materially embody or document the family contract, including the authoritative sync/query modules and the foundations-specific command pages.
- `req.foundation_index_family_contract_alignment.002`: The live standard index and standards query surface must resolve `std.data_contracts.foundation_index` for the repaired foundations family operationalization paths.
- `req.foundation_index_family_contract_alignment.003`: Regression coverage must fail closed if the foundation-index standard drops the repaired surfaces or if standards lookup stops resolving the governing standard from those surfaces.

## Acceptance Criteria
- `ac.foundation_index_family_contract_alignment.001`: [foundation_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/foundation_index_standard.md) publishes `sync`, `query`, and `documentation` operationalization coverage for [foundation_index.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/repo_ops/sync/foundation_index.py), [foundations.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/repo_ops/query/foundations.py), [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/foundations/README.md), [watchtower_core_query_foundations.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_query_foundations.md), and [watchtower_core_sync_foundation_index.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_sync_foundation_index.md).
- `ac.foundation_index_family_contract_alignment.002`: [watchtower-core query standards](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_query_standards.md) resolves `std.data_contracts.foundation_index` for the authoritative foundations sync/query modules and the two foundations-specific command pages.
- `ac.foundation_index_family_contract_alignment.003`: Targeted CLI, standard-index sync, and integration documentation regressions plus full repository validation remain green after the family-contract alignment lands.

## Risks and Dependencies
- The slice depends on the current standards-query descendant and exact-path matching semantics remaining authoritative, because the acceptance behavior is expressed through that live lookup surface.
- The repair must not erase the complementary [std.documentation.foundation_md](/home/j/WatchTowerPlan/docs/standards/documentation/foundation_md_standard.md) matches that legitimately apply to the underlying foundation document family surfaces.
- The slice depends on a refreshed [standard_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/standards/standard_index.v1.json) so machine-readable lookup reflects the edited standard in the same change set.

## References
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md)
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md)
