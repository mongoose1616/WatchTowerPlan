---
trace_id: trace.internal_project_code_review_followup
id: design.implementation.internal_project_code_review_followup
title: Internal Project Code Review Follow-up Implementation Plan
summary: Breaks the follow-up bootstrap hardening work into planning, scaffold-validity,
  semantic-validation, and coordination-phase slices.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-11T16:37:08Z'
audience: shared
authority: supporting
applies_to:
- core/python/
- core/control_plane/
- docs/
---

# Internal Project Code Review Follow-up Implementation Plan

## Record Metadata
- `Trace ID`: `trace.internal_project_code_review_followup`
- `Plan ID`: `design.implementation.internal_project_code_review_followup`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.internal_project_code_review_followup`
- `Linked Decisions`: `decision.internal_project_code_review_followup_direction`
- `Source Designs`: `design.features.internal_project_code_review_followup`
- `Linked Acceptance Contracts`: `contract.acceptance.internal_project_code_review_followup`
- `Updated At`: `2026-03-11T16:37:08Z`

## Summary
Breaks the follow-up bootstrap hardening work into planning, scaffold-validity, semantic-validation, and coordination-phase slices.

## Source Request or Design
- design.features.internal_project_code_review_followup

## Scope Summary
- Replace the placeholder planning chain with the confirmed review findings, accepted direction, and bounded execution tasks.
- Fix decision scaffold rendering and validation so bootstrap-generated decision docs are governed-valid and repo semantic validation enforces the same applied-reference rule.
- Fix initiative and planning phase derivation so bootstrap-only traces remain in `implementation_planning`.
- Update docs, trackers, evidence, and tests in the same change set.

## Assumptions and Constraints
- Bootstrap remains the canonical one-step trace starter and should stay validation-compatible by default.
- The bootstrap task must remain visible as active work while the phase semantics are corrected.
- A bootstrap-only trace should not be treated as active execution until a non-bootstrap active task exists.

## Internal Standards and Canonical References Applied
- [decision_capture_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/decision_capture_standard.md): generated decision records must satisfy the governed section model and remain easy to review.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): phase semantics need to reflect actual lifecycle state rather than optimistic projection.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): task, planning, acceptance, and evidence surfaces must stay aligned through the review and closeout cycle.
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md): the final closeout commit should preserve the trace-linked context in one logical slice.

## Proposed Technical Approach
- Update `planning_scaffold_support.py` so decision scaffolds emit `Applied References and Implications`, and extend scaffold validation to enforce the same explained-bullet section for decision docs.
- Update `planning_documents.py` and `validation/document_semantics.py` so repo semantic validation treats the decision applied-reference section as a required explained-bullet surface and `validate all` catches omissions.
- Update `initiative_index.py` so bootstrap-only active task sets do not force `execution`; the phase should continue to derive from the planning and evidence surfaces until non-bootstrap execution work exists.
- Add targeted unit and integration coverage for both changes before rerunning the full repository baseline.
- Update bootstrap-facing docs and the planning artifacts for this trace so the runtime behavior and the governed review narrative remain aligned.

## Work Breakdown
1. Rewrite the PRD, feature design, implementation plan, decision record, acceptance contract, evidence stub, and bootstrap task so the trace captures the confirmed findings and bounded task split.
2. Implement the decision scaffold hardening, align decision-semantic validation with the same rule, and add regression coverage proving bootstrap-generated decision docs satisfy the governed applied-reference requirement across both targeted and aggregate validation paths.
3. Implement the bootstrap phase-semantics alignment and add regression coverage proving bootstrap-only traces stay in `implementation_planning` until non-bootstrap active tasks exist.
4. Refresh bootstrap docs and workspace guidance, run the full validation stack, close the bootstrap and execution tasks, publish final evidence, and close the initiative.

## Risks
- Decision scaffold and semantic-validation changes may surface latent fixture assumptions because the shared helper is reused across bootstrap and standalone scaffold flows.
- Bootstrap-phase semantics need a precise exception so they do not regress existing active execution traces.
- Final sync churn will be broad because this trace touches planning docs, task records, generated indexes, and coordination views together.

## Validation Plan
- `./.venv/bin/pytest -q tests/unit/test_planning_scaffolds.py tests/unit/test_document_semantics_validation.py tests/unit/test_initiative_index_sync.py tests/integration/test_planning_scaffolds_service.py tests/integration/test_control_plane_artifacts.py`
- `./.venv/bin/python -m mypy src/watchtower_core/repo_ops/planning_scaffold_support.py src/watchtower_core/repo_ops/planning_documents.py src/watchtower_core/repo_ops/validation/document_semantics.py src/watchtower_core/repo_ops/sync/initiative_index.py`
- `./.venv/bin/ruff check src/watchtower_core/repo_ops/planning_scaffold_support.py src/watchtower_core/repo_ops/planning_documents.py src/watchtower_core/repo_ops/validation/document_semantics.py src/watchtower_core/repo_ops/sync/initiative_index.py tests/unit/test_planning_scaffolds.py tests/unit/test_document_semantics_validation.py tests/unit/test_initiative_index_sync.py tests/integration/test_planning_scaffolds_service.py`
- `./.venv/bin/watchtower-core validate acceptance --trace-id trace.internal_project_code_review_followup --format json`
- `./.venv/bin/watchtower-core validate all --format json`
- `./.venv/bin/pytest -q`
- `./.venv/bin/python -m mypy src/watchtower_core`
- `./.venv/bin/ruff check`

## References
- docs/planning/design/features/internal_project_code_review_follow_up.md
- docs/commands/core_python/watchtower_core_plan_bootstrap.md
- core/python/README.md
