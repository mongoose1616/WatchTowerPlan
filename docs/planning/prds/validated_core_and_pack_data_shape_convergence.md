---
trace_id: trace.validated_core_pack_data_shape_convergence
id: prd.validated_core_pack_data_shape_convergence
title: Validated Core and Pack Data Shape Convergence PRD
summary: Converges the repository data model toward a validated reusable core plus
  plan-domain-pack artifact shape aligned with the future pack standard.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-16T05:47:10Z'
audience: shared
authority: authoritative
---

# Validated Core and Pack Data Shape Convergence PRD

## Record Metadata
- `Trace ID`: `trace.validated_core_pack_data_shape_convergence`
- `PRD ID`: `prd.validated_core_pack_data_shape_convergence`
- `Status`: `active`
- `Linked Decisions`: `decision.validated_core_pack_data_shape_convergence_direction`
- `Linked Designs`: `design.features.validated_core_pack_data_shape_convergence`
- `Linked Implementation Plans`: `design.implementation.validated_core_pack_data_shape_convergence`
- `Updated At`: `2026-03-16T05:47:10Z`

## Summary
Converges the repository data model toward a validated reusable core plus plan-domain-pack artifact shape aligned with the future pack standard.

## Problem Statement
- `STEP1_FINAL` points toward a pack-shaped runtime where shared core loads pack-declared schemas, registries, and index surfaces instead of embedding repository-specific assumptions.
- WatchTowerPlan can be treated as the first plan and implementation domain pack that consumes that reusable core, but the Python helper and harness still default to repository-local planning families and legacy control-plane shapes.
- Without an explicit pack-settings load root and domain-fit registry or index surfaces, later migration of artifact families, registries, and indexes will stay tightly coupled to the current repository shape.
- The current repository also mixes reusable-core load-root data with repo-local planning projections, evidence ledgers, and schema example fixtures. Without an explicit classification boundary, those families look more canonical to shared core than they actually are and create maintenance drag.

## Goals
- Publish a validated pack-settings contract that describes the repository as a plan and implementation domain pack consuming shared core.
- Make reusable loader startup surfaces consume that contract instead of depending only on hardcoded repository-specific assumptions.
- Flatten and simplify retained registry surfaces so core can load a smaller canonical control-plane shape.
- Explicitly classify current machine-readable families as pack source artifacts, retained reusable-core governance surfaces, derived pack projections, or transitional fixtures so follow-on cleanup does not rely on compatibility shims.
- Preserve the current repository behavior while opening a controlled path toward pack-owned artifact families and derived index surfaces.

## Non-Goals
- Deliver a complete external pack implementation in this trace.
- Migrate every current planning index, ledger, and document family to generic pack artifacts in one slice.
- Remove every legacy evidence or example surface in the same trace that establishes the new pack-ready contract boundary.
- Move environment adapters or other pack-specific execution semantics into shared core.

## Requirements
- `req.validated_core_pack_data_shape_convergence.001`: A machine-readable `pack_settings` load root plus supporting registries must declare the governed surfaces that shared core may rely on for a plan and implementation domain pack.
- `req.validated_core_pack_data_shape_convergence.002`: `watchtower_core.control_plane` must expose that pack-settings contract through validated typed surfaces without relying on the retired runtime-manifest bridge.
- `req.validated_core_pack_data_shape_convergence.003`: The migration must preserve the current repository's query, sync, validation, and planning behavior while explicitly classifying surviving machine-readable families as reusable-core load-root surfaces, pack-local derived projections, or transitional fixtures.
- `req.validated_core_pack_data_shape_convergence.004`: Follow-on slices must keep plan-domain semantics, workflows, and environment adapters outside shared core even when generic helpers move inward.

## Acceptance Criteria
- `ac.validated_core_pack_data_shape_convergence.001`: The planning chain describes WatchTowerPlan as a plan and implementation domain pack consuming reusable core through a pack-settings load root and simplified governed surfaces.
- `ac.validated_core_pack_data_shape_convergence.002`: `pack_settings.json`, the supporting flat registry files, and their schemas validate cleanly, while the runtime-manifest and policy bridges are removed from the canonical control-plane shape.
- `ac.validated_core_pack_data_shape_convergence.003`: Shared core loads the pack-settings contract and retained governed surfaces through typed loader APIs, current planning indexes remain explicit repo-local derived pack projections, and the retired prototype pack interfaces are no longer published as active core contracts.

## Risks and Dependencies
- Over-generalizing the runtime contract before a second concrete pack exists could create abstractions that do not pay for themselves.
- The current repository still exposes planning-specific typed models and named loader methods, so additional slices are required before shared core is truly pack-agnostic.
- This trace depends on keeping the current validation and sync surfaces green while adding new contract artifacts and startup logic.

## References
- /home/j/mvp_reference/STEP1_FINAL.md
- docs/planning/design/features/core_export_ready_architecture.md
