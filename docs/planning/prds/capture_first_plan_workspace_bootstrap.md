---
trace_id: trace.capture_first_plan_workspace_bootstrap
id: prd.capture_first_plan_workspace_bootstrap
title: Capture-First Plan Workspace Bootstrap PRD
summary: Bootstraps the new plan workspace, initiative-local machine state, and strict
  capture-before-execution gating for pack-wide and project-scoped initiatives.
type: prd
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

# Capture-First Plan Workspace Bootstrap PRD

## Record Metadata
- `Trace ID`: `trace.capture_first_plan_workspace_bootstrap`
- `PRD ID`: `prd.capture_first_plan_workspace_bootstrap`
- `Status`: `active`
- `Linked Decisions`: `decision.capture_first_plan_workspace_bootstrap_direction`
- `Linked Designs`: `design.features.capture_first_plan_workspace_bootstrap`
- `Linked Implementation Plans`: `design.implementation.capture_first_plan_workspace_bootstrap`
- `Updated At`: `2026-03-17T03:30:21Z`

## Summary
Bootstraps the new plan workspace, initiative-local machine state, and strict capture-before-execution gating for pack-wide and project-scoped initiatives.

## Problem Statement
- [requirements.md](/requirements.md) defines an initiative-centric `plan/**` workspace with initiative-local `.wt/` machine state, pack-level `plan/.wt/` aggregates, project containers, rendered visibility views, and hard source-of-truth boundaries, but the current repository still keeps live planning under `docs/planning/**`.
- The repo has no first-class `plan/initiatives/<initiative_slug>/`, `plan/projects/<project_slug>/initiatives/<initiative_slug>/`, or `plan/projects/<project_slug>/` roots, so new work still starts from docs-backed planning families and derived control-plane projections rather than from live initiative containers.
- The repo has no strict capture-before-execution gate for new initiatives. Without that gate, initiatives can begin with partial capture, ambiguous scope placement, missing evidence or closeout shells, and stale rendered or aggregate surfaces.
- The first implementation slice must follow the future authority model in [requirements.md](/requirements.md) while staying bounded: it needs to establish the live workspace, prove both pack-wide and project-scoped initiative flows, and defer legacy history cleanup to a separate follow-up tranche.

## Goals
- Establish the `plan/**` live-work roots and the first tracked bootstrap path that makes `plan/.wt/**` the authoritative machine root for new planning work.
- Require every new initiative to be fully captured before execution starts, including dual ids, authored intake docs, initiative-local machine state, event history, tasks, deferred or discrepancy records when needed, evidence shell, closeout shell, promotion shell, and scope-tied rendered views.
- Support both pack-wide and project-scoped initiative roots in the first tranche, with pack-wide flow primary but project-scoped flow fully provable.
- Deliver a bootstrap workflow harness and readiness validation path that create, validate, gate, approve, and prove one pack-wide and one project-scoped initiative package.
- Record an explicit second tranche for historical migration and retention-policy reconciliation rather than mixing that work into the first milestone.

## Non-Goals
- Migrate the historical `docs/planning/**` corpus into the new `plan/**` model during the first tranche.
- Treat rendered views such as `plan.md`, `progress.md`, `summary.md`, or `plan_overview.md` as manually authoritative authored surfaces.
- Finalize the long-term retention or purge policy for legacy planning history in the first tranche beyond the explicitly transitional archive choice already locked.
- Implement every future registry, schema family, or helper named in [requirements.md](/requirements.md) when it is not needed to prove the first milestone.

## Requirements
- `req.capture_first_plan_workspace_bootstrap.001`: The first tranche must establish `plan/`, `plan/.wt/`, `plan/initiatives/`, and `plan/projects/` through the locked two-step seed, then record the Stage 1 bootstrap itself as tracked machine state inside `plan/.wt/` before broader implementation begins.
- `req.capture_first_plan_workspace_bootstrap.002`: Every new initiative must be bootstrapped from a full initiative package under either `plan/initiatives/<initiative_slug>/` or `plan/projects/<project_slug>/initiatives/<initiative_slug>/`, with required `initiative_id` and `trace_id` derived from one canonical stem, authored intake docs inside the initiative root, authoritative initiative-local `.wt/` state, task state, maximum pre-execution event history, deferred-item artifacts when needed, evidence shell, closeout shell, promotion shell, and rendered views tied to scope.
- `req.capture_first_plan_workspace_bootstrap.003`: The operating model must be machine-first with authored intake docs as editable inputs: docs may propose changes, but machine state confirms them through authorized-maintainer approval, discrepancy handling, and fail-closed gating.
- `req.capture_first_plan_workspace_bootstrap.004`: No implementation, prototype, or execution task may start until the initiative package is complete, machine-valid, reviewed, approved, marked `ready_for_execution`, and free of blocking deferred items, discrepancies, or stale derived surfaces.
- `req.capture_first_plan_workspace_bootstrap.005`: The first tranche must support both pack-wide and project-scoped initiative flows, including policy-assisted manual scope classification, strict full project bootstrap before project-scoped initiative creation, and rendered surfaces appropriate to the initiative scope.
- `req.capture_first_plan_workspace_bootstrap.006`: The bootstrap workflow harness must create initiative packages end to end, seed event history, wire readiness state, expose coordination, readiness, initiative, task, project, and discrepancy query surfaces, and fail closed when rendered views or aggregate indexes drift from authoritative machine state.
- `req.capture_first_plan_workspace_bootstrap.007`: The first milestone must prove the full capture-first loop for one pack-wide initiative and one project-scoped initiative, then record a named follow-up tranche that reconciles legacy history, archive policy, and clean-endstate retention with [requirements.md](/requirements.md). That follow-up now lives at [plan_legacy_history_retention_reconciliation](/home/j/WatchTowerPlan/plan/initiatives/plan_legacy_history_retention_reconciliation/initiative_brief.md).

## Acceptance Criteria
- `ac.capture_first_plan_workspace_bootstrap.001`: The traced planning chain, accepted direction decision, acceptance contract, planning-baseline evidence, and bounded execution task set define the initiative as the first requirements-driven `plan/**` bootstrap slice rather than another docs-backed planning extension.
- `ac.capture_first_plan_workspace_bootstrap.002`: The repo can create the `plan/**` live roots through the two-step seed and immediately persist a tracked Stage 1 bootstrap record under `plan/.wt/`.
- `ac.capture_first_plan_workspace_bootstrap.003`: A pack-wide initiative package can be created by the bootstrap workflow harness with authored intake docs, initiative-local `.wt/` state, event trail, task set, deferred-item handling, evidence shell, closeout shell, promotion shell, scope-tied rendered views, and pre-execution gate state.
- `ac.capture_first_plan_workspace_bootstrap.004`: A project container can be bootstrapped with its required machine package and rendered basics, and a project-scoped initiative package can then be created under `plan/projects/<project_slug>/initiatives/<initiative_slug>/` through the same capture-first gate.
- `ac.capture_first_plan_workspace_bootstrap.005`: Readiness validation fails closed on incomplete package capture, missing project bootstrap, unconfirmed doc-to-machine proposals, stale rendered views, stale aggregate indexes, and attempts to move into execution before approval.
- `ac.capture_first_plan_workspace_bootstrap.006`: The first tranche exposes the planned coordination, readiness, initiative, task, project, and discrepancy query surfaces from the new authority model instead of requiring `docs/planning/**` as the operational source of truth for new work.
- `ac.capture_first_plan_workspace_bootstrap.007`: The implementation plan names a second tranche that reconciles legacy-history handling and retention policy with the requirements endstate after the first capture-first milestone is proven.

## Risks and Dependencies
- [requirements.md](/requirements.md) is intentionally broader than the first tranche; if the implementation does not keep the scope bounded, the bootstrap initiative will sprawl into a general full-runtime rewrite.
- Current query and sync behavior is still largely docs-backed under `watchtower_core.repo_ops`, so the first tranche must re-root authority carefully without breaking current repository coherence during the cutover.
- The hard cutover choice leaves historical `docs/planning/**` state intentionally unsurfaced in the new operational model for now; that is a deliberate temporary gap that the recorded follow-up tranche must close.
- Project-scoped proof depends on introducing the minimum project-record, project-repository-map, and rendered project surfaces early enough that a project-scoped initiative does not become another ad hoc exception path.

## References
- [requirements.md](/requirements.md)
- [repository_scope.md](/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/docs/foundations/engineering_design_principles.md)
- [repository_standards_posture.md](/docs/foundations/repository_standards_posture.md)
