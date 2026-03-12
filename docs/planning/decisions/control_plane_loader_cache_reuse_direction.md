---
trace_id: trace.control_plane_loader_cache_reuse
id: decision.control_plane_loader_cache_reuse_direction
title: Control Plane Loader Cache Reuse Direction Decision
summary: Adopt command-scoped, override-aware loader caches instead of adding ad hoc reuse only inside validation services.
type: decision_record
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

# Control Plane Loader Cache Reuse Direction Decision

## Record Metadata
- `Trace ID`: `trace.control_plane_loader_cache_reuse`
- `Decision ID`: `decision.control_plane_loader_cache_reuse_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.control_plane_loader_cache_reuse`
- `Linked Designs`: `design.features.control_plane_loader_cache_reuse`
- `Linked Implementation Plans`: `design.implementation.control_plane_loader_cache_reuse`
- `Updated At`: `2026-03-12T19:33:27Z`

## Summary
Adopt command-scoped, override-aware loader caches instead of adding ad hoc reuse only inside validation services.

## Decision Statement
`ControlPlaneLoader` will own command-scoped validated-document and typed-artifact caches with
explicit invalidation and directory-view rebuilds on override publication, rather than adding
one-off reuse only inside the services that currently exhibit repeated loads.

## Trigger or Source Request
- Do a comprehensive project review for refactoring and potential optimizations without reducing capability, fidelity, or performance.

## Current Context and Constraints
- The loader already owns current-run validated-document and directory overrides, so it is the
  natural place to preserve coherent command-scoped reuse semantics.
- Current measurement shows `ValidationAllService(ControlPlaneLoader()).run()` rematerializing
  the validator registry `799` times in one clean run.
- Follow-up review after the first cache change showed that document-level overrides beneath a
  governed directory were not reflected when that directory rebuilt typed artifact views.

## Applied References and Implications
- `docs/foundations/engineering_design_principles.md`: favors deterministic local-first reuse
  over opaque global caching.
- `docs/foundations/repository_standards_posture.md`: performance work must preserve same-change
  validation fidelity and current-run authority surfaces.
- `docs/standards/governance/traceability_standard.md`: the optimization must close with
  planning, evidence, and validation state aligned.

## Affected Surfaces
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/validation/
- core/python/tests/

## Options Considered
### Option 1
- Add local caches only inside the validation services that currently call
  `load_validator_registry()` repeatedly.
- Minimal initial change surface.
- Pushes a loader concern into higher-level orchestration code and leaves future repeated-load
  cases to be rediscovered one service at a time.

### Option 2
- Add command-scoped caches inside `ControlPlaneLoader` for validated documents and typed
  artifacts, with override invalidation and directory-backed rebuilds that merge direct-child
  document overrides.
- Keeps reuse at the canonical artifact-loading boundary and helps future consumers without
  changing their interfaces.
- Requires careful invalidation and regression coverage to prove current-run override fidelity.

## Chosen Outcome
Adopt Option 2. The loader will cache current-run validated documents and typed artifact
materializations by canonical path or directory, invalidate affected cache entries when a new
override is published, and rebuild directory-backed views from the merged current-run source set
instead of filesystem-only directory reads.

## Rationale and Tradeoffs
- The repeated-load concern originates at the shared loader boundary, not in one specific
  validation family.
- A command-scoped cache keeps the optimization local, deterministic, and aligned with the
  loader's existing override semantics.
- The main tradeoff is cache invalidation complexity, which is acceptable if covered by direct
  tests and a full repository validation baseline.

## Consequences and Follow-Up Impacts
- Loader internals will grow modestly to track validated-document and typed-artifact cache state.
- Current validation and sync behavior must be retested against override publication,
  directory-backed reloads, writer coherence, and repository-wide validation flows.

## Risks, Dependencies, and Assumptions
- The design assumes loader consumers do not mutate cached artifacts in place.
- Any stale-cache defect would be correctness-impacting, so validation and follow-up review are
  mandatory closeout steps.

## References
- `docs/planning/prds/control_plane_loader_cache_reuse.md`
- `docs/planning/design/features/control_plane_loader_cache_reuse.md`
- `core/python/src/watchtower_core/control_plane/loader.py`
