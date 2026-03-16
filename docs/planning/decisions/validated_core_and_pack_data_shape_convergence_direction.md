---
trace_id: trace.validated_core_pack_data_shape_convergence
id: decision.validated_core_pack_data_shape_convergence_direction
title: Validated Core and Pack Data Shape Convergence Direction Decision
summary: Records the initial direction decision for Validated Core and Pack Data Shape
  Convergence.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-16T04:32:27Z'
audience: shared
authority: supporting
---

# Validated Core and Pack Data Shape Convergence Direction Decision

## Record Metadata
- `Trace ID`: `trace.validated_core_pack_data_shape_convergence`
- `Decision ID`: `decision.validated_core_pack_data_shape_convergence_direction`
- `Record Status`: `active`
- `Decision Status`: `proposed`
- `Linked PRDs`: `prd.validated_core_pack_data_shape_convergence`
- `Linked Designs`: `design.features.validated_core_pack_data_shape_convergence`
- `Linked Implementation Plans`: `design.implementation.validated_core_pack_data_shape_convergence`
- `Updated At`: `2026-03-16T04:32:27Z`

## Summary
Records the initial direction decision for Validated Core and Pack Data Shape Convergence.

## Decision Statement
Adopt a contract-first migration where shared core becomes pack-ready by loading a validated pack-runtime manifest before wider repo-local data families move to the future pack standard.

## Trigger or Source Request
- Review STEP1_FINAL and convert the current repo data shape toward that pack-ready standard.

## Current Context and Constraints
- Generic pack-facing schemas already exist in `core/control_plane`, but startup, loader, and typed-model surfaces still bias toward the current repository shape.
- The repository must stay green while the boundary moves, so a one-shot replacement of planning, query, sync, and validation data families is too risky.

## Applied References and Implications
- `STEP1_FINAL`: Shared core should load pack-declared contracts, provide generic validation/query/sync machinery, and leave pack semantics and environment behavior outside core.
- `docs/planning/design/features/core_export_ready_architecture.md`: The current architecture already points toward injected workspace and artifact interfaces plus repo-local orchestration boundaries.

## Affected Surfaces
- `docs/planning/prds/validated_core_and_pack_data_shape_convergence.md`
- `docs/planning/design/features/validated_core_and_pack_data_shape_convergence.md`
- `docs/planning/design/implementation/validated_core_and_pack_data_shape_convergence.md`
- `core/control_plane/manifests/`
- `core/control_plane/schemas/artifacts/`
- `core/python/src/watchtower_core/control_plane/`

## Options Considered
### Option 1
- Perform a large direct migration from current planning-heavy data shapes to the full future pack model in one trace slice.
- Minimizes the number of transition artifacts.
- Forces startup, loader, validator, query, and index changes to move together with too much regression risk.

### Option 2
- Land a validated startup contract first, then move typed models, queries, and data families behind that boundary in later slices.
- Creates a reusable core boundary that can serve a future pack without blocking the current repository.
- Requires an additional transition phase where both old repo-specific surfaces and the new startup contract coexist.

## Chosen Outcome
Option 2. The repository will first publish and consume a validated pack-runtime manifest, then use that contract to drive later extraction of pack-facing models, generic query surfaces, and data-family alignment.

## Rationale and Tradeoffs
- The startup contract is the smallest change that makes the reusable core meaningfully pack-aware.
- It keeps pack-specific semantics, environment adapters, and repo-local orchestration in the pack layer where `STEP1_FINAL` says they belong.

## Consequences and Follow-Up Impacts
- Shared core gains a first-class runtime-boundary artifact and typed API.
- Follow-on tasks must reduce planning-specific typed exports and named loader methods in favor of pack-facing models and generic family-driven loaders.
- Future data-shape conversion can proceed incrementally because the startup boundary becomes explicit.

## Risks, Dependencies, and Assumptions
- Assumes the repository remains the first pack-shaped consumer during the transition and that future external packs can bind to the same contract family.
- Risks leaving the migration half-finished if follow-on tasks do not move the remaining planning-specific data surfaces.

## References
- /home/j/mvp_reference/STEP1_FINAL.md
