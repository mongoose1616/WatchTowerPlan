---
trace_id: trace.capture_first_plan_workspace_bootstrap
id: decision.capture_first_plan_workspace_bootstrap_direction
title: Capture-First Plan Workspace Bootstrap Direction Decision
summary: Records the accepted direction for implementing the requirements-defined
  `plan/**` workspace through a strict capture-first first tranche.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-17T03:30:21Z'
audience: shared
authority: supporting
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

# Capture-First Plan Workspace Bootstrap Direction Decision

## Record Metadata
- `Trace ID`: `trace.capture_first_plan_workspace_bootstrap`
- `Decision ID`: `decision.capture_first_plan_workspace_bootstrap_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.capture_first_plan_workspace_bootstrap`
- `Linked Designs`: `design.features.capture_first_plan_workspace_bootstrap`
- `Linked Implementation Plans`: `design.implementation.capture_first_plan_workspace_bootstrap`
- `Updated At`: `2026-03-17T03:30:21Z`

## Summary
Records the accepted direction for implementing the requirements-defined `plan/**` workspace through a strict capture-first first tranche.

## Decision Statement
Implement [requirements.md](/requirements.md) through a machine-first `plan/**` workspace that requires full initiative capture before execution, keeps authored intake docs inside initiative roots as editable inputs, supports both pack-wide and project-scoped initiative flows in the first tranche, and uses a hard cutover for new work with a later follow-up tranche for legacy history and retention reconciliation.

## Trigger or Source Request
- Implement requirements.md with capture-first initiative capture and storage prioritized before any execution work starts.
- The locked clarification pass resolved the remaining design and governance ambiguities before planning began, including source-of-truth choice, readiness gate strictness, project bootstrap rules, query scope, rendered-surface strictness, and the historical follow-up requirement.

## Current Context and Constraints
- The repository still stores live planning under `docs/planning/**`, even though [requirements.md](/requirements.md) treats that as a current-state compromise rather than the long-term authority model.
- There is no first-class `plan/**` root, initiative-local `.wt/` machine layer, pack-level `plan/.wt/` aggregate root, or project container package today.
- The first implementation slice must be strict about capture-before-execution without turning into a full historical migration program or a speculative "implement every future helper" initiative.

## Applied References and Implications
- [requirements.md](/requirements.md): the accepted direction must honor the target live roots, machine-first authority model, rendered-surface rules, project container rules, and staged implementation order documented there.
- [engineering_design_principles.md](/docs/foundations/engineering_design_principles.md): the new model must keep readable views derived from stronger machine state and keep the authority boundary easy to inspect.
- [repository_standards_posture.md](/docs/foundations/repository_standards_posture.md): the first tranche must maintain one primary authority surface per question, synchronized companions, and explicit gating instead of dual-truth compatibility.
- [repository_scope.md](/docs/foundations/repository_scope.md): the tranche must stay inside the repository's current charter as reusable substrate plus the first internal planning pack, not drift into a separate product runtime or broad history-migration program.

## Affected Surfaces
- requirements.md
- plan/
- core/control_plane/
- core/python/
- docs/planning/
- workflows/

## Options Considered
### Option 1
- Keep `docs/planning/**` as the effective live authority and add more compatibility layers while gradually introducing `plan/**`.
- Strength: lowest immediate change cost.
- Tradeoff: leaves the authority mismatch intact and does not satisfy the strict capture-before-execution requirement.

### Option 2
- Adopt a machine-first `plan/**` workspace now, keep authored intake docs inside each initiative root as editable inputs, enforce a strict readiness gate, support both scope roots in tranche one, and defer history or retention cleanup to a named follow-up tranche.
- Strength: matches the requirements direction and the locked clarification decisions while keeping the first milestone bounded and operationally usable.
- Tradeoff: requires immediate root creation, contract work, cutover work, and new lifecycle enforcement before any implementation benefit lands.

### Option 3
- Jump directly to a pure machine-only model and combine it with historical migration or full retention cleanup in the same tranche.
- Strength: would approach the conceptual endstate fastest if it could land safely.
- Tradeoff: too large for the first milestone, conflicts with the chosen authored-intake transition model, and mixes separate governance cleanup into the bootstrap slice.

## Chosen Outcome
Choose Option 2. The first tranche will create the `plan/**` authority roots, make `plan/.wt/**` the machine root for new live plan work, require a fully captured initiative package before any execution begins, support both pack-wide and project-scoped initiative flows, and cut new operational entrypoints over to the new authority model immediately. Authored intake docs remain allowed inside initiative roots, but they only propose updates after bootstrap; machine state confirms them through authorized-maintainer approval and discrepancy handling. Historical `docs/planning/**` handling and clean-endstate retention reconciliation are deferred into a named follow-up tranche.

## Rationale and Tradeoffs
- This option is the only one that aligns cleanly with the strongest requirements direction while respecting the locked clarification decisions.
- It gives the repo a usable first milestone: one complete capture-first loop for pack-wide work and one for project-scoped work, instead of another round of docs-backed compatibility planning.
- The tradeoff is front-loaded infrastructure work and a temporary operational gap around legacy history surfacing, which is why the follow-up tranche is part of the accepted direction rather than an afterthought.

## Consequences and Follow-Up Impacts
- The repo will gain a first-class `plan/**` workspace and plan-pack machine authority roots.
- Planning, query, sync, and rendered-surface helpers will need to re-root from docs-backed authority to initiative-backed authority.
- The bootstrap-only planning task should close once the finalized planning package and initial execution backlog exist, and bounded implementation tasks should take over.
- A later traced initiative or explicit tranche must reconcile archive policy, history surfacing, and clean-endstate retention with [requirements.md](/requirements.md).

## Risks, Dependencies, and Assumptions
- The approach assumes the first tranche can stay bounded to bootstrap, gating, both root types, and proof, rather than trying to land every possible future pack helper at once.
- The hard cutover assumes new query and rebuild paths can become trustworthy quickly enough that the repo does not need a long dual-authority transition.
- The accepted direction depends on explicit follow-through for the history or retention reconciliation tranche; otherwise the temporary legacy gap becomes accidental long-term policy.

## References
- [requirements.md](/requirements.md)
- [capture_first_plan_workspace_bootstrap.md](/docs/planning/prds/capture_first_plan_workspace_bootstrap.md)
- [capture_first_plan_workspace_bootstrap.md](/docs/planning/design/features/capture_first_plan_workspace_bootstrap.md)
- [repository_scope.md](/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/docs/foundations/engineering_design_principles.md)
- [repository_standards_posture.md](/docs/foundations/repository_standards_posture.md)
