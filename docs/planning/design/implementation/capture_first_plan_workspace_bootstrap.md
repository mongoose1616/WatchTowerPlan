---
trace_id: trace.capture_first_plan_workspace_bootstrap
id: design.implementation.capture_first_plan_workspace_bootstrap
title: Capture-First Plan Workspace Bootstrap Implementation Plan
summary: Breaks Capture-First Plan Workspace Bootstrap into a bounded implementation
  slice.
type: implementation_plan
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

# Capture-First Plan Workspace Bootstrap Implementation Plan

## Record Metadata
- `Trace ID`: `trace.capture_first_plan_workspace_bootstrap`
- `Plan ID`: `design.implementation.capture_first_plan_workspace_bootstrap`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.capture_first_plan_workspace_bootstrap`
- `Linked Decisions`: `decision.capture_first_plan_workspace_bootstrap_direction`
- `Source Designs`: `design.features.capture_first_plan_workspace_bootstrap`
- `Linked Acceptance Contracts`: `contract.acceptance.capture_first_plan_workspace_bootstrap`
- `Updated At`: `2026-03-17T03:30:21Z`

## Summary
Breaks Capture-First Plan Workspace Bootstrap into a bounded implementation slice.

## Source Request or Design
- Implement requirements.md with capture-first initiative capture and storage prioritized before any execution work starts.
- PRD: [capture_first_plan_workspace_bootstrap.md](/docs/planning/prds/capture_first_plan_workspace_bootstrap.md)
- Decision: [capture_first_plan_workspace_bootstrap_direction.md](/docs/planning/decisions/capture_first_plan_workspace_bootstrap_direction.md)
- Feature design: [capture_first_plan_workspace_bootstrap.md](/docs/planning/design/features/capture_first_plan_workspace_bootstrap.md)

## Scope Summary
- Deliver the first bounded implementation tranche for the requirements-defined `plan/**` workspace.
- Cover Stage 1 root seed, Stage 1 tracked bootstrap record, initiative package contracts and gating, pack-wide rendered and query surfaces, project container bootstrap, project-scoped initiative flow, hard cutover for new work, and first-milestone proofs.
- Seed the first bounded execution backlog for those slices so the initiative has actionable implementation work after planning closes.
- Exclude historical `docs/planning/**` migration and permanent retention-policy reconciliation beyond naming the required follow-up tranche.

## Assumptions and Constraints
- [requirements.md](/requirements.md) remains the primary authority for the target model; the locked decision set narrows tranche-one scope and governance without overruling the requirements endstate.
- New live work must cut over to `plan/**` authority rather than adding more `docs/planning/**`-hosted live planning.
- Authored intake docs remain editable inputs, but machine state remains authoritative and all confirmation or discrepancy rules must be enforced.
- The first milestone must prove both a pack-wide and a project-scoped initiative path.
- Legacy history handling, archive cleanup, and clean-endstate purge policy remain explicit follow-up work, not hidden first-tranche scope growth.

## Current-State Context
- Current planning query and sync helpers already provide coordination, planning-catalog, initiative, task, and traceability projections, but they are still built primarily from docs-backed planning families.
- The repository has no `plan/**` roots, no project package roots, no initiative-local `.wt/` state, and no pack-level `plan/.wt/` aggregates yet.
- The bootstrap planning trace already exists under `docs/planning/**`, so the first implementation slice should use that trace to install the new authority model rather than starting another untracked bootstrap.

## Internal Standards and Canonical References Applied
- [requirements.md](/requirements.md): defines the target roots, authority rules, lifecycle families, query expectations, rendered surfaces, and staged implementation direction.
- [traceability_standard.md](/docs/standards/governance/traceability_standard.md): execution work must keep the initiative trace consistent across planning, tasks, acceptance, evidence, and derived projections.
- [task_md_standard.md](/docs/standards/documentation/task_md_standard.md): the execution backlog must stay in bounded task records rather than only in plan prose.
- [watchtower_core_sync.md](/docs/commands/core_python/watchtower_core_sync.md): this work will touch traced planning plus derived indexes and trackers, so rebuild steps must be part of the implementation sequence.
- [implementation_plan_md_standard.md](/docs/standards/documentation/implementation_plan_md_standard.md): the plan needs concrete, execution-oriented slices and validation expectations before implementation starts.

## Proposed Technical Approach
- Use the planning trace to drive one staged bootstrap program rather than several unrelated exploratory changes.
- Sequence the work so the authority substrate lands before higher-level flows:
  - roots and bootstrap record first
  - initiative contracts and readiness gate second
  - pack-wide rendered and query surfaces third
  - project container and project-scoped flow fourth
  - hard cutover and proof last
- Reuse current query and sync infrastructure where practical, but re-root it onto `plan/**` state instead of extending the docs-backed authority model.
- Seed the first implementation backlog directly from this plan so the coordination surfaces can point to concrete slices after the planning package is finalized.

## Work Breakdown
1. Finalize the traced planning baseline, acceptance contract, evidence ledger, and bounded execution task set for this initiative.
2. Add the `plan/**` roots, `plan/.wt/**` aggregate shell, and the tracked Stage 1 bootstrap record flow using the two-step seed.
3. Add initiative package contracts and lifecycle behavior for dual ids, authored intake docs, initiative-local machine state, maximum pre-execution event trail, deferred items, discrepancies, evidence or closeout or promotion shells, doc-to-machine confirmation, and strict readiness gating.
4. Add pack-wide rendered and query surfaces, including coordination, readiness, initiative, task, and discrepancy views, and make readiness fail closed on stale derived surfaces.
5. Add the project bootstrap package, project record and repository-map contracts, project rendered basics, policy-assisted scope classification checks, and the project-scoped initiative bootstrap path.
6. Cut new work over to `plan/**` entrypoints, prove one pack-wide and one project-scoped full capture-first flow, and record the follow-up tranche for history and retention reconciliation.

## Dependencies
- Current planning query and sync infrastructure under `watchtower_core.repo_ops`.
- Actor and approval surfaces that already define repository maintainers and agent roles.
- New plan-pack contract and registry work that will likely live under `plan/.wt/**` with core-shared schemas or helpers where ownership belongs in reusable core.

## Risks
- If the Stage 1 bootstrap record is treated as a documentation note instead of as authoritative machine state, the initiative will violate its own capture-first rule.
- If pack-wide rendered and query surfaces are implemented before initiative contracts and gate logic are stable, the repo will accumulate compatibility surfaces without a clean authority boundary.
- If project bootstrap is deferred too late, the first milestone will prove only pack-wide flow and leave the stricter project-scoped requirement untested.
- Hard cutover will create confusion if the implementation does not update machine and human entrypoints in the same change set.

## Validation Plan
- Validate all new plan-pack contracts, indexes, and rendered-surface inputs through schema-first and fail-closed checks.
- Add negative coverage for incomplete initiative packages, missing project container bootstrap, stale rendered or aggregate surfaces, unconfirmed doc-to-machine proposals, blocking discrepancies, and attempts to enter execution before approval.
- Prove one pack-wide initiative bootstrap and one project-scoped initiative bootstrap end to end through the harness, readiness validation, approval, and `ready_for_execution` transition.
- Rebuild the touched planning and traceability surfaces with `watchtower-core sync` and verify coordination, planning, initiative, task, and other affected query paths against the new trace state.
- Record the explicit history and retention reconciliation follow-up tranche in the planning package so the first milestone does not leave that gap implicit.

## Rollout or Migration Plan
- Introduce the bare `plan/**` roots first so the new authority can exist without inventing a temporary second storage root.
- Treat the new model as a hard cutover for new work only; do not surface historical `docs/planning/**` state in the first-tranche operational path.
- Keep whole-package archive retention as a transitional policy for now and route clean-endstate retention reconciliation to the named follow-up tranche after the first milestone lands.

## References
- [requirements.md](/requirements.md)
- [capture_first_plan_workspace_bootstrap.md](/docs/planning/prds/capture_first_plan_workspace_bootstrap.md)
- [capture_first_plan_workspace_bootstrap.md](/docs/planning/design/features/capture_first_plan_workspace_bootstrap.md)
- [capture_first_plan_workspace_bootstrap_direction.md](/docs/planning/decisions/capture_first_plan_workspace_bootstrap_direction.md)
- [watchtower_core_sync.md](/docs/commands/core_python/watchtower_core_sync.md)
