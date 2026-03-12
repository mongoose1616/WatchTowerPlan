---
trace_id: trace.reference_resolution_reuse_hardening
id: prd.reference_resolution_reuse_hardening
title: Reference Resolution Reuse Hardening PRD
summary: Eliminate repeated full reference-index rebuilds in workflow semantics validation
  and dependent sync families while preserving current validation, sync, and query
  behavior.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-12T15:09:05Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/src/watchtower_core/repo_ops/sync/
- core/python/tests/
---

# Reference Resolution Reuse Hardening PRD

## Record Metadata
- `Trace ID`: `trace.reference_resolution_reuse_hardening`
- `PRD ID`: `prd.reference_resolution_reuse_hardening`
- `Status`: `active`
- `Linked Decisions`: `decision.reference_resolution_reuse_hardening_direction`
- `Linked Designs`: `design.features.reference_resolution_reuse_hardening`
- `Linked Implementation Plans`: `design.implementation.reference_resolution_reuse_hardening`
- `Updated At`: `2026-03-12T15:09:05Z`

## Summary
Eliminate repeated full reference-index rebuilds in workflow semantics validation and dependent sync families while preserving current validation, sync, and query behavior.

## Problem Statement
The comprehensive refactoring and optimization review found one bounded but real scale defect in the repo-local orchestration layer. Workflow document-semantics validation currently rebuilds the full governed reference index once per workflow file, so a `validate all --document-semantics` pass in the live repo rebuilds that index `30` times. Aggregate `sync all` also rebuilds the same reference index `4` times across the explicit `reference-index` target plus the dependent foundation, standard, and workflow index builders. As the repository grows, those repeated full scans increase runtime cost and widen maintenance pressure without improving fidelity because the reused reference-resolution data is identical within a single command run.

## Goals
- Reuse one command-scoped reference-resolution snapshot across workflow semantics validation.
- Reuse one command-scoped reference-resolution snapshot across reference-dependent `sync all` targets.
- Preserve generated artifacts, validation outcomes, and command contracts exactly.
- Close the review finding with explicit regression coverage and normal traced closeout evidence.

## Non-Goals
- Changing workflow semantics, reference-index contents, or any query or sync output shape.
- Adding a long-lived mutable cache that survives across separate commands or repository changes.
- Relaxing validation coverage or skipping dependent sync families to reduce work.

## Requirements
- `req.reference_resolution_reuse_hardening.001`: Repo-local reference-resolution helpers must expose one explicit way to derive `reference_urls_by_path` from a fresh governed reference-index build so dependent services can reuse the same data without reparsing it ad hoc.
- `req.reference_resolution_reuse_hardening.002`: Workflow document-semantics validation must reuse one workflow-loading context per validation-service run instead of rebuilding the governed reference index once per workflow document.
- `req.reference_resolution_reuse_hardening.003`: Aggregate sync orchestration must build one shared reference-resolution snapshot for the `reference-index`, `foundation-index`, `standard-index`, and `workflow-index` slice and reuse it without changing generated artifacts.
- `req.reference_resolution_reuse_hardening.004`: The initiative must prove the reuse behavior with targeted regression tests and keep the repo green on the normal validation baseline.

## Acceptance Criteria
- `ac.reference_resolution_reuse_hardening.001`: The planning corpus publishes the active PRD, accepted direction decision, active feature design, active implementation plan, acceptance contract, evidence ledger, bootstrap task, implementation task, and validation-closeout task for `trace.reference_resolution_reuse_hardening`.
- `ac.reference_resolution_reuse_hardening.002`: Direct instrumentation shows workflow document-semantics validation rebuilds the reference index once per service run instead of once per workflow file.
- `ac.reference_resolution_reuse_hardening.003`: Direct instrumentation shows `sync all` rebuilds the reference index once while keeping the reference, foundation, standard, and workflow index outputs unchanged.
- `ac.reference_resolution_reuse_hardening.004`: Targeted regressions plus the full repository validation baseline pass after the reuse hardening lands.
- `ac.reference_resolution_reuse_hardening.005`: A follow-up review of adjacent validation and sync surfaces finds no additional actionable issues.

## Risks and Dependencies
- Hidden mutable caching could create stale reference resolution if it crossed command boundaries or outlived the current loader inputs.
- Sync orchestration changes could accidentally alter dependency ordering or generated artifact contents if the shared snapshot were wired to the wrong targets.
- The work depends on the current reference index remaining the canonical source for governed reference-to-upstream resolution inside the repo-local orchestration layer.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): reduce repeated work by making shared data derivation explicit and command-scoped instead of relying on hidden implicit behavior.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): optimization work must preserve fail-closed behavior and same-change alignment across code, tests, and planning surfaces.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): scaling the governed core should remove internal friction before future product implementation increases repository load further.

## References
- [reference_resolution_reuse_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/reference_resolution_reuse_hardening.md)
- [reference_resolution_reuse_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/reference_resolution_reuse_hardening.md)
- [repository_validation_standard.md](/home/j/WatchTowerPlan/docs/standards/validations/repository_validation_standard.md)
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md)
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md)

## Updated At
- `2026-03-12T15:09:05Z`
