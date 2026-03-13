---
trace_id: trace.derived_projection_status_semantics
id: design.implementation.derived_projection_status_semantics
title: Derived Projection Status Semantics Alignment Implementation Plan
summary: Breaks Derived Projection Status Semantics Alignment into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-11T03:29:01Z'
audience: shared
authority: supporting
applies_to:
- core/control_plane/indexes/initiatives/
- core/control_plane/indexes/coordination/
- core/python/src/watchtower_core/
- docs/commands/core_python/
- docs/standards/
---

# Derived Projection Status Semantics Alignment Implementation Plan

## Record Metadata
- `Trace ID`: `trace.derived_projection_status_semantics`
- `Plan ID`: `design.implementation.derived_projection_status_semantics`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.derived_projection_status_semantics`
- `Linked Decisions`: `decision.derived_projection_status_semantics_direction`
- `Source Designs`: `design.features.derived_projection_status_semantics`
- `Linked Acceptance Contracts`: `contract.acceptance.derived_projection_status_semantics`
- `Updated At`: `2026-03-11T03:29:01Z`

## Summary
Breaks Derived Projection Status Semantics Alignment into a bounded implementation slice.

## Source Request or Design
- Follow-up from whole-repo review verification after planning-authority closeout.

## Scope Summary
- Covers one bounded contract-alignment slice for derived initiative and coordination projections.
- Covers planning updates, implementation, docs, tests, validation, and initiative closeout for the renamed entry field.
- Excludes broader traceability-family status normalization outside the initiative-family projections.

## Assumptions and Constraints
- The planning catalog remains the canonical deep-planning path, so this initiative only needs to fix the remaining derived projection ambiguity.
- Root artifact `status` fields stay unchanged because they describe the index artifacts themselves, not initiative entries.

## Current-State Context
- The active initiative-family query surfaces still reproduce the summary finding by returning closed initiatives with `artifact_status` absent and `initiative_status` present.
- The sync graph already rebuilds initiative and coordination indexes together, so one coordinated contract rename can propagate cleanly through the derived artifacts.
- The new trace only needs one execution task because the work is one bounded contract-alignment slice rather than a multi-phase architecture change.

## Internal Standards and Canonical References Applied
- [initiative_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/initiative_index_standard.md): the implementation must update the initiative-entry contract and its companion schema together.
- [coordination_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/coordination_index_standard.md): the coordination projection must remain schema-valid after inheriting the renamed initiative-entry field.
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): query docs need to describe the JSON contract change in the same slice as the code.

## Proposed Technical Approach
- Update the planning chain and decision first so the contract change is explicit before code and schema edits land.
- Rename initiative-family entry fields from `status` to `artifact_status` across schemas, derived artifacts, sync services, typed models, query handlers, docs, and tests.
- Rebuild derived coordination and planning surfaces, then validate the repository baseline and close the initiative once the machine contract is explicit and green.

## Work Breakdown
1. Finalize the PRD, design, implementation plan, acceptance contract, and accepted decision; create one execution task and close the bootstrap task.
2. Implement the initiative-index and coordination-index contract rename with synchronized code, schema, doc, and test updates.
3. Rebuild derived artifacts, run the full validation baseline, close the execution task, and close out the initiative.

## Risks
- A missed schema or typed-model update could leave the coordination path inconsistent with the initiative path.
- Because this is a contract rename, stale tests or docs could pass local inspection but leave the repo guidance misleading if not updated together.

## Validation Plan
- Verify the reproduced summary issue first by confirming that a closed initiative currently returns `status: active` plus `initiative_status: completed`.
- Run targeted tests for initiative and coordination loading, sync, and CLI query output after the rename.
- Run `watchtower-core sync all --write --format json`, `watchtower-core validate all --format json`, `python -m mypy src`, `ruff check .`, and `pytest -q` before closeout.

## References
- [derived_projection_status_semantics_alignment.md](/home/j/WatchTowerPlan/docs/planning/prds/derived_projection_status_semantics_alignment.md)
