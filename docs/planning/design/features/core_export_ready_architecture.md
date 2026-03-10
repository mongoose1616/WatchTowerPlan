---
trace_id: "trace.core_export_readiness_and_optimization"
id: "design.features.core_export_ready_architecture"
title: "Core Export-Ready Architecture Design"
summary: "Defines the in-repo architecture needed to separate reusable core behavior from WatchTowerPlan repo-operations, reduce maintenance fan-out, and publish generic pack-facing contracts."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T04:28:34Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/src/watchtower_core/"
  - "core/control_plane/"
  - "docs/standards/"
  - "docs/planning/design/"
aliases:
  - "core export architecture"
  - "repo ops boundary design"
---

# Core Export-Ready Architecture Design

## Record Metadata
- `Trace ID`: `trace.core_export_readiness_and_optimization`
- `Design ID`: `design.features.core_export_ready_architecture`
- `Design Status`: `active`
- `Linked PRDs`: `prd.core_export_readiness_and_optimization`
- `Linked Decisions`: `None`
- `Linked Implementation Plans`: `design.implementation.core_export_readiness_execution`
- `Updated At`: `2026-03-10T04:28:34Z`

## Summary
Defines the in-repo architecture needed to separate reusable core behavior from WatchTowerPlan repo-operations, reduce maintenance fan-out, and publish generic pack-facing contracts.

## Source Request
- User request to synthesize `IMPLEMENT.md` and `OPTIMIZE.md` into one clean initiative that prepares core for export and future CTF-backed product work without starting WatchTower product implementation yet.

## Scope and Feature Boundary
- Covers the reusable versus repo-specific architecture split inside `watchtower_core`.
- Covers command, sync, validation, retrieval, coordination, and pack-facing contract boundaries needed to make the core export-ready in place.
- Covers the machine-readable and human-readable companion surfaces that must change with the architectural split.
- Does not publish a standalone package, wire `WatchTower` to consume it, or bootstrap domain-pack scaffolding in this design.
- Does not implement the CTF pack or domain-specific workflows in this design.

## Current-State Context
- [main.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/cli/main.py) is the dominant coupling point for CLI registration, help text, and command-family imports.
- [loader.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/control_plane/loader.py) and [paths.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/control_plane/paths.py) still assume the `WatchTowerPlan` repository layout directly.
- [all.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/sync/all.py) and [all.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/validation/all.py) still maintain manual family enumerations.
- [models.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/control_plane/models.py) concentrates many artifact families into one dense shared layer.
- Query, sync, and validation families currently mix reusable coordination logic with repo-specific planning-doc and Markdown-semantics behavior.
- The current workspace is healthy: `doctor`, `pytest`, `mypy`, and `ruff` all pass against the live repo, so the main problem is architecture and maintenance fan-out rather than baseline instability.

## Foundations References Applied
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): the design must preserve the split between domain-agnostic core and future domain-pack implementation.
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): reusable core behavior must stay deterministic, inspectable, and separated from pack-specific or repo-specific authority.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): architecture changes must keep human-readable and machine-readable companion surfaces synchronized instead of introducing parallel truth.
- [customer_story.md](/home/j/WatchTowerPlan/docs/foundations/customer_story.md): the design must prepare core to support future CTF-oriented operator workflows without hard-coding offensive-security concepts into shared layers.

## Internal Standards and Canonical References Applied
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): the refactor must stay inside the canonical Python workspace under `core/python/`.
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): the design should prefer thin CLI entrypoints, modular services, and same-change companion updates.
- [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md): command lookup must remain machine-readable and aligned with human command docs as the command authority model changes.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): retrieval improvements must remain index-backed instead of collapsing into more README scanning.
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md): workflow discovery metadata can grow, but the workflow modules remain the procedural authority.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): new pack-facing contracts must land as governed interfaces with fail-closed schemas and companion examples.
- [core_python_foundation.md](/home/j/WatchTowerPlan/docs/planning/prds/core_python_foundation.md): the new design must build on the existing validated core foundation instead of reopening its closed scope.
- [command_documentation_and_lookup.md](/home/j/WatchTowerPlan/docs/planning/design/features/command_documentation_and_lookup.md): the new command authority model must preserve human command pages while improving machine-authoritative command wiring.

## Design Goals and Constraints
- Make the reusable-versus-repo-ops boundary explicit before any extraction attempt.
- Reduce CLI, sync, and validation maintenance fan-out without weakening traceability or validation guarantees.
- Keep the current repo working throughout the refactor.
- Preserve the current package name and in-repo workspace layout for this initiative.
- Publish only generic pack-facing contracts, not domain-pack implementation.

## Options Considered
### Option 1
- Extract the package first and clean up the architecture afterward.
- Forces the export boundary into immediate focus.
- Was not chosen because it would carry the current repo-specific coupling and manual fan-out into the extracted surface.

### Option 2
- Optimize the current repo in place without defining an exportable boundary.
- Reduces some maintenance cost quickly.
- Was not chosen because it would leave the future `WatchTower` adoption boundary ambiguous and likely require a second major refactor later.

### Option 3
- Modularize in place around an explicit reusable core boundary, registry-first orchestration, and injected workspace interfaces.
- Reduces current maintenance fan-out while creating a usable export boundary for later product work.
- Chosen because it addresses both current repository efficiency and future export readiness in one coherent architecture.

## Recommended Design
### Architecture
- Split `watchtower_core` conceptually into `kernel`, `coordination`, `integrations`, `repo_ops`, and `cli`.
- Treat `kernel`, `coordination`, and `integrations` as the future exportable surface.
- Treat `repo_ops` as the `WatchTowerPlan`-specific surface for planning-doc parsing, Markdown semantics, indexes, trackers, and repository maintenance.
- Keep `cli` thin and registry-driven, with commands registered from lower layers instead of one monolithic import hub.

### Data and Interface Impacts
- Introduce injected infrastructure boundaries:
  - `WorkspaceConfig`
  - `ArtifactSource`
  - `ArtifactStore`
- Introduce registry-backed authority surfaces:
  - `CommandSpec` and `CommandGroupSpec`
  - `SyncFamilySpec`
  - `ValidationFamilySpec`
- Introduce generic pack-facing interfaces under `core/control_plane/schemas/interfaces/` and companion examples for:
  - work-item notes
  - artifact manifests
  - extraction output envelopes
  - promoted knowledge
  - promotion records
  - pack work indexes
  - knowledge indexes
- Extend repository-path and workflow-index entries with retrieval metadata so authoritative entrypoints rank above boundary or scaffold surfaces.

### Execution Flow
1. Authoritative planning docs define the target boundary, migration sequence, and open task set for the initiative.
2. CLI command registration moves to a registry-first hybrid model that drives parser wiring and machine lookup while preserving human command docs.
3. Repo-specific query, sync, validation, and planning-document behavior moves under `repo_ops`.
4. Reusable services switch from repo-root discovery to injected workspace and artifact interfaces.
5. Sync, validation, retrieval, and coordination orchestration move from manual lists to governed registries and deterministic slices.
6. Pack-facing interface contracts land as governed control-plane artifacts, ready for future product work to consume.

### Invariants and Failure Cases
- Reusable layers must not depend on planning-doc structure, repo Markdown semantics, or repo-local command-doc parsing.
- Validation, evidence, closeout, and traceability behavior must remain fail-closed while the boundaries move.
- The CLI must preserve current operator-visible behavior during the refactor even while authority moves behind it.
- New generic interfaces must not import domain terminology or domain-owned mutable state into `core/control_plane/`.

## Affected Surfaces
- `core/python/src/watchtower_core/cli/`
- `core/python/src/watchtower_core/control_plane/`
- `core/python/src/watchtower_core/query/`
- `core/python/src/watchtower_core/sync/`
- `core/python/src/watchtower_core/validation/`
- `core/python/src/watchtower_core/closeout/`
- `core/python/src/watchtower_core/evidence/`
- `core/python/src/watchtower_core/integrations/github/`
- `core/control_plane/schemas/interfaces/`
- `core/control_plane/examples/`
- `core/control_plane/indexes/`
- `docs/commands/core_python/`
- `docs/standards/`

## Design Guardrails
- Do not rename or extract the package in this initiative just to signal architecture.
- Do not let `repo_ops` logic leak back into reusable layers through convenience imports.
- Do not make command docs the machine-authoritative source again once registry-backed command authority exists.
- Do not add domain-pack scaffolding or CTF pack implementation to satisfy generic contract publication.

## Implementation-Planning Handoff Notes
- Break the implementation plan into phases that can land while the current repo stays green.
- Put CLI registry work first because it reduces the largest current coupling point and informs later registry patterns.
- Add explicit import-boundary and dependency-injection tests once the reusable boundary exists.
- Include same-change updates for standards, indexes, trackers, and command docs whenever an authoritative surface changes.

## Dependencies
- Existing `core/python` workspace tooling and validation baseline.
- Existing command, planning, task, traceability, and initiative indexes.
- Existing standards and templates for planning docs, task records, and governed data contracts.

## Risks
- Boundary extraction could become over-engineered if abstractions are defined before a concrete consumer shape exists.
- Registry-first authority could become another layer of duplication if docs and indexes are not clearly derived or reconciled against it.
- The pack-facing interface set could become domain-specific too early if it is drafted from CTF needs without preserving generic naming and provenance rules.

## References
- [core_export_readiness_and_optimization.md](/home/j/WatchTowerPlan/docs/planning/prds/core_export_readiness_and_optimization.md)
- [core_python_foundation.md](/home/j/WatchTowerPlan/docs/planning/prds/core_python_foundation.md)
- [control_plane_loaders_and_schema_store.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/control_plane_loaders_and_schema_store.md)
- [command_documentation_and_lookup.md](/home/j/WatchTowerPlan/docs/planning/design/features/command_documentation_and_lookup.md)
- [local_task_tracking_and_github_sync.md](/home/j/WatchTowerPlan/docs/planning/design/features/local_task_tracking_and_github_sync.md)
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md)

## Updated At
- `2026-03-10T04:28:34Z`
