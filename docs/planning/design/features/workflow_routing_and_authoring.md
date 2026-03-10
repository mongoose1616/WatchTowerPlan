---
trace_id: "trace.workflow_system_operationalization"
id: "design.features.workflow_routing_and_authoring"
title: "Workflow Routing and Authoring Design"
summary: "Defines the architecture for executable route preview, governed workflow metadata, lean planning scaffolds, and task lifecycle commands."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T21:59:21Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "workflows/"
  - "docs/planning/"
  - "core/control_plane/"
  - "core/python/src/watchtower_core/"
aliases:
  - "workflow routing design"
  - "workflow authoring design"
---

# Workflow Routing and Authoring Design

## Record Metadata
- `Trace ID`: `trace.workflow_system_operationalization`
- `Design ID`: `design.features.workflow_routing_and_authoring`
- `Design Status`: `active`
- `Linked PRDs`: `prd.workflow_system_operationalization`
- `Linked Decisions`: `decision.workflow_operationalization_direction`
- `Linked Implementation Plans`: `design.implementation.workflow_system_operationalization_execution`
- `Updated At`: `2026-03-10T21:59:21Z`

## Summary
Defines the architecture for executable route preview, governed workflow metadata, lean planning scaffolds, and task lifecycle commands.

## Source Request
- User request to verify the workflow assessment findings, remediate the still-valid gaps, and carry the work through the full planning and execution cycle.

## Scope and Feature Boundary
- Covers executable route preview for repository workflow modules.
- Covers governed workflow metadata authority and derived route lookup artifacts.
- Covers CLI scaffolds for planning and task-authoring flows already governed by repo standards and templates.
- Covers reconciliation-family decision guidance.
- Does not replace workflow documents, planning documents, or task records as the authored sources of truth.

## Current-State Context
- `ROUTING_TABLE.md` is the human routing authority, but there is no executable route-preview command.
- Workflow retrieval metadata is still hardcoded in [workflow_index.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/repo_ops/sync/workflow_index.py).
- Task documents already have helpers for parsing and front-matter updates, which means task lifecycle commands can reuse existing invariants instead of reimplementing them.
- The existing lifecycle issues around initiative closeout and zero-open-task active initiatives were already fixed, so this follow-up can stay focused on the still-open workflow-system gaps.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): favor deterministic machine seams and bounded automation.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): keep human and machine workflow surfaces aligned in the same change set.

## Internal Standards and Canonical References Applied
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): `AGENTS.md` and `ROUTING_TABLE.md` remain the human routing authority.
- [routing_table_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/routing_table_md_standard.md): route rows stay compact and table-first.
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md): workflow lookup remains an index derived from workflow docs, but retrieval metadata can come from a governed companion artifact.
- [task_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/task_md_standard.md): task commands must preserve required sections and placement rules.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): task docs remain authoritative and derived trackers stay in sync.

## Design Goals and Constraints
- Add executable support without adding another parallel truth surface.
- Keep scaffold output compact and high-signal rather than template-heavy.
- Reuse current templates, standards, and sync machinery instead of creating new planning formats.
- Preserve the existing durable command contract style and command-doc expectations.

## Options Considered
### Option 1
- Keep workflow routing and planning or task authoring fully documentary.
- Strength: no new code or schemas.
- Tradeoff: leaves the externally verified workflow-system gaps unresolved.

### Option 2
- Add one large autonomous router and one broad planning mutator that rewrites multiple artifact families directly.
- Strength: fewer command entrypoints.
- Tradeoff: too much hidden behavior and too much mutation authority in one surface.

### Option 3
- Add a derived route index, a governed workflow metadata registry, one bounded route-preview command, one bounded planning scaffold family, and one bounded task lifecycle family.
- Strength: keeps authority boundaries explicit while improving execution ergonomics.
- Tradeoff: adds a few new artifacts and command docs that must stay aligned.

## Recommended Design
### Architecture
- Keep `workflows/ROUTING_TABLE.md` as the human routing authority.
- Add a derived `route_index` artifact for machine lookup over route rows.
- Add an authored `workflow_metadata_registry` artifact for machine-owned workflow retrieval metadata currently duplicated in Python.
- Add a `route` CLI family with a `preview` subcommand that consumes the route index and workflow index.
- Add a `plan` CLI family with bounded scaffold operations driven by existing templates.
- Add a `task` CLI family that reuses current task-document helpers for create, update, and transition behavior.

### Data and Interface Impacts
- New governed artifact family: `workflow_metadata_registry`.
- New governed artifact family: `route_index`.
- New sync target: `route-index`.
- New loader and typed-model support for the new registry and index.
- New top-level CLI families: `route`, `plan`, `task`.

### Execution Flow
1. Workflow authors update workflow docs and the workflow metadata registry together when retrieval metadata changes.
2. `sync route-index` rebuilds the machine-readable route index from `ROUTING_TABLE.md`.
3. `route preview` scores route rows from a request or accepts an explicit task type, then returns the merged workflow set.
4. `plan scaffold` and `plan bootstrap` materialize compact planning docs from current repo templates.
5. `task create`, `task update`, and `task transition` mutate governed task docs and then refresh task, initiative, traceability, and coordination surfaces when needed.

### Invariants and Failure Cases
- Route preview must stay advisory and deterministic; it must not claim that the route is authoritative beyond the current routing data.
- Workflow modules and routing docs remain the procedural authority even when route indexes and preview commands exist.
- Planning scaffolds must not emit oversized placeholder sections by default.
- Task lifecycle commands must fail closed on invalid task statuses, unresolved task IDs, duplicate task IDs, or mismatched open versus closed placement.

## Affected Surfaces
- `workflows/ROUTING_TABLE.md`
- `workflows/modules/`
- `core/control_plane/registries/`
- `core/control_plane/indexes/`
- `core/control_plane/schemas/artifacts/`
- `docs/commands/core_python/`
- `docs/standards/`
- `core/python/src/watchtower_core/cli/`
- `core/python/src/watchtower_core/control_plane/`
- `core/python/src/watchtower_core/repo_ops/`
- `core/python/tests/`

## Design Guardrails
- Do not move routing truth into Python constants again.
- Do not let scaffolding commands become the only supported way to author planning docs or tasks.
- Do not generate large boilerplate blocks that add little value relative to the small current project scope.

## Implementation-Planning Handoff Notes
- Land route metadata authority before route preview so the preview command has stable machine inputs.
- Keep scaffold commands compact by default and let operators add optional depth afterward.
- Reuse the current task-document helpers and sync services instead of hand-rolling a second task-state model.

## Dependencies
- Existing command registry and command index sync.
- Existing task-document parsing and sync services.
- Existing planning templates under `docs/templates/`.

## Risks
- New artifact families can drift if schema, registry, validator, and docs updates do not land together.
- Task mutation commands can create file-move edge cases around terminal and non-terminal states.

## References
- [workflow_system_operationalization.md](/home/j/WatchTowerPlan/docs/planning/prds/workflow_system_operationalization.md)
- [end_to_end_repo_rationalization_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/end_to_end_repo_rationalization_direction.md)
- [task_template.md](/home/j/WatchTowerPlan/docs/templates/task_template.md)
- [prd_template.md](/home/j/WatchTowerPlan/docs/templates/prd_template.md)

## Updated At
- `2026-03-10T21:59:21Z`
