---
trace_id: trace.documentation_surface_alignment_for_core_pack_model
id: decision.documentation_surface_alignment_for_core_pack_model_direction
title: Documentation Surface Alignment For Core and Pack Model Direction Decision
summary: Records the direction decision for aligning the documentation corpus with
  the current reusable-core plus plan-domain-pack model.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-16T05:57:19Z'
audience: shared
authority: supporting
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

# Documentation Surface Alignment For Core and Pack Model Direction Decision

## Record Metadata
- `Trace ID`: `trace.documentation_surface_alignment_for_core_pack_model`
- `Decision ID`: `decision.documentation_surface_alignment_for_core_pack_model_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.documentation_surface_alignment_for_core_pack_model`
- `Linked Designs`: `design.features.documentation_surface_alignment_for_core_pack_model`
- `Linked Implementation Plans`: `design.implementation.documentation_surface_alignment_for_core_pack_model`
- `Updated At`: `2026-03-16T05:57:19Z`

## Summary
Records the direction decision for aligning the documentation corpus with the current reusable-core plus plan-domain-pack model.

## Decision Statement
Treat WatchTowerPlan documentation as the operator surface for reusable core plus the first plan-domain pack, and refresh that corpus from the live pack-settings, flat-registry, and explicit derived-projection boundaries instead of preserving compatibility wording for retired shapes.

## Trigger or Source Request
- Add a tracked documentation update follow-on after closing the data-shape convergence trace.

## Current Context and Constraints
- The underlying control-plane and loader surfaces already moved to the pack-settings startup boundary.
- The documentation corpus is broader than the implementation slice and still needs a bounded cleanup pass to remove stale assumptions without turning into an untracked rewrite.

## Applied References and Implications
- [validated_core_and_pack_data_shape_convergence.md](/docs/planning/prds/validated_core_and_pack_data_shape_convergence.md): the documentation slice should treat the pack-settings cutover and flat registries as the new baseline rather than reopening that technical decision.
- [repository_standards_posture.md](/docs/foundations/repository_standards_posture.md): human-readable guidance and machine-readable lookup surfaces should stay aligned in the same change set.

## Affected Surfaces
- docs/
- core/control_plane/README.md
- core/control_plane/manifests/README.md
- core/control_plane/registries/README.md
- core/control_plane/schemas/artifacts/README.md
- core/python/README.md
- docs/commands/core_python/
- docs/standards/

## Options Considered
### Option 1
- Refresh only a few top-level READMEs and leave deeper standards or command pages for later.
- Strength: small immediate diff.
- Tradeoff: leaves the documentation corpus internally inconsistent.

### Option 2
- Run one bounded documentation initiative that refreshes the current start-here, standards, and command surfaces from the live core-plus-pack boundary.
- Strength: produces one coherent documentation baseline.
- Tradeoff: requires a wider but still bounded audit pass.

## Chosen Outcome
Run one documentation-first follow-on that updates the repository's entrypoints, standards, and command docs from the new core-plus-pack baseline, then validate and close the slice cleanly.

## Rationale and Tradeoffs
- The repository already paid the implementation cost for the new boundary, so leaving the docs half-updated would create needless maintenance drag.
- A bounded documentation initiative is cheaper than repeated opportunistic edits that keep rediscovering the same stale assumptions.

## Consequences and Follow-Up Impacts
- Documentation refresh becomes explicit tracked work instead of background cleanup.
- Future contributors get one clearer vocabulary for startup authority, pack-local projections, and retired surfaces.

## Risks, Dependencies, and Assumptions
- Assumes the current pack-settings and flat-registry boundary is stable enough to document directly.
- Depends on keeping adjacent command and planning trackers aligned if the documentation refresh changes lookup guidance materially.

## References
- [documentation_surface_alignment_for_core_pack_model.md](/docs/planning/prds/documentation_surface_alignment_for_core_pack_model.md)
- [validated_core_and_pack_data_shape_convergence.md](/docs/planning/prds/validated_core_and_pack_data_shape_convergence.md)
