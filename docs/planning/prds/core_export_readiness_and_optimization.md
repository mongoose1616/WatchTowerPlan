---
trace_id: "trace.core_export_readiness_and_optimization"
id: "prd.core_export_readiness_and_optimization"
title: "Core Export Readiness and Optimization PRD"
summary: "Defines the product and engineering requirements for making WatchTowerPlan core export-ready, lower-fan-out to maintain, and prepared to publish generic pack-facing contracts for future WatchTower work."
type: "prd"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T04:28:34Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/"
  - "core/control_plane/"
  - "docs/planning/design/"
  - "docs/standards/engineering/"
aliases:
  - "core export readiness"
  - "core optimization initiative"
---

# Core Export Readiness and Optimization PRD

## Record Metadata
- `Trace ID`: `trace.core_export_readiness_and_optimization`
- `PRD ID`: `prd.core_export_readiness_and_optimization`
- `Status`: `active`
- `Linked Decisions`: `None`
- `Linked Designs`: `design.features.core_export_ready_architecture`
- `Linked Implementation Plans`: `design.implementation.core_export_readiness_execution`
- `Updated At`: `2026-03-10T04:28:34Z`

## Summary
Defines the product and engineering requirements for making WatchTowerPlan core export-ready, lower-fan-out to maintain, and prepared to publish generic pack-facing contracts for future WatchTower work.

## Problem Statement
The current `watchtower_core` package is functional and validated, but its reusable runtime behavior is still mixed with `WatchTowerPlan`-specific repository operations, hardcoded repository-shape assumptions, and manual orchestration points. That makes future export into `WatchTower` risky, increases maintenance fan-out when command or sync surfaces change, and leaves future pack-facing contracts underspecified.

## Goals
- Make the reusable core substrate explicit without extracting it from the repository yet.
- Reduce maintenance fan-out across CLI wiring, command lookup, sync orchestration, validation orchestration, and retrieval surfaces.
- Replace hardcoded repository-shape assumptions with injected workspace and artifact boundaries.
- Publish generic pack-facing interfaces and provenance contracts needed by future product work without starting domain-pack implementation.
- Keep the current planning repository operational and validated throughout the refactor.

## Non-Goals
- Publishing a standalone package or wiring `WatchTower` to consume it in this initiative.
- Starting `domain_packs/`, offensive-security pack scaffolding, or the CTF implementation layer in this initiative.
- Moving pack-owned mutable content into `core/control_plane/`.
- Replacing repo-local planning, standards, or traceability with GitHub-hosted authority.

## Target Users or Actors
- Repository maintainers responsible for evolving `WatchTowerPlan` safely.
- Engineers implementing reusable runtime behavior under `core/python/`.
- Future `WatchTower` product work that must consume shared core services without importing planning-repo maintenance behavior.
- Future pack-facing workflows that need governed contracts for notes, artifacts, extraction outputs, promoted knowledge, and provenance.

## Key Scenarios
- An engineer needs to add a new CLI command family without touching one monolithic parser file, multiple hand-maintained inventories, and wording-sensitive tests.
- A reusable task, traceability, closeout, evidence, or GitHub integration service needs to run against injected workspace configuration instead of assuming the `WatchTowerPlan` repository layout.
- A repo-specific planning or Markdown-governance concern needs to stay in `WatchTowerPlan` without leaking into the future exported core.
- A future product workflow needs generic contracts for work-item notes, extraction outputs, promoted knowledge, and promotion provenance before domain-specific pack logic is built.

## Requirements
- `req.core_export_readiness_and_optimization.001`: Core must separate exportable reusable layers from `WatchTowerPlan`-specific repo-operations behavior.
- `req.core_export_readiness_and_optimization.002`: Core must replace hardcoded repository discovery and artifact-location assumptions with injected workspace and artifact boundaries.
- `req.core_export_readiness_and_optimization.003`: Core must make CLI command authority registry-driven so runtime wiring, lookup metadata, and docs alignment no longer depend on one monolithic manual surface.
- `req.core_export_readiness_and_optimization.004`: Core must make sync and validation family orchestration registry-driven rather than manual list maintenance.
- `req.core_export_readiness_and_optimization.005`: Core must extend retrieval surfaces so humans and agents can identify authoritative paths and workflows with less README fan-out.
- `req.core_export_readiness_and_optimization.006`: Core must publish generic pack-facing interfaces for work-item notes, artifact manifests, extraction outputs, promoted knowledge, promotion records, and pack indexes.
- `req.core_export_readiness_and_optimization.007`: The initiative must preserve current `WatchTowerPlan` behavior, traceability, and validation posture while refactoring in place.

## Acceptance Criteria
- `ac.core_export_readiness_and_optimization.001`: The planning corpus contains an active PRD, feature design, implementation plan, and durable task set for `trace.core_export_readiness_and_optimization`.
- `ac.core_export_readiness_and_optimization.002`: The package has an explicit reusable-versus-repo-ops boundary, and reusable services can be constructed without implicit repo-root discovery.
- `ac.core_export_readiness_and_optimization.003`: CLI command wiring, command lookup metadata, and sync or validation orchestration are registry-backed rather than maintained through one monolithic manual authority surface.
- `ac.core_export_readiness_and_optimization.004`: Repository-path and workflow retrieval surfaces publish additional ranking or routing metadata that reduces ambiguity about authoritative entrypoints.
- `ac.core_export_readiness_and_optimization.005`: Generic pack-facing contracts and examples exist under `core/control_plane/` without adding domain-pack runtime content.
- `ac.core_export_readiness_and_optimization.006`: The repository remains green on the current Python validation baseline while the refactor lands in place.
- `ac.core_export_readiness_and_optimization.007`: This initiative stops at an export-ready in-repo boundary and does not extract a standalone package or start CTF pack implementation.

## Success Metrics
- Adding or changing one command family requires materially fewer coordinated edits than the current CLI flow.
- Adding a sync or validation family uses one canonical registration path instead of multiple manual enumerations.
- Reusable services can be instantiated against injected workspace configuration in tests without assuming `core/control_plane/` and `core/python/` live in one fixed repo layout.
- The planning corpus shows one active initiative with explicit tasks instead of relying on the closed core foundation initiative for follow-up work.

## Risks and Dependencies
- Over-abstracting too early could slow product delivery instead of reducing coordination cost.
- If repo-specific document semantics leak into exported layers, `WatchTower` adoption will inherit the wrong boundary.
- If planning docs, standards, tasks, and machine-readable indexes are not kept aligned in the same change sets, the traceability and initiative views will drift again.
- The initiative depends on the existing validated `core/python` workspace, current command and planning indexes, and the current task and initiative tracking model.

## Open Questions
- Whether the eventual export should remain an in-repo package boundary or later become a separately published package once the boundary is stable.

## Foundations References Applied
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): core must stop at the shared governed substrate and generic pack-facing contracts rather than absorbing domain-pack implementation.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the refactor must stay deterministic, local-first, schema-first, and explicit about human versus machine authority boundaries.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): human-readable and machine-readable companion surfaces must stay aligned as the architecture and tooling boundaries change.
- [customer_story.md](/home/j/WatchTowerPlan/docs/foundations/customer_story.md): future core contracts should support the first CTF-oriented product path without embedding offensive-security-specific content inside shared core.

## References
- [core_python_foundation.md](/home/j/WatchTowerPlan/docs/planning/prds/core_python_foundation.md)
- [command_documentation_and_lookup.md](/home/j/WatchTowerPlan/docs/planning/design/features/command_documentation_and_lookup.md)
- [local_task_tracking_and_github_sync.md](/home/j/WatchTowerPlan/docs/planning/design/features/local_task_tracking_and_github_sync.md)
- [github_collaboration_scaffolding.md](/home/j/WatchTowerPlan/docs/planning/design/features/github_collaboration_scaffolding.md)
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)

## Updated At
- `2026-03-10T04:28:34Z`
