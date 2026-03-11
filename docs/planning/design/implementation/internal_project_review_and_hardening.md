---
trace_id: trace.internal_project_review_and_hardening
id: design.implementation.internal_project_review_and_hardening
title: Internal Project Review and Hardening Implementation Plan
summary: Breaks the internal review remediation into bounded slices for bootstrap hardening, projection canonicalization, and traced closeout.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-11T15:11:22Z'
audience: shared
authority: supporting
applies_to:
- core/python/
- core/control_plane/
- docs/
- workflows/
---

# Internal Project Review and Hardening Implementation Plan

## Record Metadata
- `Trace ID`: `trace.internal_project_review_and_hardening`
- `Plan ID`: `design.implementation.internal_project_review_and_hardening`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.internal_project_review_and_hardening`
- `Linked Decisions`: `decision.internal_project_review_and_hardening_direction`
- `Source Designs`: `design.features.internal_project_review_and_hardening`
- `Linked Acceptance Contracts`: `contract.acceptance.internal_project_review_and_hardening`
- `Updated At`: `2026-03-11T15:11:22Z`

## Summary
Breaks the internal review remediation into bounded slices for bootstrap hardening, projection canonicalization, and traced closeout.

## Source Request or Design
- Feature design: [internal_project_review_and_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/internal_project_review_and_hardening.md)
- PRD: [internal_project_review_and_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/internal_project_review_and_hardening.md)
- Decision: [internal_project_review_and_hardening_direction.md](/home/j/WatchTowerPlan/docs/planning/decisions/internal_project_review_and_hardening_direction.md)

## Scope Summary
- Complete the current trace's planning baseline so bootstrap state becomes validation-compatible.
- Harden `watchtower-core plan bootstrap` to emit compliant design docs plus the initial acceptance and evidence artifacts.
- Consolidate coordination and planning payload shaping behind shared serializers.
- Close the bootstrap task, execute the bounded follow-up tasks, and close the initiative only after the repository returns to green.

## Assumptions and Constraints
- Acceptance and documentation validators remain strict; the implementation must improve generated artifacts rather than relaxing repository rules.
- Bootstrap dry-run mode must remain side-effect free even if write mode expands the set of artifacts it publishes.
- Query payload shapes must remain stable for existing consumers while internals become less duplicated.
- Tracker and index refreshes must stay in the same change set as any authored planning, contract, or evidence artifacts they depend on.

## Current-State Context
- The current trace already exists in the planning corpus and currently causes `validate all` and `pytest` failures until its planning baseline is completed.
- The bootstrap code path already knows the trace ID, derived IDs, and authored planning surfaces, so it has enough information to generate the matching acceptance contract and baseline evidence without asking the operator for extra inputs.
- The initiative, planning catalog, and coordination query outputs share the same structural fields today but are shaped through separate helper stacks.

## Internal Standards and Canonical References Applied
- [acceptance_contract_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/acceptance_contract_standard.md): bootstrap must publish the contract in the canonical family and keep it aligned with PRD acceptance IDs.
- [acceptance_evidence_reconciliation_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/acceptance_evidence_reconciliation_standard.md): baseline evidence must cover the trace acceptance IDs so `validate all` remains green.
- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md): scaffolded feature-design output must satisfy the repo's applied-reference expectations.
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md): scaffolded implementation-plan output must satisfy the same governed-document expectations.
- [planning_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_catalog_standard.md): projection changes must preserve machine-readable planning structure while reducing duplicate shaping logic.

## Proposed Technical Approach
- Add deterministic scaffold helpers for the applied-reference sections and reuse them in feature-design and implementation-plan rendering.
- Extend `PlanningScaffoldService.bootstrap()` to build and write the acceptance contract, refresh derived planning surfaces, then record a bootstrap validation-evidence artifact and refresh derived mirrors again.
- Surface the new bootstrap artifacts in CLI results and command docs so the write-mode contract is explicit.
- Add a shared projection serialization module and reuse it from initiative-index sync, planning-catalog sync, and coordination/planning query handlers.

## Work Breakdown
1. Replace the trace placeholders with real PRD, decision, design, implementation-plan, acceptance-contract, and evidence content, and create bounded execution tasks from the bootstrap record.
2. Harden scaffold rendering and bootstrap write mode so generated design docs, acceptance contracts, evidence artifacts, result payloads, and command docs stay aligned.
3. Extract shared projection serializers, wire them into sync and query surfaces, and add regression coverage for payload stability.
4. Rebuild derived surfaces, run the full validation baseline, close the bootstrap and execution tasks, and close the initiative with durable evidence.

## Dependencies
- `watchtower_core.repo_ops.task_lifecycle` for bootstrap task creation and closeout updates.
- `watchtower_core.evidence.validation_evidence` for durable evidence recording.
- `watchtower_core.repo_ops.sync` services for tracker and index refreshes.

## Risks
- Bootstrap write ordering could leave partial state if acceptance-contract or evidence recording is inserted at the wrong point in the sync sequence.
- Shared serializer extraction could unintentionally change optional-field omission semantics if regression coverage is incomplete.
- Completing the current trace baseline and changing the reusable bootstrap path in one initiative will create broad but legitimate derived-surface churn.

## Validation Plan
- Run targeted unit and integration tests for planning scaffolds, plan handlers, and coordination/query payloads while implementing the slices.
- Run `./.venv/bin/watchtower-core validate all --format json` after the bootstrap baseline and again after projection consolidation.
- Run `./.venv/bin/pytest -q`, `./.venv/bin/python -m mypy src/watchtower_core`, and `./.venv/bin/ruff check`.
- Record updated validation evidence for this trace before initiative closeout.

## Rollout or Migration Plan
- Land one slice for trace completion plus reusable bootstrap hardening.
- Land one slice for shared projection serialization after the bootstrap path is stable again.
- Perform final sync, validation, task closure, and initiative closeout in the last slice.

## References
- docs/planning/coordination_tracking.md
- docs/commands/core_python/watchtower_core_plan_bootstrap.md
- core/control_plane/contracts/acceptance/README.md
