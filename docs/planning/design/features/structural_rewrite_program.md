---
trace_id: "trace.structural_rewrite_program"
id: "design.features.structural_rewrite_program"
title: "Structural Rewrite Program Feature Design"
summary: "Defines the repo-native execution design for completing rewrite Phase 0 and Phase 1, closing the Phase 2 gate, delivering one bounded artifact-role metadata slice, and handing the trace to a Phase 3 entry package."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-14T04:31:59Z"
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
- `Linked Implementation Plans`: `design.implementation.structural_rewrite_program`
- `Bounded Slice Plan`: `design.implementation.structural_rewrite_artifact_role_registry_pilot`
- `Next Entry Package`: `design.implementation.structural_rewrite_phase3_command_authority_entry`
- `Updated At`: `2026-03-14T04:31:59Z`

## Summary
Defines the repo-native execution design for completing rewrite Phase 0 and Phase 1, closing the Phase 2 gate explicitly, delivering one bounded artifact-role metadata slice, and carrying the trace to the next explicit phase-entry checkpoint without starting Phase 3 implementation.

## Source Request
- Execute the approved structural rewrite program against the live repository, close the remaining pre-Phase-2 gate work, and if the gate is approved cleanly deliver exactly one bounded artifact-role metadata slice before stopping for review.

## Scope and Feature Boundary
- Covers the traced planning chain, rewrite-specific governance standards, machine-readable parity and evidence artifacts, migration records, and task chain needed to execute Phase 0 and Phase 1 safely.
- Covers current-state baseline refresh, hotspot inventory refresh, critical-surface classification, history and compatibility consumer mapping, support-level classification, no-go conditions, rollback expectations, and Phase 2 pilot-family selection.
- Covers the Phase 2 entry review outcome, the dedicated first-slice checkpoint package, and one additive, read-only artifact-role metadata implementation slice.
- Does not start Phase 2 runtime, loader, sync, query, or validator-dispatch behavior changes.
- Does not move or delete historical or compatibility surfaces.
- Does not create a second public planning authority or a second command-authority source.

## Current-State Context
- The current live checkpoint is healthy: `watchtower-core doctor --format json` reports `status: ok` with `60` commands, `48` schemas, `55` validators, `64` standards, `31` workflows, `62` initiatives, `209` tasks, and `62` traces loaded.
- `watchtower-core validate all` passes `1219/1219` targets, and `watchtower-core query authority --domain planning --format json` still resolves the same five public planning questions to coordination, planning catalog, initiatives, tasks, and traceability.
- `watchtower-core query coordination --format json` reports `active_work`, and the rewrite trace's current actionable task after the pilot review is `task.structural_rewrite_program.phase3_entry_review.006`.
- The hotspot picture has shifted since earlier rewrite prose. The current largest Python files include `initiative_index.py` (`540` lines), `document_semantics.py` (`494`), `task_lifecycle.py` (`492`), `acceptance.py` (`471`), `workflow_index.py` (`463`), `planning_scaffold_specs.py` (`431`), `loader.py` (`431`), and `planning_projection_serialization.py` (`419`). The older `planning_scaffolds.py` hotspot has already fallen to `307` lines, so later rewrite work must use fresh live counts instead of stale hotspot examples.
- The repo still carries mixed compatibility surfaces on purpose: `watchtower_core.query/` and `watchtower_core.sync/` are current boundary-layer namespaces, `watchtower_core.validation.all` is still a compatibility wrapper for aggregate validation, `query_coordination_handlers.py` is now a thin compatibility facade, and several test-marker files remain in place for repository-path continuity.

## Foundations References Applied
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): the rewrite remains inside repository governance, planning, and shared-core maintenance work.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the design should preserve explicit authority seams, treat compatibility shims carefully, and keep helper-layer complexity reviewable.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): the rewrite must preserve one canonical answer per question and must not widen risky changes without explicit control surfaces.

## Internal Standards and Canonical References Applied
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): the rewrite needs one traced PRD, design, plan, evidence, and task chain rather than prose-only execution.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): the rewrite must keep one active task-backed initiative while the Phase 3 entry review remains open.
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
- Stop after the pilot review closes with one explicit Phase 3 entry-review task open so the repository does not imply automatic authorization for broader rollout.

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
- Use the Phase 2 review task to decide the storage shape explicitly, then route implementation through one dedicated slice plan, one dedicated migration record, one dedicated validation-evidence artifact, one explicit pilot review outcome, and a successor Phase 3 entry-review task.
- Choose a small dedicated registry for the first artifact-role metadata slice rather than embedding additive metadata inside an existing governed family. That keeps the pilot additive, keeps family boundaries explicit, and avoids prematurely binding metadata rollout to any one existing authority source.

### Data and Interface Impacts
- New governed docs under `docs/planning/design/implementation/` and `docs/planning/tasks/` capture the gate outcome, the bounded slice, and the successor review checkpoint.
- New machine-readable control artifacts under `core/control_plane/ledgers/migrations/` and `core/control_plane/ledgers/validation_evidence/` record the approved slice and its validation outcome.
- New control-plane schema, registry, validator, and example surfaces publish the dedicated artifact-role metadata family.
- No runtime code, command behavior, authority-map answers, query outputs, or planning-index schemas change in this slice.

### Execution Flow
1. Re-run the required baseline commands from `core/python/` and refresh the live hotspot inventory from the current source tree.
2. Publish rewrite classification and execution-control guidance in standards, plus the machine-readable acceptance, migration, and evidence artifacts that anchor the rewrite package.
3. Publish the implementation-plan review package with critical-surface classification, consumer maps, compatibility classifications, and one fixed Phase 2 pilot family.
4. Review the Phase 2 entry package, choose the dedicated-registry storage shape, and record the bounded approval outcome.
5. Publish the dedicated slice plan, migration record, validation-evidence artifact, schema, registry, validator, and example companions for the approved dedicated-registry slice.
6. Sync the derived planning surfaces, validate the repo, close the pilot review explicitly, and stop with one Phase 3 entry-review task still open.

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
- None that block the first bounded slice. The storage-shape decision is fixed to a small dedicated registry for the approved pilot.

## Updated At
- `2026-03-14T04:31:59Z`
