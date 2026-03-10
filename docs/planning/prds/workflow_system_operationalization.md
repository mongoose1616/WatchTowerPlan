---
trace_id: "trace.workflow_system_operationalization"
id: "prd.workflow_system_operationalization"
title: "Workflow System Operationalization PRD"
summary: "Defines the follow-up work needed to make workflow routing, planning scaffolding, and task lifecycle handling executable, machine-readable, and easier to use before WatchTower implementation begins."
type: "prd"
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
  - "workflow operationalization"
  - "workflow routing follow-up"
---

# Workflow System Operationalization PRD

## Record Metadata
- `Trace ID`: `trace.workflow_system_operationalization`
- `PRD ID`: `prd.workflow_system_operationalization`
- `Status`: `active`
- `Linked Decisions`: `decision.workflow_operationalization_direction`
- `Linked Designs`: `design.features.workflow_routing_and_authoring`
- `Linked Implementation Plans`: `design.implementation.workflow_system_operationalization_execution`
- `Updated At`: `2026-03-10T21:59:21Z`

## Summary
Defines the follow-up work needed to make workflow routing, planning scaffolding, and task lifecycle handling executable, machine-readable, and easier to use before WatchTower implementation begins.

## Problem Statement
The repository now has a strong workflow-document set, healthy sync and validation surfaces, and fixed initiative-closeout lifecycle behavior. The remaining gap is operational support around the workflow system itself. Routing is still documentary rather than executable, workflow retrieval metadata still lives in Python constants instead of a governed machine-readable source, planning-authoring flows still require manual file creation for every new initiative, and task lifecycle or handoff updates still depend on direct Markdown edits. The result is a workflow library that is structurally good but still uneven in day-to-day execution support.

## Goals
- Add an executable route-preview surface that can deterministically project the active workflow set for a request.
- Move workflow retrieval metadata to a governed machine-readable authority surface under `core/control_plane/`.
- Add lean planning scaffolds for PRDs, feature designs, implementation plans, decisions, and initiative bootstrap.
- Add a first-class task CLI for task creation, metadata updates, and handoff-style transitions.
- Clarify the reconciliation workflow family so humans and agents can choose the correct route with less ambiguity.

## Non-Goals
- Replacing workflow modules or `ROUTING_TABLE.md` as the human procedural authority.
- Building a full autonomous router that tries to execute tasks directly from natural-language prompts.
- Collapsing the current planning-family model into one authored artifact.
- Starting WatchTower product implementation or the CTF pack.

## Target Users or Actors
- Maintainers and agents that need deterministic workflow selection without manually replaying the routing table every time.
- Contributors bootstrapping new traced initiatives and bounded planning artifacts.
- Contributors updating task state, blockers, or ownership during active execution.

## Key Scenarios
- An agent receives a user request and needs a compact route preview that says which workflow modules are active and why.
- A maintainer starts a new traced initiative and wants the PRD, feature design, implementation plan, decision, and bootstrap task scaffolded with the correct IDs and paths.
- A task moves from implementation to validation and ownership changes; the task record should update through a command rather than hand-editing front matter and filenames.
- A contributor needs to decide whether a drift issue belongs to documentation-implementation reconciliation, traceability reconciliation, governed artifact reconciliation, or acceptance-evidence reconciliation.

## Requirements
- `req.workflow_system_operationalization.001`: The initiative must publish a traced planning chain, accepted direction, acceptance contract, planning evidence, and bounded task set for workflow operationalization follow-up.
- `req.workflow_system_operationalization.002`: The repository must expose a deterministic route-preview command backed by governed routing data rather than only prose instructions.
- `req.workflow_system_operationalization.003`: Workflow retrieval metadata must move from Python-only constants to a governed machine-readable artifact under `core/control_plane/`.
- `req.workflow_system_operationalization.004`: The CLI must expose planning scaffold operations for the main pre-implementation planning artifact families and initiative bootstrap.
- `req.workflow_system_operationalization.005`: The CLI must expose task lifecycle operations for creating tasks, updating structured task metadata, and handoff-style transitions.
- `req.workflow_system_operationalization.006`: Workflow-routing guidance must include a compact decision aid for choosing the reconciliation family correctly.
- `req.workflow_system_operationalization.007`: The repository must remain green on the current validation baseline throughout the initiative.

## Acceptance Criteria
- `ac.workflow_system_operationalization.001`: The planning corpus publishes the PRD, decision record, feature design, implementation plan, acceptance contract, planning evidence, closed bootstrap task, and bounded execution tasks for this initiative.
- `ac.workflow_system_operationalization.002`: A governed route index and workflow metadata registry exist, and `watchtower-core route preview` can project workflow-module sets in human and JSON forms.
- `ac.workflow_system_operationalization.003`: Planning scaffold commands can generate bounded PRD, feature-design, implementation-plan, decision-record, and initiative-bootstrap documents using the repository templates and conventions.
- `ac.workflow_system_operationalization.004`: Task lifecycle commands can create new governed task docs, update structured task metadata, and perform handoff-style transitions while keeping placement and derived surfaces aligned.
- `ac.workflow_system_operationalization.005`: Reconciliation route guidance clearly distinguishes the four reconciliation families with compact decision support, and the repo remains green after the changes land.

## Success Metrics
- Route selection for common requests no longer depends solely on rereading `ROUTING_TABLE.md`.
- Starting a new initiative requires materially less manual file authoring than the current process.
- Task state transitions require fewer manual document edits and fewer chances to leave trackers stale.

## Risks and Dependencies
- Route preview can create false confidence if it over-claims semantic understanding instead of staying deterministic and bounded.
- Generated planning scaffolds can turn into low-value boilerplate if they are too large or require too many follow-up edits.
- Task mutation commands must preserve current task-document invariants and file-placement rules.
- The initiative depends on the existing command-doc, sync, validation, and planning-index machinery staying aligned in the same change sets.

## Open Questions
- Whether future WatchTower product packs should eventually consume the same route-index pattern for pack-local workflows.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): workflow operationalization should add deterministic, low-ambiguity seams rather than more hidden behavior.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): human and machine workflow surfaces must stay aligned.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): this work should stop at shared workflow infrastructure, not start product implementation.

## References
- [end_to_end_repo_review_and_rationalization.md](/home/j/WatchTowerPlan/docs/planning/prds/end_to_end_repo_review_and_rationalization.md)
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md)
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md)
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md)

## Updated At
- `2026-03-10T21:59:21Z`
