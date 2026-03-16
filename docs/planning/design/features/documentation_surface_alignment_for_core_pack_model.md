---
trace_id: trace.documentation_surface_alignment_for_core_pack_model
id: design.features.documentation_surface_alignment_for_core_pack_model
title: Documentation Surface Alignment For Core and Pack Model Feature Design
summary: Defines the technical design boundary for aligning repository documentation
  with the current reusable-core plus plan-domain-pack model.
type: feature_design
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

# Documentation Surface Alignment For Core and Pack Model Feature Design

## Record Metadata
- `Trace ID`: `trace.documentation_surface_alignment_for_core_pack_model`
- `Design ID`: `design.features.documentation_surface_alignment_for_core_pack_model`
- `Design Status`: `active`
- `Linked PRDs`: `prd.documentation_surface_alignment_for_core_pack_model`
- `Linked Decisions`: `decision.documentation_surface_alignment_for_core_pack_model_direction`
- `Linked Implementation Plans`: `design.implementation.documentation_surface_alignment_for_core_pack_model`
- `Updated At`: `2026-03-16T05:57:19Z`

## Summary
Defines the technical design boundary for aligning repository documentation with the current reusable-core plus plan-domain-pack model.

## Source Request
- Add a tracked documentation update follow-on after the reusable-core plus pack data-shape convergence trace closed.

## Scope and Feature Boundary
- Covers documentation entrypoints, standards, command pages, and README surfaces that should reflect the current pack-settings startup boundary and flat registry layout.
- Covers classification language for reusable-core startup inputs, derived pack projections, and transitional support surfaces.
- Excludes new implementation changes unless a documentation refresh exposes a concrete same-change-set drift bug.

## Current-State Context
- The core-plus-pack boundary is now live in control-plane and loader surfaces, but the surrounding docs were updated incrementally and not yet reviewed as one documentation corpus.
- The repo still contains command pages, standards, and READMEs that were written before the pack-settings cutover or the policy-surface removal.

## Foundations References Applied
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): authoritative docs and machine-readable lookup surfaces should move together.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): prefer clear, inspectable seams over compatibility wording that hides the current boundary.

## Internal Standards and Canonical References Applied
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): command pages should reflect the current CLI and repository boundaries.
- [compact_document_authoring_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/compact_document_authoring_standard.md): refresh the docs by clarifying current authority, not by expanding stale prose.

## Design Goals and Constraints
- Keep the slice documentation-first and bounded.
- Refresh the current docs from live repository surfaces instead of preserving historical compatibility wording.
- Avoid importing external domain terminology directly when native repository wording is clearer.

## Options Considered
### Option 1
- Update only start-here READMEs.
- Strength: smallest change set.
- Tradeoff: command pages and standards would still drift.

### Option 2
- Refresh the start-here READMEs, standards, and command docs together as one bounded corpus.
- Strength: one coherent operator-facing baseline.
- Tradeoff: requires more up-front audit work.

## Recommended Design
### Architecture
- Use the live control-plane tree and planning projections as the source of truth for what documentation should describe.
- Refresh docs in clusters: start-here entrypoints, standards, command pages, and adjacent READMEs.
- Remove documentation language that still presents retired bridges or deleted policy surfaces as live.

## Affected Surfaces
- docs/
- core/control_plane/README.md
- core/control_plane/manifests/README.md
- core/control_plane/registries/README.md
- core/control_plane/schemas/artifacts/README.md
- core/python/README.md
- docs/commands/core_python/
- docs/standards/

## Design Guardrails
- Keep domain terminology native to WatchTowerPlan rather than importing external domain vocabulary directly.
- Prefer deleting stale wording over adding compatibility caveats.

## Risks
- The audit can widen quickly unless the refresh stays anchored to the current startup and documentation entrypoint surfaces.
- Command docs may expose adjacent implementation drift that has to be resolved before the documentation slice can close.

## References
- [documentation_surface_alignment_for_core_pack_model.md](/home/j/WatchTowerPlan/docs/planning/prds/documentation_surface_alignment_for_core_pack_model.md)
