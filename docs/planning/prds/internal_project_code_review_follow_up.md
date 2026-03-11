---
trace_id: trace.internal_project_code_review_followup
id: prd.internal_project_code_review_followup
title: Internal Project Code Review Follow-up PRD
summary: Captures the next ultra-deep internal code-review findings around invalid
  bootstrap decision scaffolds, missing decision-semantic enforcement, and
  bootstrap-phase coordination semantics.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-11T16:37:08Z'
audience: shared
authority: authoritative
applies_to:
- core/python/
- core/control_plane/
- docs/
---

# Internal Project Code Review Follow-up PRD

## Record Metadata
- `Trace ID`: `trace.internal_project_code_review_followup`
- `PRD ID`: `prd.internal_project_code_review_followup`
- `Status`: `active`
- `Linked Decisions`: `decision.internal_project_code_review_followup_direction`
- `Linked Designs`: `design.features.internal_project_code_review_followup`
- `Linked Implementation Plans`: `design.implementation.internal_project_code_review_followup`
- `Updated At`: `2026-03-11T16:37:08Z`

## Summary
Captures the next ultra-deep internal code-review findings around invalid bootstrap decision scaffolds, missing decision-semantic enforcement, and bootstrap-phase coordination semantics.

## Problem Statement
The follow-up internal code review reproduced three still-live issues in the planning bootstrap path. First, `watchtower-core plan bootstrap --include-decision --write` emits a governed decision document that does not include the required `Applied References and Implications` section. Second, the document-semantics path used by `watchtower-core validate all` still treats that decision section as optional, so the aggregate validation surface stays green while the repository integration rules reject the same omission. Third, a bootstrap-only trace that has only the generated bootstrap task is projected into initiative and coordination `execution` phase immediately, even though the repository standard defines `implementation_planning` as the state before bounded execution work has actually started.

These problems undermine the repository's intended bootstrap contract in different ways. The decision-template gap means bootstrap output is not fully validation-compatible with the repo's governed document expectations. The semantic-validation gap means the repository's primary aggregate validation command does not enforce the same rule that the integration suite already treats as mandatory. The phase-semantics gap means the machine-readable current-state layer misstates where a newly bootstrapped initiative sits in its lifecycle, which makes coordination noisier and less trustworthy before real execution tasks exist.

## Goals
- Make bootstrap-generated decision records satisfy the governed decision-document shape by default.
- Keep bootstrap-only traces in `implementation_planning` until non-bootstrap execution work exists.
- Preserve active bootstrap task visibility in task, traceability, initiative, planning, and coordination views while correcting phase semantics.
- Update docs, tests, acceptance artifacts, and derived planning surfaces in the same bounded change.
- Return the repository to a green baseline on validation, tests, type checking, and linting after the fixes land.

## Non-Goals
- Redesigning the bootstrap workflow into a broader initiative-planning wizard.
- Relaxing the governed decision-document tests or initiative-phase standards to tolerate incorrect output.
- Changing task-status vocabulary, command names, or the overall planning-family authority model.
- Reclassifying every non-terminal task type into a new phase taxonomy beyond the bootstrap-specific correction.

## Requirements
- `req.internal_project_code_review_followup.001`: This trace must publish a real PRD, accepted direction decision, feature design, implementation plan, acceptance contract, updated planning-baseline evidence, a closed bootstrap task, and bounded execution tasks for the confirmed follow-up findings.
- `req.internal_project_code_review_followup.002`: `watchtower-core plan bootstrap --include-decision --write` and decision scaffolds must emit the governed `Applied References and Implications` section with explained bullets, and both scaffold validation and repo document-semantics validation must reject decision output that omits or leaves that section unexplained.
- `req.internal_project_code_review_followup.003`: Initiative, planning, and coordination projections must keep bootstrap-only traces in `implementation_planning` until at least one non-bootstrap active task exists, while still projecting the bootstrap task itself as active work.
- `req.internal_project_code_review_followup.004`: Bootstrap command docs, planning guidance, and regression coverage must stay aligned with the decision-scaffold and bootstrap-phase semantics after the fix.
- `req.internal_project_code_review_followup.005`: The repository must return to a green baseline on `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/python -m mypy src/watchtower_core`, and `./.venv/bin/ruff check`.

## Acceptance Criteria
- `ac.internal_project_code_review_followup.001`: This trace publishes the full planning chain, the accepted direction decision, the acceptance contract, updated planning-baseline evidence, the closed bootstrap task, and two bounded execution tasks covering bootstrap decision-scaffold hardening and bootstrap phase-semantics alignment.
- `ac.internal_project_code_review_followup.002`: Regression coverage proves that bootstrap-generated decision records publish the governed applied-reference section and that both targeted decision-semantic validation and aggregate repo validation reject omissions of that section.
- `ac.internal_project_code_review_followup.003`: Regression coverage proves that bootstrap-only traces stay in `implementation_planning` until non-bootstrap execution tasks exist, and that initiative and planning projections stay aligned on the corrected phase.
- `ac.internal_project_code_review_followup.004`: The `plan bootstrap` command docs, workspace guidance, and accepted decision record describe the corrected decision-template and bootstrap-phase behavior accurately.
- `ac.internal_project_code_review_followup.005`: The repository passes `./.venv/bin/watchtower-core validate acceptance --trace-id trace.internal_project_code_review_followup --format json`, `./.venv/bin/watchtower-core validate all --format json`, `./.venv/bin/pytest -q`, `./.venv/bin/python -m mypy src/watchtower_core`, and `./.venv/bin/ruff check` after the trace closes.

## Risks and Dependencies
- The bootstrap decision-template fix touches reusable scaffold generation and needs to stay aligned with the governed decision index, semantic validator, and test expectations.
- The phase-semantics fix changes a high-visibility coordination projection, so the intended bootstrap exception must stay explicit and well tested.
- The trace depends on keeping planning docs, task records, acceptance artifacts, and derived indexes synchronized throughout the review cycle.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): reusable write paths should produce valid outputs by default instead of depending on downstream cleanup or manual interpretation.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): the repository's authored standards remain authoritative, so fixes should align generated artifacts and derived projections to those rules rather than weakening the rules.

## References
- docs/planning/coordination_tracking.md
- core/python/README.md
- docs/standards/governance/initiative_tracking_standard.md
- docs/standards/governance/task_tracking_standard.md
