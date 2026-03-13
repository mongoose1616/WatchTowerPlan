---
trace_id: trace.planning_authoring_hotspot_regression_hardening
id: prd.planning_authoring_hotspot_regression_hardening
title: Planning Authoring Hotspot Regression Hardening PRD
summary: Review and refactor the regrown planning scaffold and task lifecycle hotspots
  so helper-backed seams stay explicit, governed companion repair is isolated, and
  the planning authoring path returns to a lower-blast-radius structure without changing
  behavior.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-13T17:26:00Z'
audience: shared
authority: authoritative
---

# Planning Authoring Hotspot Regression Hardening PRD

## Record Metadata
- `Trace ID`: `trace.planning_authoring_hotspot_regression_hardening`
- `PRD ID`: `prd.planning_authoring_hotspot_regression_hardening`
- `Status`: `active`
- `Linked Decisions`: `decision.planning_authoring_hotspot_regression_hardening_direction`
- `Linked Designs`: `design.features.planning_authoring_hotspot_regression_hardening`
- `Linked Implementation Plans`: `design.implementation.planning_authoring_hotspot_regression_hardening`
- `Updated At`: `2026-03-13T17:26:00Z`

## Summary
Review and refactor the regrown planning scaffold and task lifecycle hotspots so helper-backed seams stay explicit, governed companion repair is isolated, and the planning authoring path returns to a lower-blast-radius structure without changing behavior.

## Problem Statement
- The March 13, 2026 external refactor audit still reproduces `RF-PY-001` and `RF-PY-002` under the planning authoring path even after the earlier `trace.repo_local_hotspot_modularity` closeout.
- The current live code shows the hotspot regrew after later behavior-preserving hardening work: `planning_scaffolds.py` is back to 756 lines, `planning_scaffold_support.py` is 714 lines, and `task_lifecycle.py` is 621 lines.
- `git diff 7f793b7..HEAD` adds 319 lines back to `planning_scaffolds.py` and 158 lines back to `task_lifecycle.py`, mostly by reabsorbing bootstrap acceptance or evidence building, planning-surface refresh coordination, canonicalized `applies_to` handling, and governed companion-path repair.
- The result is the same risk pattern the audit called out: small planning-process changes now touch rendering, artifact generation, task mutation, acceptance or evidence rewriting, and coordination refresh logic in too few files.

## Goals
- Recover explicit helper-backed seams around planning scaffold specs, rendering, bootstrap artifact generation, and planning-surface refresh without changing current CLI behavior or artifact shapes.
- Isolate governed task companion-path repair from the core task mutation flow so `TaskLifecycleService` no longer owns acceptance-contract and validation-evidence internals directly.
- Re-run the themed refactor review loop until the planning authoring hotspot is clean under targeted validation, full validation, post-fix review, and adversarial confirmation.
- Record the regression context from the earlier modularity trace explicitly instead of silently treating the new hotspot as the same already-closed work.

## Non-Goals
- Reopening the already-closed sync CLI, traceability-sync, GitHub sync, or GitHub client hotspot slices from `trace.repo_local_hotspot_modularity`.
- Changing `watchtower-core plan` or `watchtower-core task` command names, flags, JSON payloads, or the shape of planning, task, acceptance-contract, or validation-evidence artifacts.
- Weakening traceability, coordination refresh behavior, fail-closed validation, or same-change companion-artifact repair.

## Requirements
- `req.planning_authoring_hotspot_regression_hardening.001`: The trace must publish and follow an explicit coverage map plus findings ledger across planning scaffold code, task lifecycle code, command handlers or docs, tests, planning trackers, indexes, acceptance contracts, evidence ledgers, and adjacent standards before remediation begins.
- `req.planning_authoring_hotspot_regression_hardening.002`: The planning scaffold path must move per-kind scaffold contracts into a more declarative helper-backed structure and split bootstrap artifact building plus planning-surface refresh responsibilities out of `planning_scaffolds.py` while preserving current command outputs and governed artifact shapes.
- `req.planning_authoring_hotspot_regression_hardening.003`: The task lifecycle path must isolate governed acceptance-contract and validation-evidence path repair from `TaskLifecycleService` while preserving canonicalized `applies_to`, stable task mutation behavior, and same-change companion-path rewrites when task paths move.
- `req.planning_authoring_hotspot_regression_hardening.004`: Adjacent docs, package READMEs, trackers, indexes, acceptance surfaces, and regression tests must stay aligned with the refactor in the same change set wherever the new helper seams materially affect the maintained hotspot boundary.
- `req.planning_authoring_hotspot_regression_hardening.005`: The initiative must run targeted validation, full repository validation, post-fix review, a second-angle no-new-issues review, and an adversarial confirmation pass; if any new same-theme issue appears, the loop must reopen until consecutive confirmation passes are clean.

## Acceptance Criteria
- `ac.planning_authoring_hotspot_regression_hardening.001`: The planning corpus for `trace.planning_authoring_hotspot_regression_hardening` contains the active PRD, accepted direction decision, active feature design, active implementation plan, aligned acceptance contract, planning-baseline evidence, closed bootstrap task, bounded execution tasks, and the explicit coverage map plus findings ledger for the slice.
- `ac.planning_authoring_hotspot_regression_hardening.002`: Planning scaffold kind contracts, section rendering, bootstrap acceptance or evidence artifact building, and planning-surface refresh responsibilities are split into smaller helper-backed seams, and `PlanningScaffoldService` remains behaviorally stable.
- `ac.planning_authoring_hotspot_regression_hardening.003`: Governed task companion-path repair is isolated from `TaskLifecycleService`, and task create or update or transition behavior still preserves canonical paths, coordination refresh, and governed acceptance or evidence rewrites.
- `ac.planning_authoring_hotspot_regression_hardening.004`: Targeted plan or task command docs, runtime boundary docs, planning trackers, indexes, and regression suites align with the touched seams and show no human-versus-machine drift inside this hotspot boundary.
- `ac.planning_authoring_hotspot_regression_hardening.005`: Targeted validation, full repository validation, post-fix review, second-angle confirmation, and adversarial confirmation all complete without finding a new actionable issue in the planning authoring hotspot theme.

## Risks and Dependencies
- Extracting too many micro-helpers could hide the end-to-end write path instead of clarifying it.
- The hotspot crosses planning docs, task docs, coordination refresh, and governed companion artifacts, so a missed same-change update could create real drift.
- The slice depends on the previous modularity trace as historical context, but it must not rewrite that older trace to hide the fact that the hotspot regrew later.

## References
- March 13, 2026 refactor audit
- [repo_local_hotspot_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/prds/repo_local_hotspot_modularity_hardening.md)
- [repo_local_hotspot_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/repo_local_hotspot_modularity_hardening.md)
- [repo_local_hotspot_modularity_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/repo_local_hotspot_modularity_hardening.md)
