---
trace_id: trace.internal_project_code_review_and_hardening
id: design.implementation.internal_project_code_review_and_hardening
title: Internal Project Code Review and Hardening Implementation Plan
summary: Breaks the code-review remediation into bounded scaffold-sync, closeout-sync,
  and validation slices.
type: implementation_plan
status: active
owner: repository_maintainer
updated_at: '2026-03-11T16:10:47Z'
audience: shared
authority: supporting
applies_to:
- core/python/
- core/control_plane/
- docs/
---

# Internal Project Code Review and Hardening Implementation Plan

## Record Metadata
- `Trace ID`: `trace.internal_project_code_review_and_hardening`
- `Plan ID`: `design.implementation.internal_project_code_review_and_hardening`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.internal_project_code_review_and_hardening`
- `Linked Decisions`: `decision.internal_project_code_review_and_hardening_direction`
- `Source Designs`: `design.features.internal_project_code_review_and_hardening`
- `Linked Acceptance Contracts`: `contract.acceptance.internal_project_code_review_and_hardening`
- `Updated At`: `2026-03-11T16:10:47Z`

## Summary
Breaks the code-review remediation into bounded scaffold-sync, closeout-sync, and validation slices.

## Source Request or Design
- design.features.internal_project_code_review_and_hardening

## Scope Summary
- Complete the traced planning chain for the code-review findings and close the bootstrap task.
- Fix traced scaffold writes so existing coordinated traces refresh their derived machine and human coordination views immediately.
- Fix initiative closeout so `planning-catalog` is refreshed and reported in the closeout payload.
- Update docs, runtime surfaces, tests, trackers, and evidence in the same change.

## Assumptions and Constraints
- Standalone scaffold writes for new traces remain valid planning-authoring operations and do not need to materialize active traceability state.
- `closeout initiative` should continue blocking open tasks by default; this trace only adds a missing derived refresh.
- Additive JSON payload changes are acceptable only when they accurately represent newly written outputs.

## Internal Standards and Canonical References Applied
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): traced planning and closeout state must stay aligned with traceability and derived coordination views.
- [planning_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_catalog_standard.md): planning-catalog is a canonical machine-readable surface and must be refreshed when initiative state changes.
- [git_commit_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/git_commit_standard.md): the final closeout commit should preserve trace-linked context in one logical slice.

## Proposed Technical Approach
- Extend `PlanningScaffoldService.scaffold()` so write mode performs the existing family-specific sync and then conditionally runs `CoordinationSyncService` only when the trace already participates in coordination.
- Extend `InitiativeCloseoutService.close()` to rebuild `planning-catalog` in write mode and report the output path through `InitiativeCloseoutResult` and the CLI handler payload.
- Add or update unit tests for service behavior and handler payloads before the final repo-wide validation pass.
- Update the command docs and workspace README to reflect the refined lifecycle semantics.

## Work Breakdown
1. Rewrite the bootstrap planning artifacts so the trace documents the confirmed code-review findings, the chosen remediation strategy, and the bounded execution tasks.
2. Implement the scaffold-sync fix and add regression coverage proving existing coordinated traces refresh immediately while standalone scaffold writes stay valid.
3. Implement the closeout planning-catalog refresh, expose the new output path, and add regression coverage for both the service and handler surfaces.
4. Refresh companion docs and workspace guidance, rebuild derived surfaces, run the full validation stack, and then close the tasks and initiative.

## Risks
- The conditional scaffold refresh relies on current traceability and task-index state, so the tests need to prove the intended branch clearly.
- Planning-catalog closeout refresh is machine-visible and must not drift from the documented output contract.
- Final tracker and index churn will be broad because this trace touches planning docs, control-plane artifacts, tasks, and derived views together.

## Validation Plan
- `./.venv/bin/pytest -q tests/unit/test_planning_scaffolds.py tests/unit/test_initiative_closeout.py tests/unit/test_closeout_handlers.py`
- `./.venv/bin/python -m mypy src/watchtower_core/repo_ops/planning_scaffolds.py src/watchtower_core/closeout/initiative.py src/watchtower_core/cli/closeout_handlers.py`
- `./.venv/bin/ruff check src/watchtower_core/repo_ops/planning_scaffolds.py src/watchtower_core/closeout/initiative.py src/watchtower_core/cli/closeout_handlers.py tests/unit/test_planning_scaffolds.py tests/unit/test_initiative_closeout.py tests/unit/test_closeout_handlers.py`
- `./.venv/bin/watchtower-core validate all --format json`
- `./.venv/bin/pytest -q`
- `./.venv/bin/python -m mypy src/watchtower_core`
- `./.venv/bin/ruff check`

## References
- docs/planning/design/features/internal_project_code_review_and_hardening.md
- docs/commands/core_python/watchtower_core_plan_scaffold.md
- docs/commands/core_python/watchtower_core_closeout_initiative.md
