---
trace_id: trace.rendered_surface_contract_enforcement
id: design.features.rendered_surface_contract_enforcement
title: Rendered Surface Contract Enforcement Feature Design
summary: Defines the technical design for governed rendered-surface contracts, generic tracker rendering, and active terminology enforcement.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-16T17:34:52Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/
- core/control_plane/
- docs/standards/
- docs/planning/
---

# Rendered Surface Contract Enforcement Feature Design

## Record Metadata
- `Trace ID`: `trace.rendered_surface_contract_enforcement`
- `Design ID`: `design.features.rendered_surface_contract_enforcement`
- `Design Status`: `active`
- `Linked PRDs`: `prd.rendered_surface_contract_enforcement`
- `Linked Decisions`: `decision.rendered_surface_contract_enforcement_direction`
- `Linked Implementation Plans`: `design.implementation.rendered_surface_contract_enforcement`
- `Updated At`: `2026-03-16T17:34:52Z`

## Summary
Defines the technical design for governed rendered-surface contracts, generic tracker rendering, and active terminology enforcement.

## Source Request
- User request to replace projection phrasing with rendered surface terminology and move derived Markdown rendering to a schema-driven style.

## Scope and Feature Boundary
- Covers the derived Markdown tracker family under `repo_ops/sync` where the authoritative content already lives in indexes or task records.
- Covers the active query, sync, and serialization helpers that still use `projection` terminology for live derived outputs.
- Covers the control-plane contract surfaces needed to publish a reusable rendered-surface registry and validate it fail-closed.
- Covers current standards, command docs, and planning entrypoint guidance that must describe the new rendered boundary consistently.
- Does not rewrite retained historical trace packages, purge-ledger history, or archived task documents purely to change wording.
- Does not move machine authority out of indexes, contracts, registries, or task records into rendered Markdown.

## Current-State Context
- [coordination_tracking.py](/core/python/src/watchtower_core/repo_ops/sync/coordination_tracking.py), [initiative_tracking.py](/core/python/src/watchtower_core/repo_ops/sync/initiative_tracking.py), [task_tracking.py](/core/python/src/watchtower_core/repo_ops/sync/task_tracking.py), [prd_tracking.py](/core/python/src/watchtower_core/repo_ops/sync/prd_tracking.py), [decision_tracking.py](/core/python/src/watchtower_core/repo_ops/sync/decision_tracking.py), and [design_tracking.py](/core/python/src/watchtower_core/repo_ops/sync/design_tracking.py) each still hand-assemble Markdown sections and tables.
- [planning_rendered_snapshot.py](/core/python/src/watchtower_core/repo_ops/planning_rendered_snapshot.py), [planning_rendered_serialization.py](/core/python/src/watchtower_core/repo_ops/planning_rendered_serialization.py), and [query_coordination_rendered_handlers.py](/core/python/src/watchtower_core/cli/query_coordination_rendered_handlers.py) now define the live rendered terminology boundary after retiring the active `projection`-named runtime seams.
- Current foundations and standards already say that human trackers are derived from stronger machine authority, so the main gap is a reusable rendering contract rather than a new authority model.
- The reusable-core boundary already carries generic pack-facing contracts and a `rendered_view_path` field in [pack_contracts.py](/core/python/src/watchtower_core/control_plane/models/pack_contracts.py), which makes a governed rendered-surface contract a natural extension of the current direction.

## Foundations References Applied
- [engineering_design_principles.md](/docs/foundations/engineering_design_principles.md): readable outputs should remain projections from stronger machine state, and reusable layers should stay explicit and inspectable.
- [repository_standards_posture.md](/docs/foundations/repository_standards_posture.md): one canonical answer per question must remain clear, so rendered surfaces cannot become a second authority.
- [engineering_stack_direction.md](/docs/foundations/engineering_stack_direction.md): JSON Schema and Python remain the right baseline for a local-first, deterministic rendered-surface contract and renderer.

## Internal Standards and Canonical References Applied
- [schema_standard.md](/docs/standards/data_contracts/schema_standard.md): the rendered-surface contract must land as a schema-backed governed surface with same-change catalog and validator updates.
- [compact_document_authoring_standard.md](/docs/standards/documentation/compact_document_authoring_standard.md): rendered Markdown outputs should stay compact and should not duplicate machine detail without human value.
- [coordination_tracking_standard.md](/docs/standards/governance/coordination_tracking_standard.md): the coordination tracker stays a rendered start-here surface driven by the coordination index rather than an authored planning record.
- [initiative_tracking_standard.md](/docs/standards/governance/initiative_tracking_standard.md): the initiative layer remains derived from traceability and task state, so terminology and rendering changes must preserve that boundary.
- [planning_catalog_standard.md](/docs/standards/data_contracts/planning_catalog_standard.md): the planning catalog remains canonical machine authority while narrower rendered surfaces stay secondary.

## Design Goals and Constraints
- Make the layout and formatting rules for derived Markdown trackers machine-readable and reusable instead of hiding them in six separate sync services.
- Retire `projection` terminology from active runtime and current authority docs without leaving parallel compatibility wrappers.
- Keep source-specific sorting, filtering, and actionability logic in code, but move section order, column layout, and render formatting into a governed contract.
- Preserve fail-closed validation, compact output, and link-safe repository-local Markdown.
- Do not broaden the rendered-surface contract into an arbitrary template engine or freeform code execution path.

## Options Considered
### Option 1
- Rename active docs only and leave runtime helpers plus tracker rendering handwritten.
- Lowest immediate implementation cost.
- Rejected because the main maintenance fan-out and generic export problem would remain in code.

### Option 2
- Add a generic renderer in Python but keep the layout rules implicit in code and preserve `projection` compatibility names.
- Reduces some duplication in Markdown assembly.
- Rejected because it still leaves the core contract non-governed and keeps the active terminology split alive.

### Option 3
- Publish a governed rendered-surface registry, render the tracker family through a generic renderer, and rename active derived-surface boundaries from `projection` to `rendered`.
- Aligns terminology, runtime seams, and machine-readable control-plane contracts in one slice.
- Chosen because it makes the rendered layer generic and export-friendly without weakening the existing authority model.

## Recommended Design
### Architecture
- Add one authored `rendered_surface_registry` under `core/control_plane/registries/` plus a schema-backed contract that describes rendered Markdown surfaces in terms of title, output path, ordered sections, table columns, empty-state text, and permitted cell formatters.
- Add typed control-plane models and loader support for the rendered-surface registry so the contract can be loaded deterministically through the existing governed surface path.
- Add a generic rendered Markdown adapter that takes one rendered-surface definition plus pre-shaped section data and emits the final Markdown document.
- Keep tracker-specific source assembly in the current sync services, but reduce those services to preparing section rows, counts, and footers before calling the generic renderer.
- Rename active `planning_projection_*` and `query_coordination_projection_handlers.py` boundaries to `planning_rendered_*` and `query_coordination_rendered_handlers.py` so the live runtime vocabulary matches the rendered-surface contract.

### Data and Interface Impacts
- New control-plane contract surfaces:
  - one rendered-surface registry artifact
  - one rendered-surface registry schema
  - aligned schema-catalog and validator-registry entries
  - pack-settings registration for the new governed surface
- New runtime surfaces:
  - generic rendered Markdown adapter
  - typed rendered-surface model or loader path
  - renamed planning-rendered serialization, snapshot, policy, and query-helper modules
- Updated rendered tracker services:
  - coordination
  - initiative
  - task
  - PRD
  - decision
  - design
- Updated current docs and standards that describe derived outputs, current-state rendered views, and related command surfaces.

### Execution Flow
1. A sync service loads the canonical source index or task corpus and prepares shaped section data for one rendered surface.
2. The service loads the governed rendered-surface definition and passes the definition plus the prepared section data to the generic renderer.
3. The generic renderer emits the Markdown document in canonical section order using the declared table columns, empty-state text, and formatters.
4. Sync orchestration writes the rendered Markdown output alongside the refreshed machine-readable indexes.
5. Query, sync, standards, and command surfaces use `rendered` terminology consistently for these derived outputs.

### Invariants and Failure Cases
- Canonical machine authority remains in indexes, contracts, registries, and task records, not in rendered Markdown.
- The rendered-surface registry must validate fail-closed before a tracker can be emitted from it.
- Unknown section kinds, column formatters, or missing declared source keys must fail fast instead of silently emitting partial Markdown.
- Historical closed trace packages and retained ledgers are not rewritten by this slice, so active enforcement must remain scoped to current runtime and authority surfaces.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/
- core/python/src/watchtower_core/adapters/
- core/python/src/watchtower_core/cli/
- core/python/tests/
- core/control_plane/
- core/control_plane/manifests/pack_settings.json
- core/control_plane/registries/
- docs/commands/core_python/
- docs/standards/
- docs/planning/

## Design Guardrails
- Do not add compatibility aliases or duplicate runtime wrappers that preserve `projection` names in active code.
- Do not move canonical task, initiative, coordination, or planning state into rendered Markdown files.
- Do not let rendered-surface definitions embed arbitrary expression languages or code execution.
- Do not widen the initiative to historical rewrites or purge work that is not required to make the current rendered contract consistent.

## Risks
- A registry that is too weak leaves per-service logic duplicated; a registry that is too expressive becomes an unbounded template system.
- Renaming active runtime boundaries can break imports, command docs, or tests if the same-change updates are incomplete.
- Generated trackers may regress if their compact empty states or conditional columns are not modeled explicitly in the new rendered contract.

## References
- [compact_document_authoring_and_tracking.md](/docs/planning/design/features/compact_document_authoring_and_tracking.md)
- [core_export_ready_architecture.md](/docs/planning/design/features/core_export_ready_architecture.md)
- [repository_standards_posture.md](/docs/foundations/repository_standards_posture.md)
