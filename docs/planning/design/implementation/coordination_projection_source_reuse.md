---
trace_id: trace.coordination_projection_source_reuse
id: design.implementation.coordination_projection_source_reuse
title: Coordination Projection Source Reuse Implementation Plan
summary: Breaks Coordination Projection Source Reuse into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-12T16:16:44Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/repo_ops/sync/
- core/python/tests/
---

# Coordination Projection Source Reuse Implementation Plan

## Record Metadata
- `Trace ID`: `trace.coordination_projection_source_reuse`
- `Plan ID`: `design.implementation.coordination_projection_source_reuse`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.coordination_projection_source_reuse`
- `Linked Decisions`: `decision.coordination_projection_source_reuse_direction`
- `Source Designs`: `design.features.coordination_projection_source_reuse`
- `Linked Acceptance Contracts`: `contract.acceptance.coordination_projection_source_reuse`
- `Updated At`: `2026-03-12T16:16:44Z`

## Summary
Breaks Coordination Projection Source Reuse into a bounded implementation slice.

## Source Request or Design
- Do a comprehensive project review for refactoring and potential optimizations without reducing capability, fidelity, or performance.

## Scope Summary
- Covers the bounded loader and sync-orchestration changes needed to reuse stable planning
  projection inputs and current-run generated documents during coordination sync.
- Covers regression coverage, acceptance evidence refresh, and final closeout validation for
  the trace.
- Excludes schema changes and unrelated refactors inside the broader planning projection
  model layer.

## Assumptions and Constraints
- The published planning, initiative, coordination, and tracker artifacts must remain
  semantically consistent with current write-mode outputs.
- The reuse mechanism should compose with the existing aggregate sync orchestration instead of
  inventing a second coordination-only pipeline.
- Generated current-run overrides must not bypass schema validation when they replace source
  reads for downstream services.

## Internal Standards and Canonical References Applied
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): keep the implementation in `core/python/` and validate with the standard Python workspace command set.
- [repository_validation_standard.md](/home/j/WatchTowerPlan/docs/standards/validations/repository_validation_standard.md): the slice closes only after targeted and full validation passes.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): the traced task set and coordination surfaces must stay aligned during execution and closeout.

## Proposed Technical Approach
- Add explicit override support to `ControlPlaneLoader` for validated single-document and
  governed-directory artifacts.
- Teach aggregate sync orchestration to preload stable coordination inputs once and publish
  newly-generated document outputs back into the runtime loader for downstream reuse after
  schema validation.
- Preserve existing per-service logic where possible so the change stays concentrated in the
  loader or orchestration boundary and is easy to instrument.

## Work Breakdown
1. Replace the placeholder planning artifacts with the concrete issue statement, accepted
   direction, and bounded task chain for this trace.
2. Add explicit validated override support to the loader and wire coordination or aggregate
   sync orchestration to prime and publish reusable planning projection artifacts.
3. Add regressions for reduced source reads, validated override publication, and downstream
   dependency fidelity, then refresh acceptance evidence and close the trace on a green
   repository baseline.

## Risks
- Orchestration could accidentally override the wrong relative path and hide a real source
  artifact.
- If downstream services rely on fresh source reads for paths outside the coordination slice,
  the override boundary must stay narrow enough not to interfere.

## Validation Plan
- Add targeted unit regressions proving coordination sync reduces repeated source reads for
  planning indexes, validates generated current-run overrides, and uses generated dependency
  artifacts.
- Run targeted sync tests, `watchtower-core sync all --write --format json`,
  `watchtower-core validate acceptance --trace-id trace.coordination_projection_source_reuse
  --format json`, final `watchtower-core validate all --format json`, `pytest -q`, `python
  -m mypy src/watchtower_core`, and `ruff check .`.
- Run a follow-up review pass of adjacent control-plane loader and sync surfaces and confirm
  no additional actionable issues remain.

## References
- [coordination_projection_source_reuse.md](/home/j/WatchTowerPlan/docs/planning/prds/coordination_projection_source_reuse.md)
- [coordination_projection_source_reuse.md](/home/j/WatchTowerPlan/docs/planning/design/features/coordination_projection_source_reuse.md)
- [coordination_projection_source_reuse_acceptance.v1.json](/home/j/WatchTowerPlan/core/control_plane/contracts/acceptance/coordination_projection_source_reuse_acceptance.v1.json)
