---
trace_id: trace.validated_core_pack_data_shape_convergence
id: design.implementation.validated_core_pack_data_shape_convergence
title: Validated Core and Pack Data Shape Convergence Implementation Plan
summary: Breaks Validated Core and Pack Data Shape Convergence into a bounded implementation
  slice.
type: implementation_plan
status: draft
owner: repository_maintainer
updated_at: '2026-03-16T04:32:27Z'
audience: shared
authority: supporting
---

# Validated Core and Pack Data Shape Convergence Implementation Plan

## Record Metadata
- `Trace ID`: `trace.validated_core_pack_data_shape_convergence`
- `Plan ID`: `design.implementation.validated_core_pack_data_shape_convergence`
- `Plan Status`: `draft`
- `Linked PRDs`: `prd.validated_core_pack_data_shape_convergence`
- `Linked Decisions`: `decision.validated_core_pack_data_shape_convergence_direction`
- `Source Designs`: `design.features.validated_core_pack_data_shape_convergence`
- `Linked Acceptance Contracts`: `None`
- `Updated At`: `2026-03-16T04:32:27Z`

## Summary
Breaks Validated Core and Pack Data Shape Convergence into a bounded implementation slice.

## Source Request or Design
- Review STEP1_FINAL and convert the current repo data shape toward that pack-ready standard.

## Scope Summary
- This plan covers the first migration slice: publish the pack-runtime manifest contract, load it as a typed governed artifact, and let workspace resolution consume manifest-declared logical prefixes.
- This plan intentionally excludes full pack-interface typed models, generic query surfaces over every future pack artifact family, and repo-local data-family replacement work.

## Assumptions and Constraints
- Current repository behavior must stay green while new contract surfaces land.
- The pack-runtime manifest is a startup declaration and migration guide, not a complete replacement for existing registries or indexes in this slice.

## Internal Standards and Canonical References Applied
- `core/control_plane/README.md`: New machine-readable startup authority belongs under `core/control_plane` and must remain versioned and governed.
- `core/python/README.md`: Python runtime contract changes must stay aligned with workspace guidance and programmatic-use documentation.

## Proposed Technical Approach
- Add a new `pack_runtime_manifest` schema and canonical manifest artifact that describe the runtime roots, supported future artifact families, derived index surfaces, and allowed extension points.
- Add a typed runtime-manifest model plus a loader entrypoint in `watchtower_core.control_plane`.
- Extend `WorkspaceConfig` with manifest-driven logical prefix support while preserving current default behavior for existing callers.
- Leave repo-local `repo_ops` behavior intact and treat this slice as the validated startup contract for later migration phases.

## Work Breakdown
1. Publish the new schema, manifest artifact, and schema-catalog updates under `core/control_plane`.
2. Implement typed Python models, loader access, workspace support, and regression tests for manifest-driven logical prefixes.
3. Replace scaffold planning text with the concrete migration design and open the next execution tasks for pack-interface and data-family convergence.

## Risks
- A partially landed runtime contract could drift from code unless validation and tests cover the new manifest path immediately.

## Validation Plan
- Run targeted unit tests for workspace injection, control-plane loader behavior, and schema-store validation.
- Run `watchtower-core sync all --write --format json` and `watchtower-core validate all --format json` after the slice lands.
- Confirm coordination reflects the new active initiative and follow-on tasks instead of leaving the repo at a bootstrap-only planning state.

## References
- /home/j/mvp_reference/STEP1_FINAL.md
