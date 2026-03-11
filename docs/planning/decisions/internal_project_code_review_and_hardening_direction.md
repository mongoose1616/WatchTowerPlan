---
trace_id: trace.internal_project_code_review_and_hardening
id: decision.internal_project_code_review_and_hardening_direction
title: Internal Project Code Review and Hardening Direction Decision
summary: Records the decision to repair lifecycle stale-state bugs with conditional
  scaffold coordination refresh and explicit planning-catalog closeout refresh.
type: decision_record
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

# Internal Project Code Review and Hardening Direction Decision

## Record Metadata
- `Trace ID`: `trace.internal_project_code_review_and_hardening`
- `Decision ID`: `decision.internal_project_code_review_and_hardening_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.internal_project_code_review_and_hardening`
- `Linked Designs`: `design.features.internal_project_code_review_and_hardening`
- `Linked Implementation Plans`: `design.implementation.internal_project_code_review_and_hardening`
- `Updated At`: `2026-03-11T16:10:47Z`

## Summary
Records the decision to repair lifecycle stale-state bugs with conditional scaffold coordination refresh and explicit planning-catalog closeout refresh.

## Decision Statement
Keep the existing planning and traceability validation model intact, refresh coordination-derived surfaces from `plan scaffold --write` only when the target trace already participates in coordination, and make `closeout initiative --write` rebuild and report `planning-catalog` alongside its other derived outputs.

## Trigger or Source Request
- User request to perform an ultra-deep internal project code review and fix every validated issue through closeout and commit.
- Reproduced bug: `watchtower-core query planning` stayed stale after `closeout initiative --write`.
- Reproduced bug: traced scaffold writes left coordination-derived surfaces stale until manual sync.
- Reproduced constraint: unconditional coordination refresh on brand-new single-document scaffolds violates the traceability schema because active traces require `task_ids`.

## Current Context and Constraints
- The repository intentionally distinguishes between standalone planning authoring and bounded coordinated initiative work.
- The coordination slice is supposed to be truthful immediately after normal lifecycle mutations; manual repair syncs are not acceptable as part of the steady-state contract.
- The planning catalog is a canonical machine-readable planning surface and should not lag behind initiative closeout.

## Applied References and Implications
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): traced lifecycle mutations need to leave traceability and coordination-derived surfaces aligned without requiring a repair sync.
- [planning_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_catalog_standard.md): initiative closeout has to refresh the canonical planning join immediately because `query planning` is part of the normal machine-readable contract.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): new scaffolded traces should not enter active coordination until bounded task state exists, which is why scaffold refresh stays conditional instead of unconditional.
- [decision_capture_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/decision_capture_standard.md): this record documents why the repository fixes the write-path defects directly rather than weakening validation or shifting the burden to operators.

## Affected Surfaces
- `core/python/src/watchtower_core/repo_ops/planning_scaffolds.py`
- `core/python/src/watchtower_core/closeout/initiative.py`
- `core/python/src/watchtower_core/cli/closeout_handlers.py`
- `core/python/tests/unit/test_planning_scaffolds.py`
- `core/python/tests/unit/test_initiative_closeout.py`
- `core/python/tests/unit/test_closeout_handlers.py`
- `docs/commands/core_python/watchtower_core_plan_scaffold.md`
- `docs/commands/core_python/watchtower_core_closeout_initiative.md`
- `core/python/README.md`

## Options Considered
### Option 1
- Preserve the current partial refresh behavior and document that operators should run `sync coordination` or `sync all` after scaffold and closeout mutations.
- Strength: smallest code change.
- Tradeoff: leaves still-live stale-state bugs in normal write paths.

### Option 2
- Refresh coordination conditionally for scaffold writes when the trace already participates in coordination or already has traced task state, and explicitly refresh `planning-catalog` in initiative closeout.
- Strength: fixes the reproduced defects while preserving the repository's existing task-handling threshold for new traces.
- Tradeoff: introduces a conditional branch in scaffold write mode that needs explicit regression coverage.

### Option 3
- Refresh coordination unconditionally for scaffold writes and relax traceability expectations so new standalone scaffolded traces can become active without tasks.
- Strength: simpler mutation story for scaffold writes.
- Tradeoff: weakens the repository's bounded-task discipline and turns single planning documents into active initiatives prematurely.

## Chosen Outcome
Adopt option 2. The repository keeps its current validation and task-handling rules, traced scaffold writes refresh coordination only when the trace already belongs there, and initiative closeout explicitly rebuilds `planning-catalog`.

## Rationale and Tradeoffs
- The reproduced defects are stale-state bugs in write paths, not evidence that the validators are too strict.
- Conditional scaffold refresh preserves the important distinction between standalone planning authoring and active, task-bounded initiative work.
- Explicit planning-catalog refresh during closeout is simpler and safer than relying on users to run a separate sync or inferring the new output indirectly.

## Consequences and Follow-Up Impacts
- The closeout JSON payload grows by one additive output-path field.
- Command docs and workspace guidance must describe the refined lifecycle behavior accurately.
- The final evidence artifact should show both reproduced defects and the repo-wide green validation baseline after remediation.

## Risks, Dependencies, and Assumptions
- The scaffold trace-participation check assumes current task-index and traceability data are the right signals for whether coordination refresh is valid.
- The closeout refresh assumes planning-catalog remains a derived consumer of initiative state rather than becoming independently mutable.
- Final derived-surface churn is expected and acceptable because the fix lands across planning docs, tests, and machine-readable indexes together.

## References
- docs/planning/prds/internal_project_code_review_and_hardening.md
- docs/planning/design/features/internal_project_code_review_and_hardening.md
- docs/commands/core_python/watchtower_core_plan_scaffold.md
- docs/commands/core_python/watchtower_core_closeout_initiative.md
