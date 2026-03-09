---
id: "std.governance.initiative_closeout"
title: "Initiative Closeout Standard"
summary: "This standard defines how traced initiatives move to a terminal closeout state without overloading artifact lifecycle status."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "initiative_closeout"
owner: "repository_maintainer"
updated_at: "2026-03-09T23:02:08Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/control_plane/indexes/traceability/traceability_index.v1.json"
  - "docs/planning/prds/prd_tracking.md"
  - "docs/planning/design/design_tracking.md"
  - "docs/planning/decisions/decision_tracking.md"
aliases:
  - "initiative closure"
  - "trace closeout"
---

# Initiative Closeout Standard

## Summary
This standard defines how traced initiatives move to a terminal closeout state without overloading artifact lifecycle status.

## Purpose
- Make completion, supersession, cancellation, and abandonment explicit at the initiative level.
- Keep artifact lifecycle `status` separate from initiative outcome.
- Provide one machine-readable closeout authority and consistent human-readable mirrors.

## Scope
- Applies to initiative-level closeout fields stored on traceability index entries.
- Applies to the human planning trackers that mirror initiative closeout status.
- Covers closeout status values, required closeout fields, and the baseline closeout workflow boundary.
- Does not redefine artifact lifecycle status for PRDs, decisions, designs, or plans.

## Use When
- A traced initiative is complete, superseded, cancelled, or abandoned.
- Reviewers need to see whether a trace is still active or has reached a terminal state.
- Updating the planning trackers or traceability index to show initiative outcome clearly.

## Related Standards and Sources
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [traceability_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/traceability_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [initiative_closeout.md](/home/j/WatchTowerPlan/workflows/modules/initiative_closeout.md): workflow surface that operationalizes or depends on this standard.
## Guidance
- Do not overload artifact lifecycle `status` with initiative outcome.
- Store initiative closeout state on the traceability entry for the shared `trace_id`.
- Use only these initiative closeout states:
  - `active`
  - `completed`
  - `superseded`
  - `cancelled`
  - `abandoned`
- Use `active` for initiatives that are still underway.
- Use terminal closeout states only when the initiative outcome is explicit and durable.
- Every terminal initiative closeout must record:
  - `closed_at`
  - `closure_reason`
- `superseded` must also record `superseded_by_trace_id`.
- Prefer closing or explicitly deferring open tasks before terminal initiative closeout.
- If a terminal closeout is recorded while open tasks remain, the exception should be explicit in the operator workflow or command invocation.
- Mirror initiative closeout status into the PRD, decision, and design trackers from the traceability index rather than maintaining a second human-authored closeout source.

## Structure or Data Model
| Field | Meaning |
|---|---|
| `initiative_status` | Initiative outcome state separate from artifact lifecycle `status` |
| `closed_at` | UTC timestamp when the initiative entered a terminal closeout state |
| `closure_reason` | Short human-readable reason for the closeout decision |
| `superseded_by_trace_id` | Replacement trace when the initiative is superseded |

## Process or Workflow
1. Confirm the initiative `trace_id` and its current linked planning or execution surfaces.
2. Choose the terminal initiative status.
3. Record `closed_at` and `closure_reason`, and `superseded_by_trace_id` when required.
4. Update the traceability index entry for that trace.
5. Refresh the human planning trackers that mirror initiative status.
6. Record any remaining open-task exception explicitly when closeout happens with unfinished task records.

## Validation
- Every traceability entry should publish `initiative_status`.
- Terminal initiative states should also publish `closed_at` and `closure_reason`.
- `superseded` entries should also publish `superseded_by_trace_id`.
- Human planning trackers should agree with the traceability index on initiative closeout status.
- Reviewers should reject closeout state that is only implied in prose and not published in the traceability layer.

## Change Control
- Update this standard when the repository changes the initiative closeout vocabulary or closeout authority surface.
- Update the traceability schema, traceability sync logic, planning trackers, and initiative-closeout workflow surface in the same change set when this closeout model changes materially.

## References
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [traceability_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/traceability_index_standard.md)
- [initiative_closeout.md](/home/j/WatchTowerPlan/workflows/modules/initiative_closeout.md)

## Updated At
- `2026-03-09T23:02:08Z`
