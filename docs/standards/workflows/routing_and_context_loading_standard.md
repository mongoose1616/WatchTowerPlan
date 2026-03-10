---
id: "std.workflows.routing_and_context_loading"
title: "Routing and Context Loading Standard"
summary: "This standard defines how repository instructions, routing surfaces, and workflow modules are loaded so task execution starts with the minimum correct context."
type: "standard"
status: "active"
tags:
  - "standard"
  - "workflows"
  - "routing_and_context_loading"
owner: "repository_maintainer"
updated_at: "2026-03-10T00:55:31Z"
audience: "shared"
authority: "authoritative"
---

# Routing and Context Loading Standard

## Summary
This standard defines how repository instructions, routing surfaces, and workflow modules are loaded so task execution starts with the minimum correct context.

## Purpose
Prevent instruction sprawl and overloading by separating root-level guidance, routing logic, and task-specific workflow content into distinct layers with clear behavior.

## Scope
- Applies to the interaction between `AGENTS.md`, `workflows/ROUTING_TABLE.md`, and routed workflow modules.
- Covers load order, minimum-context behavior, ambiguity handling, and module selection rules.
- Does not define the internal contents of every workflow module.

## Use When
- Defining or reviewing repository routing behavior.
- Adding new workflow modules that should be loaded by task classification.
- Deciding whether a rule belongs in `AGENTS.md`, the routing table, or a module.

## Related Standards and Sources
- [agents_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/agents_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [routing_table_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/routing_table_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [agent_workflow_authoring_reference.md](/home/j/WatchTowerPlan/docs/references/agent_workflow_authoring_reference.md): distilled external guidance for separating stable routing context from task-specific extra files to load.
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md): workflow surface that operationalizes or depends on this standard.

## Guidance
- Load `AGENTS.md` first as the repository-wide instruction wrapper.
- Apply only the global rules from `AGENTS.md` before task routing.
- After reading `AGENTS.md`, consult `workflows/ROUTING_TABLE.md` to determine the minimum relevant workflow modules.
- Always include the shared core workflow module in routed task sets.
- Load only the minimum modules required for the matched task type or task types.
- Route from the full prompt context rather than exact keyword matching alone. Treat routing-table trigger keywords as examples that help classification, not as an exhaustive command grammar.
- Workflow modules remain repository-available, but they are inactive unless the routing result selects them, the user explicitly requests them, or the active route merges them after new scope or risk is discovered.
- Prefer loading narrow task-family modules plus any required shared phase modules over reintroducing copied cross-cutting steps into every route.
- Treat `AGENTS.md`, `workflows/ROUTING_TABLE.md`, and `workflows/modules/core.md` as the normal routed baseline rather than as per-module load hints.
- Let workflow modules name only the extra repo-local files to load beyond that baseline when they materially change execution.
- Do not force every workflow module to restate the same baseline authorities; that increases token cost without improving routing accuracy.
- If a request includes explicit commit or closeout intent, merge `modules/commit_closeout.md` into the dominant route or use the Commit Closeout route alone when commit creation is the only requested action.
- Do not auto-load `modules/commit_closeout.md` merely because the active task may eventually be committed.
- If multiple task types match, merge the smallest necessary set rather than loading the whole workflow library.
- If a non-documentation workflow uncovers a documentation gap, merge the smallest necessary documentation route into the active task set, including any required shared phase modules not already loaded, rather than handling the gap ad hoc without a documentation workflow.
- If a task's main risk is drift between implementation behavior and companion docs or lookup surfaces, load `modules/documentation_implementation_reconciliation.md` or use the dedicated reconciliation route rather than relying only on broad review or handoff steps.
- If a task's main risk is drift between traced planning or governance artifacts and their companion trackers, family indexes, or unified traceability joins, load `modules/traceability_reconciliation.md` or use the dedicated reconciliation route rather than relying only on planning leaf modules or handoff review.
- If a task's main risk is drift between schema-backed governed artifacts and their companion schemas, examples, indexes, registries, or loader and validator assumptions, load `modules/governed_artifact_reconciliation.md` or use the dedicated reconciliation route rather than relying only on generic validation.
- If the routing result is ambiguous, prefer clarification or the nearest minimal route rather than speculative broad loading.
- Task-specific logic belongs in workflow modules, not in `AGENTS.md`.
- Classification logic belongs in the routing table, not in the workflow modules themselves.
- Prompt-context auto-routing belongs to the routing layer formed by `AGENTS.md` plus `ROUTING_TABLE.md`, not to a separate workflow module.

## Process or Workflow
1. Read `AGENTS.md`.
2. Apply repository-wide constraints and root-level dos and don'ts.
3. Consult `workflows/ROUTING_TABLE.md`.
4. Match the request to the nearest task type or task types using full prompt context rather than exact keyword matching alone.
5. Load `modules/core.md` plus the minimum additional workflow modules required by the routing result, and treat all unselected modules as available but inactive.
6. Load any `Additional Files to Load` sections only after the route is known, and only for the modules that were actually selected.
7. If the request explicitly includes commit creation or change-set closeout, add `modules/commit_closeout.md` to the dominant route or select the Commit Closeout route alone when commit creation is the only requested task.
8. Execute the task using the loaded modules and any directly relevant repository context.
9. If execution reveals a material documentation gap, add the smallest documentation route needed: load `modules/documentation_generation.md` for new docs or `modules/documentation_refresh.md` for stale docs, plus any required shared phase modules not already loaded, unless the gap is minor enough to fix as an adjacent same-change update.
10. If execution reveals a material implementation-versus-documentation drift risk, add `modules/documentation_implementation_reconciliation.md` or switch to the dedicated reconciliation route unless the drift has already been checked explicitly inside the active route.
11. If execution reveals a material traceability-drift risk, add `modules/traceability_reconciliation.md` or switch to the dedicated reconciliation route unless the trace agreement has already been checked explicitly inside the active route.
12. If execution reveals a material governed-artifact coherence risk, add `modules/governed_artifact_reconciliation.md` or switch to the dedicated reconciliation route unless the artifact-family agreement has already been checked explicitly inside the active route.
13. If routing is unclear or incomplete, request clarification or improve the routing surfaces rather than silently broadening context.

## Validation
- A routed task should start with enough context to act correctly but not so much context that unrelated instructions compete.
- The same request should route to the same module set under normal conditions.
- `AGENTS.md`, the routing table, and the workflow modules should not duplicate each other's responsibilities.
- Routing changes should be reflected in all three layers when needed.

## Change Control
- Update this standard when the repository changes how routing or context loading works.
- Update `AGENTS.md`, `ROUTING_TABLE.md`, and related workflow standards together when load order or routing semantics change.

## References
- [agents_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/agents_md_standard.md)
- [routing_table_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/routing_table_md_standard.md)
- [workflow_design_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/workflow_design_standard.md)
- [agent_workflow_authoring_reference.md](/home/j/WatchTowerPlan/docs/references/agent_workflow_authoring_reference.md)

## Notes
- This concern belongs under `workflows/` because it defines routing behavior and context-loading semantics.
- The file-level shape of `AGENTS.md` and `ROUTING_TABLE.md` still belongs under `documentation/`.

## Updated At
- `2026-03-10T00:55:31Z`
