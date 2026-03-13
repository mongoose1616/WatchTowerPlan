---
trace_id: trace.derived_projection_status_semantics
id: prd.derived_projection_status_semantics
title: Derived Projection Status Semantics Alignment PRD
summary: Make initiative and coordination projections publish explicit artifact-status
  fields so machine consumers do not misread closed initiatives as active.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-11T03:29:01Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/indexes/initiatives/
- core/control_plane/indexes/coordination/
- core/python/src/watchtower_core/
- docs/commands/core_python/
- docs/standards/
---

# Derived Projection Status Semantics Alignment PRD

## Record Metadata
- `Trace ID`: `trace.derived_projection_status_semantics`
- `PRD ID`: `prd.derived_projection_status_semantics`
- `Status`: `active`
- `Linked Decisions`: `decision.derived_projection_status_semantics_direction`
- `Linked Designs`: `design.features.derived_projection_status_semantics`
- `Linked Implementation Plans`: `design.implementation.derived_projection_status_semantics`
- `Updated At`: `2026-03-11T03:29:01Z`

## Summary
Make initiative and coordination projections publish explicit artifact-status fields so machine consumers do not misread closed initiatives as active.

## Problem Statement
The repository now has a canonical planning catalog and authority map, but the derived initiative-family projections still expose one misleading contract detail. Initiative-index and coordination-index entries publish a generic `status` field copied from traceability artifact lifecycle state while also publishing `initiative_status` for initiative outcome. For closed initiatives, that yields payloads such as `status: active` and `initiative_status: completed`, which is correct internally but easy for machine consumers to misread as contradictory or stale. An earlier whole-repo review called out this exact ambiguity, and verification after the planning-authority closeout confirmed that it still reproduces on `watchtower-core query initiatives`.

## Goals
- Replace ambiguous per-entry initiative-family `status` fields with explicit `artifact_status` naming in derived machine-readable initiative and coordination projections.
- Keep initiative outcome semantics explicit and separate through `initiative_status`, without reopening the traceability closeout model.
- Update schemas, sync logic, query surfaces, docs, and tests together so the repository publishes one coherent contract change.

## Non-Goals
- Change the root artifact-level lifecycle field on the initiative or coordination index documents themselves.
- Rename lifecycle `status` fields across unrelated artifact families such as traceability, tasks, PRDs, or design documents.
- Introduce a new planning authority surface beyond the planning catalog and authority map that already landed.

## Requirements
- `req.derived_projection_status_semantics.001`: Initiative-index entries and coordination-index embedded initiative entries must publish `artifact_status` instead of a generic per-entry `status` field.
- `req.derived_projection_status_semantics.002`: Query and loader surfaces that expose initiative-family entries must use the explicit `artifact_status` field while preserving `initiative_status`, `current_phase`, and task-state fields.
- `req.derived_projection_status_semantics.003`: The initiative-index and coordination-index standards, command docs, schemas, examples, and repository tests must be updated in the same change set.

## Acceptance Criteria
- `ac.derived_projection_status_semantics.001`: `watchtower-core query initiatives --trace-id trace.planning_authority_unification --format json` returns a closed initiative entry with `artifact_status` and `initiative_status`, and no ambiguous entry-level `status` field.
- `ac.derived_projection_status_semantics.002`: The initiative-index and coordination-index artifact contracts validate after the entry-field rename, with embedded initiative entries aligned to the new field name.
- `ac.derived_projection_status_semantics.003`: Companion docs and standards explain that root artifact `status` remains lifecycle metadata for the index artifact, while entry-level initiative-family lifecycle uses `artifact_status`.
- `ac.derived_projection_status_semantics.004`: `watchtower-core sync all --write --format json`, `watchtower-core validate all --format json`, `python -m mypy src`, `ruff check .`, and `pytest -q` pass after the contract change.

## Risks and Dependencies
- Repo-owned consumers of initiative-family JSON must move in lockstep with the schema change or they will fail to parse entry payloads.
- The change must stay bounded to derived initiative-family projections so it does not reopen the larger traceability contract unnecessarily.
- The planning-authority work is a dependency because this follow-up assumes the planning catalog and authority map remain the canonical deep-planning path.

## References
- [watchtower_core_query_initiatives.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_query_initiatives.md)
- [planning_authority_unification.md](/home/j/WatchTowerPlan/docs/planning/prds/planning_authority_unification.md)
