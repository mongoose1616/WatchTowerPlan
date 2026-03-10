---
trace_id: "trace.workflow_system_operationalization"
id: "design.implementation.workflow_system_operationalization_execution"
title: "Workflow System Operationalization Implementation Plan"
summary: "Breaks workflow-system operationalization into bounded slices for route metadata, route preview, planning scaffolds, task lifecycle commands, and reconciliation guidance."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T21:59:21Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "workflows/"
  - "docs/planning/"
  - "core/control_plane/"
  - "core/python/src/watchtower_core/"
aliases:
  - "workflow operationalization execution"
  - "workflow system implementation plan"
---

# Workflow System Operationalization Implementation Plan

## Record Metadata
- `Trace ID`: `trace.workflow_system_operationalization`
- `Plan ID`: `design.implementation.workflow_system_operationalization_execution`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.workflow_system_operationalization`
- `Linked Decisions`: `decision.workflow_operationalization_direction`
- `Source Designs`: `design.features.workflow_routing_and_authoring`
- `Linked Acceptance Contracts`: `contract.acceptance.workflow_system_operationalization`
- `Updated At`: `2026-03-10T21:59:21Z`

## Summary
Breaks workflow-system operationalization into bounded slices for route metadata, route preview, planning scaffolds, task lifecycle commands, and reconciliation guidance.

## Source Request or Design
- Feature design: [workflow_routing_and_authoring.md](/home/j/WatchTowerPlan/docs/planning/design/features/workflow_routing_and_authoring.md)
- PRD: [workflow_system_operationalization.md](/home/j/WatchTowerPlan/docs/planning/prds/workflow_system_operationalization.md)

## Scope Summary
- Add governed workflow metadata and route lookup artifacts.
- Add route-preview, planning-scaffold, and task-lifecycle command families.
- Tighten reconciliation choice guidance for humans and agents.
- Keep command docs, indexes, schemas, validators, and tests aligned.

## Assumptions and Constraints
- Workflow modules and routing docs stay authoritative.
- Planning docs and task docs remain authored Markdown sources of truth.
- Scaffold output should stay compact and must not assume a large product backlog.

## Current-State Context
- The CLI already has registry-backed top-level families, so new families can plug into the same pattern cleanly.
- The repo already has stable templates for the target planning docs and tasks.
- Task front matter can already be parsed and updated, which reduces the task-command implementation surface.

## Internal Standards and Canonical References Applied
- [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md): new command families must keep command docs and the command index aligned.
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md): workflow lookup stays derived from workflow docs plus governed metadata.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): task commands must refresh the derived task and initiative surfaces in the same change.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): all code and tests stay inside `core/python/`.

## Proposed Technical Approach
- Add the new machine-readable workflow metadata registry and route index first.
- Build route preview on top of those machine inputs rather than parsing ad hoc structures in the CLI.
- Add planning scaffolds as compact template renderers with explicit required inputs.
- Add task lifecycle commands as bounded document and front-matter mutators that reuse existing helpers and sync services.
- Finish with guidance updates and regression coverage for route ambiguity and task placement invariants.

## Work Breakdown
1. Add the workflow metadata registry, route index schema and sync service, loader support, and command-doc or validation surfaces needed for the new artifacts.
2. Add `watchtower-core route preview`, tests, command docs, and root-command examples.
3. Add `watchtower-core plan scaffold` and `watchtower-core plan bootstrap`, plus template-driven rendering tests and command docs.
4. Add `watchtower-core task create`, `watchtower-core task update`, and `watchtower-core task transition`, plus sync-aware tests and command docs.
5. Tighten reconciliation route guidance, refresh generated indexes and trackers, and run the full validation baseline.

## Risks
- Route scoring can mislead if it is too heuristic-heavy or opaque.
- Template rendering can drift from governed templates if the command logic forks instead of reusing them.
- Task lifecycle commands can break traceability if they fail to refresh dependent surfaces consistently.

## Validation Plan
- Run targeted unit tests for workflow metadata loading, route-index sync, route preview, planning scaffold rendering, and task lifecycle mutations.
- Run `uv run watchtower-core sync all --write --format json` after governed-surface changes.
- Run `uv run pytest -q`, `uv run mypy src`, `uv run ruff check .`, `uv run watchtower-core validate all --format json`, and `uv run watchtower-core doctor --format json` before closeout.

## Rollout or Migration Plan
- Land the initiative in small commits: planning bootstrap, route metadata, route preview, planning scaffolds, task CLI, and reconciliation guidance.
- Preserve current behavior for existing query, sync, validation, and closeout surfaces while new families are added.

## References
- [workflow_system_operationalization.md](/home/j/WatchTowerPlan/docs/planning/prds/workflow_system_operationalization.md)
- [workflow_routing_and_authoring.md](/home/j/WatchTowerPlan/docs/planning/design/features/workflow_routing_and_authoring.md)
- [workflow_system_operationalization_acceptance.v1.json](/home/j/WatchTowerPlan/core/control_plane/contracts/acceptance/workflow_system_operationalization_acceptance.v1.json)
- [routing_table_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/routing_table_md_standard.md)

## Updated At
- `2026-03-10T21:59:21Z`
