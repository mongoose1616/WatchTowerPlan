---
trace_id: "trace.structural_rewrite_program"
id: "prd.structural_rewrite_program"
title: "Structural Rewrite Program PRD"
summary: "Execute the structural rewrite as a guarded phased program that refreshes live baseline evidence, publishes rewrite control surfaces, closes the Phase 2 gate, lands one bounded Phase 3 command companion normalization slice, closes the first Phase 4 slice and outcome review explicitly, approves the closeout-coordination entry review, lands one bounded Phase 4 closeout coordination sync-reuse slice, closes that slice through explicit outcome review, and hands the trace to one bounded Phase 4 closeout-tracking entry review."
type: "prd"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-15T07:35:59Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/standards/"
  - "docs/planning/"
  - "core/control_plane/"
  - "core/python/"
aliases:
  - "structural rewrite"
  - "rewrite program"
  - "phase gated rewrite"
---

# Structural Rewrite Program PRD

## Record Metadata
- `Trace ID`: `trace.structural_rewrite_program`
- `PRD ID`: `prd.structural_rewrite_program`
- `Status`: `active`
- `Linked Decisions`: `None`
- `Linked Designs`: `design.features.structural_rewrite_program`
- `Linked Implementation Plans`: `design.implementation.structural_rewrite_program`; `design.implementation.structural_rewrite_phase3_command_companion_source_surface_normalization`; `design.implementation.structural_rewrite_phase4_shared_projection_entry`; `design.implementation.structural_rewrite_phase4_planning_projection_snapshot`; `design.implementation.structural_rewrite_phase4_closeout_coordination_entry`; `design.implementation.structural_rewrite_phase4_closeout_coordination_sync_reuse`; `design.implementation.structural_rewrite_phase4_closeout_tracking_entry`
- `Historical Phase 2 Slice Plan`: `design.implementation.structural_rewrite_artifact_role_registry_pilot`
- `Historical Phase 3 Slice Plan`: `design.implementation.structural_rewrite_phase3_command_companion_source_surface_normalization`
- `Phase 3 Entry Package`: `design.implementation.structural_rewrite_phase3_command_authority_entry`
- `Historical Phase 4 Entry Package`: `design.implementation.structural_rewrite_phase4_shared_projection_entry`
- `Historical Phase 4 Slice Plan`: `design.implementation.structural_rewrite_phase4_planning_projection_snapshot`
- `Historical Phase 4 Closeout Entry Package`: `design.implementation.structural_rewrite_phase4_closeout_coordination_entry`
- `Historical Phase 4 Closeout Slice Plan`: `design.implementation.structural_rewrite_phase4_closeout_coordination_sync_reuse`
- `Current Phase 4 Entry Package`: `design.implementation.structural_rewrite_phase4_closeout_tracking_entry`
- `Current Phase 4 Review Task`: `task.structural_rewrite_program.phase4_closeout_tracking_entry_review.015`
- `Updated At`: `2026-03-15T07:35:59Z`

## Summary
Execute the structural rewrite as a guarded phased program that refreshes live baseline evidence, publishes rewrite control surfaces, closes the Phase 2 gate explicitly, delivers one bounded artifact-role metadata slice, closes the Phase 3 entry review explicitly, lands one bounded command companion source-surface normalization slice, closes that slice through an explicit outcome review, closes the Phase 4 shared-projection entry review explicitly, implements one bounded Phase 4 planning projection snapshot slice, closes that slice through an explicit outcome review, approves the bounded Phase 4 closeout-coordination entry review explicitly, lands one bounded Phase 4 closeout coordination sync-reuse slice, closes that slice through an explicit outcome review, and hands the trace to one bounded Phase 4 closeout-tracking entry review.

## Problem Statement
The live repository is healthy and validated, but the rewrite program originally existed only as external prose until it was anchored in repo-native planning, standards, contracts, and ledger surfaces. That gap created two risks. First, later rewrite work could start from stale hotspot examples or generalized cleanup language instead of the current repo state. Second, high-blast-radius work such as descriptor rollout, projection changes, history cleanup, or compatibility retirement could start without a local parity contract, consumer maps, rollback expectations, and a bounded pilot family.

Phase 0 and Phase 1 have now closed those prerequisite gaps, and the first bounded Phase 2 pilot proved the low-blast-radius metadata pattern cleanly. The first bounded Phase 3 slice then resolved the immediate command companion drift by aligning the root, doctor, sync, and validate command companion surfaces to the parser-owned or family-owned implementation paths while keeping command authority in the current registry plus parser tree. That slice passed its explicit outcome review, the later Phase 4 entry review named the full coordination-sync and mutation-path consumer boundary plus one exact rollback-safe seam, and the approved first Phase 4 slice landed as one private shared planning projection helper. Its outcome review then passed cleanly, the successor closeout-coordination entry review approved one exact next slice, and that bounded closeout slice then passed its own explicit outcome review after holding parity and result-contract boundaries at the approved shared seam. The current rewrite question is whether the remaining direct PRD, decision, and design tracking refresh step deserves its own bounded entry checkpoint without implying broader tracker-family convergence or later-phase rollout.

## Goals
- Refresh the live baseline and hotspot inventory from current repository commands and source files.
- Publish rewrite governance surfaces in repo-native homes instead of relying on free-floating review prose.
- Classify critical authority, history, and compatibility surfaces before any retirement or relocation work begins.
- Fix exactly one low-blast-radius Phase 2 pilot family and justify it against the live repo.
- Close the Phase 2 entry review gate with an explicit approval or block outcome.
- Deliver exactly one bounded, additive, read-only Phase 2 slice for the artifact-role metadata pilot family if and only if the gate is approved cleanly.
- Close the Phase 3 entry review gate with an explicit approval or block outcome.
- If the Phase 3 gate is approved, implement exactly one rollback-safe command companion normalization slice, close that slice through an explicit outcome review, and stop broader rewrite implementation at a later-phase entry review rather than implied continuation.
- If the Phase 3 outcome review passes, open one bounded Phase 4 shared-projection entry package and review gate before any Phase 4 implementation begins.
- If the Phase 4 entry review passes, implement one bounded Phase 4 planning projection snapshot slice, record its outcome explicitly, and keep broader Phase 4, Phase 5, Phase 6, and Phase 7 work blocked.
- If the first Phase 4 slice outcome review passes, open one bounded Phase 4 closeout-coordination entry package and review gate before any further Phase 4 implementation begins.
- If the closeout-coordination entry review passes, implement one bounded Phase 4 closeout coordination sync-reuse slice, stop it at an explicit outcome review, and keep broader mutation-path convergence and later-phase work blocked.
- If the closeout coordination sync-reuse outcome review passes, open one bounded Phase 4 closeout-tracking entry package and review gate before any further Phase 4 implementation begins.

## Non-Goals
- Reopening accepted planning-authority, command-authority, or repository-scope decisions.
- Inventing a new archive directory, new lifecycle vocabulary, or parallel rewrite-specific storage tree.
- Performing runtime code changes, history relocation, compatibility retirement, or public authority rewrites beyond the first bounded artifact-role metadata slice.
- Letting the first Phase 2 slice drive live query routing, sync selection, validator dispatch, command presence, or planning-boundary changes.
- Expanding the implemented Phase 3 slice into broader command-authority, workflow, route, compatibility, or public-planning rollout without a new explicit checkpoint.
- Starting broader Phase 4 implementation directly from a clean Phase 3 outcome review or a clean Phase 4 entry review without one named rollback-safe first slice.
- Starting broader mutation-path convergence, broader tracker-family convergence, or Phase 5 work directly from a clean first Phase 4 slice outcome review, a clean closeout-coordination entry review, or a clean closeout coordination sync-reuse outcome review without one named successor slice.

## Requirements
- `req.structural_rewrite_program.001`: The rewrite trace must re-run the required baseline commands from `core/python/` and publish the resulting live baseline and hotspot inventory in repo-native planning surfaces.
- `req.structural_rewrite_program.002`: The rewrite must publish repo-native guidance for four-axis surface classification, compatibility support-level classification, retention reasons, and rewrite execution control before later implementation phases begin.
- `req.structural_rewrite_program.003`: The rewrite must publish a machine-readable public planning-authority parity contract that preserves the five current planning questions and their current canonical machine answers.
- `req.structural_rewrite_program.004`: Phase 1 work must classify the approved critical-surface gate scope for public planning, command-boundary, compatibility, and historical-retention candidate surfaces, must map current consumers for candidate cleanup surfaces, and must require a later family-specific classification or parity package before untouched workflow, route, sync, validator, projection, history, or compatibility families are implemented.
- `req.structural_rewrite_program.005`: The rewrite must choose exactly one low-blast-radius Phase 2 pilot family with clear authored truth, derived outputs, and rollback expectations, and it must reject higher-blast-radius pilot options for now.
- `req.structural_rewrite_program.006`: The trace must prepare a durable Phase 2 entry review package, keep an explicit review task for that checkpoint, and record an explicit approval or block outcome before any Phase 2 implementation work begins.
- `req.structural_rewrite_program.007`: If the Phase 2 gate is approved, the first slice must stay bounded to the artifact-role metadata family, use one declared authored-truth surface, and remain additive and read-only.
- `req.structural_rewrite_program.008`: The first approved Phase 2 slice must publish a dedicated checkpoint document, migration record, validation-evidence artifact, and follow-up review task that capture storage shape, parity method, current consumers, and rollback expectations.
- `req.structural_rewrite_program.009`: Before any Phase 3 implementation begins, the trace must record an explicit Phase 3 entry review outcome that reaffirms the current CLI registry plus parser tree as command authority, names the first rollback-safe slice, and records whether any additional command-adjacent classification addendum is required for that slice.
- `req.structural_rewrite_program.010`: The first implemented Phase 3 slice must reconcile the root, doctor, sync, and validate command companion source surfaces to the parser-owned or family-owned implementation paths already published in the command index and must publish a bounded drift guard plus successor review task without changing command authority or public planning parity.
- `req.structural_rewrite_program.011`: After the first Phase 3 slice lands, the trace must record an explicit pass or block outcome for that slice and, if it passes, name a new bounded successor checkpoint rather than implying broader Phase 3 or Phase 4 continuation.
- `req.structural_rewrite_program.012`: If the Phase 3 outcome review passes, the next checkpoint must be a dedicated Phase 4 shared-projection entry package that preserves the five public planning answers, keeps any internal planning graph private by default, publishes the projection-family classification addendum for the touched surfaces, and keeps Phase 4 implementation blocked until its own review closes.
- `req.structural_rewrite_program.013`: Before any Phase 4 implementation begins, the trace must record an explicit Phase 4 entry review outcome that reaffirms the private internal-graph boundary, names the full coordination-sync and mutation-path consumer boundary, and names one exact rollback-safe first slice.
- `req.structural_rewrite_program.014`: If the Phase 4 entry review passes, the approved first Phase 4 slice must stay fixed to one private trace-scoped planning projection snapshot behind `initiative_index` and `planning_catalog` while preserving the five public planning-authority answers, the current coordination-sync ordering, the current mutation-path callers, and downstream coordination behavior.
- `req.structural_rewrite_program.015`: If the first Phase 4 slice outcome review passes, the next checkpoint must be a dedicated Phase 4 closeout-coordination entry package that preserves the five public planning answers, keeps the private planning graph private, names `InitiativeCloseoutService` as the exact remaining direct write-path outlier, and keeps further Phase 4 implementation blocked until its own review closes.
- `req.structural_rewrite_program.016`: Before any closeout-coordination implementation begins, the trace must record an explicit closeout-coordination entry review outcome that enumerates the closeout result contract boundary, names the exact in-seam shared outputs and the exact out-of-seam direct tracker outputs, and opens one bounded implementation task plus ready ledgers for the approved slice.
- `req.structural_rewrite_program.017`: If the closeout-coordination entry review passes, the approved first Phase 4 closeout slice must stay fixed to one post-traceability coordination-sync reuse seam for `initiative_index`, `planning_catalog`, `coordination_index`, `initiative_tracking`, and `coordination_tracking` while preserving `traceability_output_path`, `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path`, the five public planning-authority answers, the private planning-graph boundary, and the current `TaskLifecycleService` and `PlanningScaffoldService` behavior.
- `req.structural_rewrite_program.018`: If the closeout coordination sync-reuse outcome review passes, the next checkpoint must be a dedicated Phase 4 closeout-tracking entry package that preserves the five public planning answers, keeps the private planning graph private, preserves the approved shared closeout seam unchanged, names the remaining direct `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` refresh step as the exact next outlier, and keeps further Phase 4 implementation blocked until its own review closes.

## Acceptance Criteria
- `ac.structural_rewrite_program.001`: The planning corpus for `trace.structural_rewrite_program` contains the active PRD, active feature design, the Phase 0 or Phase 1 implementation package, the bounded Phase 2 slice plan, the aligned acceptance contract, the companion migration and validation-evidence artifacts, the closed bootstrap and Phase 0 or Phase 1 package tasks, and traced review or execution tasks for the Phase 2 gate and first slice.
- `ac.structural_rewrite_program.002`: The required baseline commands report a healthy workspace, current planning-authority answers, and the ready-for-bootstrap baseline before the new trace is introduced, and the published hotspot inventory reflects the live repo rather than stale review assumptions.
- `ac.structural_rewrite_program.003`: The rewrite publishes the four-axis classification standard and the rewrite execution-control standard under `docs/standards/governance/`.
- `ac.structural_rewrite_program.004`: The acceptance contract and companion planning surfaces preserve the five current planning-authority answers for coordination, planning, initiatives, tasks, and traceability.
- `ac.structural_rewrite_program.005`: The implementation package publishes critical-surface classification, history and compatibility consumer maps, support-level classifications, retention reasons, no-go conditions, rollback expectations, and Phase 2 entry conditions.
- `ac.structural_rewrite_program.006`: The implementation package fixes Phase 2 to the artifact-role metadata family only, explains why broader pilot families are deferred, and records the required Phase 2 review question.
- `ac.structural_rewrite_program.007`: Before any Phase 2 implementation begins, the trace records the Phase 2 entry review package, the gate outcome, and the approved storage shape for the first artifact-role metadata slice.
- `ac.structural_rewrite_program.008`: If the gate is approved, the first slice publishes one dedicated artifact-role metadata family, its schema and validator companions, and the dedicated checkpoint package without changing the five public planning-authority answers.
- `ac.structural_rewrite_program.009`: The first slice remains additive and read-only, with no live query-routing, sync-selection, validator-dispatch, command-authority, or planning-boundary behavior changes.
- `ac.structural_rewrite_program.010`: After the first slice lands, the trace records an explicit pilot follow-up review outcome and opens a new bounded checkpoint instead of expanding automatically into broader Phase 2 or Phase 3 implementation.
- `ac.structural_rewrite_program.011`: Before any Phase 3 implementation begins, the trace records the explicit Phase 3 entry review outcome, names the first rollback-safe command companion normalization slice, reaffirms the current command-authority boundary, and records whether any additional classification addendum is required for that slice.
- `ac.structural_rewrite_program.012`: If the first Phase 3 slice lands, the root, doctor, sync, and validate command companion surfaces plus the command-index sync guard converge on the registry-backed implementation paths, command authority remains unchanged, public planning parity remains unchanged, and the trace stops at an explicit outcome review task.
- `ac.structural_rewrite_program.013`: The Phase 3 outcome review records an explicit pass or block decision for the bounded command companion slice and, if it passes, names one bounded successor checkpoint rather than implying broader Phase 3 or Phase 4 rollout.
- `ac.structural_rewrite_program.014`: If the Phase 3 outcome review passes, the trace publishes one dedicated Phase 4 shared-projection entry package, its machine-readable ready records, and one explicit Phase 4 review task while keeping shared projection and internal planning-graph implementation blocked.
- `ac.structural_rewrite_program.015`: Before any Phase 4 implementation begins, the trace records the explicit Phase 4 entry review outcome, names the full coordination-sync and mutation-path consumer boundary, names one exact rollback-safe seam, and opens one bounded implementation task plus ready ledgers for the approved first slice.
- `ac.structural_rewrite_program.016`: If the Phase 4 entry review passes, the approved first Phase 4 slice plan and implementation task stay limited to one private trace-scoped planning projection snapshot behind `initiative_index` and `planning_catalog` while the five public planning-authority answers, coordination-sync ordering, mutation callers, and downstream coordination behavior remain unchanged.
- `ac.structural_rewrite_program.017`: If the first Phase 4 slice outcome review passes, the trace publishes one dedicated Phase 4 closeout-coordination entry package, its machine-readable ready records, and one explicit review task while keeping further shared-projection, mutation-path, and later-phase implementation blocked.
- `ac.structural_rewrite_program.018`: Before any closeout-coordination implementation begins, the trace records the explicit closeout-coordination entry review outcome, names the closeout result contract boundary, names the exact in-seam and out-of-seam outputs, and opens one bounded implementation task plus ready ledgers for the approved slice.
- `ac.structural_rewrite_program.019`: If the closeout-coordination entry review passes, the approved first Phase 4 closeout slice plan and implementation task stay limited to one post-traceability coordination-sync reuse seam for `initiative_index`, `planning_catalog`, `coordination_index`, `initiative_tracking`, and `coordination_tracking` while `traceability_output_path`, `prd_tracking_output_path`, `decision_tracking_output_path`, and `design_tracking_output_path` remain explicit and the five public planning-authority answers, current mutation callers, and private planning-graph boundary remain unchanged.
- `ac.structural_rewrite_program.020`: If the closeout coordination sync-reuse outcome review passes, the trace publishes one dedicated Phase 4 closeout-tracking entry package, its machine-readable ready records, and one explicit review task while keeping further coordination-group, tracker-family, and later-phase implementation blocked.

## Risks and Dependencies
- The rewrite can create accidental authority drift if its parity contract is weaker than the live authority map and query behavior.
- Historical or compatibility cleanup can become unsafe quickly if consumer maps and discoverability checks are incomplete.
- The Phase 2 pilot can stop being low blast radius if it touches live command authority, planning queries, or repo-wide sync selection instead of an additive metadata family.
- The first artifact-role metadata slice can still become misleading if it overstates current coverage or begins classifying broader compatibility and workflow families that the Phase 1 evidence package did not yet table explicitly.
- The first Phase 3 slice can still widen unsafely if command companion cleanup is allowed to act like a second command-authority definition instead of staying a companion-surface normalization pass.
- Supporting trace documents can still create execution ambiguity if stale current-state narration is left in place after the live checkpoint advances.
- Later-phase projection work can still reset the public planning boundary accidentally if an internal graph or shared builder is allowed to behave like a new public authority surface.
- The trace depends on the existing authority map, planning indexes, traceability projections, task tracking model, and acceptance or evidence ledgers remaining authoritative.

## Foundations References Applied
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md): the rewrite remains a repository-governance and shared-core maintenance program, not future product implementation work.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the rewrite must preserve explicit authority boundaries, deterministic local artifacts, and bounded compatibility shims.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): the rewrite must keep one canonical answer per important question and must gate risky operations explicitly.

## References
- [authority_map.v1.json](/home/j/WatchTowerPlan/core/control_plane/registries/authority_map/authority_map.v1.json)
- [coordination_tracking.md](/home/j/WatchTowerPlan/docs/planning/coordination_tracking.md)
- [rewrite_surface_classification_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_surface_classification_standard.md)
- [rewrite_execution_control_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/rewrite_execution_control_standard.md)
- [structural_rewrite_artifact_role_registry_pilot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_artifact_role_registry_pilot.md)

## Updated At
- `2026-03-15T07:35:59Z`
