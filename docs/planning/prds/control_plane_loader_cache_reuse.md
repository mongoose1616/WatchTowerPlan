---
trace_id: trace.control_plane_loader_cache_reuse
id: prd.control_plane_loader_cache_reuse
title: Control Plane Loader Cache Reuse PRD
summary: Eliminate repeated command-scoped rematerialization of stable governed artifacts,
  starting with the validator-registry hotspot in validate all, by adding override-aware
  loader caches without weakening validation fidelity or current-run override semantics.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-12T19:33:27Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/validation/
- core/python/tests/
---

# Control Plane Loader Cache Reuse PRD

## Record Metadata
- `Trace ID`: `trace.control_plane_loader_cache_reuse`
- `PRD ID`: `prd.control_plane_loader_cache_reuse`
- `Status`: `active`
- `Linked Decisions`: `decision.control_plane_loader_cache_reuse_direction`
- `Linked Designs`: `design.features.control_plane_loader_cache_reuse`
- `Linked Implementation Plans`: `design.implementation.control_plane_loader_cache_reuse`
- `Updated At`: `2026-03-12T19:33:27Z`

## Summary
Eliminate repeated command-scoped rematerialization of stable governed artifacts, starting with the validator-registry hotspot in validate all, by adding override-aware loader caches without weakening validation fidelity or current-run override semantics.

## Problem Statement
The repository's command-scoped `ControlPlaneLoader` does not cache typed single-document
artifacts or validated JSON documents. During the current comprehensive optimization review,
direct instrumentation of `ValidationAllService(ControlPlaneLoader()).run()` showed one clean
repository validation run rematerializing the same validator registry document `799` times
through the same loader instance. That repeated rematerialization adds avoidable JSON loading,
schema validation, and typed model construction cost to a core validation path that already
operates across hundreds of governed targets.

The optimization boundary is not "add a global cache." The repository already depends on
current-run validated overrides during sync and validation flows, so any reuse must stay
command-scoped, remain override-aware, and preserve fail-closed semantics whenever a new
current-run document is published.

The stop-condition follow-up review surfaced one additional correctness gap after the initial
cache change landed. `set_validated_document_override()` invalidated typed single-document
caches, but directory-backed artifact families still rebuilt from filesystem-only directory
iteration and could retain stale cached parent-directory state. That left
`ValidationEvidenceRecorder.record()` able to write new canonical evidence and traceability
artifacts while the same loader instance still returned the old validation-evidence and
traceability view if those caches had been primed earlier in the command.

## Goals
- Reduce repeated rematerialization of stable governed artifacts inside one loader-backed
  command run.
- Eliminate the measured validator-registry hotspot in `watchtower-core validate all` without
  changing validation results.
- Keep current-run override publication authoritative by invalidating stale cache entries when
  documents or directories are replaced during the same command.

## Non-Goals
- Introduce any persistent cache across commands, processes, or repository states.
- Weaken schema validation, typed model construction, or fail-closed behavior for newly
  published current-run artifacts.
- Redesign validation-family orchestration beyond the cache boundary needed for safe reuse.

## Requirements
- `req.control_plane_loader_cache_reuse.001`: `ControlPlaneLoader` must reuse stable
  command-scoped validated documents and typed artifact instances for repeated single-document
  loads without changing the existing public loader API.
- `req.control_plane_loader_cache_reuse.002`: Loader caches must invalidate or replace stale
  entries when `set_validated_document_override` or `set_validated_directory_override`
  publishes new current-run artifacts, including parent directory caches and directory-backed
  typed artifact tuples.
- `req.control_plane_loader_cache_reuse.003`: Validation behavior and fail-closed semantics
  must stay unchanged for `validate all`, direct validation-family calls, and current-run
  override consumers such as `ValidationEvidenceRecorder`.
- `req.control_plane_loader_cache_reuse.004`: The change must be covered by regression tests,
  measured against the current validator-registry hotspot, and closed with a full repository
  validation baseline plus a clean follow-up review of adjacent loader and validation surfaces.

## Acceptance Criteria
- `ac.control_plane_loader_cache_reuse.001`: The trace publishes a fully-authored planning
  chain, accepted direction decision, refreshed acceptance contract, refreshed evidence
  artifact, and a bounded closed task set for the loader-cache slice.
- `ac.control_plane_loader_cache_reuse.002`: Aggregate repository validation reuses one
  command-scoped validator registry materialization instead of rematerializing it hundreds of
  times through the same loader instance.
- `ac.control_plane_loader_cache_reuse.003`: Current-run override publication invalidates or
  refreshes affected loader cache entries so single-document and directory-backed sync and
  validation flows still consume the latest in-memory artifacts.
- `ac.control_plane_loader_cache_reuse.004`: The repository stays green on sync, acceptance
  validation, full validation, tests, mypy, and ruff after the cache change lands.
- `ac.control_plane_loader_cache_reuse.005`: A follow-up review of adjacent loader,
  validation, and sync surfaces finds no additional actionable issues in the touched area.

## Risks and Dependencies
- Loader cache invalidation could silently serve stale typed artifacts if override publication
  does not clear affected entries precisely.
- Returning cached documents and typed artifacts assumes current loader consumers treat them as
  read-only current-run state, which must remain true after the change.
- The optimization depends on preserving the existing command-scoped loader lifetime rather than
  introducing long-lived shared state.

## References
- `core/python/src/watchtower_core/control_plane/loader.py`
- `core/python/src/watchtower_core/repo_ops/validation/all.py`
- `core/python/src/watchtower_core/validation/front_matter.py`
- `core/python/src/watchtower_core/validation/artifact.py`
- `core/python/src/watchtower_core/repo_ops/validation/document_semantics.py`
- `SUMMARY.md`
