---
trace_id: "trace.initiative_closeout"
id: "design.features.initiative_closeout_and_planning_trackers"
title: "Initiative Closeout and Planning Trackers"
summary: "Defines the first initiative closeout model, its traceability fields, and the generated planning trackers that mirror initiative outcome for humans."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-09T18:25:06Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/control_plane/indexes/traceability/traceability_index.v1.json"
  - "docs/planning/prds/prd_tracking.md"
  - "docs/planning/design/design_tracking.md"
  - "docs/planning/decisions/decision_tracking.md"
aliases:
  - "initiative closeout design"
  - "planning tracker sync design"
---

# Initiative Closeout and Planning Trackers

## Record Metadata
- `Trace ID`: `trace.initiative_closeout`
- `Design ID`: `design.features.initiative_closeout_and_planning_trackers`
- `Design Status`: `active`
- `Linked PRDs`: `None`
- `Linked Decisions`: `None`
- `Linked Implementation Plans`: `None`
- `Updated At`: `2026-03-09T18:25:06Z`

## Summary
This document defines the first initiative closeout model, its traceability fields, and the generated planning trackers that mirror initiative outcome for humans.

## Source Request
- User request to close the full PRD to design to implementation to validated chain explicitly.
- User request for clearer human and machine tracking so multiple engineers do not lose state across handoffs.

## Scope and Feature Boundary
- Covers initiative closeout state on traceability entries.
- Covers generated PRD, decision, and design trackers that mirror initiative status.
- Covers a reusable closeout command and workflow module boundary.
- Does not change artifact lifecycle `status`.
- Does not add a separate closeout document family yet.

## Current-State Context
- The repository already has human planning trackers plus machine-readable PRD, decision, design, task, and traceability indexes.
- The machine traceability layer can already join most of the planning chain.
- No single surface currently records whether a traced initiative is completed, superseded, cancelled, or abandoned.

## Foundations References Applied
- [design_philosophy.md](/home/j/WatchTowerPlan/docs/foundations/design_philosophy.md): keep machine-readable authority explicit and use derived human surfaces for orientation.
- [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md): preserve reusable closeout behavior tied to planning, validation, and execution.
- [technology_stack.md](/home/j/WatchTowerPlan/docs/foundations/technology_stack.md): keep JSON for machine-readable join state and Markdown for human-readable tracker views.
- [standards.md](/home/j/WatchTowerPlan/docs/foundations/standards.md): keep one source of truth for initiative outcome and derive secondary mirrors from it.

## Internal Standards and Canonical References Applied
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): initiative lifecycle closeout has to update the shared trace record rather than only the human trackers.
- [traceability_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/traceability_index_standard.md): closure state and linked planning surfaces must remain queryable through the unified trace index.
- [initiative_closeout_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_closeout_standard.md): closeout must set initiative outcome, timestamp, and closure reason consistently.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): planning closeout should leave local task tracking aligned with final initiative state.

## Design Goals and Constraints
- Keep initiative outcome separate from artifact lifecycle state.
- Give both humans and agents one deterministic initiative-status surface.
- Avoid adding a large manual closeout spreadsheet or tracker that drifts immediately.
- Make the first closeout flow narrow and explicit instead of auto-closing linked work silently.

## Options Considered
### Option 1
- Overload existing artifact `status` with initiative completion meaning.
- Strengths: no new fields required.
- Tradeoffs or reasons not chosen: collapses artifact lifecycle and initiative outcome into one ambiguous field.

### Option 2
- Add a closeout-only field set on the traceability entry and derive the human trackers from it.
- Strengths: one machine authority, clear semantics, and generated human mirrors.
- Tradeoffs or reasons not chosen: requires tracker rebuild logic and a narrow closeout command.

### Option 3
- Keep closeout state only in prose trackers or commit messages.
- Strengths: minimal schema work.
- Tradeoffs or reasons not chosen: weak queryability, poor agent retrieval, and high drift risk.

## Recommended Design
### Architecture
- Add `initiative_status`, `closed_at`, `closure_reason`, and `superseded_by_trace_id` to traceability entries.
- Preserve those fields across traceability-index rebuilds.
- Generate PRD, decision, and design tracking documents from their machine indexes plus traceability closeout state.
- Provide a narrow `watchtower-core closeout initiative` command for dry-run or canonical writes.

### Data and Interface Impacts
- Extend the traceability schema and typed models.
- Add a closeout command plus generated planning-tracker sync commands.
- Add one reusable initiative-closeout workflow module.

### Execution Flow
1. Resolve the target `trace_id`.
2. Check whether linked tasks are still open.
3. Record the terminal initiative status and closeout metadata on the traceability entry.
4. Persist the updated traceability artifact.
5. Rebuild the PRD, decision, and design trackers from the machine-readable indexes and closeout state.

### Invariants and Failure Cases
- Every traceability entry always publishes `initiative_status`.
- Terminal initiative closeout requires `closed_at` and `closure_reason`.
- `superseded` also requires `superseded_by_trace_id`.
- Open linked tasks should block closeout by default unless the operator explicitly allows the exception.

## Affected Surfaces
- `core/control_plane/schemas/artifacts/traceability_index.v1.schema.json`
- `core/control_plane/indexes/traceability/traceability_index.v1.json`
- `docs/planning/prds/prd_tracking.md`
- `docs/planning/decisions/decision_tracking.md`
- `docs/planning/design/design_tracking.md`
- `core/python/src/watchtower_core/closeout/initiative.py`
- `core/python/src/watchtower_core/sync/prd_tracking.py`
- `core/python/src/watchtower_core/sync/decision_tracking.py`
- `core/python/src/watchtower_core/sync/design_tracking.py`

## Design Guardrails
- Keep initiative closeout state at the trace layer, not copied into every family index.
- Do not auto-close linked task records as a side effect of initiative closeout.
- Prefer generated planning trackers over hand-edited tables wherever initiative status matters.

## Implementation-Planning Handoff Notes
- Add tracker sync commands before relying on human tracker closeout state in normal operation.
- Preserve closeout fields across traceability rebuilds so initiative outcome is not lost on sync.
- Make the closeout command dry-run by default and require `--write` for canonical mutation.

## Dependencies
- Existing PRD, decision, design, task, and traceability indexes.
- Existing task status vocabulary for checking open linked tasks.

## Risks
- If tracker regeneration is skipped after closeout writes, humans will still see stale planning state.
- If closeout is allowed freely with open tasks, terminal initiative state may not mean what operators expect.
- If traceability rebuilds do not preserve closeout fields, initiative outcome will drift or disappear.

## Open Questions
- Should a later closeout phase emit a durable closeout report artifact in addition to trace-level state?
- Should future initiative closeout also summarize validation-evidence coverage requirements before allowing `completed`?

## References
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [initiative_closeout_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_closeout_standard.md)
- [traceability_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/traceability_index_standard.md)

## Updated At
- `2026-03-09T18:25:06Z`
