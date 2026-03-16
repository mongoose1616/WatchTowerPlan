---
trace_id: trace.planning_projection_pipeline_modularity_hardening
id: prd.planning_projection_pipeline_modularity_hardening
title: Planning Projection Pipeline Modularity Hardening PRD
summary: Reduce remaining responsibility concentration in the private planning-projection
  pipeline by narrowing shared serialization, catalog-summary assembly, and sync
  composition seams without changing public planning outputs.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-15T23:55:21Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/planning_projection_snapshot.py
- core/python/src/watchtower_core/repo_ops/planning_projection_source_assembly.py
- core/python/src/watchtower_core/repo_ops/planning_projection_policy.py
- core/python/src/watchtower_core/repo_ops/planning_projection_task_selection.py
- core/python/src/watchtower_core/repo_ops/planning_projection_serialization.py
- core/python/src/watchtower_core/repo_ops/planning_projection_serialization_helpers.py
- core/python/src/watchtower_core/repo_ops/sync/initiative_index.py
- core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py
---

# Planning Projection Pipeline Modularity Hardening PRD

## Record Metadata
- `Trace ID`: `trace.planning_projection_pipeline_modularity_hardening`
- `PRD ID`: `prd.planning_projection_pipeline_modularity_hardening`
- `Status`: `active`
- `Linked Decisions`: `decision.planning_projection_pipeline_modularity_hardening_direction`
- `Linked Designs`: `design.features.planning_projection_pipeline_modularity_hardening`
- `Linked Implementation Plans`: `design.implementation.planning_projection_pipeline_modularity_hardening`
- `Updated At`: `2026-03-15T23:55:21Z`

## Summary
Reduce remaining responsibility concentration in the private planning-projection pipeline by narrowing shared serialization, catalog-summary assembly, and sync composition seams without changing public planning outputs.

## Problem Statement
- The March 15, 2026 live code shows the original Phase 4 snapshot extraction already landed: `planning_projection_snapshot.py` is `134` lines, `planning_projection_source_assembly.py` is `89`, `planning_projection_task_selection.py` is `169`, and trace-scoped coordination policy already lives in `planning_projection_policy.py`.
- The remaining responsibility concentration now sits deeper in the private projection pipeline. `planning_projection_serialization.py` is `378` lines and still serializes coordination, initiative, PRD, decision, design, task, acceptance-contract, validation-evidence, and full planning-catalog payloads, while `planning_catalog.py` is `359` lines and still owns validator aggregation, related-path expansion, tag derivation, updated-at calculation, and summary projection for the same trace-scoped snapshot.
- Small private planning-output changes still require synchronized edits across serializer fan-out, catalog-only aggregation logic, initiative parity coverage, and planning-query-facing surfaces, which keeps the blast radius too large for a repo-local seam that is supposed to stay private.

## Goals
- Extract smaller helper-backed seams around planning-catalog summary assembly and per-family serialization while preserving current initiative and planning payloads.
- Keep the trace-scoped planning snapshot private and avoid changes to public planning authority answers, sync ordering, or CLI contracts.
- Leave an explicit coverage map, findings ledger, and bounded execution queue so the slice can be implemented and closed without reopening scope discovery.

## Non-Goals
- Reopening the already-closed Phase 4 planning-projection snapshot slice or changing the public planning authority boundary.
- Changing control-plane schemas, query payload fields, sync ordering, or the meaning of `artifact_status`, `initiative_status`, `decision_status`, or `task_status`.
- Bundling unrelated hotspot work from `acceptance.py`, `loader.py`, `workflow_index.py`, or planning authoring surfaces into this trace.

## Requirements
- `req.planning_projection_pipeline_modularity_hardening.001`: The trace must publish and follow an explicit coverage map plus findings ledger across private planning-projection helpers, sync consumers, targeted tests, runtime-boundary docs, trackers, acceptance surfaces, and evidence before implementation begins.
- `req.planning_projection_pipeline_modularity_hardening.002`: The shared planning-projection serialization surface must split into smaller family-focused seams or helpers while preserving compact and non-compact payload semantics for initiative and planning projections.
- `req.planning_projection_pipeline_modularity_hardening.003`: `planning_catalog.py` and `initiative_index.py` must consume slimmer shared composition helpers so catalog-only aggregation of validator IDs, related paths, tags, and updated-at state no longer crowds the sync entrypoints, and coordination parity remains stable.
- `req.planning_projection_pipeline_modularity_hardening.004`: Same-change tests, repo-local runtime docs, trackers, indexes, the acceptance contract, and validation evidence must stay aligned with the refactor, and the initiative must close through targeted and full validation rather than informal signoff.

## Acceptance Criteria
- `ac.planning_projection_pipeline_modularity_hardening.001`: The planning corpus for `trace.planning_projection_pipeline_modularity_hardening` contains the active PRD, accepted direction decision, active feature design, active implementation plan, aligned acceptance contract, planning-baseline evidence, closed bootstrap task, and bounded open execution tasks for the remaining hotspot.
- `ac.planning_projection_pipeline_modularity_hardening.002`: The shared serialization surface no longer owns all projection payload families in one file, and initiative or planning payloads stay stable under focused regression coverage.
- `ac.planning_projection_pipeline_modularity_hardening.003`: `planning_catalog.py` and `initiative_index.py` consume smaller private composition helpers, and coordination parity plus validator or related-path or tag projection semantics stay stable.
- `ac.planning_projection_pipeline_modularity_hardening.004`: Targeted sync or query tests, repo-wide validation, acceptance or evidence refresh, and initiative closeout complete without a new actionable issue in this private seam.

## Risks and Dependencies
- Over-splitting the private pipeline could make the sync path harder to read rather than easier.
- Planning catalog and initiative coordination must remain semantically identical even if implementation helpers diverge.
- The slice depends on live query, sync, and test coverage being strong enough to catch payload drift without introducing a new public artifact.

## References
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [structural_rewrite_phase4_shared_projection_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_shared_projection_entry.md)
- [structural_rewrite_phase4_planning_projection_snapshot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md)
