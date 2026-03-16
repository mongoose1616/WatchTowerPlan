---
trace_id: trace.rendered_surface_contract_enforcement
id: prd.rendered_surface_contract_enforcement
title: Rendered Surface Contract Enforcement PRD
summary: Replaces live projection terminology with rendered-surface terminology and
  introduces schema-driven rendered Markdown surfaces for derived human outputs.
type: prd
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

# Rendered Surface Contract Enforcement PRD

## Record Metadata
- `Trace ID`: `trace.rendered_surface_contract_enforcement`
- `PRD ID`: `prd.rendered_surface_contract_enforcement`
- `Status`: `active`
- `Linked Decisions`: `decision.rendered_surface_contract_enforcement_direction`
- `Linked Designs`: `design.features.rendered_surface_contract_enforcement`
- `Linked Implementation Plans`: `design.implementation.rendered_surface_contract_enforcement`
- `Updated At`: `2026-03-16T17:34:52Z`

## Summary
Replaces live projection terminology with rendered-surface terminology and introduces schema-driven rendered Markdown surfaces for derived human outputs.

## Problem Statement
- The repository still uses `projection` terminology across active code, query handlers, standards, and command docs for non-authoritative derived outputs, even where the concern is explicitly rendering a human or machine-facing surface.
- Derived Markdown trackers are still assembled through handwritten per-service string logic in the sync layer, which makes them harder to configure, harder to export for future pack use, and easy to let drift from the machine-readable indexes they summarize.
- The current shape leaves active terminology, rendering seams, and governed control-plane contracts inconsistent at the same time the repository is trying to slim down toward a more reusable core boundary.

## Goals
- Replace live `projection` terminology with `rendered` terminology across active runtime code, current standards, command docs, and other current authority surfaces that describe derived outputs.
- Introduce one governed rendered-surface contract so derived Markdown trackers are driven by a reusable machine-readable registry instead of handwritten layout logic per tracker file.
- Keep canonical machine authority in indexes, contracts, registries, and task records while making rendered human surfaces thinner, more generic, and easier to export.
- Remove the need for compatibility wording or parallel legacy render paths in the active codebase for this slice.

## Non-Goals
- Rewriting retained closed trace packages, archived task history, or historical validation ledgers purely for terminology cleanup.
- Replacing the canonical planning catalog, initiative index, coordination index, or task index with Markdown surfaces.
- Introducing an unrestricted templating engine or freeform runtime script layer for rendered surfaces.
- Preserving parallel `projection`-named compatibility wrappers after the active runtime and documentation surfaces move.

## Requirements
- `req.rendered_surface_contract_enforcement.001`: The initiative must publish a bounded traced planning chain, supporting decision, acceptance contract, and execution tasks for the rendered-surface contract change.
- `req.rendered_surface_contract_enforcement.002`: Active runtime code and current authority docs must retire `projection` terminology for derived outputs in favor of `rendered` terminology wherever the surface remains live and non-historical.
- `req.rendered_surface_contract_enforcement.003`: Derived Markdown trackers built from index-backed repository data must render through a governed rendered-surface registry and a generic renderer rather than handwritten per-service layout assembly.
- `req.rendered_surface_contract_enforcement.004`: The rendered-surface contract must be machine-readable, schema-validated, and cataloged through the control-plane schema and validator surfaces so future reusable-core or pack work can load it deterministically.
- `req.rendered_surface_contract_enforcement.005`: The initiative must update companion pack settings, loader or typed-model surfaces, standards, command docs, and sync logic in the same change set when the rendered-surface contract becomes live.
- `req.rendered_surface_contract_enforcement.006`: The initiative must close without leaving active compatibility wrappers, duplicate render paths, or stale rendered-surface terminology on current runtime or authority surfaces inside this bounded scope.
- `req.rendered_surface_contract_enforcement.007`: The repository must remain green on sync, acceptance reconciliation, artifact validation, document validation, tests, type checking, and linting after the rendered-surface change lands.

## Acceptance Criteria
- `ac.rendered_surface_contract_enforcement.001`: The trace publishes an active PRD, accepted direction decision, active feature design, active implementation plan, aligned acceptance contract, planning-baseline evidence, and bounded execution tasks for `trace.rendered_surface_contract_enforcement`.
- `ac.rendered_surface_contract_enforcement.002`: A governed rendered-surface registry and supporting schema or validator entries exist under `core/control_plane/`, and the active tracker family renders through that contract rather than per-service handwritten section assembly.
- `ac.rendered_surface_contract_enforcement.003`: Active runtime modules, query helpers, and current command or standards guidance use `rendered` terminology instead of `projection` terminology for live derived outputs, without leaving active compatibility aliases behind.
- `ac.rendered_surface_contract_enforcement.004`: Current rendered trackers stay compact, link-safe, and index-backed after the refactor, with no behavioral regression in their active-first or actionable-first output.
- `ac.rendered_surface_contract_enforcement.005`: `watchtower-core sync all --write --format json`, `watchtower-core validate acceptance --trace-id trace.rendered_surface_contract_enforcement --format json`, `watchtower-core validate all --format json`, `pytest -q`, `mypy src`, and `ruff check .` pass after the initiative changes land.
- `ac.rendered_surface_contract_enforcement.006`: Initiative closeout records that the bounded rendered-surface contract and terminology enforcement slice is complete with no remaining active `projection` compatibility surface in the scoped runtime or authority layers.

## Risks and Dependencies
- Historical traces and retained ledgers still carry earlier `projection` wording in archived records, so this initiative must keep its no-history-rewrite boundary explicit instead of silently mutating historical evidence.
- A rendered-surface registry that is too expressive could become a second templating language rather than a stable governed contract.
- Renaming active query, sync, and serialization helpers can create import or command-doc drift if same-change companion updates are missed.
- The initiative depends on the existing planning indexes and trackers staying canonical for machine state while the rendered Markdown layer becomes more generic.

## References
- [compact_document_authoring_and_tracking.md](/docs/planning/design/features/compact_document_authoring_and_tracking.md)
- [core_export_ready_architecture.md](/docs/planning/design/features/core_export_ready_architecture.md)
- [repository_standards_posture.md](/docs/foundations/repository_standards_posture.md)
