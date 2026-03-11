---
trace_id: trace.internal_project_code_review_followup
id: decision.internal_project_code_review_followup_direction
title: Internal Project Code Review Follow-up Direction Decision
summary: Records the accepted direction to harden bootstrap decision scaffolds,
  require the same decision-semantic rule in aggregate validation, and keep
  bootstrap-only traces in implementation_planning until real execution work
  exists.
type: decision_record
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

# Internal Project Code Review Follow-up Direction Decision

## Record Metadata
- `Trace ID`: `trace.internal_project_code_review_followup`
- `Decision ID`: `decision.internal_project_code_review_followup_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.internal_project_code_review_followup`
- `Linked Designs`: `design.features.internal_project_code_review_followup`
- `Linked Implementation Plans`: `design.implementation.internal_project_code_review_followup`
- `Updated At`: `2026-03-11T16:37:08Z`

## Summary
Records the accepted direction to harden bootstrap decision scaffolds, require the same decision-semantic rule in aggregate validation, and keep bootstrap-only traces in implementation_planning until real execution work exists.

## Decision Statement
Keep the existing repository standards strict, make shared decision scaffolds emit the governed applied-reference section by default, require repo document-semantics validation to enforce that same decision rule, and treat bootstrap-only traces as `implementation_planning` until a non-bootstrap active task exists.

## Trigger or Source Request
- User request to perform another ultra-deep and expansive internal project code review, fix every validated issue end to end, and commit the final closeout.
- Reproduced failure: `./.venv/bin/pytest -q` fails immediately after bootstrap when `--include-decision` is used because the generated decision record omits `Applied References and Implications`.
- Reproduced validation mismatch: `./.venv/bin/watchtower-core validate all --format json` stays green because the decision document-semantics rule still treats that section as optional.
- Reproduced semantic gap: a newly bootstrapped trace with only the bootstrap task projects `execution` in initiative, planning, and coordination surfaces even before bounded execution work exists.

## Current Context and Constraints
- Bootstrap is meant to be a safe, reusable path for creating new traced initiatives and should not require manual repair before the repo baseline is green again.
- Aggregate validation should enforce the same decision-document rule that the repository already treats as mandatory elsewhere so the primary validation command remains trustworthy.
- The repository already treats bootstrap tasks as a special planning concern that is usually closed before bounded execution tasks carry the initiative forward.
- The initiative-tracking standard already defines `implementation_planning` as the phase before execution begins, so the issue is in the projection logic rather than the standard.

## Applied References and Implications
- [decision_capture_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/decision_capture_standard.md): generated decision records must include the applied-reference rationale that makes later review and governance checks meaningful.
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md): the aggregate validation surfaces should preserve the same deterministic rule set that repository workflows and automation rely on.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): bootstrap-only traces should not project `execution` before real execution work exists because the standard already reserves `implementation_planning` for that state.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): the bootstrap task should remain visible and authoritative as a task record even when it does not yet imply execution phase.
- [task_handling_threshold_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_handling_threshold_standard.md): the repository still needs explicit bounded execution tasks after bootstrap, which is why bootstrap-only coordination should remain a planning-phase state.

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

## Options Considered
### Option 1
- Patch the current follow-up trace manually and leave the reusable bootstrap generator and phase logic unchanged.
- Strength: smallest immediate patch.
- Tradeoff: future traces would keep failing the same bootstrap path and coordination would stay misleading.

### Option 2
- Harden shared decision scaffolds and bootstrap validation, require aggregate semantic validation to enforce the same decision rule, and teach initiative-phase projection to keep bootstrap-only traces in planning until non-bootstrap execution work exists.
- Strength: fixes the reusable bootstrap path and aligns machine-readable lifecycle state with authored standards.
- Tradeoff: adds a narrow bootstrap-specific phase rule that must remain explicit in tests and docs.

### Option 3
- Relax the governed decision-doc and initiative-phase expectations so current bootstrap output is treated as acceptable.
- Strength: least implementation work.
- Tradeoff: lowers repository trust by normalizing invalid scaffolds and overstated progress.

## Chosen Outcome
Adopt option 2. Shared bootstrap output should become governed-valid by default, aggregate semantic validation should catch the same decision omission directly, and bootstrap-only traces should remain in `implementation_planning` until real execution work exists.

## Rationale and Tradeoffs
- The failures are in reusable bootstrap behavior, so fixing only the current trace would leave the same defect ready to recur.
- The repository already has the right standards; the scaffold and semantic-validation implementations are the inconsistent layers here.
- A narrow bootstrap-specific phase rule is preferable to a broader rewrite because it addresses the reproduced gap without destabilizing current execution traces.

## Consequences and Follow-Up Impacts
- Bootstrap-related tests need to cover decision-template validity, aggregate decision-semantic validation, and the corrected planning-phase projection.
- The bootstrap command docs and workspace guidance need to explain the refined behavior explicitly.
- This trace should close only after the bootstrap task is closed, the two bounded execution tasks are closed, and the final evidence records the green repo baseline.

## Risks, Dependencies, and Assumptions
- The bootstrap-task exception assumes the `.bootstrap.` task-ID convention remains the durable signal for bootstrap-only work.
- Scaffold validation and aggregate document-semantics validation must stay aligned with the governed decision-index expectations so the same issue does not split across validation layers again.
- Final sync churn is expected because the fix touches planning docs, tasks, and derived projections together.

## References
- docs/planning/prds/internal_project_code_review_follow_up.md
- docs/planning/design/features/internal_project_code_review_follow_up.md
- docs/commands/core_python/watchtower_core_plan_bootstrap.md
- core/python/README.md
