---
trace_id: trace.validated_core_pack_data_shape_convergence
id: design.implementation.validated_core_pack_data_shape_convergence
title: Validated Core and Pack Data Shape Convergence Implementation Plan
summary: Breaks Validated Core and Pack Data Shape Convergence into a bounded implementation
  slice.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-16T05:47:10Z'
audience: shared
authority: supporting
---

# Validated Core and Pack Data Shape Convergence Implementation Plan

## Record Metadata
- `Trace ID`: `trace.validated_core_pack_data_shape_convergence`
- `Plan ID`: `design.implementation.validated_core_pack_data_shape_convergence`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.validated_core_pack_data_shape_convergence`
- `Linked Decisions`: `decision.validated_core_pack_data_shape_convergence_direction`
- `Source Designs`: `design.features.validated_core_pack_data_shape_convergence`
- `Linked Acceptance Contracts`: `None`
- `Updated At`: `2026-03-16T05:47:10Z`

## Summary
Breaks Validated Core and Pack Data Shape Convergence into a bounded implementation slice.

## Source Request or Design
- Review STEP1_FINAL and convert the current repo data shape toward that pack-ready standard.

## Scope Summary
- This plan covers the contract-cutover slices that make reusable core consume `pack_settings` plus simplified registries while retiring the runtime-manifest and policy bridges.
- This plan also covers explicit classification of the current repository's machine-readable families so planning indexes stay repo-local pack projections and example or ledger families stop looking like reusable-core startup inputs.
- This plan intentionally excludes full generic query surfaces over every future pack artifact family and excludes repo-local planning data-family replacement work beyond the bounded convergence changes in this trace.

## Assumptions and Constraints
- Current repository behavior must stay green while new contract surfaces land.
- `pack_settings` is the load root for this trace, while schema catalog, validator registry, and retained flat registries stay authoritative for their own families.
- Current examples and ledgers may remain in place temporarily, but they must be demoted from the active startup contract so later cleanup can delete or replace them cleanly.

## Internal Standards and Canonical References Applied
- `core/control_plane/README.md`: New machine-readable startup authority belongs under `core/control_plane` and must remain versioned and governed.
- `core/python/README.md`: Python runtime contract changes must stay aligned with workspace guidance and programmatic-use documentation.

## Proposed Technical Approach
- Use `pack_settings.json` plus retained registries as the canonical load root for reusable core.
- Flatten the registry layout to single root files and remove obsolete policy and prototype interface families instead of preserving them as compatibility layers.
- Keep direct `WorkspaceConfig` construction for non-default layouts while removing the runtime-manifest-specific helper path.
- Leave repo-local `repo_ops` behavior intact and treat this slice as the validated contract cutover for later migration phases.
- Publish the current-to-future family mapping in the planning chain so future cleanup can delete legacy surfaces instead of wrapping them.

## Surface Alignment Map
| Family | Treatment In This Trace |
|---|---|
| `pack_settings` and retained flat registries | Canonical reusable-core startup boundary. |
| `PackContext` typed loader surfaces | Shared core consumption path for the canonical startup boundary. |
| Planning indexes and coordination trackers | Retained repo-local pack projections derived from planning docs. |
| Schema examples and evidence or migration ledgers | Transitional support surfaces outside the startup contract. |
| Runtime-manifest, policy, and prototype pack interfaces | Removed outright. |

## Work Breakdown
1. Publish `pack_settings`, supporting registries, and schema-catalog updates under `core/control_plane`.
2. Remove runtime-manifest, policy, and retired prototype-interface contracts from the canonical control-plane shape.
3. Implement typed loader access, PackContext support, documentation updates, and regression coverage for the simplified boundary.
4. Reclassify current planning indexes, examples, and ledgers in the planning chain so they are treated as pack-local projections or transitional support surfaces rather than reusable-core startup contracts.

## Risks
- A partially landed contract cutover could drift from code unless validation and tests cover the simplified load root and removed surfaces immediately.

## Validation Plan
- Run targeted unit tests for workspace injection, control-plane loader behavior, and schema-store validation.
- Run `watchtower-core sync all --write --format json` and `watchtower-core validate all --format json` after the slice lands.
- Confirm coordination reflects the new active initiative and follow-on tasks instead of leaving the repo at a bootstrap-only planning state.

## References
- /home/j/mvp_reference/STEP1_FINAL.md
