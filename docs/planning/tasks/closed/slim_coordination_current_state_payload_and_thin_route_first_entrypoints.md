---
id: task.refactor_review_and_hardening.current_state_surface_simplification.003
trace_id: trace.refactor_review_and_hardening
title: Slim coordination current-state payload and thin route-first entrypoints
summary: Keep coordination current-state projections compact and route planning and
  command entrypoints through the smallest useful surfaces instead of handbook-style
  repetition.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T14:42:27Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/sync/coordination_index.py
- core/control_plane/indexes/coordination/
- docs/standards/data_contracts/coordination_index_standard.md
- docs/standards/governance/coordination_tracking_standard.md
- docs/planning/README.md
- docs/planning/initiatives/README.md
- docs/commands/core_python/watchtower_core.md
- docs/commands/core_python/watchtower_core_query.md
- docs/commands/core_python/watchtower_core_sync.md
- core/python/tests/
related_ids:
- trace.refactor_review_and_hardening
- prd.refactor_review_and_hardening
- design.features.refactor_review_and_hardening
- design.implementation.refactor_review_and_hardening
- decision.refactor_review_and_hardening_direction
- contract.acceptance.refactor_review_and_hardening
---

# Slim coordination current-state payload and thin route-first entrypoints

## Summary
Keep coordination current-state projections compact and route planning and command entrypoints through the smallest useful surfaces instead of handbook-style repetition.

## Scope
- Slim coordination index entries and recent-closeout projection so the machine start-here surface stays current-state focused.
- Keep the coordination tracking guidance, planning entrypoints, and initiative-family README aligned with the compact current-state contract.
- Thin the root and group command pages so they route to help, indexes, and leaf docs instead of re-enumerating the full command surface.

## Done When
- Coordination index and companion standards keep closed-history context compact instead of reproducing initiative-family detail.
- Planning and command umbrella entrypoints stay route-first and stop duplicating low-value example catalogs.
- Targeted sync, query, and documentation regressions pass on the simplified surfaces.
