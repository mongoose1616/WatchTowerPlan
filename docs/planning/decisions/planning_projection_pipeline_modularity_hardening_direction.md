---
trace_id: trace.planning_projection_pipeline_modularity_hardening
id: decision.planning_projection_pipeline_modularity_hardening_direction
title: Planning Projection Pipeline Modularity Hardening Direction Decision
summary: Records the initial direction decision for Planning Projection Pipeline Modularity
  Hardening.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-15T23:55:21Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/repo_ops/planning_projection_snapshot.py
- core/python/src/watchtower_core/repo_ops/planning_projection_source_assembly.py
- core/python/src/watchtower_core/repo_ops/planning_projection_policy.py
- core/python/src/watchtower_core/repo_ops/planning_projection_task_selection.py
- core/python/src/watchtower_core/repo_ops/planning_projection_serialization.py
- core/python/src/watchtower_core/repo_ops/planning_projection_serialization_helpers.py
- core/python/src/watchtower_core/repo_ops/sync/initiative_index.py
- core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py
- core/python/src/watchtower_core/repo_ops/README.md
- core/python/tests/unit/test_initiative_index_sync.py
- core/python/tests/unit/test_planning_catalog_sync.py
---

# Planning Projection Pipeline Modularity Hardening Direction Decision

## Record Metadata
- `Trace ID`: `trace.planning_projection_pipeline_modularity_hardening`
- `Decision ID`: `decision.planning_projection_pipeline_modularity_hardening_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.planning_projection_pipeline_modularity_hardening`
- `Linked Designs`: `design.features.planning_projection_pipeline_modularity_hardening`
- `Linked Implementation Plans`: `design.implementation.planning_projection_pipeline_modularity_hardening`
- `Updated At`: `2026-03-15T23:55:21Z`

## Summary
Records the initial direction decision for Planning Projection Pipeline Modularity Hardening.

## Decision Statement
Keep the existing private trace-scoped snapshot boundary, then refactor the remaining planning-projection hotspot by extracting family-focused serialization and catalog-only composition helpers while preserving current public planning outputs.

## Trigger or Source Request
- Turn the current WatchTowerPlan planning-projection hotspot review into a concrete bounded planning slice.

## Current Context and Constraints
- The earlier Phase 4 snapshot slice already landed, and the live March 15, 2026 code now shows `planning_projection_snapshot.py` at `134` lines while the heavier remaining files are `planning_projection_serialization.py` at `378` and `planning_catalog.py` at `359`.
- The structural rewrite docs still identify planning projection as a live rewrite-relevant hotspot, but the current remaining boundary is deeper in serialization and catalog composition rather than raw trace-source assembly.
- The refactor must preserve the public planning authority boundary, initiative-versus-planning coordination semantics, control-plane schemas, and current sync ordering.

## Applied References and Implications
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md): the rewrite inventory still treats planning projection as a live hotspot and requires fresh live-state grounding instead of stale examples.
- [structural_rewrite_phase4_shared_projection_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_shared_projection_entry.md): the shared planning projection remains a private runtime detail rather than a new public artifact family.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): use explicit repo-local helpers and readable orchestration rather than a broader framework rewrite.
- [authority_map_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/authority_map_standard.md): do not disturb the public planning-authority answers while tightening the private pipeline.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/planning_projection_snapshot.py
- core/python/src/watchtower_core/repo_ops/planning_projection_source_assembly.py
- core/python/src/watchtower_core/repo_ops/planning_projection_policy.py
- core/python/src/watchtower_core/repo_ops/planning_projection_task_selection.py
- core/python/src/watchtower_core/repo_ops/planning_projection_serialization.py
- core/python/src/watchtower_core/repo_ops/planning_projection_serialization_helpers.py
- core/python/src/watchtower_core/repo_ops/sync/initiative_index.py
- core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py
- core/python/src/watchtower_core/repo_ops/README.md
- core/python/tests/unit/test_initiative_index_sync.py
- core/python/tests/unit/test_planning_catalog_sync.py

## Options Considered
### Option 1
- Leave the current private projection boundary in place because the earlier Phase 4 snapshot extraction already delivered the big structural win.
- Strength: avoids another internal refactor pass.
- Tradeoff: leaves the remaining serializer and planning-catalog concentration intact and keeps small payload changes high-risk.

### Option 2
- Reopen a broader shared-projection or internal planning-graph rewrite.
- Strength: could normalize more of the projection family at once.
- Tradeoff: too broad for the remaining hotspot and risks accidental public-boundary drift.

### Option 3
- Keep the current private snapshot boundary and extract bounded helper seams around serialization and planning-catalog composition.
- Strength: addresses the live hotspot with the smallest behavior-preserving change.
- Tradeoff: requires careful parity coverage and same-change alignment across docs, trackers, and evidence.

## Chosen Outcome
Adopt option 3. The repository should keep the current private snapshot graph, then narrow the remaining hotspot by splitting serializer families and catalog-only composition while keeping public planning outputs stable.

## Rationale and Tradeoffs
- The live March 15 code shows that the earlier source-assembly extraction already happened, so repeating that older slice would aim at the wrong seam.
- The remaining hotspot is still material enough to justify a bounded follow-up, but it is small enough to handle without another broad rewrite package.
- Keeping the public planning authority boundary unchanged minimizes operator-facing risk while still reducing the internal blast radius for future planning-output changes.

## Consequences and Follow-Up Impacts
- New private helper seams may appear under `core/python/src/watchtower_core/repo_ops/` for serializer families and catalog projection support.
- The targeted sync tests and `repo_ops/README.md` need same-change updates so the new private boundary remains inspectable.
- If payload parity breaks or the slice widens into public planning surfaces, rollback should restore the current serialization and planning-catalog assembly paths.

## Risks, Dependencies, and Assumptions
- Risk: serializer splits can introduce subtle compact-mode drift or coordination mismatches.
- Dependency: targeted sync or query coverage must be strong enough to detect payload regressions quickly.
- Assumption: the remaining hotspot can be reduced without changing query payloads, sync ordering, or public planning contracts.

## References
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [structural_rewrite_phase4_shared_projection_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_shared_projection_entry.md)
- [structural_rewrite_phase4_planning_projection_snapshot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md)
