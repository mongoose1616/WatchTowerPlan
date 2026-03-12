---
trace_id: trace.control_plane_loader_cache_reuse
id: design.features.control_plane_loader_cache_reuse
title: Control Plane Loader Cache Reuse Feature Design
summary: Defines the technical design boundary for Control Plane Loader Cache Reuse.
type: feature_design
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

# Control Plane Loader Cache Reuse Feature Design

## Record Metadata
- `Trace ID`: `trace.control_plane_loader_cache_reuse`
- `Design ID`: `design.features.control_plane_loader_cache_reuse`
- `Design Status`: `active`
- `Linked PRDs`: `prd.control_plane_loader_cache_reuse`
- `Linked Decisions`: `decision.control_plane_loader_cache_reuse_direction`
- `Linked Implementation Plans`: `design.implementation.control_plane_loader_cache_reuse`
- `Updated At`: `2026-03-12T19:33:27Z`

## Summary
Defines the technical design boundary for Control Plane Loader Cache Reuse.

## Source Request
- Do a comprehensive project review for refactoring and potential optimizations without reducing capability, fidelity, or performance.

## Scope and Feature Boundary
- Add command-scoped cache layers inside `ControlPlaneLoader` for repeated validated-document
  and typed-artifact loads that are known to be stable within one command run.
- Cover single-document typed artifacts such as the validator registry and keep the design open
  to the same cache mechanism for other single-path artifact families.
- Exclude persistent cross-command caching, cross-process memoization, and any change to the
  public loader method names or return types.

## Current-State Context
- The loader already carries current-run override maps for validated documents and governed
  directories, so the right optimization boundary is the loader instance itself.
- Direct instrumentation of `ValidationAllService(ControlPlaneLoader()).run()` on the current
  repository state showed `load_validator_registry()` rematerializing the same registry `799`
  times in one command run.
- Follow-up review after the first cache change exposed one missing invariant: directory-backed
  artifact families rebuilt from filesystem directory iteration only, so a later
  document-level override inside a governed directory could leave cached directory views stale.
- `ValidationEvidenceRecorder.record()` reproduced that gap by writing new evidence and
  traceability artifacts while the same loader instance still returned the old evidence set when
  validation-evidence caches had already been primed.

## Foundations References Applied
- `docs/foundations/engineering_design_principles.md`: reuse should stay deterministic,
  local-first, and explicit about the machine-readable authority boundary.
- `docs/foundations/repository_standards_posture.md`: same-change validation fidelity matters
  more than opportunistic performance gains, so the cache must preserve fail-closed behavior.

## Internal Standards and Canonical References Applied
- `docs/standards/engineering/python_workspace_standard.md`: the optimization belongs in the
  canonical Python workspace and must keep runtime boundaries explicit.
- `docs/standards/governance/traceability_standard.md`: the change is non-trivial and must keep
  the planning, evidence, and closeout chain aligned.

## Design Goals and Constraints
- Reuse already-validated or already-materialized artifacts inside one loader-backed command.
- Keep override publication authoritative so newly generated documents displace stale cache
  entries immediately.
- Preserve the current loader API and every validation result emitted by existing services.

## Options Considered
### Option 1
- Add narrow ad hoc caches only to the validation services that currently show repeated loads.
- Smallest code change in the short term.
- Leaves the repeated-load concern fragmented across services and misses future loader-level
  reuse opportunities.

### Option 2
- Add command-scoped cache layers to `ControlPlaneLoader` with explicit invalidation when
  validated document or directory overrides are published.
- Centralizes reuse in the repository's canonical artifact-loading boundary.
- Requires careful cache invalidation so current-run override consumers never observe stale
  state.

## Recommended Design
### Architecture
- Keep `ControlPlaneLoader` as the command-scoped cache owner.
- Cache validated JSON documents by repository-relative path after successful schema validation.
- Cache typed single-document artifacts by repository-relative path after successful
  materialization.
- Cache typed directory-backed artifact tuples by repository-relative directory when applicable,
  and invalidate them when a document or directory override changes the underlying source set.
- Rebuild directory-backed artifact views from the merged current-run source set: filesystem
  documents plus any document-level overrides published beneath the same governed directory.

### Data and Interface Impacts
- No schema or CLI contract changes are expected.
- Loader internals gain cache state and explicit invalidation helpers.
- Tests should cover the hot-path reuse case, override invalidation behavior, and same-loader
  coherence for artifact writers that publish canonical outputs.

### Execution Flow
1. A loader method requests a validated document or typed artifact.
2. The loader returns the cached current-run object when the same path or directory has already
   been validated and no newer override has displaced it.
3. Override publication replaces the authoritative in-memory document and invalidates dependent
   typed or directory cache entries before later consumers load them.
4. When a directory-backed artifact family reloads after a document-level override, the loader
   merges direct-child document overrides into the rebuilt directory view before rematerializing
   typed artifacts.

### Invariants and Failure Cases
- Cached artifacts must always reflect the newest current-run override visible to the loader.
- A cache miss must still perform the same schema validation and typed construction as today's
  uncached path.
- If a caller publishes a new override beneath a governed directory, directory-backed cache
  entries must not survive with stale members, and rebuilt directory views must reflect the
  latest direct-child document overrides.

## Affected Surfaces
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/validation/
- core/python/tests/

## Design Guardrails
- Keep cache lifetime bounded to one `ControlPlaneLoader` instance.
- Do not introduce implicit global state, file mtime heuristics, or persistent on-disk caches.

## Risks
- Mutable cached documents could leak state if a caller mutates loader-returned artifacts in
  place; regression review must confirm current consumers treat them as read-only.

## References
- `docs/planning/prds/control_plane_loader_cache_reuse.md`
- `docs/planning/design/implementation/control_plane_loader_cache_reuse.md`
- `core/python/src/watchtower_core/control_plane/loader.py`
