---
trace_id: "trace.structural_rewrite_program"
id: "design.features.structural_rewrite_program"
title: "Structural Rewrite Program Feature Design"
summary: "Defines the repo-native execution design for completing rewrite Phase 0 and Phase 1, landing one bounded Phase 3 command companion normalization slice, closing the first Phase 4 slice and outcome review explicitly, approving the closeout-coordination entry review, landing one bounded Phase 4 closeout coordination sync-reuse slice, closing that slice through explicit outcome review, and handing the trace to one bounded Phase 4 closeout-tracking refresh-boundary slice."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-15T08:14:01Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/standards/"
  - "docs/planning/"
  - "core/control_plane/"
  - "core/python/"
aliases:
  - "rewrite execution design"
  - "structural rewrite design"
  - "phase 2 gate design"
---

# Structural Rewrite Program Feature Design

## Record Metadata
- `Trace ID`: `trace.structural_rewrite_program`
- `Design ID`: `design.features.structural_rewrite_program`
- `Design Status`: `active`
- `Linked PRDs`: `prd.structural_rewrite_program`
- `Linked Decisions`: `None`
- `Linked Implementation Plans`: `design.implementation.structural_rewrite_program`; `design.implementation.structural_rewrite_phase3_command_companion_source_surface_normalization`; `design.implementation.structural_rewrite_phase4_shared_projection_entry`; `design.implementation.structural_rewrite_phase4_planning_projection_snapshot`; `design.implementation.structural_rewrite_phase4_closeout_coordination_entry`; `design.implementation.structural_rewrite_phase4_closeout_coordination_sync_reuse`; `design.implementation.structural_rewrite_phase4_closeout_tracking_entry`; `design.implementation.structural_rewrite_phase4_closeout_tracking_refresh_boundary`
- `Historical Phase 2 Slice Plan`: `design.implementation.structural_rewrite_artifact_role_registry_pilot`
- `Phase 3 Entry Package`: `design.implementation.structural_rewrite_phase3_command_authority_entry`
- `Historical Phase 3 Slice Plan`: `design.implementation.structural_rewrite_phase3_command_companion_source_surface_normalization`
- `Historical Phase 4 Entry Package`: `design.implementation.structural_rewrite_phase4_shared_projection_entry`
- `Historical Phase 4 Slice Plan`: `design.implementation.structural_rewrite_phase4_planning_projection_snapshot`
- `Historical Phase 4 Closeout Entry Package`: `design.implementation.structural_rewrite_phase4_closeout_coordination_entry`
- `Historical Phase 4 Closeout Slice Plan`: `design.implementation.structural_rewrite_phase4_closeout_coordination_sync_reuse`
- `Historical Phase 4 Tracking Entry Package`: `design.implementation.structural_rewrite_phase4_closeout_tracking_entry`
- `Current Phase 4 Slice Plan`: `design.implementation.structural_rewrite_phase4_closeout_tracking_refresh_boundary`
- `Current Phase 4 Implementation Task`: `task.structural_rewrite_program.phase4_closeout_tracking_refresh_boundary.016`
- `Updated At`: `2026-03-15T08:14:01Z`

## Summary
Defines the repo-native execution design for completing rewrite Phase 0 and Phase 1, closing the Phase 2 gate explicitly, delivering one bounded artifact-role metadata slice, closing the Phase 3 entry review explicitly, implementing one bounded Phase 3 command companion normalization slice, closing that slice through explicit outcome review, closing the Phase 4 entry review explicitly, implementing one bounded Phase 4 planning projection snapshot slice, closing that slice through explicit outcome review, approving the bounded closeout-coordination entry review explicitly, landing one bounded Phase 4 closeout coordination sync-reuse slice, closing that slice through explicit outcome review, approving the bounded closeout-tracking entry review explicitly, and handing the trace to one bounded Phase 4 closeout-tracking refresh-boundary slice rather than broader rollout.

## Source Request
- Execute the approved structural rewrite program against the live repository, preserve the current public planning and command-authority boundaries, land the bounded artifact-role metadata and command-companion slices recorded in the trace, close the command-companion slice through explicit outcome review, close the bounded Phase 4 entry review explicitly, implement the approved Phase 4 planning projection snapshot slice, close that slice through explicit outcome review, and continue only through the next explicit bounded checkpoint.

## Scope and Feature Boundary
- Covers the traced planning chain, rewrite-specific governance standards, machine-readable parity and evidence artifacts, migration records, and task chain needed to execute Phase 0 and Phase 1 safely.
- Covers current-state baseline refresh, hotspot inventory refresh, critical-surface classification, history and compatibility consumer mapping, support-level classification, no-go conditions, rollback expectations, and Phase 2 pilot-family selection.
- Covers the Phase 2 entry review outcome, the dedicated first-slice checkpoint package, and one additive, read-only artifact-role metadata implementation slice.
- Covers the Phase 3 entry review outcome, the first rollback-safe command companion normalization slice, and the closed outcome review that handed the trace to the next bounded checkpoint.
- Covers the Phase 3 outcome-review outcome, the dedicated Phase 4 shared-projection entry package, the explicit Phase 4 entry-review outcome, the implemented first Phase 4 planning projection snapshot slice, the closed outcome review for that slice, the closed closeout-coordination entry review, the implemented bounded Phase 4 closeout coordination sync-reuse slice, the closed outcome review for that slice, the closed closeout-tracking entry review, and the current bounded closeout-tracking refresh-boundary implementation checkpoint.
- Does not start Phase 2 runtime, loader, sync, query, or validator-dispatch behavior changes.
- Does not move or delete historical or compatibility surfaces.
- Does not create a second public planning authority or a second command-authority source.

## Current-State Context
- The current live checkpoint remains healthy under `watchtower-core doctor --format json` and `watchtower-core validate all`, and `watchtower-core query authority --domain planning --format json` still resolves the same five public planning questions to coordination, planning catalog, initiatives, tasks, and traceability.
- `watchtower-core query coordination --format json` reports `active_work`, and the rewrite trace's only actionable task at this checkpoint is `task.structural_rewrite_program.phase4_closeout_tracking_refresh_boundary.016`.
- `watchtower-core sync command-index --format json` stays green with `60` entries and no write, and `python -m pytest tests/unit/test_command_index_sync.py` passes `4/4` tests for the new fail-closed command-companion drift guard.
- The first Phase 4 slice has now passed both implementation and explicit outcome review as `core/python/src/watchtower_core/repo_ops/planning_projection_snapshot.py`, the closeout-coordination entry review has now passed explicitly, the bounded closeout coordination sync-reuse slice has now landed, that slice's outcome review has now also passed, the closeout-tracking entry review has now passed explicitly, and the next boundary is a bounded closeout-tracking refresh-boundary slice rather than broader Phase 4 rollout.
- The hotspot picture has shifted since earlier rewrite prose. The new `planning_projection_snapshot.py` is now `513` lines, `initiative_index.py` has dropped to `129`, and the remaining larger Python files still include `repo_ops/validation/document_semantics.py` (`494`), `task_lifecycle.py` (`492`), `acceptance.py` (`471`), `workflow_index.py` (`463`), `planning_scaffold_specs.py` (`431`), `loader.py` (`431`), and `planning_projection_serialization.py` (`419`). Later rewrite work must keep using fresh live counts instead of stale hotspot examples.
- The repo still carries mixed compatibility surfaces on purpose: `watchtower_core.query/` and `watchtower_core.sync/` are current boundary-layer namespaces, `watchtower_core.validation.all` is still a compatibility wrapper for aggregate validation, `query_coordination_handlers.py` is now a thin compatibility facade, and several test-marker files remain in place for repository-path continuity.

## Foundations References Applied
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): the rewrite remains inside repository governance, planning, and shared-core maintenance work.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the design should preserve explicit authority seams, treat compatibility shims carefully, and keep helper-layer complexity reviewable.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): the rewrite must preserve one canonical answer per question and must not widen risky changes without explicit control surfaces.

## Internal Standards and Canonical References Applied
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): the rewrite needs one traced PRD, design, plan, evidence, and task chain rather than prose-only execution.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): the rewrite must keep one active task-backed initiative while the bounded Phase 4 closeout-tracking refresh-boundary slice remains open.
- [task_handling_threshold_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_handling_threshold_standard.md): the rewrite crosses the durable-task threshold and cannot stay as no-task work.
- [authority_map_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/authority_map_standard.md): the rewrite parity contract must preserve the current authority answers rather than reconstructing them informally.
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md): the public planning-authority parity contract should be machine-readable and acceptance-oriented.
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md): baseline, parity, and review completion need durable evidence, not transient notes.
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md): critical, historical, and compatibility surfaces need the same classification vocabulary before any later cleanup slice.
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md): later rewrite slices need explicit checkpoint packages, authored-truth declarations, and rollback paths.

## Design Goals and Constraints
- Publish all Phase 0 and Phase 1 rewrite prerequisites in repo-native homes before any deeper implementation starts.
- Preserve the five live public planning-authority answers and their current query surfaces.
- Keep the Phase 2 pilot limited to one additive family with clear authored truth, explicit storage shape, and no public behavior change requirement.
- Reuse existing standards, acceptance, migration, evidence, planning, and task families instead of creating parallel rewrite-only homes.
- Stop after the bounded closeout-tracking refresh-boundary slice is published as the next checkpoint and keep broader Phase 4 rollout blocked until that slice reaches its explicit outcome review.

## Options Considered
### Option 1
- Treat the external rewrite program as sufficient authorization and start Phase 2 implementation directly.
- Strength: fastest path to code changes.
- Tradeoff: violates the live repo's traced-planning and task-threshold rules, leaves the pilot family ambiguous, and risks starting high-blast-radius work without consumer maps or rollback control.

### Option 2
- Publish a traced repo-native rewrite package that completes Phase 0 and Phase 1, fixes the pilot family, closes the gate explicitly, and lands one bounded slice only if the approval outcome is clean.
- Strength: aligns with live authority, planning, acceptance, migration, and evidence patterns while doing the maximum safe work now.
- Tradeoff: requires several planning and governance artifacts before implementation and still stops after a deliberately small Phase 2 result.

### Option 3
- Keep the rewrite as external prose only and defer repo-local execution until a later session.
- Strength: avoids immediate planning churn.
- Tradeoff: leaves the rewrite unactionable inside the repo and preserves the same ambiguity the review already identified.

## Recommended Design
### Architecture
- Create one traced rewrite initiative with a PRD, feature design, implementation plans, acceptance contract, migration records, validation-evidence artifacts, and an explicit task chain.
- Publish one rewrite classification standard for the four-axis model, compatibility support levels, and retention reasons.
- Publish one rewrite execution-control standard that defines the machine and human checkpoint package, the public planning parity boundary, authored-versus-derived declaration requirements, no-go conditions, and rollback expectations.
- Use the implementation plan as the human Phase 0 and Phase 1 package: baseline evidence, hotspot inventory, critical-surface classification, consumer maps, compatibility classifications, pilot selection, and the Phase 2 entry-review question all live there.
- Use the Phase 2 review task to decide the storage shape explicitly, then route implementation through one dedicated slice plan, one dedicated migration record, one dedicated validation-evidence artifact, one explicit pilot review outcome, a successor Phase 3 entry-review task, one bounded Phase 3 slice plan plus implementation task, one explicit Phase 3 outcome-review task, a successor Phase 4 entry package plus review task that, if approved, hands work to one bounded Phase 4 planning projection snapshot slice, a later Phase 4 slice outcome review that, if clean, hands work only to one bounded closeout-coordination entry package, a bounded closeout-coordination entry review that, if clean, hands work only to one bounded closeout coordination sync-reuse slice, a later closeout coordination sync-reuse outcome review that, if clean, hands work only to one bounded closeout-tracking entry package, and a later closeout-tracking entry review that, if clean, hands work only to one bounded closeout-tracking refresh-boundary slice.
- Choose a small dedicated registry for the first artifact-role metadata slice rather than embedding additive metadata inside an existing governed family. That keeps the pilot additive, keeps family boundaries explicit, and avoids prematurely binding metadata rollout to any one existing authority source.

### Data and Interface Impacts
- New governed docs under `docs/planning/design/implementation/` and `docs/planning/tasks/` capture the gate outcomes, the bounded slices, and the successor review or implementation checkpoints.
- New machine-readable control artifacts under `core/control_plane/ledgers/migrations/` and `core/control_plane/ledgers/validation_evidence/` record the approved slice boundaries and their validation outcomes.
- New control-plane schema, registry, validator, and example surfaces publish the dedicated artifact-role metadata family.
- The landed Phase 3 slice adds a bounded sync-guard implementation change in `core/python/src/watchtower_core/repo_ops/sync/command_index.py` plus direct unit coverage in `core/python/tests/unit/test_command_index_sync.py` so command companion metadata fails closed on future drift.
- Command behavior, authority-map answers, query outputs, and planning-index schemas remain unchanged across the bounded slices.

### Execution Flow
1. Re-run the required baseline commands from `core/python/` and refresh the live hotspot inventory from the current source tree.
2. Publish rewrite classification and execution-control guidance in standards, plus the machine-readable acceptance, migration, and evidence artifacts that anchor the rewrite package.
3. Publish the implementation-plan review package with critical-surface classification, consumer maps, compatibility classifications, and one fixed Phase 2 pilot family.
4. Review the Phase 2 entry package, choose the dedicated-registry storage shape, and record the bounded approval outcome.
5. Publish the dedicated slice plan, migration record, validation-evidence artifact, schema, registry, validator, and example companions for the approved dedicated-registry slice.
6. Sync the derived planning surfaces, validate the repo, close the pilot review explicitly, review the Phase 3 entry package, implement the first bounded Phase 3 slice with its migration and evidence companions, and stop with one Phase 3 outcome-review task open.
7. If the Phase 3 outcome review passes, publish the bounded Phase 4 shared-projection entry package, its ready ledgers, and the dedicated Phase 4 review task; if that review passes, implement one private planning projection snapshot slice, publish its slice ledgers, close that slice through explicit outcome review, publish the bounded closeout-coordination entry package, and keep broader Phase 4 rollout blocked.
8. If the closeout-coordination entry review passes, publish one bounded closeout coordination sync-reuse slice plan, its ready ledgers, and one explicit implementation task without widening the seam to `TaskLifecycleService`, `PlanningScaffoldService`, or broader tracker-family convergence.
9. If the closeout coordination sync-reuse outcome review passes, publish one bounded closeout-tracking entry package, its ready ledgers, and one explicit review task without widening into broader tracker-family convergence, coordination-group redesign, or later-phase work.
10. If the closeout-tracking entry review passes, publish one bounded closeout-tracking refresh-boundary slice plan, its ready ledgers, and one explicit implementation task without widening into broader tracker-family convergence, coordination-group redesign, or later-phase work.

### Invariants and Failure Cases
- `watchtower-core query authority --domain planning --format json` must keep the same five planning answers through this slice.
- No historical relocation or compatibility retirement may start from this trace.
- If the pilot family cannot be fixed to one additive, low-blast-radius choice, the rewrite stops as not ready for Phase 2.
- If the review package cannot show current consumers for candidate cleanup surfaces, later cleanup phases remain blocked.
- If the first slice changes live query routing, sync selection, validator dispatch, command authority, or planning-boundary behavior, the slice has exceeded its approved boundary and must be rolled back.

## Affected Surfaces
- `docs/standards/governance/`
- `docs/planning/prds/`
- `docs/planning/design/features/`
- `docs/planning/design/implementation/`
- `docs/planning/tasks/`
- `core/control_plane/contracts/acceptance/`
- `core/control_plane/ledgers/migrations/`
- `core/control_plane/ledgers/validation_evidence/`
- `core/control_plane/schemas/artifacts/`
- `core/control_plane/registries/`
- `core/control_plane/examples/`

## Design Guardrails
- Do not treat prior hotspot counts as authoritative once the live repo has moved.
- Do not choose command authority, planning-authority projections, or broad sync selection as the first pilot family.
- Do not invent a rewrite-only archive or review namespace outside the current planning and control-plane families.
- Do not let the first slice do more than publish additive artifact-role metadata and its validation companions.

## Risks
- The rewrite can still look "ready" in prose while remaining unsafe if the review task and machine control artifacts drift.
- Compatibility surfaces may look removable even when they still anchor supported imports or repository-path discoverability.
- The chosen pilot family can expand by accident if its authored truth boundary is not kept smaller than the later Phase 4 and Phase 7 concerns.
- A dedicated-registry slice can still create false confidence if later readers mistake its published metadata for runtime authority instead of bounded descriptive state.

## References
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/prds/structural_rewrite_program.md)
- [authority_map.v1.json](/home/j/WatchTowerPlan/core/control_plane/registries/authority_map/authority_map.v1.json)
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md)
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md)
- [structural_rewrite_artifact_role_registry_pilot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_artifact_role_registry_pilot.md)

## Open Questions
- None that block the current checkpoint. The current next question belongs to the bounded Phase 4 closeout-tracking refresh-boundary slice rather than to implied broader Phase 4 rollout or Phase 5 work.

## Updated At
- `2026-03-15T08:14:01Z`
