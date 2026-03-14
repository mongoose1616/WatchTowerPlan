---
trace_id: "trace.structural_rewrite_program"
id: "prd.structural_rewrite_program"
title: "Structural Rewrite Program PRD"
summary: "Execute the structural rewrite as a guarded phased program that refreshes live baseline evidence, publishes rewrite control surfaces, closes the Phase 2 gate, and delivers one bounded artifact-role metadata slice."
type: "prd"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-14T03:56:23Z"
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
- `Linked Implementation Plans`: `design.implementation.structural_rewrite_program`
- `Bounded Slice Plan`: `design.implementation.structural_rewrite_artifact_role_registry_pilot`
- `Updated At`: `2026-03-14T03:56:23Z`

## Summary
Execute the structural rewrite as a guarded phased program that refreshes live baseline evidence, publishes rewrite control surfaces, closes the Phase 2 gate explicitly, and delivers one bounded artifact-role metadata slice before stopping for follow-up review.

## Problem Statement
The live repository is healthy and validated, but the rewrite program originally existed only as external prose until it was anchored in repo-native planning, standards, contracts, and ledger surfaces. That gap created two risks. First, later rewrite work could start from stale hotspot examples or generalized cleanup language instead of the current repo state. Second, high-blast-radius work such as descriptor rollout, projection changes, history cleanup, or compatibility retirement could start without a local parity contract, consumer maps, rollback expectations, and a bounded pilot family.

Phase 0 and Phase 1 have now closed those prerequisite gaps. The remaining risk is procedural: Phase 2 cannot begin safely unless the repository records an explicit gate outcome, fixes the storage shape for the first artifact-role metadata slice, and keeps that first slice additive and read-only. The trace therefore needs one bounded Phase 2 pilot that proves the metadata family without letting it drive live query routing, sync selection, validator dispatch, command authority, or planning-boundary changes.

## Goals
- Refresh the live baseline and hotspot inventory from current repository commands and source files.
- Publish rewrite governance surfaces in repo-native homes instead of relying on free-floating review prose.
- Classify critical authority, history, and compatibility surfaces before any retirement or relocation work begins.
- Fix exactly one low-blast-radius Phase 2 pilot family and justify it against the live repo.
- Close the Phase 2 entry review gate with an explicit approval or block outcome.
- Deliver exactly one bounded, additive, read-only Phase 2 slice for the artifact-role metadata pilot family if and only if the gate is approved cleanly.

## Non-Goals
- Reopening accepted planning-authority, command-authority, or repository-scope decisions.
- Inventing a new archive directory, new lifecycle vocabulary, or parallel rewrite-specific storage tree.
- Performing runtime code changes, history relocation, compatibility retirement, or public authority rewrites beyond the first bounded artifact-role metadata slice.
- Letting the first Phase 2 slice drive live query routing, sync selection, validator dispatch, command presence, or planning-boundary changes.

## Requirements
- `req.structural_rewrite_program.001`: The rewrite trace must re-run the required baseline commands from `core/python/` and publish the resulting live baseline and hotspot inventory in repo-native planning surfaces.
- `req.structural_rewrite_program.002`: The rewrite must publish repo-native guidance for four-axis surface classification, compatibility support-level classification, retention reasons, and rewrite execution control before later implementation phases begin.
- `req.structural_rewrite_program.003`: The rewrite must publish a machine-readable public planning-authority parity contract that preserves the five current planning questions and their current canonical machine answers.
- `req.structural_rewrite_program.004`: Phase 1 work must classify the critical planning, command, workflow, runtime-boundary, and history or compatibility surfaces and must map current consumers for candidate cleanup surfaces.
- `req.structural_rewrite_program.005`: The rewrite must choose exactly one low-blast-radius Phase 2 pilot family with clear authored truth, derived outputs, and rollback expectations, and it must reject higher-blast-radius pilot options for now.
- `req.structural_rewrite_program.006`: The trace must prepare a durable Phase 2 entry review package, keep an explicit review task for that checkpoint, and record an explicit approval or block outcome before any Phase 2 implementation work begins.
- `req.structural_rewrite_program.007`: If the Phase 2 gate is approved, the first slice must stay bounded to the artifact-role metadata family, use one declared authored-truth surface, and remain additive and read-only.
- `req.structural_rewrite_program.008`: The first approved Phase 2 slice must publish a dedicated checkpoint document, migration record, validation-evidence artifact, and follow-up review task that capture storage shape, parity method, current consumers, and rollback expectations.

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
- `ac.structural_rewrite_program.010`: After the first slice lands, the trace stops with one explicit open follow-up review task instead of expanding automatically into broader Phase 2 or Phase 3 work.

## Risks and Dependencies
- The rewrite can create accidental authority drift if its parity contract is weaker than the live authority map and query behavior.
- Historical or compatibility cleanup can become unsafe quickly if consumer maps and discoverability checks are incomplete.
- The Phase 2 pilot can stop being low blast radius if it touches live command authority, planning queries, or repo-wide sync selection instead of an additive metadata family.
- The first artifact-role metadata slice can still become misleading if it overstates current coverage or begins classifying broader compatibility and workflow families that the Phase 1 evidence package did not yet table explicitly.
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
- `2026-03-14T03:56:23Z`
