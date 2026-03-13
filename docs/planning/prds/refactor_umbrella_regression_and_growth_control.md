---
trace_id: trace.refactor_umbrella_regression_and_growth_control
id: prd.refactor_umbrella_regression_and_growth_control
title: Refactor Umbrella Regression and Growth Control PRD
summary: Audits the March 13, 2026 refactor program across the external audit, completed
  refactor traces, and commit history, then hardens closeout and review-loop behavior
  to stop repeated acceptance-drift regressions and unnecessary trace-sprawl growth.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-13T22:30:01Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/closeout/initiative.py
- workflows/modules/repository_review.md
- workflows/modules/initiative_closeout.md
- docs/commands/core_python/watchtower_core_closeout_initiative.md
- docs/commands/core_python/watchtower_core_closeout.md
- docs/standards/governance/initiative_closeout_standard.md
- docs/planning/
---

# Refactor Umbrella Regression and Growth Control PRD

## Record Metadata
- `Trace ID`: `trace.refactor_umbrella_regression_and_growth_control`
- `PRD ID`: `prd.refactor_umbrella_regression_and_growth_control`
- `Status`: `active`
- `Linked Decisions`: `decision.refactor_umbrella_regression_and_growth_control_direction`
- `Linked Designs`: `design.features.refactor_umbrella_regression_and_growth_control`
- `Linked Implementation Plans`: `design.implementation.refactor_umbrella_regression_and_growth_control`
- `Updated At`: `2026-03-13T22:30:01Z`

## Summary
Audits the March 13, 2026 refactor program across the external audit, completed refactor traces, and commit history, then hardens closeout and review-loop behavior to stop repeated acceptance-drift regressions and unnecessary trace-sprawl growth.

## Problem Statement
The March 13, 2026 external refactor audit in `REFACTOR.md` identified a broad set of
repository simplification opportunities. Since then, seven refactor follow-up traces have
landed and closed cleanly in isolation, but the repository still lacks one master refactor
ledger that answers three questions deterministically:

- which original audit findings are actually resolved versus only partially mitigated
- whether the pass series is removing root causes or merely shifting work into new traced slices
- whether the review and closeout workflows themselves are creating repeated late regressions

The current commit range since `origin/initiative/core-export-readiness-and-optimization`
changed `202` files with `26514` insertions and `12953` deletions. Most of the original code
and documentation hotspots improved materially, but the same acceptance or evidence closeout
drift reopened across several traces and the planning corpus grew from `359` to `431` planning
documents plus `159` to `196` closed task files. Without an umbrella review and root-cause
hardening, the repository can keep reporting local slice completion while the overall refactor
theme still expands surface area and duplicates review work.

## Goals
- Publish one umbrella refactor status view that maps every original `RF-*` audit finding to
  its current repository status, supporting evidence, and related traced work.
- Stop initiative closeout from silently succeeding when PRD acceptance IDs, acceptance
  contracts, validation evidence, and traceability are out of sync.
- Encode the stable-theme review rule so one continuing review theme stays under one trace and
  one findings ledger until it is truly exhausted.
- Preserve capability, fidelity, determinism, and performance while reducing duplicated review
  work and late closeout churn.

## Non-Goals
- Rewriting or deleting historical traced planning artifacts that were valid at the time they
  landed.
- Collapsing acceptance contracts or validation evidence back into prose-only planning docs.
- Performing a full CLI-family redesign or a broad policy rewrite of planning thresholds in this
  same change.
- Reopening already-resolved refactor slices unless this umbrella review finds a concrete
  regression in the current tree.

## Requirements
- `req.refactor_umbrella_regression_and_growth_control.001`: The trace must publish a master
  refactor coverage map that spans the external audit findings, the completed refactor traces,
  and the recent refactor commit range, and it must classify each original audit finding as
  resolved, partially mitigated, remaining design debt, or intentionally preserved.
- `req.refactor_umbrella_regression_and_growth_control.002`: Terminal initiative closeout must
  fail closed when trace-level acceptance reconciliation reports issues, unless an operator
  explicitly records the exception through a dedicated override.
- `req.refactor_umbrella_regression_and_growth_control.003`: The initiative closeout workflow,
  command docs, and governing standard must describe the acceptance-reconciliation gate and the
  explicit override semantics in the same change set as the runtime implementation.
- `req.refactor_umbrella_regression_and_growth_control.004`: The repository-review workflow must
  direct same-theme review loops to remain under one stable trace, one findings ledger, and one
  closeout boundary instead of spawning new traces for each adjacent finding under the same
  continuing theme.
- `req.refactor_umbrella_regression_and_growth_control.005`: Targeted validation, full
  repository validation, post-fix review, second-angle confirmation, and adversarial
  confirmation must show no new actionable issue under this root-cause boundary after the
  implementation lands.

## Acceptance Criteria
- `ac.refactor_umbrella_regression_and_growth_control.001`: The planning corpus for
  `trace.refactor_umbrella_regression_and_growth_control` contains the active PRD, accepted
  direction decision, active feature design, active implementation plan, acceptance contract,
  evidence ledger, bounded execution tasks, the master audit coverage map, and the findings
  ledger for the umbrella refactor review.
- `ac.refactor_umbrella_regression_and_growth_control.002`: A dry-run initiative closeout fails
  when the trace has acceptance-reconciliation issues and the operator did not pass the explicit
  acceptance-drift override.
- `ac.refactor_umbrella_regression_and_growth_control.003`: When the explicit override is used,
  closeout still succeeds and makes the validation exception explicit in the runtime result plus
  companion docs or workflow guidance.
- `ac.refactor_umbrella_regression_and_growth_control.004`: The repository-review workflow and
  closeout guidance both reflect the stable-theme umbrella rule and stop treating adjacent
  same-theme findings as justification for new disconnected traces.
- `ac.refactor_umbrella_regression_and_growth_control.005`: Targeted tests, full validation,
  repeated confirmation passes, and the final closeout state all pass without finding a new
  actionable issue inside the pass-trace regression and surface-growth boundary.

## Risks and Dependencies
- The historical planning corpus will remain large after this change; this trace is intended to
  stop repeated late drift and future same-theme trace sprawl, not to erase already-committed
  history.
- A fail-closed closeout gate adds friction for operators, so the override path must remain
  explicit and well-documented.
- The umbrella review depends on the existing refactor traces, planning trackers, and commit
  history remaining queryable and aligned.

## References
- REFACTOR.md
- docs/planning/design/implementation/refactor_review_and_hardening.md
- docs/planning/design/implementation/planning_authoring_hotspot_regression_hardening.md
- docs/planning/design/implementation/typed_query_surface_modularity_hardening.md
- docs/planning/design/implementation/validation_test_hotspot_rebalancing.md
- docs/planning/design/implementation/data_contract_index_family_baseline_alignment.md
- docs/planning/design/implementation/active_first_planning_query_history_alignment.md
- docs/planning/design/implementation/workflow_route_boundary_discoverability_hardening.md
- docs/planning/design/implementation/query_family_source_surface_alignment.md
