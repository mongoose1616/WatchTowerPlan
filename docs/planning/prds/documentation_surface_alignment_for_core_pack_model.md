---
trace_id: trace.documentation_surface_alignment_for_core_pack_model
id: prd.documentation_surface_alignment_for_core_pack_model
title: Documentation Surface Alignment For Core and Pack Model PRD
summary: Align the repository documentation corpus with the current reusable-core
  plus plan-domain-pack model so entrypoints, standards, and command docs stop
  describing retired shapes as live.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-16T05:57:19Z'
audience: shared
authority: authoritative
applies_to:
- docs/
- core/control_plane/README.md
- core/control_plane/manifests/README.md
- core/control_plane/registries/README.md
- core/control_plane/schemas/artifacts/README.md
- core/python/README.md
- docs/commands/core_python/
- docs/standards/
---

# Documentation Surface Alignment For Core and Pack Model PRD

## Record Metadata
- `Trace ID`: `trace.documentation_surface_alignment_for_core_pack_model`
- `PRD ID`: `prd.documentation_surface_alignment_for_core_pack_model`
- `Status`: `active`
- `Linked Decisions`: `decision.documentation_surface_alignment_for_core_pack_model_direction`
- `Linked Designs`: `design.features.documentation_surface_alignment_for_core_pack_model`
- `Linked Implementation Plans`: `design.implementation.documentation_surface_alignment_for_core_pack_model`
- `Updated At`: `2026-03-16T05:57:19Z`

## Summary
Align the repository documentation corpus with the current reusable-core plus plan-domain-pack model so entrypoints, standards, and command docs stop describing retired shapes as live.

## Problem Statement
- The pack-settings cutover established a cleaner reusable-core boundary, but the broader documentation corpus still contains older assumptions about nested registries, policy surfaces, retired bridges, and transitional artifact families.
- Those stale descriptions increase human maintenance cost and create drift between the live repository shape and the docs that should guide future work.
- The repository now needs one bounded documentation initiative that treats WatchTowerPlan as reusable core plus the first plan and implementation domain pack, then refreshes the surrounding docs from that baseline.

## Goals
- Refresh start-here documentation, standards, and command docs to match the current core-plus-pack model.
- Remove or rewrite documentation that still treats retired control-plane surfaces as active.
- Make the surviving documentation explicit about which families are canonical startup inputs, which are derived projections, and which remain transitional support surfaces.

## Non-Goals
- Reworking the underlying code or governed artifact shapes again in this trace unless documentation review finds a concrete same-change drift bug.
- Performing a broad prose cleanup unrelated to the core-plus-pack alignment boundary.
- Deleting every historical document that mentions retired shapes.

## Requirements
- `req.documentation_surface_alignment_for_core_pack_model.001`: The planning chain must define the documentation-alignment scope as a follow-on to the validated core and pack data-shape convergence trace.
- `req.documentation_surface_alignment_for_core_pack_model.002`: Repository entrypoints, standards, and command docs must describe the current pack-settings boundary, flat registries, and retired legacy surfaces consistently.
- `req.documentation_surface_alignment_for_core_pack_model.003`: The trace must close with refreshed planning trackers and validation confirming the documentation corpus no longer points users at retired live surfaces.

## Acceptance Criteria
- `ac.documentation_surface_alignment_for_core_pack_model.001`: The planning corpus contains the PRD, decision, design, implementation plan, acceptance contract, planning-baseline evidence, closed bootstrap task, and bounded open tasks for the documentation-alignment slice.
- `ac.documentation_surface_alignment_for_core_pack_model.002`: The documentation corpus consistently describes the repository as reusable core plus a plan-domain pack with pack-settings startup, flat registries, and no live policy or runtime-manifest bridge surfaces.
- `ac.documentation_surface_alignment_for_core_pack_model.003`: Validation and planning projections refresh cleanly after the documentation slice lands.

## Risks and Dependencies
- The scope is broad enough that unbounded prose cleanup could sprawl unless the trace stays focused on start-here, standards, and command surfaces.
- The slice depends on the current control-plane and planning projections staying authoritative while documentation is refreshed from them.
- Documentation changes can expose adjacent command-index or tracker drift that must be repaired in the same slice to keep lookup surfaces coherent.

## References
- [validated_core_and_pack_data_shape_convergence.md](/home/j/WatchTowerPlan/docs/planning/prds/validated_core_and_pack_data_shape_convergence.md)
