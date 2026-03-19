---
id: "std.governance.planning_retention_and_purge"
title: "Planning Retention and Purge Standard"
summary: "This standard defines the promote-then-purge retention model for closed traced planning artifacts so active policy lives in current canonical surfaces instead of accumulating indefinitely in historical trace packages."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "planning_retention"
  - "purge"
owner: "repository_maintainer"
updated_at: "2026-03-19T20:15:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "plan/initiatives/"
  - "plan/projects/"
  - "core/control_plane/ledgers/"
  - "core/control_plane/indexes/"
  - "core/python/src/watchtower_core/plan_runtime/"
  - "core/python/src/watchtower_core/cli/"
aliases:
  - "trace purge"
  - "planning retention"
  - "promote then purge"
---

# Planning Retention and Purge Standard

## Summary
This standard defines the promote-then-purge retention model for closed traced planning artifacts so active policy lives in current canonical surfaces instead of accumulating indefinitely in historical trace packages.

## Purpose
- Keep current repository policy in standards and other surviving canonical artifacts instead of in closed trace-local planning chains.
- Prevent the live planning workspace from growing indefinitely through retained closed initiative packages, task histories, acceptance contracts, and evidence artifacts that no longer carry unique active authority.
- Define one safe purge boundary that preserves minimal machine-readable history without silently breaking traceability or leaving partial cleanup behind.

## Scope
- Applies to traced planning artifacts after their initiative has reached a terminal closeout state.
- Applies to the retention decision for trace-local initiative briefs, design records, implementation slices, optional decision notes, task state, acceptance contracts, validation evidence, and related derived planning surfaces.
- Applies to the minimal surviving machine-readable ledger that records a completed purge.
- Does not authorize purging active traces, partial family cleanup, or deleting a trace whose durable policy still exists only inside the to-be-purged artifacts.

## Use When
- Deciding whether a closed trace should remain in the planning corpus or become purge-eligible.
- Promoting a past decision or one-off planning rule into a standard or other surviving canonical artifact.
- Implementing or reviewing a repo-local purge workflow for traced planning artifacts.

## Related Standards and Sources
- [traceability_standard.md](/plan/docs/standards/governance/traceability_standard.md): purge must preserve explicit surviving authority and must not create silent trace-link drift.
- [decision_capture_standard.md](/plan/docs/standards/governance/decision_capture_standard.md): accepted decisions should move into canonical artifacts instead of remaining the only active policy surface.
- [initiative_closeout_standard.md](/plan/docs/standards/governance/initiative_closeout_standard.md): only terminal traces are eligible for purge consideration.
- [task_tracking_standard.md](/plan/docs/standards/governance/task_tracking_standard.md): initiative-local task state remains governed in place until an explicit purge removes the full trace package.
- [compact_document_authoring_standard.md](/core/docs/standards/documentation/compact_document_authoring_standard.md): low-value retained history should not become default clutter when stronger authority already exists elsewhere.
- [repository_standards_posture.md](/core/docs/foundations/repository_standards_posture.md): retained history must not compete with one clear current authority answer.

## Guidance
- Treat closed trace-local planning artifacts as temporary retained history, not automatic permanent authority.
- Keep active current policy in standards, current command docs, current repository guidance, and machine-readable control-plane surfaces that remain in use after a trace is closed.
- A closed trace is purge-eligible only when all of these conditions are true:
  - the trace has a terminal `initiative_status`
  - the trace has no open tasks
  - any durable rule or rationale that must remain current has been promoted into a surviving canonical artifact
  - acceptance, evidence, and closeout work are complete or an explicit exception is recorded in the purge decision
  - no surviving canonical surface still depends directly on a path inside the trace package
- Purge by `trace_id`, not by individual file family.
- An explicit purge must remove the whole trace package in one governed change set, including:
  - trace-local `initiative_brief.md`, `design_record.md`, `implementation_slice.md`, and optional `decision_notes.md`
  - initiative-local `.wt/tasks/**` state and events
  - trace-local acceptance contracts and validation evidence
  - derived tracker and index entries that only exist because the trace package remains present
  - direct surviving references that would otherwise point to removed paths
- Keep one minimal surviving purge ledger entry instead of the full trace package.
- The purge ledger entry should record at least:
  - `trace_id`
  - `title`
  - `initiative_status`
  - `closed_at`
  - `purged_at`
  - `closure_reason`
  - surviving canonical standards or authority paths
- Do not purge a decision record when its unique rationale has not yet been absorbed into a surviving canonical artifact.
- Do not let standards, workflows, README files, or command pages depend on purgeable historical task documents as their canonical operationalization surface.
- Until a trace is explicitly purged under this standard, the closed initiative package and its initiative-local machine state remain governed in place under `plan/initiatives/**` or `plan/projects/**`.

## Structure or Data Model
### Retention states
| State | Meaning |
|---|---|
| Retained closed trace | Closed trace still present as an initiative package in the live repository. |
| Purge-eligible trace | Closed trace that satisfies the purge preconditions and can be removed safely. |
| Purged trace | Trace-local package removed; minimal surviving history remains only in the purge ledger and any promoted canonical artifacts. |

### Surviving authority after purge
| Concern | Surviving canonical surface |
|---|---|
| Current policy or rule | Standards, current command docs, or other surviving canonical documentation |
| Minimal historical trace record | Purge ledger entry |
| Current machine-readable planning state | Rebuilt initiative, task, traceability, coordination, and related live indexes after purge |

## Process or Workflow
1. Close the trace normally through initiative closeout, task closeout, acceptance, and evidence reconciliation.
2. Promote any still-needed policy, rationale, or guidance into surviving canonical artifacts.
3. Confirm that no surviving canonical surface still depends on a trace-local path that would be removed.
4. Record the purge decision and the surviving canonical authority surfaces.
5. Remove the whole trace package in one governed change set.
6. Write the minimal purge ledger entry.
7. Rebuild the affected planning trackers and machine-readable indexes.
8. Validate that the removed trace no longer appears in retained planning surfaces except through the purge ledger.

## Operationalization
- `Modes`: `documentation`; `artifact`; `workflow`
- `Operational Surfaces`: `plan/initiatives/`; `plan/projects/`; `core/control_plane/ledgers/`; `core/python/src/watchtower_core/plan_runtime/`; `core/python/src/watchtower_core/cli/`

## Validation
- A purged trace should have no surviving open tasks.
- A purged trace should have one purge ledger entry.
- Surviving canonical surfaces should not reference removed trace-local paths after purge.
- Rebuilt planning trackers and indexes should no longer surface the purged trace as a retained planning package.
- Reviewers should reject partial or ad hoc file deletion that bypasses the trace-level purge boundary.

## Change Control
- Update this standard when the purge eligibility rules, surviving authority model, or purge ledger contract changes materially.
- Update the purge ledger schema or artifact shape, purge workflow surface, planning trackers, and affected indexes in the same change set when this standard changes structurally.

## References
- [traceability_standard.md](/plan/docs/standards/governance/traceability_standard.md)
- [decision_capture_standard.md](/plan/docs/standards/governance/decision_capture_standard.md)
- [initiative_closeout_standard.md](/plan/docs/standards/governance/initiative_closeout_standard.md)
- [task_tracking_standard.md](/plan/docs/standards/governance/task_tracking_standard.md)
- [repository_standards_posture.md](/core/docs/foundations/repository_standards_posture.md)

## Updated At
- `2026-03-19T20:15:00Z`
