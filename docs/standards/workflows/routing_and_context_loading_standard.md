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
updated_at: "2026-03-09T05:23:35Z"
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

## Guidance
- Load `AGENTS.md` first as the repository-wide instruction wrapper.
- Apply only the global rules from `AGENTS.md` before task routing.
- After reading `AGENTS.md`, consult `workflows/ROUTING_TABLE.md` to determine the minimum relevant workflow modules.
- Always include the shared core workflow module in routed task sets.
- Load only the minimum modules required for the matched task type or task types.
- Prefer loading narrow task-family modules plus any required shared phase modules over reintroducing copied cross-cutting steps into every route.
- If multiple task types match, merge the smallest necessary set rather than loading the whole workflow library.
- If a non-documentation workflow uncovers a documentation gap, merge the smallest necessary documentation route into the active task set, including any required shared phase modules not already loaded, rather than handling the gap ad hoc without a documentation workflow.
- If a task's main risk is drift between implementation behavior and companion docs or lookup surfaces, load `modules/documentation_implementation_reconciliation.md` or use the dedicated reconciliation route rather than relying only on broad review or handoff steps.
- If the routing result is ambiguous, prefer clarification or the nearest minimal route rather than speculative broad loading.
- Task-specific logic belongs in workflow modules, not in `AGENTS.md`.
- Classification logic belongs in the routing table, not in the workflow modules themselves.

## Process or Workflow
1. Read `AGENTS.md`.
2. Apply repository-wide constraints and root-level dos and don'ts.
3. Consult `workflows/ROUTING_TABLE.md`.
4. Match the request to the nearest task type or task types.
5. Load `modules/core.md` plus the minimum additional workflow modules required by the routing result.
6. Execute the task using the loaded modules and any directly relevant repository context.
7. If execution reveals a material documentation gap, add the smallest documentation route needed: load `modules/documentation_generation.md` for new docs or `modules/documentation_refresh.md` for stale docs, plus any required shared phase modules not already loaded, unless the gap is minor enough to fix as an adjacent same-change update.
8. If execution reveals a material implementation-versus-documentation drift risk, add `modules/documentation_implementation_reconciliation.md` or switch to the dedicated reconciliation route unless the drift has already been checked explicitly inside the active route.
9. If routing is unclear or incomplete, request clarification or improve the routing surfaces rather than silently broadening context.

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

## Notes
- This concern belongs under `workflows/` because it defines routing behavior and context-loading semantics.
- The file-level shape of `AGENTS.md` and `ROUTING_TABLE.md` still belongs under `documentation/`.

## Updated At
- `2026-03-09T05:23:35Z`
