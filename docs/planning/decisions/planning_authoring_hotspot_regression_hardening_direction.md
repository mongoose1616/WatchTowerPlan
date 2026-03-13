---
trace_id: trace.planning_authoring_hotspot_regression_hardening
id: decision.planning_authoring_hotspot_regression_hardening_direction
title: Planning Authoring Hotspot Regression Hardening Direction Decision
summary: Records the initial direction decision for Planning Authoring Hotspot Regression
  Hardening.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-13T17:26:00Z'
audience: shared
authority: supporting
---

# Planning Authoring Hotspot Regression Hardening Direction Decision

## Record Metadata
- `Trace ID`: `trace.planning_authoring_hotspot_regression_hardening`
- `Decision ID`: `decision.planning_authoring_hotspot_regression_hardening_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.planning_authoring_hotspot_regression_hardening`
- `Linked Designs`: `design.features.planning_authoring_hotspot_regression_hardening`
- `Linked Implementation Plans`: `design.implementation.planning_authoring_hotspot_regression_hardening`
- `Updated At`: `2026-03-13T17:26:00Z`

## Summary
Records the initial direction decision for Planning Authoring Hotspot Regression Hardening.

## Decision Statement
Recover the planning authoring hotspot through bounded helper extraction: split scaffold-kind specs, scaffold rendering, bootstrap artifact building, planning-surface refresh, and task companion-path repair into explicit repo-local collaborators while keeping `PlanningScaffoldService`, `TaskLifecycleService`, and the `plan` or `task` CLI contracts stable.

## Trigger or Source Request
- Perform another comprehensive internal refactor review, follow the traced task cycle, and continue the review loop until repeated confirmation passes find no new actionable issue.

## Current Context and Constraints
- The earlier `trace.repo_local_hotspot_modularity` correctly reduced the hotspot for the March 11 codebase, but later fixes added the same responsibility concentration back into planning scaffold and task lifecycle files.
- The March 13, 2026 external audit still reproduces `RF-PY-001` and `RF-PY-002` under the planning authoring path, so treating the old trace as final would leave a live same-theme regression unresolved.
- The refactor must preserve current CLI behavior, planning artifact contracts, task mutation behavior, governed companion rewrites, and coordination refresh semantics.

## Applied References and Implications
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): use explicit helper seams inside `repo_ops` rather than a new generic framework or reusable-core migration.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): same-change updates must keep docs, trackers, indexes, acceptance, and evidence aligned with the refactor.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): task path moves still require same-change governed companion repair, but that responsibility does not need to live inside the mutation service itself.
- [prd_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/prd_md_standard.md): scaffold behavior must preserve the current document contracts rather than changing the planning authoring model.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/planning_scaffolds.py
- core/python/src/watchtower_core/repo_ops/planning_scaffold_support.py
- core/python/src/watchtower_core/repo_ops/task_lifecycle.py
- core/python/src/watchtower_core/repo_ops/task_lifecycle_support.py
- core/python/src/watchtower_core/cli/plan_handlers.py
- core/python/src/watchtower_core/cli/task_handlers.py
- core/python/tests/
- docs/planning/

## Options Considered
### Option 1
- Leave the regrown hotspot in place because a prior modularity trace already closed it once.
- Strength: avoids another refactor pass.
- Tradeoff: leaves a confirmed same-theme regression unresolved and makes the fresh refactor audit incomplete.

### Option 2
- Redesign planning and task authoring around a new generalized orchestration framework.
- Strength: could centralize repeated authoring patterns in one new abstraction.
- Tradeoff: too broad for this bounded slice and likely to change behavior or inspectability while solving a narrower hotspot regression.

### Option 3
- Extract bounded helper-backed collaborators for scaffold specs, scaffold rendering, bootstrap artifact building, planning-surface refresh, and task companion-path repair while preserving current top-level services and command behavior.
- Strength: directly targets the regrown responsibilities the audit reproduced.
- Tradeoff: requires disciplined same-change alignment across docs, tests, and planning projections.

## Chosen Outcome
Adopt option 3. The repository should recover smaller explicit seams around planning scaffold and task lifecycle authoring without reopening unrelated modularity slices or changing current runtime contracts.

## Rationale and Tradeoffs
- The live code and the fresh audit both reproduce the hotspot, so the theme is still actionable even though an earlier trace addressed the same area for an older code state.
- Bounded helper extraction is enough because the issue is responsibility concentration, not a fundamentally wrong architecture.
- Keeping the stable services and CLI behavior intact minimizes the risk of operator-facing regressions while still shrinking the implementation blast radius.

## Consequences and Follow-Up Impacts
- New helper modules will exist under `core/python/src/watchtower_core/repo_ops/` to hold scaffold specs, scaffold rendering, bootstrap artifacts, planning-surface refresh, and task companion-path repair logic.
- Adjacent runtime-boundary docs and regression suites will need same-change updates so the hotspot boundary remains easy to inspect after the split.
- If the post-fix review finds another same-theme concentration point nearby, this trace will reopen before closeout rather than deferring it informally.

## Risks, Dependencies, and Assumptions
- Risk: over-splitting the write path could reduce readability.
- Dependency: the current tests and planning projections must stay green after the split or the slice is not complete.
- Assumption: the hotspot can be brought back to a cleaner state without changing command semantics or governed artifact shapes.

## References
- March 13, 2026 refactor audit
- [planning_authoring_hotspot_regression_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/planning_authoring_hotspot_regression_hardening.md)
- [repo_local_hotspot_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/repo_local_hotspot_modularity_hardening.md)
