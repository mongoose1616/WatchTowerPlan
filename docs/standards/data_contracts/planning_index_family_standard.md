---
id: "std.data_contracts.planning_index_family"
title: "Planning Index Family Standard"
summary: "This standard defines the shared baseline for planning-related derived index standards stored under `core/control_plane/indexes/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "planning_index_family"
owner: "repository_maintainer"
updated_at: "2026-03-13T20:01:23Z"
audience: "shared"
authority: "authoritative"
---

# Planning Index Family Standard

## Summary
This standard defines the shared baseline for planning-related derived index standards stored under `core/control_plane/indexes/`.

## Purpose
- Keep the planning-oriented derived index standards explicit and governable while avoiding repeated restatement of the same baseline derivation, storage, validation, and discoverability contract.
- Give the planning-related index standards one stable family identity for both human navigation and machine-readable retrieval.

## Scope
- Applies to the planning-related derived index standards for coordination, initiatives, planning catalogs, PRDs, decisions, design documents, tasks, and traceability.
- Covers the shared baseline that those member standards inherit around derivation, storage, discoverability, validation, and same-change alignment.
- Does not replace the family-specific fields, invariants, validation rules, or change-control deltas that each member standard must still publish explicitly.

## Use When
- Reviewing whether a planning-related index standard is repeating only family boilerplate or publishing a real family-specific contract.
- Refreshing the planning-related index standards as one bounded family rather than editing them as isolated documents.
- Improving discoverability for the planning-related derived index family in README, standard-index, or query surfaces.

## Related Standards and Sources
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md): keeps the shared baseline pattern explicit and section-complete instead of turning the member standards into vague stubs.
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md): requires the family baseline and member standards to stay queryable through the governed standard index.
- [compact_document_authoring_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/compact_document_authoring_standard.md): supports reducing repeated boilerplate only when the remaining member-standard deltas stay readable and reviewable.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): requires companion human-readable and machine-readable surfaces to move together when this family changes.

## Guidance
- Treat the member standards in this family as derived indexes over governed planning, task, or traceability authority surfaces rather than as primary authored authorities themselves.
- Keep the member standards explicit about their own entry fields, family-specific invariants, validation rules, and change-control deltas; this baseline only covers the repeated family contract.
- Publish live planning-index-family artifacts under `core/control_plane/indexes/` and keep their companion schemas under `core/control_plane/schemas/artifacts/`.
- Use JSON for the published artifacts governed by this family unless a narrower family standard says otherwise.
- Rebuild the live artifacts from their governed source documents or source indexes rather than reparsing human trackers or relying on manual index edits.
- Keep the shared retrieval tag `planning_index_family` on this baseline standard and every member standard in the family so machine consumers can retrieve the family deterministically.
- Keep standards navigation README surfaces, the governed standard index, and `watchtower-core query standards` guidance aligned when family membership or discoverability changes.

## Operationalization
- `Modes`: `documentation`; `artifact`; `query`
- `Operational Surfaces`: `docs/standards/data_contracts/planning_index_family_standard.md`; `docs/standards/data_contracts/coordination_index_standard.md`; `docs/standards/data_contracts/initiative_index_standard.md`; `docs/standards/data_contracts/planning_catalog_standard.md`; `docs/standards/data_contracts/prd_index_standard.md`; `docs/standards/data_contracts/decision_index_standard.md`; `docs/standards/data_contracts/design_document_index_standard.md`; `docs/standards/data_contracts/task_index_standard.md`; `docs/standards/data_contracts/traceability_index_standard.md`; `docs/standards/data_contracts/README.md`; `core/control_plane/indexes/standards/README.md`; `core/control_plane/indexes/standards/standard_index.v1.json`; `docs/commands/core_python/watchtower_core_query_standards.md`

## Validation
- Every member standard in this family should cite this baseline in `Related Standards and Sources`.
- Every member standard in this family should keep the shared tag `planning_index_family`.
- The member standards should still publish explicit family-specific `Guidance`, `Validation`, and `Change Control` deltas after applying this baseline.
- `watchtower-core query standards --tag planning_index_family --format json` should retrieve this baseline and the member standards in the family.

## Change Control
- Update this standard when the shared derivation, storage, discoverability, or same-change alignment contract for the family changes.
- Update the affected member standards, `docs/standards/README.md`, `docs/standards/data_contracts/README.md`, the governed standard index, the `watchtower-core query standards` command page, and the direct regression tests in the same change set when family membership or family-wide discoverability changes.

## References
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md)
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md)
- [README.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/README.md)

## Updated At
- `2026-03-13T20:01:23Z`
