---
trace_id: trace.standard_runtime_and_route_explicitness
id: design.implementation.standard_runtime_and_route_explicitness
title: Standard, Runtime, and Route Explicitness Hardening Implementation Plan
summary: Breaks Standard, Runtime, and Route Explicitness Hardening into a bounded
  implementation slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-11T06:45:00Z'
audience: shared
authority: supporting
applies_to:
- docs/standards/
- core/control_plane/indexes/standards/standard_index.v1.json
- core/python/src/watchtower_core/
- docs/commands/core_python/
- workflows/ROUTING_TABLE.md
---

# Standard, Runtime, and Route Explicitness Hardening Implementation Plan

## Record Metadata
- `Trace ID`: `trace.standard_runtime_and_route_explicitness`
- `Plan ID`: `design.implementation.standard_runtime_and_route_explicitness`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.standard_runtime_and_route_explicitness`
- `Linked Decisions`: `decision.standard_runtime_and_route_explicitness_direction`
- `Source Designs`: `design.features.standard_runtime_and_route_explicitness`
- `Linked Acceptance Contracts`: `contract.acceptance.standard_runtime_and_route_explicitness`
- `Updated At`: `2026-03-11T06:45:00Z`

## Summary
Breaks Standard, Runtime, and Route Explicitness Hardening into a bounded implementation slice.

## Source Request or Design
- design.features.standard_runtime_and_route_explicitness

## Scope Summary
- Covers the planning close-in work plus three execution slices:
  1. standard-operationalization metadata and derived standard-index updates
  2. runtime package README and workspace-navigation updates
  3. advisory route-preview scoring hardening, docs, and tests
- Excludes the broader planning-document contract-unification workstream because no active drift is reproducing in the current runtime contract path.
- Excludes already-closed health-reporting and maintenance-loop remediation work.

## Assumptions and Constraints
- Standard docs remain the authored authority, so the operationalization fields must be captured in the documents themselves rather than in a new parallel registry.
- The runtime package boundary is already partly enforced by compatibility guards in `query`, `sync`, and `validation`; the new docs must align with that real boundary.
- Route-preview changes must preserve deterministic ordering and advisory semantics.
- The initiative should land in small commits rather than one large repository-wide sweep.

## Proposed Technical Approach
- First, finish the planning chain and create one bounded execution task per reproduced gap.
- Second, extend the standard-doc shape, standard-index sync path, schema, examples, query payloads, and tests in one coherent same-change slice.
- Third, add runtime package READMEs plus the workspace README navigation updates using the current export boundary as the documentation source of truth.
- Fourth, update route-preview scoring, handler output expectations, command docs, and tests so realistic broad maintenance requests become matchable without changing the route index itself.

## Work Breakdown
1. Replace the bootstrap scaffolds with verified report-driven planning content and create the three execution tasks.
2. Implement standard-operationalization metadata end to end:
   - update the standard-doc standard
   - backfill live standards
   - extend the standard-index schema, sync, typed model, query surface, examples, and tests
3. Publish runtime package boundary docs:
   - add package-level READMEs under `core/python/src/watchtower_core/`
   - update `core/python/README.md`
   - keep the docs aligned with the actual export-safe and repo-local package boundaries
4. Harden advisory route preview:
   - update route scoring
   - add tests for realistic report-driven requests
   - refresh the route-preview command docs
5. Run sync and validation, close the bootstrap task and execution tasks, then close the initiative.

## Risks
- The standard backfill is mechanically broad and can introduce stale timestamps or formatting drift if handled sloppily.
- Route scoring changes can accidentally over-match common routing words if the threshold logic is too permissive.
- Package README coverage may miss one meaningful package boundary if the first pass is too shallow.

## Validation Plan
- Run targeted unit tests while implementing:
  - `core/python/tests/unit/test_standard_index_sync.py`
  - route-preview unit and handler tests
- Before closeout, run the broad workspace baseline:
  - `./.venv/bin/watchtower-core sync all --write`
  - `./.venv/bin/watchtower-core validate all --format json`
  - `./.venv/bin/python -m mypy src`
  - `./.venv/bin/ruff check src tests/unit tests/integration`
  - `./.venv/bin/python -m pytest`
- Review the refreshed planning, initiative, task, and coordination surfaces to confirm the traced closeout state is coherent.

## References
- [standard_runtime_and_route_explicitness_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/standard_runtime_and_route_explicitness_hardening.md)
- [standard_runtime_and_route_explicitness_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/standard_runtime_and_route_explicitness_hardening.md)
- [repository_validation_standard.md](/home/j/WatchTowerPlan/docs/standards/validations/repository_validation_standard.md)
- [repository_maintenance_loop_standard.md](/home/j/WatchTowerPlan/docs/standards/operations/repository_maintenance_loop_standard.md)
