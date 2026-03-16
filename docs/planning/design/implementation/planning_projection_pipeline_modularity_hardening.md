---
trace_id: trace.planning_projection_pipeline_modularity_hardening
id: design.implementation.planning_projection_pipeline_modularity_hardening
title: Planning Projection Pipeline Modularity Hardening Implementation Plan
summary: Breaks Planning Projection Pipeline Modularity Hardening into a bounded implementation
  slice.
type: implementation_plan
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

# Planning Projection Pipeline Modularity Hardening Implementation Plan

## Record Metadata
- `Trace ID`: `trace.planning_projection_pipeline_modularity_hardening`
- `Plan ID`: `design.implementation.planning_projection_pipeline_modularity_hardening`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.planning_projection_pipeline_modularity_hardening`
- `Linked Decisions`: `decision.planning_projection_pipeline_modularity_hardening_direction`
- `Source Designs`: `design.features.planning_projection_pipeline_modularity_hardening`
- `Linked Acceptance Contracts`: `contract.acceptance.planning_projection_pipeline_modularity_hardening`
- `Updated At`: `2026-03-15T23:55:21Z`

## Summary
Breaks Planning Projection Pipeline Modularity Hardening into a bounded implementation slice.

## Source Request or Design
- Turn the current WatchTowerPlan planning-projection hotspot review into a concrete bounded planning slice.
- Feature design: [planning_projection_pipeline_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/planning_projection_pipeline_modularity_hardening.md)
- PRD: [planning_projection_pipeline_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/planning_projection_pipeline_modularity_hardening.md)
- Decision: [planning_projection_pipeline_modularity_hardening_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/planning_projection_pipeline_modularity_hardening_direction.md)

## Scope Summary
- Tighten the remaining private planning-projection hotspot around shared serialization, catalog-only aggregation, and initiative/planning sync composition.
- Cover code, tests, runtime-boundary docs, acceptance surfaces, evidence, trackers, and indexes directly touched by that seam.
- Leave public planning authority boundaries, CLI contracts, sync ordering, and unrelated hotspots untouched.

## Assumptions and Constraints
- Public payload fields, ordering, and coordination semantics must remain stable through the refactor.
- The slice stays inside repo-local projection helpers and the existing sync services; it does not introduce a new artifact family or shared public API.
- The planning-baseline evidence only proves planning-chain alignment at bootstrap time; implementation evidence expands later during validation closeout.

## Internal Standards and Canonical References Applied
- [authority_map_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/authority_map_standard.md): the public planning boundary must remain unchanged while the private helpers move.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): initiative phase and next-step semantics must remain stable in the generated indexes.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): bounded task sequencing, task moves, and derived coordination surfaces must stay aligned.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): new helper seams and tests must remain inside the governed Python workspace.

## Proposed Technical Approach
- Establish the live baseline counts, payload contracts, and hotspot boundary from the current snapshot helpers, serializers, and sync tests.
- Extract family-focused serializers behind a smaller private serialization surface while keeping compact-mode helper semantics centralized.
- Extract catalog-only projection helpers for validator, related-path, tag, and updated-at derivation so `PlanningCatalogSyncService` becomes an assembly entrypoint rather than the full projection engine.
- Keep initiative sync on shared coordination plus initiative-entry projection only, and refresh `repo_ops/README.md` plus targeted tests so the private boundary remains inspectable.

## Coverage Map
| Coverage Area | Surfaces | Review Focus |
|---|---|---|
| Upstream private snapshot boundary | `core/python/src/watchtower_core/repo_ops/planning_projection_snapshot.py`; `core/python/src/watchtower_core/repo_ops/planning_projection_source_assembly.py`; `core/python/src/watchtower_core/repo_ops/planning_projection_policy.py`; `core/python/src/watchtower_core/repo_ops/planning_projection_task_selection.py` | Preserve the current private graph boundary and avoid needlessly widening back into source assembly or phase policy work. |
| Shared serialization surface | `core/python/src/watchtower_core/repo_ops/planning_projection_serialization.py`; `core/python/src/watchtower_core/repo_ops/planning_projection_serialization_helpers.py`; adjacent private serializer helpers if introduced | Family boundaries, compact semantics, and payload parity. |
| Sync consumers | `core/python/src/watchtower_core/repo_ops/sync/initiative_index.py`; `core/python/src/watchtower_core/repo_ops/sync/planning_catalog.py` | Smaller orchestration, stable coordination parity, and isolated catalog-only aggregation. |
| Runtime docs and trace surfaces | `core/python/src/watchtower_core/repo_ops/README.md`; `docs/planning/**`; `core/control_plane/contracts/acceptance/planning_projection_pipeline_modularity_hardening_acceptance.v1.json`; `core/control_plane/ledgers/validation_evidence/planning_projection_pipeline_modularity_hardening_planning_baseline.v1.json` | Same-change documentation, tracker, and traceability alignment. |
| Regression coverage and validation | `core/python/tests/unit/test_initiative_index_sync.py`; `core/python/tests/unit/test_planning_catalog_sync.py`; any new focused serializer or catalog-helper tests; `watchtower-core sync all`; `watchtower-core query initiatives`; `watchtower-core query planning`; `watchtower-core validate all` | Payload drift detection and clean closeout evidence. |

## Findings Ledger
| Finding ID | Severity | Status | Affected Surfaces | Verification Evidence |
|---|---|---|---|---|
| `finding.planning_projection_pipeline_modularity_hardening.001` | `high` | `open` | `planning_projection_serialization.py`; initiative and planning payload serialization | The March 15, 2026 live scan shows `planning_projection_serialization.py` at `378` lines and still serializing coordination, initiative, planning-summary families, and the full planning catalog payload. |
| `finding.planning_projection_pipeline_modularity_hardening.002` | `high` | `open` | `planning_catalog.py`; planning-catalog summary projection; validator or related-path or tag derivation | The live scan shows `planning_catalog.py` at `359` lines and still coupling summary conversion with validator aggregation, related-path expansion, tag derivation, and updated-at calculation. |
| `finding.planning_projection_pipeline_modularity_hardening.003` | `medium` | `open` | `test_initiative_index_sync.py`; `test_planning_catalog_sync.py`; repo-local projection helpers | Current tests prove whole-document coordination parity, but they do not yet isolate serializer or catalog-helper contracts directly, which increases drift risk during the refactor. |

## Work Breakdown
1. Replace the bootstrap placeholders with the accepted direction, coverage map, findings ledger, aligned acceptance contract, planning-baseline evidence, and bounded task queue for the current hotspot.
2. Complete `task.planning_projection_pipeline_modularity_hardening.serialization_boundary.002` by splitting family-focused serializers and tightening compact-mode regression coverage.
3. Complete `task.planning_projection_pipeline_modularity_hardening.sync_surface_alignment.003` by extracting catalog-only aggregation or composition helpers and aligning runtime docs plus sync parity coverage.
4. Complete `task.planning_projection_pipeline_modularity_hardening.validation_closeout.004` by running targeted sync or query tests, `sync all`, full validation, evidence refresh, and task or initiative closeout.

## Risks
- Compact-mode omissions can drift silently if serializer helpers do not preserve the current helper semantics.
- A helper split that hides data provenance could make related-path or validator aggregation harder to inspect.
- Full-document parity tests alone may not catch field-level regressions unless the slice adds narrower direct coverage.

## Validation Plan
- Run targeted sync coverage with `./.venv/bin/python -m pytest tests/unit/test_initiative_index_sync.py` and `./.venv/bin/python -m pytest tests/unit/test_planning_catalog_sync.py`.
- Add and run direct serializer or catalog-helper coverage if the refactor introduces new private helpers.
- Re-run `./.venv/bin/watchtower-core sync all --write --format json`, `./.venv/bin/watchtower-core query initiatives --format json`, and `./.venv/bin/watchtower-core query planning --trace-id trace.planning_projection_pipeline_modularity_hardening --format json`.
- Re-run `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/ruff check .`, and `./.venv/bin/python -m mypy src/watchtower_core`.

## References
- [structural_rewrite_program.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_program.md)
- [structural_rewrite_phase4_shared_projection_entry.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_shared_projection_entry.md)
- [structural_rewrite_phase4_planning_projection_snapshot.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md)
