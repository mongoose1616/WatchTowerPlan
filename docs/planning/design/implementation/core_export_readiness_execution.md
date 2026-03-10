---
trace_id: "trace.core_export_readiness_and_optimization"
id: "design.implementation.core_export_readiness_execution"
title: "Core Export Readiness and Optimization Implementation Plan"
summary: "Breaks the export-readiness architecture into concrete in-repo phases that isolate repo-ops, reduce maintenance fan-out, and publish generic pack-facing contracts without extracting the package yet."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T04:44:27Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "core/python/src/watchtower_core/"
  - "core/control_plane/"
  - "docs/commands/core_python/"
  - "docs/standards/"
aliases:
  - "core export execution plan"
  - "core optimization execution plan"
---

# Core Export Readiness and Optimization Implementation Plan

## Record Metadata
- `Trace ID`: `trace.core_export_readiness_and_optimization`
- `Plan ID`: `design.implementation.core_export_readiness_execution`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.core_export_readiness_and_optimization`
- `Linked Decisions`: `None`
- `Source Designs`: `design.features.core_export_ready_architecture`
- `Linked Acceptance Contracts`: `contract.acceptance.core_export_readiness_and_optimization`
- `Updated At`: `2026-03-10T04:44:27Z`

## Summary
Breaks the export-readiness architecture into concrete in-repo phases that isolate repo-ops, reduce maintenance fan-out, and publish generic pack-facing contracts without extracting the package yet.

## Source Request or Design
- Feature design: [core_export_ready_architecture.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_ready_architecture.md)
- PRD: [core_export_readiness_and_optimization.md](/home/j/WatchTowerPlan/docs/planning/prds/core_export_readiness_and_optimization.md)
- User request to synthesize the implementation and optimization goals into one clean initiative that prepares core for future WatchTower product work.

## Scope Summary
- Implement the export-ready boundary in place inside `watchtower_core`.
- Move command, sync, validation, retrieval, and repo-ops authority toward explicit registries and injected interfaces.
- Publish the first generic pack-facing control-plane interfaces and examples.
- Keep the current repo validated and operational during each phase.
- Do not extract a standalone package, wire `WatchTower` to consume it, or bootstrap domain-pack scaffolding in this plan.

## Assumptions and Constraints
- `core/python/` remains the only Python workspace root for this repository.
- `core/control_plane/` remains the canonical versioned machine-readable authority.
- The package name stays `watchtower_core` during this initiative.
- The existing command surface and validation baseline must remain operational while internals move.
- Future CTF support in this phase is limited to generic pack-facing contracts and reusable runtime boundaries.

## Current-State Context
- The current CLI, loader, sync, validation, and model layers are healthy but overly centralized around manual lists and repo-specific assumptions.
- The existing core foundation initiative is closed, so this work needs a new traced initiative instead of implicit follow-up on the old one.
- Existing standards already govern command docs, planning docs, task records, indexes, and schema-backed contracts, which means the main execution burden is keeping same-change companion updates aligned.
- Current repo tooling can already rebuild indexes and trackers deterministically through the local Python workspace.

## Internal Standards and Canonical References Applied
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): the implementation should prefer thin CLI entrypoints, modular services, explicit arguments, and synchronized companion updates.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): all package code, tests, and command execution stay under `core/python/`.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): new generic interfaces must land with fail-closed schemas, examples, and aligned validation surfaces.
- [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md): registry-backed command authority still has to preserve governed command lookup and command-doc alignment.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): retrieval metadata changes must remain index-backed and aligned with README inventories.
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md): workflow-discovery metadata changes must preserve the workflow modules as the procedural authority.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): the initiative must move through durable open tasks instead of relying on implied execution state.
- [git_workflow_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_workflow_standard.md): the work should continue on bounded initiative and task branches with clear trace alignment and linear local history expectations.

## Proposed Technical Approach
- Phase the work so each architectural improvement lands behind current behavior rather than as a large extraction-first rewrite.
- Make CLI registry work the first slice because it reduces the current monolithic import surface and establishes the authority pattern reused by sync and validation families.
- Isolate repo-ops behavior before inverting loader dependencies so reusable layers stop importing planning-repo semantics.
- Add pack-facing interfaces only after the reusable boundary is explicit enough to place them correctly.
- Use import-boundary tests and injected workspace tests to prove the new exportable surface is real, not only implied by folder names.

## Work Breakdown
1. Bootstrap the initiative artifacts, tasks, and the missing git workflow standard.
2. Split the CLI into family modules and introduce registry-backed command definitions, parser builders, and command-index alignment checks.
3. Move repository-specific query, sync, validation, and planning-document semantics into explicit `repo_ops` package surfaces.
4. Introduce `WorkspaceConfig`, `ArtifactSource`, and `ArtifactStore`, then refactor reusable services to consume them instead of implicit repo-root discovery.
5. Replace manual sync and validation family enumerations with registry-driven orchestration and add a coordination slice rebuild path.
6. Extend repository-path and workflow indexes with retrieval metadata and update the related query or ranking logic.
7. Split central models by concern and add import-boundary coverage for reusable versus repo-specific layers.
8. Publish generic pack-facing interface schemas, examples, and validation coverage for future product work.
9. Rebalance CLI tests toward contract assertions and keep the full workspace validation baseline green.

## Dependencies
- The current `watchtower-core` sync and validation commands for deterministic rebuilds.
- Existing planning and standards corpus under `docs/`.
- Existing schema catalog, validator registry, and artifact schemas under `core/control_plane/`.

## Risks
- Large multi-file refactors can leave command docs, indexes, and trackers stale if the sync step is skipped.
- Import-boundary cleanup can expose hidden coupling that takes longer to unwind than the initial module move.
- Retrieval metadata expansion can turn noisy if ranking semantics are added before the consumer logic is updated.
- Generic pack-facing contracts could need revision later if the future product surface proves meaningfully different from this initial abstraction set.

## Validation Plan
- Keep `./.venv/bin/watchtower-core doctor --format json` green through the initiative.
- Run `./.venv/bin/pytest -q`, `./.venv/bin/mypy src`, and `./.venv/bin/ruff check .` after each meaningful implementation slice.
- Rebuild governed indexes and trackers with `./.venv/bin/watchtower-core sync all --write` whenever authoritative planning, standards, or machine-readable surfaces change.
- Add targeted tests for command registry parity, sync and validation registry coverage, injected workspace construction, import boundaries, and coordination-slice rebuild behavior.
- Run `./.venv/bin/watchtower-core validate all` before considering the export-ready boundary stable.

## Rollout or Migration Plan
- Land the refactor in bounded in-repo slices rather than one extraction-first migration.
- Preserve compatibility re-exports where needed while package internals move.
- Treat standalone package extraction and `WatchTower` adoption as explicit follow-up work after this plan is delivered and validated.

## References
- [core_export_readiness_and_optimization.md](/home/j/WatchTowerPlan/docs/planning/prds/core_export_readiness_and_optimization.md)
- [core_export_ready_architecture.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_ready_architecture.md)
- [core_python_foundation.md](/home/j/WatchTowerPlan/docs/planning/prds/core_python_foundation.md)
- [control_plane_loaders_and_schema_store.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/control_plane_loaders_and_schema_store.md)
- [core_export_readiness_and_optimization_acceptance.v1.json](/home/j/WatchTowerPlan/core/control_plane/contracts/acceptance/core_export_readiness_and_optimization_acceptance.v1.json)
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md)
- [git_workflow_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_workflow_standard.md)

## Updated At
- `2026-03-10T04:44:27Z`
