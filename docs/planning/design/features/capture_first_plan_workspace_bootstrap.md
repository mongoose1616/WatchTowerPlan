---
trace_id: trace.capture_first_plan_workspace_bootstrap
id: design.features.capture_first_plan_workspace_bootstrap
title: Capture-First Plan Workspace Bootstrap Feature Design
summary: Defines the machine-first `plan/**` workspace design and the first-tranche
  runtime needed to enforce capture-before-execution.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-17T03:30:21Z'
audience: shared
authority: authoritative
applies_to:
- requirements.md
- core/control_plane/
- core/python/
- docs/planning/
- workflows/
aliases:
- capture-first plan workspace
- plan workspace bootstrap
---

# Capture-First Plan Workspace Bootstrap Feature Design

## Record Metadata
- `Trace ID`: `trace.capture_first_plan_workspace_bootstrap`
- `Design ID`: `design.features.capture_first_plan_workspace_bootstrap`
- `Design Status`: `active`
- `Linked PRDs`: `prd.capture_first_plan_workspace_bootstrap`
- `Linked Decisions`: `decision.capture_first_plan_workspace_bootstrap_direction`
- `Linked Implementation Plans`: `design.implementation.capture_first_plan_workspace_bootstrap`
- `Updated At`: `2026-03-17T03:30:21Z`

## Summary
Defines the machine-first `plan/**` workspace design and the first-tranche runtime needed to enforce capture-before-execution.

## Source Request
- Implement requirements.md with capture-first initiative capture and storage prioritized before any execution work starts.
- The locked clarification pass narrowed the first tranche to machine-first authority, maximum upfront capture, strict no-start gating, both root types in tranche one, and a later history or retention reconciliation tranche.

## Scope and Feature Boundary
- Covers the `plan/**` workspace roots, Stage 1 bootstrap seed, initiative container layout, project container layout, rendered-view strategy, query surface expectations, and the readiness or discrepancy model needed for the first tranche.
- Covers the capture-first bootstrap workflow harness and the machine contracts required for initiative state, task state, event history, deferred items, evidence shell, closeout shell, promotion shell, and readiness approval state.
- Covers both pack-wide and project-scoped initiative flows, with pack-wide flow primary and project-scoped proof mandatory in the first milestone.
- Excludes historical `docs/planning/**` migration, permanent archive or purge policy finalization, and any optional future artifact families from [requirements.md](/requirements.md) that are not required to prove the first milestone.

## Current-State Context
- The repository currently keeps live planning under `docs/planning/**`, with coordination, initiative, task, design, PRD, and decision views projected from that docs-backed corpus plus control-plane indexes.
- `watchtower_core.repo_ops` already owns planning query, sync, rendered-tracker, and task-lifecycle helpers, but those helpers still assume docs-backed planning authority rather than initiative-local live state under `plan/**`.
- There is no first-class `plan/`, `plan/.wt/`, `plan/initiatives/`, or `plan/projects/` root today, no initiative-local `.wt/` machine state, and no project container package that can safely host project-scoped initiatives.
- [requirements.md](/requirements.md) is explicit that this is a current-state mismatch and that the long-term authority model is initiative-centric, event-backed, rendered from stronger machine state, and queryable without relying on recursive scans of docs-backed families.

## Foundations References Applied
- [repository_scope.md](/docs/foundations/repository_scope.md): the first tranche must stay inside the current repository's charter as reusable substrate plus the first internal planning pack, not drift into a separate product repo or a broad live product runtime.
- [engineering_design_principles.md](/docs/foundations/engineering_design_principles.md): the design must keep machine authority inspectable, local-first, fail-closed, and clearly separated from rendered human outputs.
- [repository_standards_posture.md](/docs/foundations/repository_standards_posture.md): the design must preserve one primary authority surface per question, synchronized companion artifacts, and explicit gating on high-impact transitions.

## Internal Standards and Canonical References Applied
- [requirements.md](/requirements.md): defines the target `plan/**` workspace shape, authority boundaries, lifecycle contracts, and the first-tranche migration direction this design implements.
- [traceability_standard.md](/docs/standards/governance/traceability_standard.md): the new initiative bootstrap must stay trace-linked to its PRD, decision, design, implementation plan, acceptance contract, evidence, and execution tasks throughout the transition.
- [task_md_standard.md](/docs/standards/documentation/task_md_standard.md): active execution work must stay in bounded task records rather than in implementation-plan prose alone.
- [docs/planning/README.md](/docs/planning/README.md): until the `plan/**` workspace becomes real, the current planning corpus still provides the authoritative traced planning family surfaces that this initiative must replace in a controlled way.
- [watchtower_core_sync.md](/docs/commands/core_python/watchtower_core_sync.md): derived trackers and indexes must rebuild in the same change set whenever traced planning or companion governed artifacts change materially.

## Design Goals and Constraints
- Make `plan/.wt/**` the machine-first authority root for new live planning work without forcing a pure machine-only authoring flow on day one.
- Capture every materially connected initiative item before execution begins, while allowing structured deferred-item contracts only for genuinely unknown items.
- Support both pack-wide and project-scoped initiative roots in the first tranche, with a strict project bootstrap gate and policy-assisted manual scope classification.
- Preserve a hard cutover for new work without dragging legacy `docs/planning/**` history into the first-tranche operational model.
- Keep Stage 1 bootstrap itself tracked and bounded so the first step does not violate the capture-first rule it is meant to introduce.
- Fail closed on stale rendered views, stale aggregate indexes, blocking discrepancies, and unapproved readiness transitions.

## Options Considered
### Option 1
- Keep `docs/planning/**` as the practical authority for new work while adding more compatibility layers and gradually introducing `plan/**`.
- Strength: smallest short-term implementation change and lowest immediate migration friction.
- Tradeoff: leaves the authority mismatch in place, keeps live work docs-backed, and weakens the core requirement that capture and storage happen under the new machine-first model before execution.

### Option 2
- Introduce `plan/**` as the live authority now, with authored intake docs inside each initiative root, initiative-local `.wt/` machine state, strict capture-before-execution gating, and both pack-wide and project-scoped flows supported in the first tranche.
- Strength: matches the requirements direction and the locked clarification decisions while staying practical about authored intake docs and staged execution.
- Tradeoff: requires new contracts, builders, and cutover work before any implementation benefits are realized.

### Option 3
- Jump straight to a pure machine-only initiative model and combine it with historical `docs/planning/**` migration in the same tranche.
- Strength: the cleanest conceptual endstate if it could land safely in one move.
- Tradeoff: too much scope for the first milestone, eliminates the explicitly chosen authored-intake transition model, and mixes legacy cleanup into the capture-first bootstrap slice.

## Recommended Design
### Architecture
- Add the minimal live roots first: `plan/`, `plan/.wt/`, `plan/initiatives/`, and `plan/projects/`.
- Treat the creation of those bare directories as the only pre-record seed step, then immediately create a tracked Stage 1 bootstrap record inside `plan/.wt/`.
- Model pack-wide initiatives under `plan/initiatives/<initiative_slug>/` and project-scoped initiatives under `plan/projects/<project_slug>/initiatives/<initiative_slug>/`.
- Keep authored intake docs inside each initiative root as `initiative_brief.md`, `design_record.md`, `implementation_slice.md`, and optional `decision_notes.md`.
- Keep authoritative machine state inside each initiative-local `.wt/` tree:
  - `initiative.json`
  - event history
  - task state
  - deferred-item artifacts
  - discrepancy records
  - evidence shell
  - closeout shell
  - promotion shell
- Rebuild initiative-local rendered views from machine state only: `plan.md`, `progress.md`, and `summary.md`.
- Rebuild pack-level and project-level visibility from machine state and aggregate indexes rather than from manually maintained docs trackers.

### Data and Interface Impacts
- New live roots and aggregate state under `plan/**`.
- New or updated plan-pack contracts for initiative state, task state, event history, deferred items, discrepancies, approvals, and project containers.
- Bootstrap workflow harness behavior for initiative creation, validation, readiness gating, and approval.
- Query surfaces for coordination, readiness, initiative, task, project, and discrepancy lookup.
- Rebuild paths for pack overview, initiative rendered views, and project rendered views.
- Hard cutover behavior for current planning and coordination entrypoints so new work resolves from `plan/**` authority instead of from `docs/planning/**`.

### Execution Flow
1. Seed `plan/`, `plan/.wt/`, `plan/initiatives/`, and `plan/projects/`, then immediately write the tracked Stage 1 bootstrap record inside `plan/.wt/`.
2. Use the bootstrap workflow harness to create a complete initiative package under the correct root with dual ids, authored intake docs, initiative-local machine state, event trail, tasks, deferred items, evidence shell, closeout shell, promotion shell, and initial rendered views.
3. Validate the package, rebuild required derived surfaces, and keep the initiative in `capture_incomplete` or `ready_for_review` until completeness, review, approval, and `ready_for_execution` all succeed.
4. When authored intake docs change later, record them as proposals and update machine state only through authorized-maintainer confirmation; unresolved proposals create discrepancies with category and severity.
5. For project-scoped work, require a full project container bootstrap package before creating the initiative, then route rendered views and query surfaces through the project root as well as the pack root.
6. Enforce hard cutover for new operational entrypoints so the new query and rebuild paths read from `plan/**` authority and fail closed if derived surfaces become stale.

### Invariants and Failure Cases
- `plan/.wt/**` is the authoritative machine root for new live plan work.
- Rendered views are never manually authoritative; stale rendered views or aggregate indexes are readiness failures.
- Pack-wide initiatives may live only under `plan/initiatives/`; project-scoped initiatives may live only under `plan/projects/<project_slug>/initiatives/`.
- No initiative may begin execution without a full captured package, maximum pre-execution event trail, explicit approval, and a clean `ready_for_execution` transition.
- If a required item is unknown, the initiative must store a deferred-item artifact and respect the item's gating category.
- If a project-scoped initiative is selected without a full project container, bootstrap must fail closed.

## Affected Surfaces
- requirements.md
- plan/
- core/control_plane/
- core/python/
- docs/planning/
- workflows/

## Design Guardrails
- Keep [requirements.md](/requirements.md) as the primary authority for the endstate and use the locked decision set only to narrow the first tranche, not to contradict the requirements.
- Do not let new live work continue to start under `docs/planning/**` once the `plan/**` bootstrap path exists.
- Do not introduce dual truth between authored intake docs and initiative-local machine state; docs propose, machine confirms.
- Do not let rendered views, trackers, or indexes become silent stale compatibility layers. Drift must fail readiness and produce discrepancies.
- Do not leave an active initiative without bounded task records.
- Keep historical `docs/planning/**` handling out of the first-tranche operating model except for the explicitly recorded follow-up tranche.

## Risks
- The initiative could sprawl if the first tranche tries to land every future helper or registry named in [requirements.md](/requirements.md) instead of the minimum set needed to prove the capture-first loop.
- Hard cutover without immediate history surfacing creates a temporary operator gap if the follow-up tranche is not carried forward explicitly.
- Project-scoped flow could become a weak edge path if the project package is treated as a stub rather than as a full preconditioned container.
- The repo's current docs-backed planning runtime may leak assumptions into the new builders and queries unless the implementation keeps the authority boundary explicit.

## References
- [requirements.md](/requirements.md)
- [capture_first_plan_workspace_bootstrap.md](/docs/planning/prds/capture_first_plan_workspace_bootstrap.md)
- [repository_scope.md](/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/docs/foundations/engineering_design_principles.md)
- [repository_standards_posture.md](/docs/foundations/repository_standards_posture.md)
