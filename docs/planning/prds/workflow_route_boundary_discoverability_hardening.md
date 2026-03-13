---
trace_id: trace.workflow_route_boundary_discoverability_hardening
id: prd.workflow_route_boundary_discoverability_hardening
title: Workflow Route Boundary Discoverability Hardening PRD
summary: Harden workflow route preview and workflow lookup so realistic reconciliation
  and handoff requests resolve to the right adjacent workflow boundaries without low-signal
  route leakage.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-13T21:17:49Z'
audience: shared
authority: authoritative
applies_to:
- workflows/ROUTING_TABLE.md
- workflows/modules/
- core/python/src/watchtower_core/repo_ops/query/routes.py
- core/python/src/watchtower_core/repo_ops/query/workflows.py
- core/control_plane/registries/workflows/
- core/control_plane/indexes/routes/
- core/control_plane/indexes/workflows/
- docs/commands/core_python/
---

# Workflow Route Boundary Discoverability Hardening PRD

## Record Metadata
- `Trace ID`: `trace.workflow_route_boundary_discoverability_hardening`
- `PRD ID`: `prd.workflow_route_boundary_discoverability_hardening`
- `Status`: `active`
- `Linked Decisions`: `decision.workflow_route_boundary_discoverability_hardening_direction`
- `Linked Designs`: `design.features.workflow_route_boundary_discoverability_hardening`
- `Linked Implementation Plans`: `design.implementation.workflow_route_boundary_discoverability_hardening`
- `Updated At`: `2026-03-13T21:17:49Z`

## Summary
Harden workflow route preview and workflow lookup so realistic reconciliation and handoff requests resolve to the right adjacent workflow boundaries without low-signal route leakage.

## Problem Statement
- The March 13, 2026 refactor audit left a live workflow-family gap after the earlier documentation-review routing fix: the adjacent reconciliation and task-management routes remain explicit in authored workflow modules, but the advisory lookup surfaces still struggle to surface the right boundary under realistic prompts.
- `watchtower-core route preview --request "reconcile command docs with current cli behavior" --format json` currently returns no route even though `Documentation-Implementation Reconciliation` is the intended route.
- `watchtower-core route preview --request "reconcile schema-backed indexes, examples, and validators for one artifact family" --format json` also returns no route even though `Governed Artifact Reconciliation` is the intended route.
- `watchtower-core route preview --request "hand off this task from implementation to validation and create successor tasks" --format json` selects the intended `Task Phase Transition` and `Task Lifecycle Management` routes, but it also leaks in `Code Validation` because a single low-signal `validation` keyword is enough to survive the merged positive-match rule.
- `watchtower-core query workflows --query "current cli behavior" --format json` and `watchtower-core query workflows --query "successor tasks" --format json` currently return zero results, which means the adjacent workflow lookup surface is not reinforcing the same boundaries the workflow modules already describe.

## Goals
- Keep the workflow family explicit and route-first while making realistic reconciliation and handoff prompts resolve to the right adjacent workflow boundaries deterministically.
- Improve workflow lookup discoverability for the same adjacent boundaries through workflow metadata, query behavior, and companion docs instead of relying on manual directory scanning.
- Preserve intended multi-route unions for truly composite requests while filtering low-signal route leakage that comes only from generic single-word matches.
- Complete the refactor under one stable traced loop with a coverage map, findings ledger, targeted fixes, repeated confirmation passes, clean validation, and explicit closeout evidence.

## Non-Goals
- Collapsing the workflow family into generic mega-procedures or removing the existing reconciliation and task-management route split.
- Reworking unrelated planning, command, or control-plane query families outside the workflow-boundary seam.
- Replacing deterministic routing with opaque fuzzy or model-driven matching.
- Reopening broad governance-threshold or workflow-count policy questions from `RF-STD-002`; this trace is about route and lookup boundary discoverability, not workflow-family consolidation.

## Requirements
- `req.workflow_route_boundary_discoverability_hardening.001`: The trace must publish and follow an explicit coverage map plus findings ledger across route preview code, workflow query code, authored routing guidance, workflow metadata, derived route and workflow indexes, command docs, tests, and adjacent workflow modules before remediation begins.
- `req.workflow_route_boundary_discoverability_hardening.002`: Realistic free-form reconciliation prompts for documentation-implementation and governed-artifact drift must resolve to the intended routes deterministically without requiring near-verbatim routing-table phrasing.
- `req.workflow_route_boundary_discoverability_hardening.003`: Low-signal single-word route matches must no longer leak unrelated workflow modules into strongly scored adjacent route previews when the request already provides a materially stronger dominant route.
- `req.workflow_route_boundary_discoverability_hardening.004`: Workflow lookup and companion guidance must expose the adjacent reconciliation and task-route boundaries clearly enough that `query workflows` and route-preview docs reinforce the same distinctions.
- `req.workflow_route_boundary_discoverability_hardening.005`: The implementation must keep the workflow family explicit, deterministic, inspectable, and synchronized across routing docs, workflow metadata, indexes, command docs, and regression coverage.
- `req.workflow_route_boundary_discoverability_hardening.006`: Targeted validation, full repository validation, post-fix review, second-angle confirmation, and adversarial confirmation must all complete cleanly before closeout.

## Acceptance Criteria
- `ac.workflow_route_boundary_discoverability_hardening.001`: The planning corpus for `trace.workflow_route_boundary_discoverability_hardening` contains the active PRD, accepted direction decision, active feature design, active implementation plan, aligned acceptance contract, planning-baseline evidence, closed bootstrap task, bounded execution tasks, and the explicit coverage map plus findings ledger for the workflow-boundary slice.
- `ac.workflow_route_boundary_discoverability_hardening.002`: `watchtower-core route preview` now resolves realistic documentation-implementation and governed-artifact reconciliation prompts to the intended routes, and low-signal `Code Validation` leakage no longer survives strongly scored phase-transition prompts.
- `ac.workflow_route_boundary_discoverability_hardening.003`: `watchtower-core query workflows` and the companion workflow metadata or docs now expose the adjacent reconciliation and task-route boundaries through realistic lookup terms instead of requiring exact module names.
- `ac.workflow_route_boundary_discoverability_hardening.004`: The authored routing guidance, workflow metadata registry, derived route or workflow indexes, and command docs stay aligned in the same change set and preserve explicit workflow-family boundaries.
- `ac.workflow_route_boundary_discoverability_hardening.005`: Targeted tests, full repository validation, post-fix review, second-angle confirmation, and adversarial confirmation all complete with no new actionable issue under the same workflow-boundary theme.

## Risks and Dependencies
- A scorer change that is too permissive could blur adjacent routes and reintroduce the route-lattice ambiguity the audit warned against.
- A docs-only fix would leave the lookup surfaces inconsistent with the actual route-preview behavior, while a code-only fix would leave users without guidance on the adjacent route boundaries.
- The slice depends on keeping `ROUTING_TABLE.md`, workflow metadata, the derived indexes, route-preview behavior, workflow lookup behavior, and command docs aligned in one change set.

## References
- March 13, 2026 refactor audit
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md)
- [workflow_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/workflow_md_standard.md)
- [route_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/route_index_standard.md)
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md)
