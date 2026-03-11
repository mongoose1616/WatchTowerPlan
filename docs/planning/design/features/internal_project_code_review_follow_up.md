---
trace_id: trace.internal_project_code_review_followup
id: design.features.internal_project_code_review_followup
title: Internal Project Code Review Follow-up Feature Design
summary: Defines the follow-up design for bootstrap decision-template validity,
  decision-semantic enforcement, and bootstrap-phase coordination semantics.
type: feature_design
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

# Internal Project Code Review Follow-up Feature Design

## Record Metadata
- `Trace ID`: `trace.internal_project_code_review_followup`
- `Design ID`: `design.features.internal_project_code_review_followup`
- `Design Status`: `active`
- `Linked PRDs`: `prd.internal_project_code_review_followup`
- `Linked Decisions`: `decision.internal_project_code_review_followup_direction`
- `Linked Implementation Plans`: `design.implementation.internal_project_code_review_followup`
- `Updated At`: `2026-03-11T16:37:08Z`

## Summary
Defines the follow-up design for bootstrap decision-template validity, decision-semantic enforcement, and bootstrap-phase coordination semantics.

## Source Request
- User request to perform another ultra-deep and expansive internal project code review, fix every identified issue through the normal task cycle, and commit the final closeout.
- Reproduced regression: bootstrap-generated decision docs fail the governed decision-document test because the required applied-reference section is missing.
- Reproduced validation gap: `watchtower-core validate all` still accepts the same missing decision section because the document-semantics validator treats it as optional.
- Reproduced semantic gap: bootstrap-only traces project `execution` even before bounded execution tasks exist.

## Scope and Feature Boundary
- Covers decision-document rendering and validation for `watchtower-core plan bootstrap --include-decision`, document-semantics validation, and decision scaffolds that share the same generation helper.
- Covers initiative and planning phase projection for traces whose only non-terminal task is the generated bootstrap task.
- Covers the docs and regression tests needed to keep bootstrap semantics explicit.
- Does not redesign initiative phases beyond the bootstrap-only case.
- Does not replace the bootstrap task or remove it from active-task projection.

## Current-State Context
- The decision scaffold helper renders the required decision sections but omits `Applied References and Implications`, even though the governed decision docs and integration test suite require that section.
- Full repository validation currently misses the problem because the decision document-semantics validator still treats `Applied References and Implications` as optional even though the governed decision corpus and integration suite treat it as required.
- Initiative-phase derivation currently returns `execution` whenever any non-terminal task exists, without distinguishing a bootstrap governance task from real bounded execution work.
- A newly bootstrapped trace therefore enters coordination as active execution even though the initiative-tracking standard defines `implementation_planning` as the phase before execution has actually started.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): shared scaffolding paths should be valid and deterministic by default because bootstrap is a common repository entrypoint.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): generated docs and derived coordination projections should conform to authored repository standards rather than competing with them.

## Internal Standards and Canonical References Applied
- [decision_capture_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/decision_capture_standard.md): generated decision records must satisfy the governed decision shape and explain the applied references that constrain the decision.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): `implementation_planning` remains the canonical phase until execution has actually started, and initiative projections should not overstate progress.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): bootstrap tasks stay visible as authoritative task records even when they do not yet imply execution phase.
- [task_handling_threshold_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_handling_threshold_standard.md): traced initiatives need explicit bounded tasks, but a bootstrap task alone is not a substitute for the later execution task set.

## Design Goals and Constraints
- Emit governed-valid decision records from shared scaffold helpers without requiring manual patching after bootstrap.
- Keep bootstrap-only traces visible and owned in coordination without projecting them into `execution` prematurely.
- Preserve the existing phase behavior once non-bootstrap active tasks exist.
- Keep the implementation local to scaffold rendering, scaffold validation, and initiative-phase projection rather than rewriting the broader planning model.
- Make the intended bootstrap exception obvious in regression coverage.

## Options Considered
### Option 1
- Patch the generated decision doc manually in each new trace and leave phase semantics unchanged.
- Strength: smallest immediate repo edit.
- Tradeoff: the reusable bootstrap path remains broken and future traces repeat the same failure.

### Option 2
- Harden decision scaffolds to emit the governed applied-reference section by default and treat bootstrap-only traces as `implementation_planning` until non-bootstrap active tasks exist.
- Strength: fixes the reusable bootstrap path and aligns coordination semantics with the authored standard.
- Tradeoff: introduces one bootstrap-specific branch in initiative-phase derivation that needs explicit regression coverage.

### Option 3
- Relax the governed decision-doc test and document that bootstrap traces are allowed to project `execution` early.
- Strength: least implementation work.
- Tradeoff: weakens repository trust by normalizing invalid generated docs and misleading lifecycle state.

## Recommended Design
### Decision Scaffold Hardening
- Add `Applied References and Implications` to the default decision scaffold sections with explained placeholder bullets.
- Extend scaffold validation for decisions to require the same explained-bullet section that the governed document tests and decision index already expect.
- Align repo document-semantics validation with the same required explained-bullet rule so `validate all` catches omissions instead of deferring to the integration suite.
- Cover bootstrap scaffolds, standalone decision scaffolds, and decision-semantic validation in regression tests because they all need to agree on the same rule.

### Bootstrap Phase Semantics
- Keep active bootstrap tasks in task, traceability, initiative, planning, and coordination projections.
- Treat traces whose only active tasks are bootstrap tasks as planning-phase traces when deriving `current_phase`.
- Reuse the existing document and evidence signals after that bootstrap-only check so the phase falls back to `prd`, `design`, `implementation_planning`, `validation`, or `closeout` consistently.
- Continue projecting `execution` as soon as at least one non-bootstrap active task exists.

### Docs and Runtime Contract
- Update the bootstrap command guidance and workspace README so maintainers know bootstrap-generated decision docs are governed-valid by default, `validate all` enforces the same applied-reference rule, and bootstrap-only traces stay in `implementation_planning`.
- Add targeted tests for scaffold generation, decision-semantic validation, and initiative-phase derivation, then preserve the existing full-suite baseline checks.

### Invariants and Failure Cases
- Bootstrap-generated decision docs must not require a manual section repair before the repo test suite passes.
- Bootstrap-only traces must not project `execution` solely because the bootstrap task exists.
- The bootstrap task must remain visible in active-task projection even when the phase stays in planning.

## Affected Surfaces
- `core/python/src/watchtower_core/repo_ops/planning_scaffold_support.py`
- `core/python/src/watchtower_core/repo_ops/planning_documents.py`
- `core/python/src/watchtower_core/repo_ops/validation/document_semantics.py`
- `core/python/src/watchtower_core/repo_ops/sync/initiative_index.py`
- `core/python/tests/unit/test_document_semantics_validation.py`
- `core/python/tests/unit/test_planning_scaffolds.py`
- `core/python/tests/unit/test_initiative_index_sync.py`
- `core/python/tests/integration/test_planning_scaffolds_service.py`
- `docs/commands/core_python/watchtower_core_plan_bootstrap.md`
- `core/python/README.md`

## Design Guardrails
- Do not weaken the governed decision-document expectations to accommodate invalid generated output.
- Do not hide bootstrap tasks from the coordination slice to achieve the phase fix.
- Do not let the bootstrap-specific phase rule affect traces that already have bounded non-bootstrap active tasks.

## Risks
- The phase fix could become too implicit if the bootstrap-task rule is encoded without clear regression tests.
- Scaffold and semantic-validation changes affect shared helpers and could surface latent invalid fixtures if the expectations drift.
- The planning docs, task records, indexes, and trackers will churn together because bootstrap semantics touch both authored and derived planning surfaces.

## References
- docs/planning/prds/internal_project_code_review_follow_up.md
- docs/commands/core_python/watchtower_core_plan_bootstrap.md
- core/python/README.md
