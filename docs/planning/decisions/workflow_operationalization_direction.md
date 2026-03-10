---
trace_id: "trace.workflow_system_operationalization"
id: "decision.workflow_operationalization_direction"
title: "Workflow Operationalization Direction"
summary: "Records the decision to keep workflow documents authoritative while adding machine-readable route and metadata artifacts plus bounded authoring commands."
type: "decision_record"
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
  - "workflow operationalization decision"
  - "workflow routing direction"
---

# Workflow Operationalization Direction

## Record Metadata
- `Trace ID`: `trace.workflow_system_operationalization`
- `Decision ID`: `decision.workflow_operationalization_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.workflow_system_operationalization`
- `Linked Designs`: `design.features.workflow_routing_and_authoring`
- `Linked Implementation Plans`: `design.implementation.workflow_system_operationalization_execution`
- `Updated At`: `2026-03-10T21:59:21Z`

## Summary
This decision records the choice to keep workflow documents authoritative while adding machine-readable route and metadata artifacts plus bounded authoring commands.

## Decision Statement
Keep `AGENTS.md`, `ROUTING_TABLE.md`, and the workflow modules as the human procedural authority, but add governed machine-readable artifacts for route lookup and workflow retrieval metadata, plus bounded CLI surfaces for route preview, planning scaffolds, and task lifecycle operations.

## Trigger or Source Request
The workflow-system follow-up confirmed that the earlier lifecycle issues were already fixed, but executable routing, governed workflow metadata authority, planning scaffolds, and task lifecycle ergonomics still needed concrete operational support.

## Current Context and Constraints
- The routing table already works as a human authority surface and should not be displaced by Python-only logic.
- Workflow metadata that is purely machine-oriented does not belong as a hardcoded Python constant.
- The repo needs more executable support, but not a large autonomous planner that hides decisions from humans.
- The project is still pre-implementation, so scaffolds should stay compact rather than enterprise-sized.

## Applied References and Implications
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): human routing authority remains in `AGENTS.md` plus `ROUTING_TABLE.md`.
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md): workflow lookup can use governed machine metadata without replacing workflow docs.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): task Markdown remains authoritative even when commands mutate structured fields.

## Affected Surfaces
- `workflows/ROUTING_TABLE.md`
- `workflows/modules/`
- `core/control_plane/registries/`
- `core/control_plane/indexes/`
- `docs/commands/core_python/`
- `core/python/src/watchtower_core/cli/`

## Options Considered
### Option 1
- Keep the workflow system fully documentary.
- Strength: no new runtime or control-plane surfaces.
- Tradeoff: leaves the validated workflow-system gaps unresolved.

### Option 2
- Move routing and planning authority into one broad autonomous runtime service.
- Strength: one executable surface.
- Tradeoff: creates a hidden second truth and too much mutation authority in one place.

### Option 3
- Keep human workflow authority where it is, add governed machine companions for route and metadata lookup, and add bounded authoring commands.
- Strength: improves execution support without eroding authority boundaries.
- Tradeoff: adds a few new artifacts and command docs that require same-change maintenance.

## Chosen Outcome
Adopt option 3. The repo keeps its current workflow-document authority model and adds the smallest useful machine and command surfaces to make the workflow system operational.

## Rationale and Tradeoffs
- This keeps durable human reviewability while giving agents and maintainers executable support.
- The new machine artifacts are lookup and metadata companions, not replacements for authored docs.
- The command surfaces stay bounded to scaffolding and structured task mutation instead of claiming to own all planning logic.

## Consequences and Follow-Up Impacts
- Workflow retrieval metadata will move into a governed registry and route rows will gain a derived machine-readable index.
- The CLI will grow with `route`, `plan`, and `task` command families.
- Reconciliation-family guidance should become more explicit so route preview and human routing reinforce the same distinctions.

## Risks, Dependencies, and Assumptions
- The approach assumes route preview can stay useful without attempting full semantic understanding of arbitrary prompts.
- The approach assumes compact scaffolds are enough for the current project size and will not need large generated sections.

## References
- [workflow_system_operationalization.md](/home/j/WatchTowerPlan/docs/planning/prds/workflow_system_operationalization.md)
- [workflow_routing_and_authoring.md](/home/j/WatchTowerPlan/docs/planning/design/features/workflow_routing_and_authoring.md)
- [end_to_end_repo_rationalization_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/end_to_end_repo_rationalization_direction.md)

## Updated At
- `2026-03-10T21:59:21Z`
