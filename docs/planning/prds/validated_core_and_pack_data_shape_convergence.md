---
trace_id: trace.validated_core_pack_data_shape_convergence
id: prd.validated_core_pack_data_shape_convergence
title: Validated Core and Pack Data Shape Convergence PRD
summary: Converges the repository data model toward a validated reusable core plus
  pack-owned artifact shape aligned with the future pack standard.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-16T04:32:27Z'
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
- `Updated At`: `2026-03-16T04:32:27Z`

## Summary
Converges the repository data model toward a validated reusable core plus pack-owned artifact shape aligned with the future pack standard.

## Problem Statement
- `STEP1_FINAL` targets a pack-shaped runtime where shared core loads pack-declared schemas, registries, and index surfaces instead of embedding repository-specific assumptions.
- The current repository already publishes several generic pack-facing schemas, but the Python helper and harness still default to WatchTowerPlan-specific workspace roots, planning-family loader methods, and planning-heavy typed exports.
- Without an explicit startup contract for the core-to-pack boundary, later migration of artifact families, registries, and indexes will stay tightly coupled to the current repository shape.

## Goals
- Publish a validated runtime contract that describes the repository as a pack-shaped consumer of shared core.
- Make reusable workspace and loader startup surfaces consume that runtime contract instead of depending only on hardcoded `core/control_plane` and `core/python` assumptions.
- Preserve the current repository behavior while opening a controlled path toward pack-owned artifact families and derived index surfaces.

## Non-Goals
- Deliver a complete external pack implementation in this trace.
- Migrate every current planning index, ledger, and document family to generic pack artifacts in one slice.
- Move environment adapters or other pack-specific execution semantics into shared core.

## Requirements
- `req.validated_core_pack_data_shape_convergence.001`: A machine-readable pack-runtime contract must declare the startup workspace roots, governed roots, supported artifact families, derived index surfaces, and extension points that shared core may rely on.
- `req.validated_core_pack_data_shape_convergence.002`: `watchtower_core.control_plane` must expose the pack-runtime contract as a validated typed surface and allow workspace resolution to consume declared logical prefixes from that contract.
- `req.validated_core_pack_data_shape_convergence.003`: The migration must preserve the current repository's query, sync, validation, and planning behavior while the reusable-core boundary moves.
- `req.validated_core_pack_data_shape_convergence.004`: Follow-on slices must keep pack-specific semantics, workflows, and environment adapters outside shared core even when generic helpers move inward.

## Acceptance Criteria
- `ac.validated_core_pack_data_shape_convergence.001`: A governed `pack_runtime_manifest` schema and canonical manifest artifact exist, validate cleanly, and are cataloged under `core/control_plane`.
- `ac.validated_core_pack_data_shape_convergence.002`: `ControlPlaneLoader` and `WorkspaceConfig` can load and consume the runtime manifest boundary, including non-default logical workspace prefixes, with regression coverage.
- `ac.validated_core_pack_data_shape_convergence.003`: The planning chain and task set describe the contract-first migration path for later pack interface, registry, and data-family convergence without reopening repository-local semantics inside shared core.

## Risks and Dependencies
- Over-generalizing the runtime contract before a second concrete pack exists could create abstractions that do not pay for themselves.
- The current repository still exposes planning-specific typed models and named loader methods, so additional slices are required before shared core is truly pack-agnostic.
- This trace depends on keeping the current validation and sync surfaces green while adding new contract artifacts and startup logic.

## References
- /home/j/mvp_reference/STEP1_FINAL.md
- docs/planning/design/features/core_export_ready_architecture.md
