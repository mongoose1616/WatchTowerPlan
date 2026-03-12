---
trace_id: trace.reference_resolution_reuse_hardening
id: design.implementation.reference_resolution_reuse_hardening
title: Reference Resolution Reuse Hardening Implementation Plan
summary: Breaks Reference Resolution Reuse Hardening into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-12T15:09:05Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/repo_ops/validation/
- core/python/src/watchtower_core/repo_ops/sync/
- core/python/tests/
---

# Reference Resolution Reuse Hardening Implementation Plan

## Record Metadata
- `Trace ID`: `trace.reference_resolution_reuse_hardening`
- `Plan ID`: `design.implementation.reference_resolution_reuse_hardening`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.reference_resolution_reuse_hardening`
- `Linked Decisions`: `decision.reference_resolution_reuse_hardening_direction`
- `Source Designs`: `design.features.reference_resolution_reuse_hardening`
- `Linked Acceptance Contracts`: `contract.acceptance.reference_resolution_reuse_hardening`
- `Updated At`: `2026-03-12T15:09:05Z`

## Summary
Breaks Reference Resolution Reuse Hardening into a bounded implementation slice.

## Source Request or Design
- Feature design: [reference_resolution_reuse_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/reference_resolution_reuse_hardening.md)
- Review request: Do a comprehensive project review for refactoring and potential optimizations without reducing capability, fidelity, or performance.

## Scope Summary
- Add one shared reference-resolution helper and workflow-document context reuse path.
- Wire `sync all` to reuse one shared reference-resolution snapshot for the reference-dependent index builders.
- Add direct build-count regressions plus the normal repository baseline validation.
- Do not change index schemas, command contracts, or repo-local workflow semantics rules.

## Assumptions and Constraints
- The reference index remains the canonical source for mapping governed reference documents to canonical upstream URLs.
- Aggregate orchestration can safely reuse one run-local reference-resolution snapshot because all affected targets examine the same current source state.
- Standalone family syncs and single-document validation calls must continue to work without requiring aggregate orchestration.

## Internal Standards and Canonical References Applied
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): the refactor should reduce duplicated work through explicit helpers and narrow injected state.
- [repository_validation_standard.md](/home/j/WatchTowerPlan/docs/standards/validations/repository_validation_standard.md): the implementation must prove both targeted reuse behavior and full baseline health.
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md): workflow-module loading must remain aligned with the derived workflow index contract.

## Proposed Technical Approach
- Add `repo_ops/reference_resolution.py` to build `reference_urls_by_path` from one fresh reference-index document.
- Extend workflow loading with a reusable `WorkflowDocumentContext` and make document-semantics validation cache that context for the life of the validation service instance.
- Extend the relevant sync services with explicit injection of precomputed reference-resolution data, and let `AllSyncService` build and reuse one shared reference-index document only when the active sync slice needs it.
- Preserve the existing fallback behavior for direct family syncs by letting each service build its own reference-resolution data when no aggregate injector provided one.

## Work Breakdown
1. Add the shared reference-resolution helper and the reusable workflow-document context.
2. Wire `DocumentSemanticsValidationService` and the reference-dependent sync services to reuse that shared data path.
3. Add direct build-count regressions for aggregate validation and sync orchestration.
4. Run targeted tests plus the full repository validation baseline, update evidence, and close the trace.

## Risks
- Shared reference-resolution plumbing could mask a real dependency-order issue if aggregate sync reused the wrong document state.
- The optimization could become a stale cache bug if the reuse scope were allowed to persist longer than a single command run.

## Validation Plan
- Run `./.venv/bin/pytest -q tests/unit/test_all_validation.py tests/unit/test_all_sync.py tests/unit/test_document_semantics_validation.py tests/unit/test_workflow_index_sync.py`.
- Run direct instrumentation checks to confirm `document_semantics_reference_index_builds=1` and `sync_all_reference_index_builds=1`.
- Run `./.venv/bin/python -m mypy src/watchtower_core`.
- Run `./.venv/bin/ruff check .`.
- Run `./.venv/bin/watchtower-core sync all --write --format json`.
- Run `./.venv/bin/watchtower-core validate acceptance --trace-id trace.reference_resolution_reuse_hardening --format json`.
- Run `./.venv/bin/watchtower-core validate all --format json`.
- Run `./.venv/bin/pytest -q`.

## References
- [reference_resolution_reuse_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/reference_resolution_reuse_hardening.md)
- [reference_resolution_reuse_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/reference_resolution_reuse_hardening.md)
- [reference_resolution_reuse_hardening_acceptance.v1.json](/home/j/WatchTowerPlan/core/control_plane/contracts/acceptance/reference_resolution_reuse_hardening_acceptance.v1.json)

## Updated At
- `2026-03-12T15:09:05Z`
