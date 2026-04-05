---
id: "std.workflows.routing_and_context_loading"
title: "Routing and Context Loading Standard"
summary: "This standard defines how repository instructions, routing surfaces, and workflow documents are loaded so task execution starts with the minimum correct context."
type: "standard"
status: "active"
tags:
  - "standard"
  - "workflows"
  - "routing_and_context_loading"
owner: "repository_maintainer"
updated_at: "2026-04-05T06:15:00Z"
audience: "shared"
authority: "authoritative"
---

# Routing and Context Loading Standard

## Summary
This standard defines how repository instructions, routing surfaces, and workflow documents are loaded so task execution starts with the minimum correct context.

## Purpose
Prevent instruction sprawl and overloading by separating root-level guidance, routing logic, and task-specific workflow content into distinct layers with clear behavior.

## Scope
- Applies to the interaction between `AGENTS.md`, the authoritative routing tables, and routed workflow documents.
- Covers load order, minimum-context behavior, ambiguity handling, and workflow selection rules.
- Does not define the internal contents of every workflow document.

## Use When
- Defining or reviewing repository routing behavior.
- Adding new workflow documents that should be loaded by task classification.
- Deciding whether a rule belongs in `AGENTS.md`, the routing table, or a workflow document.

## Related Standards and Sources
- [agents_md_standard.md](/core/docs/standards/documentation/agents_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [routing_table_md_standard.md](/core/docs/standards/documentation/routing_table_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [source_and_citation_standard.md](/core/docs/standards/governance/source_and_citation_standard.md): lookup-order discipline should keep authoritative observation separate from later inference or policy selection.
- [workflow_design_standard.md](/core/docs/standards/workflows/workflow_design_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [route_index_standard.md](/core/docs/standards/data_contracts/route_index_standard.md): defines the derived machine-readable route surface used for advisory route preview.
- [agent_workflow_authoring_reference.md](/core/docs/references/agent_workflow_authoring_reference.md): distilled external guidance for separating stable routing context from task-specific extra files to load.
- [core/workflows/ROUTING_TABLE.md](/core/workflows/ROUTING_TABLE.md): shared routing surface that operationalizes or depends on this standard.
- Pack-owned routing surfaces: they operationalize this standard alongside the shared routing table.

## Guidance
- Load `AGENTS.md` first as the repository-wide instruction wrapper.
- Apply only the global rules from `AGENTS.md` before task routing.
- After reading `AGENTS.md`, consult the shared routing table and any pack-owned routing tables to determine the minimum relevant workflow documents.
- Use `watchtower-core route preview` when a focused executable preview helps, but treat it as advisory over the authored routing surfaces rather than as a replacement authority.
- Treat `route_overlay_registry.json` and `route_merge_policy_registry.json` as the governed machine-readable layer for modifier intents such as adversarial lenses, closeout companions, and route-suppression normalization. The overlay registry should publish explicit intent metadata such as `intent_kind`, dominant-route retention mode, companion-route scoring boundaries, and intent-suppression relationships rather than leaving those semantics implicit in Python-only heuristics.
- When governed overlays attach companion task types, allow route-preview consumers to synthesize those companion routes from the route index even if the free-form scorer did not independently hit the companion route, as long as the overlay intent itself matched deterministically.
- When a governed overlay explicitly expresses companion intent such as remediation loops or commit closeout, route-preview consumers should resolve dominant substantive routes first and attach the companion route after that pass instead of letting the companion route crowd out the originating review, implementation, benchmarking, or standards-alignment scope.
- If route preview cannot select any governed route, it may emit workflow-index-derived advisory module suggestions for agent-assisted loading, but those suggestions remain secondary hints and must not be treated as authoritative route activation.
- Treat the authoritative routing tables as the only surface that activates workflow documents for one request.
- Always include the shared core workflow module in routed task sets.
- Load only the minimum workflow documents required for the matched task type or task types.
- Route from the full prompt context rather than exact keyword matching alone. Treat routing-table trigger keywords as examples that help classification, not as an exhaustive command grammar.
- When the active question is which governed surface is authoritative, resolve that first through `watchtower-core query authority`, then move to the narrow family query command, then the exact canonical doc or registry, and only then raw repo search such as `rg` if no governed lookup surface exists or if unindexed implementation detail still needs direct verification.
- Workflow documents remain repository-available, but they are inactive unless the routing result selects them, the user explicitly requests them, or the active route merges them after new scope or risk is discovered.
- Prefer loading narrow task-family modules plus any required workflow roles or shared phase modules over reintroducing copied cross-cutting steps into every route.
- Workflow roles must publish direct role-to-module orchestration through `Composes Modules`, but that section is audit and retrieval metadata unless the routing result also selected those module documents.
- Treat `AGENTS.md`, the authoritative routing tables, and `core/workflows/modules/core.md` as the normal routed baseline rather than as per-module load hints.
- Let workflow documents name only the extra repo-local files to load beyond that baseline when they materially change execution.
- Do not force every workflow document to restate the same baseline authorities; that increases token cost without improving routing accuracy.
- If a request includes explicit commit or closeout intent, merge `modules/commit_closeout.md` into the dominant route or use the Commit Closeout route alone when commit creation is the only requested action.
- Do not auto-load `modules/commit_closeout.md` merely because the active task may eventually be committed.
- If multiple task types match, merge the smallest necessary set rather than loading the whole workflow library.
- If a non-documentation workflow uncovers a documentation gap, merge the smallest necessary documentation route into the active task set, including any required shared phase modules not already loaded, rather than handling the gap ad hoc without a documentation workflow.
- If a request explicitly asks to align documentation or workflow guidance with repository foundations, use the dedicated foundations-alignment review route or merge `modules/foundations_context_review.md` with `modules/documentation_refresh.md` rather than leaving foundations alignment implicit.
- If a task's main risk is drift between implementation behavior and companion docs or lookup surfaces, load `modules/documentation_implementation_reconciliation.md` or use the dedicated reconciliation route rather than relying only on broad review or handoff steps.
- If a task's main risk is drift between traced planning or governance artifacts and their companion trackers, family indexes, or unified traceability joins, load `modules/traceability_reconciliation.md` or use the dedicated reconciliation route rather than relying only on planning leaf modules or handoff review.
- If a task's main risk is drift between schema-backed governed artifacts and their companion schemas, examples, indexes, registries, or loader and validator assumptions, load `modules/governed_artifact_reconciliation.md` or use the dedicated reconciliation route rather than relying only on generic validation.
- If the routing result is ambiguous, prefer clarification or the nearest minimal route rather than speculative broad loading.
- Task-specific logic belongs in workflow documents, not in `AGENTS.md`.
- Classification logic belongs in the routing table, not in the workflow documents themselves.
- Prompt-context auto-routing belongs to the routing layer formed by `AGENTS.md` plus `ROUTING_TABLE.md`, not to a separate workflow document.

## Reconciliation Route Selection
| Primary Drift Boundary | Preferred Route | Typical Surfaces |
|---|---|---|
| Implementation behavior versus companion docs or lookup surfaces | `Documentation-Implementation Reconciliation` | code, tests, CLI help, command pages, README files, examples, lookup indexes |
| Traced planning or governance artifacts versus trackers, initiative views, family indexes, or trace joins | `Traceability Reconciliation` | initiative briefs, design records, implementation slices, decision notes, task or initiative trackers, traceability and initiative indexes |
| Schema-backed artifact families versus schemas, examples, registries, indexes, loaders, or validators | `Governed Artifact Reconciliation` | contracts, schemas, registries, catalogs, examples, validators, loader assumptions |
| One trace's acceptance intent versus its acceptance contract, evidence, validator linkage, or trace coverage | `Acceptance and Evidence Reconciliation` | initiative acceptance IDs, acceptance contracts, validation evidence, validator registry, traceability coverage |

## Process or Workflow
1. Read `AGENTS.md`.
2. Apply repository-wide constraints and root-level dos and don'ts.
3. Consult the shared routing table and any pack-owned routing tables.
4. Match the request to the nearest task type or task types using full prompt context rather than exact keyword matching alone.
5. If the request first asks which governed surface or doc family is authoritative, resolve that with `watchtower-core query authority` before broad repository search or manual directory browsing.
6. Load `modules/core.md` plus the minimum additional workflow documents required by the routing result, and treat all unselected workflow documents as available but inactive.
7. Load any `Additional Files to Load` sections only after the route is known, and only for the workflow documents that were actually selected.
8. If the request explicitly includes commit creation or change-set closeout, add `modules/commit_closeout.md` to the dominant route or select the Commit Closeout route alone when commit creation is the only requested task.
9. Execute the task using the loaded modules and any directly relevant repository context.
10. If execution reveals a material documentation gap, add the smallest documentation route needed: load `modules/documentation_generation.md` for new docs or `modules/documentation_refresh.md` for stale docs, plus any required shared phase modules not already loaded, unless the gap is minor enough to fix as an adjacent same-change update.
11. If execution reveals a material implementation-versus-documentation drift risk, add `modules/documentation_implementation_reconciliation.md` or switch to the dedicated reconciliation route unless the drift has already been checked explicitly inside the active route.
12. If execution reveals a material traceability-drift risk, add `modules/traceability_reconciliation.md` or switch to the dedicated reconciliation route unless the trace agreement has already been checked explicitly inside the active route.
13. If execution reveals a material governed-artifact coherence risk, add `modules/governed_artifact_reconciliation.md` or switch to the dedicated reconciliation route unless the artifact-family agreement has already been checked explicitly inside the active route.
14. If routing is unclear or incomplete, request clarification or improve the routing surfaces rather than silently broadening context.

## Operationalization
- `Modes`: `workflow`
- `Operational Surfaces`: `AGENTS.md`; `core/workflows/modules/core.md`; `core/workflows/ROUTING_TABLE.md`; `<pack>/workflows/ROUTING_TABLE.md`

## Validation
- A routed task should start with enough context to act correctly but not so much context that unrelated instructions compete.
- The same request should route to the same workflow-document set under normal conditions.
- `AGENTS.md`, the routing table, and the workflow documents should not duplicate each other's responsibilities.
- When workflow roles publish `Composes Modules`, the listed module paths should stay coherent with the routed workflow stacks that normally pair with those roles.
- Routing changes should be reflected in all three layers when needed.
- Route-preview, route-index, route-overlay, and route-merge-policy surfaces should stay aligned with `AGENTS.md`, the routing table, and workflow metadata when routing behavior changes.

## Change Control
- Update this standard when the repository changes how routing or context loading works.
- Update `AGENTS.md`, `ROUTING_TABLE.md`, route overlay and merge registries, and related workflow standards together when load order or routing semantics change.

## References
- [agents_md_standard.md](/core/docs/standards/documentation/agents_md_standard.md)
- [routing_table_md_standard.md](/core/docs/standards/documentation/routing_table_md_standard.md)
- [workflow_design_standard.md](/core/docs/standards/workflows/workflow_design_standard.md)
- [route_index_standard.md](/core/docs/standards/data_contracts/route_index_standard.md)
- [agent_workflow_authoring_reference.md](/core/docs/references/agent_workflow_authoring_reference.md)

## Notes
- This concern belongs under the shared and pack-owned workflow roots because it defines routing behavior and context-loading semantics.
- The file-level shape of `AGENTS.md` and `ROUTING_TABLE.md` still belongs under `documentation/`.

## Updated At
- `2026-04-05T06:15:00Z`
