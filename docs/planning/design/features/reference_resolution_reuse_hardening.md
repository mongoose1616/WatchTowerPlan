---
trace_id: trace.reference_resolution_reuse_hardening
id: design.features.reference_resolution_reuse_hardening
title: Reference Resolution Reuse Hardening Feature Design
summary: Defines the technical design boundary for Reference Resolution Reuse Hardening.
type: feature_design
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

# Reference Resolution Reuse Hardening Feature Design

## Record Metadata
- `Trace ID`: `trace.reference_resolution_reuse_hardening`
- `Design ID`: `design.features.reference_resolution_reuse_hardening`
- `Design Status`: `active`
- `Linked PRDs`: `prd.reference_resolution_reuse_hardening`
- `Linked Decisions`: `decision.reference_resolution_reuse_hardening_direction`
- `Linked Implementation Plans`: `design.implementation.reference_resolution_reuse_hardening`
- `Updated At`: `2026-03-12T15:09:05Z`

## Summary
Defines the technical design boundary for Reference Resolution Reuse Hardening.

## Source Request
- Do a comprehensive project review for refactoring and potential optimizations without reducing capability, fidelity, or performance.

## Scope and Feature Boundary
- Covers shared reference-resolution reuse for workflow semantics validation and the reference-dependent `sync all` targets.
- Covers one shared helper module, workflow-loading context reuse, sync-service injection points, and regression coverage for the reuse behavior.
- Does not change reference-index contents, workflow semantics rules, generated artifact schemas, or CLI contracts.
- Does not introduce persistent cross-command caches or wider architecture changes outside the bounded reuse path.

## Current-State Context
- The live repo passes its full validation baseline, so the remaining issue is scale efficiency rather than correctness drift.
- Direct instrumentation showed `DocumentSemanticsValidationService` rebuilding the governed reference index `30` times during the current document-semantics aggregate pass because each workflow-module validation called `load_workflow_document()` with a fresh reference-index build.
- Direct instrumentation also showed `AllSyncService` rebuilding the governed reference index `4` times during one `sync all` pass across the explicit `reference-index` target plus the dependent foundation, standard, and workflow index builders.
- The reused reference-resolution data is command-local and identical across those repeated builds, so the current behavior spends time rescanning the same governed reference corpus without improving correctness.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the fix should create one explicit seam for derived reference resolution instead of burying repeated work inside downstream loaders.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): the refactor must stay fail closed and preserve same-change alignment across code, tests, and planning evidence.
- [engineering_stack_direction.md](/home/j/WatchTowerPlan/docs/foundations/engineering_stack_direction.md): the Python helper layer should remain deterministic and small, favoring bounded in-process reuse over heavier persistence machinery.

## Internal Standards and Canonical References Applied
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): prefer explicit helper seams and narrow bounded state over copy-pasted logic or hidden globals.
- [repository_validation_standard.md](/home/j/WatchTowerPlan/docs/standards/validations/repository_validation_standard.md): optimization changes must keep the broad validation baseline green and explicitly tested.
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md): workflow-module loading and indexing must stay aligned with the derived workflow index contract.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): workflow semantic validation must preserve the current structure and link guardrails while the loader internals change.

## Design Goals and Constraints
- Reuse derived reference-resolution data exactly once per command-scoped validation or sync run when the same loader inputs are being examined repeatedly.
- Keep standalone sync-service behavior intact so direct family syncs still work without aggregate orchestration.
- Preserve generated JSON and Markdown outputs byte-for-byte except for expected timestamp changes from the traced planning work.

## Options Considered
### Option 1
- Leave each validation or sync surface responsible for rebuilding its own reference-resolution data.
- Strength: zero refactor churn and no new shared seam.
- Tradeoff: preserves the review finding, keeps repeated full scans in the hottest validation and sync paths, and scales poorly as the repo grows.

### Option 2
- Add one command-scoped shared reference-resolution seam and inject it only into the validation and sync paths that repeat the work.
- Strength: removes the duplicated scans without changing durable contracts or adding long-lived mutable caches.
- Tradeoff: adds a small amount of orchestration plumbing and new regression expectations around reuse counts.

## Recommended Design
### Architecture
- Add a shared helper that can derive `reference_urls_by_path` from one fresh reference-index document.
- Make workflow loading support one reusable `WorkflowDocumentContext` containing workflow metadata plus that reference-resolution map.
- Let `DocumentSemanticsValidationService` lazily build and reuse one workflow-document context per service instance.
- Let `AllSyncService` build one shared reference-index document only when the active sync slice includes the reference-dependent targets, then inject the derived map into `FoundationIndexSyncService`, `StandardIndexSyncService`, and `WorkflowIndexSyncService`.

### Data and Interface Impacts
- No control-plane schemas, indexes, or command payload shapes change.
- Three sync services gain an internal setter for precomputed reference-resolution data.
- Workflow loading gains an internal reusable context object that preserves the existing public loader behavior.

### Execution Flow
1. Build one fresh governed reference-index document when the validation or sync slice first needs reference-resolution data.
2. Derive `reference_urls_by_path` once and reuse it for workflow semantic loading or dependent sync services inside the same run.
3. Keep standalone service execution paths able to build their own reference-resolution data when no aggregate orchestrator injected one.
4. Prove the reuse behavior directly with build-count regressions and then rerun the full repository baseline.

### Invariants and Failure Cases
- Workflow semantics validation must still fail for real structural or link issues; only the redundant reference-resolution rebuilds should disappear.
- `sync all` must still emit the same reference, foundation, standard, and workflow index contents it emitted before the refactor.
- Coordination-only sync slices must not build unused reference-resolution state.
- Shared reference-resolution data must remain command-scoped; it must not silently persist across unrelated repo mutations.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/src/watchtower_core/repo_ops/sync/
- core/python/tests/

## Design Guardrails
- Keep the reference index as the canonical upstream-resolution source rather than introducing a second authority path.
- Keep the reuse seam internal to repo-local orchestration; do not expand it into a generic persistent caching framework.
- Prefer explicit injection or context reuse over implicit module-global state.

## Risks
- A poorly scoped reuse helper could accidentally cross command boundaries and go stale if it were treated as a persistent cache instead of one run-local snapshot.
- Sync orchestration changes could introduce subtle artifact drift if the shared reference-resolution map were wired to the wrong targets or built from stale documents.

## References
- [reference_resolution_reuse_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/reference_resolution_reuse_hardening.md)
- [reference_resolution_reuse_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/reference_resolution_reuse_hardening.md)
- [repository_validation_standard.md](/home/j/WatchTowerPlan/docs/standards/validations/repository_validation_standard.md)
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md)

## Updated At
- `2026-03-12T15:09:05Z`
