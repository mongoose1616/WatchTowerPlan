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
updated_at: "2026-03-15T15:30:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/control_plane/indexes/traceability/traceability_index.json"
  - "plan/.wt/indexes/initiative_index.json"
  - "plan/tracking/coordination_tracking.md"
  - "plan/tracking/initiative_tracking.md"
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
- Applies to the live human tracking surfaces and derived initiative coordination views that mirror initiative closeout status.
- Covers closeout status values, required closeout fields, and the baseline closeout workflow boundary.
- Does not redefine artifact lifecycle status for initiative briefs, decision notes, design records, or implementation slices.

## Use When
- A traced initiative is complete, superseded, cancelled, or abandoned.
- Reviewers need to see whether a trace is still active or has reached a terminal state.
- Updating the live plan trackers or traceability index to show initiative outcome clearly.

## Related Standards and Sources
- [traceability_standard.md](/plan/docs/standards/governance/traceability_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [traceability_index_standard.md](/plan/docs/standards/data_contracts/traceability_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [task_tracking_standard.md](/plan/docs/standards/governance/task_tracking_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [timestamp_standard.md](/core/docs/standards/metadata/timestamp_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [planning_retention_and_purge_standard.md](/plan/docs/standards/governance/planning_retention_and_purge_standard.md): companion standard that constrains when a terminal trace can later become purge-eligible.
- [initiative_closeout.md](/plan/workflows/modules/initiative_closeout.md): workflow surface that operationalizes or depends on this standard.

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
- Treat terminal closeout as a precondition for later purge consideration, not as a purge action by itself.
- Every terminal initiative closeout must record:
  - `closed_at`
  - `closure_reason`
- `superseded` must also record `superseded_by_trace_id`.
- Prefer closing or explicitly deferring open tasks before terminal initiative closeout.
- If a terminal closeout is recorded while open tasks remain, the exception should be explicit in the operator workflow or command invocation.
- Prefer reconciling initiative acceptance IDs, acceptance contracts, validation evidence, and traceability before terminal initiative closeout when those surfaces exist for the trace.
- If a terminal closeout proceeds with known acceptance-reconciliation issues, the exception should be explicit in the operator workflow or command invocation rather than implied by a successful closeout alone.
- When terminal closeout metadata changes the traceability entry, `updated_at` should advance to the effective closeout timestamp.
- Mirror initiative closeout status into the derived initiative index, coordination surfaces, and initiative tracker from the traceability index rather than maintaining a second initiative-closeout authority.
- If a terminal trace later becomes purge-eligible, keep the surviving authority in current standards, indexes, and any purge record rather than in removed trace-local artifacts.

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
3. Check whether the trace has acceptance-contract or validation-evidence surfaces and reconcile them before closeout when they exist.
4. Record `closed_at` and `closure_reason`, and `superseded_by_trace_id` when required.
5. Update the traceability index entry for that trace and advance its effective `updated_at`.
6. Refresh the derived initiative and coordination surfaces.
7. Refresh the live human plan trackers that mirror initiative status.
8. Record any remaining open-task or acceptance-validation exception explicitly when closeout happens with unfinished or unreconciled work.

## Operationalization
- `Modes`: `workflow`; `documentation`; `artifact`
- `Operational Surfaces`: `plan/workflows/modules/initiative_closeout.md`; `plan/tracking/initiative_tracking.md`; `plan/.wt/indexes/initiative_index.json`; `core/control_plane/indexes/traceability/traceability_index.json`

## Validation
- Every traceability entry should publish `initiative_status`.
- Terminal initiative states should also publish `closed_at` and `closure_reason`.
- `superseded` entries should also publish `superseded_by_trace_id`.
- Terminal closeout should not leave `updated_at` behind `closed_at`.
- Terminal closeout should not silently bypass known acceptance-reconciliation issues when the trace publishes acceptance or evidence surfaces, unless the operator used an explicit exception path.
- Human plan trackers should agree with the traceability index on initiative closeout status.
- Reviewers should reject closeout state that is only implied in prose and not published in the traceability layer.

## Change Control
- Update this standard when the repository changes the initiative closeout vocabulary or closeout authority surface.
- Update the traceability schema, traceability sync logic, planning trackers, and initiative-closeout workflow surface in the same change set when this closeout model changes materially.

## References
- [traceability_standard.md](/plan/docs/standards/governance/traceability_standard.md)
- [initiative_tracking_standard.md](/plan/docs/standards/governance/initiative_tracking_standard.md)
- [traceability_index_standard.md](/plan/docs/standards/data_contracts/traceability_index_standard.md)
- [initiative_closeout.md](/plan/workflows/modules/initiative_closeout.md)
- [planning_retention_and_purge_standard.md](/plan/docs/standards/governance/planning_retention_and_purge_standard.md)

## Updated At
- `2026-03-15T15:30:00Z`
