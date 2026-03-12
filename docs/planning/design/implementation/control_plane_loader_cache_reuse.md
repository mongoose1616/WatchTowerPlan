---
trace_id: trace.control_plane_loader_cache_reuse
id: design.implementation.control_plane_loader_cache_reuse
title: Control Plane Loader Cache Reuse Implementation Plan
summary: Breaks Control Plane Loader Cache Reuse into a bounded implementation slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-12T19:33:27Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/validation/
- core/python/tests/
---

# Control Plane Loader Cache Reuse Implementation Plan

## Record Metadata
- `Trace ID`: `trace.control_plane_loader_cache_reuse`
- `Plan ID`: `design.implementation.control_plane_loader_cache_reuse`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.control_plane_loader_cache_reuse`
- `Linked Decisions`: `decision.control_plane_loader_cache_reuse_direction`
- `Source Designs`: `design.features.control_plane_loader_cache_reuse`
- `Linked Acceptance Contracts`: `contract.acceptance.control_plane_loader_cache_reuse`
- `Updated At`: `2026-03-12T19:33:27Z`

## Summary
Breaks Control Plane Loader Cache Reuse into a bounded implementation slice.

## Source Request or Design
- Do a comprehensive project review for refactoring and potential optimizations without reducing capability, fidelity, or performance.

## Scope Summary
- Add command-scoped validated-document and typed-artifact cache paths to
  `ControlPlaneLoader`.
- Add targeted regression coverage and measurement coverage for validator-registry reuse and
  override invalidation.
- Keep same-loader artifact writers coherent by republishing canonical writes into loader state
  and making directory-backed reloads reflect document-level overrides.
- Exclude unrelated validation-family restructures or broader sync orchestration changes.

## Assumptions and Constraints
- The loader instance remains the unit of command-scoped reuse and does not outlive one command
  run.
- Existing loader consumers continue to treat returned artifacts as read-only current-run data.

## Internal Standards and Canonical References Applied
- `docs/standards/engineering/python_workspace_standard.md`: implementation and regression
  coverage stay inside `core/python/`.
- `docs/standards/governance/task_tracking_standard.md`: non-trivial implementation and
  validation closeout work must be tracked explicitly.
- `docs/standards/governance/traceability_standard.md`: code, planning, acceptance, and
  evidence surfaces must close together.

## Proposed Technical Approach
- Add internal cache dictionaries to `ControlPlaneLoader` for validated documents, directory
  document tuples, typed single-document artifacts, and typed directory-backed artifact tuples.
- Route single-document loader methods through one shared helper that caches typed artifacts by
  canonical path while preserving the existing public methods.
- Invalidate affected cache entries when `set_validated_document_override` or
  `set_validated_directory_override` publishes new current-run state.
- Rebuild directory-backed loads from filesystem documents plus direct-child document overrides
  so one overridden document can refresh a cached governed directory without requiring a full
  directory override publication.
- Publish canonical validation-evidence and traceability writes back into the loader when
  `ValidationEvidenceRecorder.record()` writes to repo-logical destinations.
- Cover the cache boundary with targeted unit tests and prove the measured validator-registry
  hotspot drops from `799` rematerializations to `1`.

## Work Breakdown
1. Update the planning chain, decision direction, acceptance contract, and task set for the
   measured loader-cache optimization boundary.
2. Implement override-aware loader caches and add regression coverage for repeated validator
   registry reuse plus document-and-directory override invalidation.
3. Close the follow-up same-loader coherence gap for `ValidationEvidenceRecorder.record()`.
4. Run targeted measurements, the full validation baseline, a follow-up loader/validation
   review, and then close the initiative cleanly.

## Risks
- Over-invalidation would blunt the performance gain; under-invalidation would serve stale
  artifacts and be unacceptable.

## Validation Plan
- Instrument `ValidationAllService(ControlPlaneLoader()).run()` before and after the change to
  measure validator-registry rematerialization counts.
- Add targeted unit tests for loader cache reuse, directory-backed override invalidation, and
  same-loader validation-evidence coherence.
- Run `watchtower-core sync all --write --format json`,
  `watchtower-core validate acceptance --trace-id trace.control_plane_loader_cache_reuse --format json`,
  `watchtower-core validate all --format json`, `pytest -q`,
  `python -m mypy src/watchtower_core`, and `ruff check .`.
- Perform a follow-up review of adjacent loader, validation, and sync surfaces and record
  whether any additional issue remains.

## References
- `docs/planning/prds/control_plane_loader_cache_reuse.md`
- `core/control_plane/contracts/acceptance/control_plane_loader_cache_reuse_acceptance.v1.json`
