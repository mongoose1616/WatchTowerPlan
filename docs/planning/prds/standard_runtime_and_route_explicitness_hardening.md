---
trace_id: trace.standard_runtime_and_route_explicitness
id: prd.standard_runtime_and_route_explicitness
title: Standard, Runtime, and Route Explicitness Hardening PRD
summary: Closes the still-valid report-set gaps around standards operationalization
  metadata, runtime package boundary documentation, and advisory route-preview matching.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-11T06:25:00Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/
- core/control_plane/indexes/standards/standard_index.v1.json
- core/python/src/watchtower_core/
- docs/commands/core_python/
- workflows/ROUTING_TABLE.md
---

# Standard, Runtime, and Route Explicitness Hardening PRD

## Record Metadata
- `Trace ID`: `trace.standard_runtime_and_route_explicitness`
- `PRD ID`: `prd.standard_runtime_and_route_explicitness`
- `Status`: `active`
- `Linked Decisions`: `decision.standard_runtime_and_route_explicitness_direction`
- `Linked Designs`: `design.features.standard_runtime_and_route_explicitness`
- `Linked Implementation Plans`: `design.implementation.standard_runtime_and_route_explicitness`
- `Updated At`: `2026-03-11T06:25:00Z`

## Summary
Closes the still-valid report-set gaps around standards operationalization metadata, runtime package boundary documentation, and advisory route-preview matching.

## Problem Statement
- The March 2026 expanded review set still reproduces three bounded gaps in the live repository:
  - the standard index can show citation relationships, but it still cannot answer what concretely operationalizes a standard
  - the `watchtower_core` package tree still has no package-level README surfaces, so reusable-core versus repo-local boundaries stay memory-based
  - `watchtower-core route preview` still depends on exact trigger-phrase matches strongly enough that realistic free-form maintenance requests return no route at all
- The same review set also identified adjacent risks that no longer reproduce as active defects in the current repo:
  - foundation-scope and root-entrypoint ambiguity were closed by `trace.foundation_scope_and_entrypoint_realignment`
  - layered health reporting and bounded maintenance review loops are now explicit in current standards and command docs
  - planning-document contract drift is not currently reproducing as an active defect because the runtime checks are already centralized in `repo_ops/planning_documents.py`
- The remaining live issues all share one root cause: important governance and runtime relationships are still too implicit for a repository that now expects agent-guided navigation and future consumer-facing core reuse.

## Report File Disposition
- `report/README.md`: Rechecked as the navigation surface for the March 2026 review set and confirmed that its focus-area map still matches the live WatchTowerPlan repository.
- `report/01_overview_and_method.md`: Rechecked the stable P1 themes and confirmed that the remaining live gaps were standards operationalization, runtime boundary documentation, and advisory route matching.
- `report/02_foundations_scope_and_cohesion.md`: Confirmed that foundation-scope and thin-root ambiguity no longer reproduce after `trace.foundation_scope_and_entrypoint_realignment`; the remaining runtime-boundary documentation gap is closed in this trace.
- `report/03_documentation_and_standards.md`: Confirmed that runtime under-documentation and implicit standard operationalization remained live and are closed in this trace; bounded maintenance-loop freshness guidance no longer reproduces as missing.
- `report/04_workflows_and_governance.md`: Confirmed that free-form advisory route matching remained live and is closed in this trace; broader workflow-authority and executable-metadata gaps were already closed by `trace.workflow_system_operationalization`.
- `report/05_control_plane_and_machine_authority.md`: Confirmed that machine-readable standard operationalization remained live and is closed in this trace; repeated planning-document contract drift does not currently reproduce as an active defect because the runtime checks are centralized in `repo_ops/planning_documents.py`.
- `report/06_core_python_architecture_and_exportability.md`: Confirmed that package-boundary documentation remained live and is closed in this trace; the export-safe runtime boundary refactors themselves were already closed by `trace.core_export_readiness_and_optimization` and `trace.core_export_hardening_followup`.
- `report/07_validation_testing_and_drift.md`: Confirmed that cross-layer implicitness around standards and routing remained live and is closed in this trace; layered health-reporting clarity and broader unit-test hardening were already closed by `trace.derived_projection_status_semantics` and `trace.unit_test_hardening_and_rebalancing`.
- `report/08_ctf_and_next_phase_readiness.md`: Confirmed that the remaining runtime-consumer documentation gap is closed in this trace; next-phase scope and export-boundary work otherwise remain aligned with the closed export-hardening traces until future pack work starts.
- `report/09_remediation_program.md`: Confirmed that only Workstreams A, B, and the free-form matching portion of D still reproduced in the live repo; this trace closes that remaining subset without reopening already-closed workstreams.

## Goals
- Publish one machine-readable operationalization map for governed standards so maintainers and agents can see how each standard is enforced, scaffolded, reviewed, and changed safely.
- Publish package-level runtime documentation that classifies the major `watchtower_core` packages as reusable core, boundary layer, or repo-local orchestration.
- Keep route preview advisory, but make it deterministic and resilient enough to match realistic free-form maintenance requests without requiring exact routing-table wording.
- Close the verified live findings in one traced initiative with updated tasks, derived surfaces, validation, and commit-ready closeout metadata.

## Non-Goals
- Do not replace `AGENTS.md`, `ROUTING_TABLE.md`, workflow modules, or standard documents as the human authority surfaces.
- Do not introduce a full semantic router, autonomous planner, or new top-level workflow system beyond advisory route preview.
- Do not reopen already-closed foundation, coordination, health-reporting, or validation-baseline initiatives.
- Do not start domain-pack implementation, package extraction, or a broader planning-document contract unification program in this slice.

## Requirements
- `req.standard_runtime_and_route_explicitness.001`: Every live governed standard under `docs/standards/**` must declare its operationalization using one consistent authored shape that the standard index can rebuild and query deterministically.
- `req.standard_runtime_and_route_explicitness.002`: The standard index, its schema, examples, query surface, and companion docs must expose operationalization metadata strongly enough to answer what enforces a standard and where that enforcement lives.
- `req.standard_runtime_and_route_explicitness.003`: The major `watchtower_core` packages must publish package-level READMEs that describe purpose, classification, supported import expectations, and non-goals, and `core/python/README.md` must link them as the runtime architecture start-here surface.
- `req.standard_runtime_and_route_explicitness.004`: `watchtower-core route preview` must remain advisory and deterministic, but it must match realistic free-form maintenance requests that refer to review, fixes, validation, tasking, and commit closeout without requiring exact trigger phrases.
- `req.standard_runtime_and_route_explicitness.005`: The initiative must record which March 2026 report findings were still valid versus already closed so future contributors do not reopen stale remediation work.

## Acceptance Criteria
- `ac.standard_runtime_and_route_explicitness.001`: `watchtower-core sync standard-index --write` rebuilds a schema-valid standard index whose entries now include operationalization metadata for every live standard.
- `ac.standard_runtime_and_route_explicitness.002`: `watchtower-core query standards --format json` returns the new operationalization metadata for affected standards, and the command docs describe the added lookup behavior.
- `ac.standard_runtime_and_route_explicitness.003`: The `watchtower_core` package tree contains package-level README documents for the major package boundaries, and `core/python/README.md` points maintainers at the supported runtime navigation and boundary classification.
- `ac.standard_runtime_and_route_explicitness.004`: A route-preview regression test proves that a realistic free-form maintenance request now returns the expected merged workflow set instead of an empty advisory result.
- `ac.standard_runtime_and_route_explicitness.005`: The planning corpus for this trace contains an updated PRD, feature design, implementation plan, accepted decision, closed bootstrap task, bounded execution tasks, and a validated closeout chain.

## Risks and Dependencies
- Backfilling operationalization metadata across the full standards corpus can drift if the authored shape is too verbose or under-specified.
- Route matching can become noisy if token-aware scoring is too permissive, so the advisory model must stay deterministic and thresholded.
- Runtime package READMEs can rot if they describe an aspirational boundary rather than the boundary that current exports and compatibility shims actually enforce.
- This slice depends on keeping human-readable docs, control-plane artifacts, command docs, and Python tests aligned in the same change set.

## References
- [standard_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/standard_index_standard.md)
- [standard_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/standard_md_standard.md)
- [workflow_operationalization_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/workflow_operationalization_direction.md)
- [core_export_ready_architecture.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_ready_architecture.md)
- [repository_maintenance_loop_standard.md](/home/j/WatchTowerPlan/docs/standards/operations/repository_maintenance_loop_standard.md)
