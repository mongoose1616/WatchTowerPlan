---
id: "std.governance.initiative_tracking"
title: "Initiative Tracking Standard"
summary: "This standard defines the repository's cross-family initiative tracking model so one trace can be followed from PRD through design, planning, execution, validation, and closeout."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "initiative_tracking"
owner: "repository_maintainer"
updated_at: "2026-03-10T16:19:08Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/initiatives/"
  - "core/control_plane/indexes/initiatives/initiative_index.v1.json"
aliases:
  - "initiative tracking"
  - "initiative coordination"
  - "cross-family planning status"
---

# Initiative Tracking Standard

## Summary
This standard defines the repository's cross-family initiative tracking model so one trace can be followed from PRD through design, planning, execution, validation, and closeout.

## Purpose
- Give humans one start-here surface for "what is this initiative, who owns it, what phase is it in, and what is next?"
- Preserve the current artifact-family structure for PRDs, decisions, designs, plans, and tasks instead of collapsing them into one mixed planning folder.
- Publish one machine-readable initiative projection so queries and workflows do not have to reconstruct current phase and ownership from several indexes every time.

## Scope
- Applies to the human-readable initiative tracker under `docs/planning/initiatives/`.
- Applies to the machine-readable initiative index under `core/control_plane/indexes/initiatives/`.
- Covers initiative phase vocabulary, owner projection rules, next-step projection, and the authority boundary between initiative views and their source artifacts.
- Does not replace PRDs, decisions, designs, plans, task records, or the unified traceability index.

## Use When
- A user needs to understand what happens after a PRD is created.
- Reviewing who is actively working on a traced initiative and what phase it is currently in.
- Building query or sync tooling that needs one joined initiative view instead of several family-specific indexes.

## Related Standards and Sources
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): defines the trace spine and joined artifact expectations that initiative tracking projects from.
- [initiative_closeout_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_closeout_standard.md): defines initiative-level closeout status and terminal-state requirements that the initiative view must mirror.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): defines the authoritative local task layer that initiative owner and active-task projection must read from.
- [initiative_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/initiative_index_standard.md): defines the machine-readable initiative projection contract.
- [prd_tracking.md](/home/j/WatchTowerPlan/docs/planning/prds/prd_tracking.md): family tracker that remains the PRD-local view under the initiative layer.
- [design_tracking.md](/home/j/WatchTowerPlan/docs/planning/design/design_tracking.md): family tracker that remains the design-local view under the initiative layer.
- [decision_tracking.md](/home/j/WatchTowerPlan/docs/planning/decisions/decision_tracking.md): family tracker that remains the decision-local view under the initiative layer.
- [task_tracking.md](/home/j/WatchTowerPlan/docs/planning/tasks/task_tracking.md): family tracker that remains the task-local view under the initiative layer.
- [README.md](/home/j/WatchTowerPlan/docs/planning/initiatives/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Keep the planning corpus split by artifact family:
  - PRDs in `docs/planning/prds/`
  - decisions in `docs/planning/decisions/`
  - designs and plans in `docs/planning/design/`
  - engineer-sized execution tasks in `docs/planning/tasks/`
- Use the initiative layer as the cross-family coordination view, not as a replacement for those authored families.
- Treat the initiative index and initiative tracker as derived projections, not as the authoritative source for artifact content or task state.
- Keep `initiative_tracking.md` compact and scan-first. Prefer brief zero-state text and linked key surfaces over repeated explanatory scaffolding.
- Use the unified traceability index as the authoritative machine join for durable artifact links and initiative closeout state.
- Use the task index and task records as the authoritative source for active owners, open tasks, blockers, and execution status.
- Publish one initiative entry per shared `trace_id`.
- Keep active initiatives explicitly task-backed; do not leave an initiative active without durable task linkage.
- Active initiatives should usually be explicitly owned through non-terminal task records.
- The one allowed exception is active `closeout` phase, where all linked tasks may already be terminal and initiative closeout is the only remaining step.
- Every initiative entry must make these questions easy to answer:
  - what this initiative is
  - whether it is active or closed
  - what phase it is currently in
  - who is actively working on it
  - what the next expected step is
  - which surface the next contributor should open
- Use only these initiative phase values:
  - `prd`
  - `design`
  - `implementation_planning`
  - `execution`
  - `validation`
  - `closeout`
  - `closed`
- Derive `primary_owner` only when exactly one active owner is present on non-terminal task records for the initiative.
- Publish `active_owners` and `active_task_ids` when open task records exist.
- Allow active `closeout` entries to publish historical `task_ids` without `active_task_ids` when no non-terminal tasks remain and initiative closeout is the only next action.
- Active initiatives outside `closeout` should carry linked task IDs and active-task projection instead of relying on implied execution ownership.
- Use `closed` as the initiative phase for terminal initiative states rather than overloading `current_phase` with `completed`, `superseded`, `cancelled`, or `abandoned`.
- Make `next_action` specific enough that the next contributor can act without re-deriving the lifecycle state from several trackers.
- Make `next_surface_path` point to the repo-local surface the next contributor should open first.

## Structure or Data Model
### Source-of-truth layers
| Layer | Role |
|---|---|
| Traceability index | Authoritative machine join for trace-linked artifact IDs and initiative closeout status |
| Task records and task index | Authoritative source for active ownership, blockers, and execution state |
| Initiative index | Derived machine-readable coordination projection |
| `initiative_tracking.md` | Derived human-readable initiative board |

### Initiative phase expectations
| Phase | Meaning | Typical Next Step |
|---|---|---|
| `prd` | Intent exists, but technical design is not yet captured. | Create or update a feature design. |
| `design` | A feature design exists, but executable planning is not yet captured. | Create or update an implementation plan. |
| `implementation_planning` | An implementation plan exists, but execution has not yet started through active tasks. | Create and assign execution tasks. |
| `execution` | Non-terminal task work is active for the initiative. | Continue, unblock, review, or close the active task set. |
| `validation` | Execution is complete enough that validation and evidence are the next controlling step. | Run validation and record evidence. |
| `closeout` | Validation is present and the initiative is ready for terminal closeout. | Run initiative closeout. |
| `closed` | The initiative has reached a terminal closeout state. | No further default action. |

## Process or Workflow
1. Keep authored planning artifacts and task records current in their family directories.
2. Rebuild the family-specific indexes and the unified traceability index when traced artifacts or tasks change materially.
3. Rebuild the initiative index after those source surfaces change.
4. Rebuild the human initiative tracker from the initiative index in the same change set.
5. Use the initiative tracker as the primary human start-here surface for cross-family planning status.

## Validation
- Every initiative entry should correspond to one current traceability entry.
- Every initiative entry should publish `current_phase`, `next_action`, and `next_surface_path`.
- Active initiative owner and active-task projection should agree with the current open task corpus whenever non-terminal tasks exist.
- Active initiatives should not remain in the index without linked task IDs.
- Active initiatives outside `closeout` should not remain in the index without non-terminal task ownership.
- Initiative closeout state should agree with the traceability index rather than competing with it.
- Reviewers should reject initiative views that hide ambiguity by inventing owners, tasks, or progress that the source surfaces do not publish.

## Change Control
- Update this standard when the repository changes initiative phase vocabulary, initiative authority boundaries, or the start-here planning experience.
- Update the initiative-index schema, initiative sync logic, initiative tracker, and affected planning README surfaces in the same change set when initiative tracking changes structurally.

## References
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [initiative_closeout_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_closeout_standard.md)
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md)
- [initiative_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/initiative_index_standard.md)
- [README.md](/home/j/WatchTowerPlan/docs/planning/initiatives/README.md)

## Updated At
- `2026-03-10T16:19:08Z`
