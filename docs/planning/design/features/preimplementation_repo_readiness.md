---
trace_id: "trace.preimplementation_repo_review_and_hardening"
id: "design.features.preimplementation_repo_readiness"
title: "Pre-Implementation Repository Readiness Design"
summary: "Defines the review-backed design for compact documentation entrypoints, a clear machine coordination start-here path, and more modular configurable core package surfaces."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T17:55:24Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/"
  - "docs/planning/"
  - "core/control_plane/"
  - "core/python/src/watchtower_core/"
aliases:
  - "preimplementation readiness design"
  - "repo review remediation design"
---

# Pre-Implementation Repository Readiness Design

## Record Metadata
- `Trace ID`: `trace.preimplementation_repo_review_and_hardening`
- `Design ID`: `design.features.preimplementation_repo_readiness`
- `Design Status`: `active`
- `Linked PRDs`: `prd.preimplementation_repo_review_and_hardening`
- `Linked Decisions`: `decision.preimplementation_machine_coordination_entrypoint`
- `Linked Implementation Plans`: `design.implementation.preimplementation_repo_hardening_execution`
- `Updated At`: `2026-03-10T17:55:24Z`

## Summary
Defines the review-backed design for compact documentation entrypoints, a clear machine coordination start-here path, and more modular configurable core package surfaces.

## Source Request
- User request to conduct a full end-to-end repository review before product implementation and complete the required planning, tasking, implementation, validation, and closeout work.

## Scope and Feature Boundary
- Covers the high-traffic documentation entrypoints where token cost and duplicated inventories are highest.
- Covers the planning coordination path for traced work and how agents should navigate it.
- Covers core Python modularity and supplemental schema loading needed for future external pack-owned artifacts.
- Does not start WatchTower product implementation or CTF/domain-pack runtime work.
- Does not collapse authored planning families into one mixed folder or replace the existing traceability model.

## Current-State Context
- The repository currently passes `doctor`, `validate all`, `pytest`, `mypy`, and `ruff`, so the main issues are structural rather than baseline instability.
- Local Markdown link validation is effectively clean; the review did not surface broken repo-local links.
- A few high-traffic README entrypoints are still oversized for their role:
  - [docs/references/README.md](/home/j/WatchTowerPlan/docs/references/README.md)
  - [docs/commands/core_python/README.md](/home/j/WatchTowerPlan/docs/commands/core_python/README.md)
  - [core/python/README.md](/home/j/WatchTowerPlan/core/python/README.md)
- The repository already has a derived machine coordination artifact in the initiative index, but agent navigation is still ambiguous because that surface is not clearly elevated above the other family indexes for traced coordination.
- The core package still has large monolithic files at [handlers.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/cli/handlers.py) and [models.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/control_plane/models.py).
- Workspace injection exists, but [schemas.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/control_plane/schemas.py) still assumes one local schema catalog and does not provide a first-class extension seam for future external schema sets.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): the chosen design should reduce ambiguity and coupling rather than hiding them behind larger abstractions.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): the design must preserve authoritative source layers and derived companion surfaces instead of creating parallel truth.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): future pack support should stay generic and configurable at the core layer.

## Internal Standards and Canonical References Applied
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): README entrypoints must stay compact and directory-scoped.
- [initiative_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/initiative_index_standard.md): the initiative index already owns the compact machine-readable coordination view for traced work.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): the initiative layer remains the cross-family coordination view rather than an authored replacement for PRDs, designs, or tasks.
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): CLI entrypoints should stay thin and long-lived behavior should move into modular package services.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): modularity work must stay inside the canonical Python workspace.

## Design Goals and Constraints
- Reduce token and scan cost in the most frequently opened orientation docs.
- Give agents one clearly documented machine coordination start-here path for traced work.
- Avoid adding another planning artifact family when the repository already has a suitable derived coordination surface.
- Improve modularity without forcing a breaking public API shift inside the same initiative.
- Add future external schema extensibility without demoting this repo's canonical control-plane catalog.

## Options Considered
### Option 1
- Collapse PRDs, decisions, designs, plans, and tasks into one new authored planning family.
- Simplifies the number of visible planning document families.
- Was not chosen because it would destroy useful authored boundaries and increase merge contention on the human source surfaces.

### Option 2
- Keep the current authored planning families, elevate the existing initiative index as the primary machine coordination start-here surface, compact README entrypoints, and split the largest core monoliths while adding supplemental schema loading.
- Preserves current authority layers while tightening navigation and modularity.
- Chosen because it solves the real friction without creating another artifact family or reopening product scope.

### Option 3
- Limit the work to documentation refresh only.
- Cheapest near-term change.
- Was not chosen because the review also identified package modularity and configuration seams that should be fixed before product work starts.

## Recommended Design
### Documentation Entry Points
- Tighten the README standard so large same-shaped directories prefer grouped entrypoints and governed lookup references over exhaustive file dumps.
- Compact [docs/references/README.md](/home/j/WatchTowerPlan/docs/references/README.md), [docs/commands/core_python/README.md](/home/j/WatchTowerPlan/docs/commands/core_python/README.md), and [core/python/README.md](/home/j/WatchTowerPlan/core/python/README.md) around category entrypoints, common tasks, and query surfaces.

### Planning Coordination
- Keep the authored planning families unchanged.
- Treat the initiative index as the canonical machine coordination entrypoint for traced work.
- Enrich the initiative index with lightweight active-task summaries so agents can answer coordination questions without reopening the task index for the first pass.
- Expose that surface directly through a `watchtower-core query coordination` command while preserving the existing `query initiatives` surface for backward-compatible family lookup.

### Core Modularity and Configurability
- Split [handlers.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/cli/handlers.py) into family-focused handler modules.
- Split [models.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/control_plane/models.py) into smaller model modules grouped by artifact family.
- Preserve compatibility re-exports through package `__init__` files so internal callers can migrate cleanly in one change set.
- Extend the schema store with supplemental schema sets that can be merged into validation for future external pack-owned artifacts without editing the local schema catalog.

## Affected Surfaces
- `docs/references/README.md`
- `docs/commands/core_python/README.md`
- `core/python/README.md`
- `docs/standards/documentation/readme_md_standard.md`
- `docs/templates/readme_template.md`
- `docs/standards/data_contracts/initiative_index_standard.md`
- `docs/standards/governance/initiative_tracking_standard.md`
- `docs/planning/README.md`
- `docs/planning/initiatives/README.md`
- `docs/commands/core_python/`
- `core/control_plane/schemas/artifacts/initiative_index.v1.schema.json`
- `core/control_plane/indexes/initiatives/initiative_index.v1.json`
- `core/python/src/watchtower_core/cli/`
- `core/python/src/watchtower_core/control_plane/`
- `core/python/src/watchtower_core/repo_ops/query/`
- `core/python/src/watchtower_core/repo_ops/sync/initiative_index.py`
- `core/python/tests/`

## Design Guardrails
- Do not create another first-class planning artifact family just to add a new start-here surface.
- Do not move authored planning authority out of PRDs, decisions, designs, plans, or task records.
- Do not make README files recursive directory dumps again once grouped entrypoints are in place.
- Do not treat supplemental schemas as if they were authored by this repository's canonical control plane.

## Implementation-Planning Handoff Notes
- Land the planning bootstrap and decision first so later slices inherit a clear coordination boundary.
- Compact README entrypoints before command and planning guidance updates so later docs can link to the slimmer entrypoints.
- Implement the coordination slice before the core modularity slice so the new query surface is in place while larger code refactors land.
- Keep compatibility imports and command docs updated in the same change sets as the code moves.

## Dependencies
- The existing initiative index, task index, and traceability index.
- The existing workspace injection seam in `watchtower_core.control_plane`.
- The current compact-authoring standards and template set.

## Risks
- Initiative-index enrichment could become a second task authority if it carries too much task detail.
- README compaction could remove useful discoverability if it cuts real entrypoints instead of low-value repetition.
- Compatibility-preserving refactors could leave stale internal imports if tests do not cover the moved modules.

## References
- [preimplementation_repo_review_and_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/preimplementation_repo_review_and_hardening.md)
- [core_export_ready_architecture.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_ready_architecture.md)
- [compact_document_authoring_and_tracking.md](/home/j/WatchTowerPlan/docs/planning/design/features/compact_document_authoring_and_tracking.md)

## Updated At
- `2026-03-10T17:55:24Z`
