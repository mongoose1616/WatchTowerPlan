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
updated_at: "2026-03-17T06:08:09Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "docs/planning/initiatives/"
  - "plan/.wt/indexes/initiative_index.json"
aliases:
  - "initiative tracking"
  - "initiative coordination"
  - "cross-family planning status"
---

# Initiative Tracking Standard

## Summary
This standard defines the repository's cross-family initiative tracking model so one trace can be followed from PRD through design, planning, execution, validation, and closeout.

## Purpose
- Give humans one family-specific initiative view for "what is this initiative, who owns it, what phase is it in, and what is next?"
- Preserve the current artifact-family structure for PRDs, decisions, designs, plans, and tasks instead of collapsing them into one mixed planning folder.
- Publish one machine-readable initiative rendered surface so the coordination layer and family-specific workflows do not have to reconstruct current phase and ownership from several indexes every time.
- Keep the retained initiative tracker available beneath the live `plan/**` coordination entrypoints while preserving `query initiatives` as the live initiative-family lookup surface.

## Scope
- Applies to the human-readable initiative tracker under `docs/planning/initiatives/`.
- Applies to the machine-readable initiative index under `plan/.wt/indexes/initiative_index.json`.
- Covers initiative phase vocabulary, owner rendering rules, next-step rendering, and the authority boundary between initiative views and their source artifacts.
- Does not replace PRDs, decisions, designs, plans, task records, or the unified traceability index.

## Use When
- A user needs to understand what happens after a PRD is created.
- Reviewing who is actively working on a traced initiative and what phase it is currently in.
- Building query or sync tooling that needs one joined initiative view instead of several family-specific indexes.

## Related Standards and Sources
- [traceability_standard.md](/docs/standards/governance/traceability_standard.md): defines the trace spine and joined artifact expectations that initiative tracking projects from.
- [initiative_closeout_standard.md](/docs/standards/governance/initiative_closeout_standard.md): defines initiative-level closeout status and terminal-state requirements that the initiative view must mirror.
- [coordination_tracking_standard.md](/docs/standards/governance/coordination_tracking_standard.md): defines the repo-level human start-here tracker that now sits above this family view.
- [task_tracking_standard.md](/docs/standards/governance/task_tracking_standard.md): defines the authoritative local task layer that initiative owner and active-task rendered detail must read from.
- [initiative_index_standard.md](/docs/standards/data_contracts/initiative_index_standard.md): defines the machine-readable initiative rendered-surface contract.
- [prd_tracking.md](/docs/planning/prds/prd_tracking.md): family tracker that remains the PRD-local view under the initiative layer.
- [design_tracking.md](/docs/planning/design/design_tracking.md): family tracker that remains the design-local view under the initiative layer.
- [decision_tracking.md](/docs/planning/decisions/decision_tracking.md): family tracker that remains the decision-local view under the initiative layer.
- [task_tracking.md](/docs/planning/tasks/task_tracking.md): family tracker that remains the task-local view under the initiative layer.
- [README.md](/docs/planning/initiatives/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Keep the planning corpus split by artifact family:
  - PRDs in `docs/planning/prds/`
  - decisions in `docs/planning/decisions/`
  - designs and plans in `docs/planning/design/`
  - engineer-sized execution tasks in `docs/planning/tasks/`
- Use the initiative layer as the cross-family coordination view, not as a replacement for those authored families.
- Use `plan/plan_overview.md` as the live human start-here surface for current planning state.
- Use `docs/planning/coordination_tracking.md` as the root human start-here surface for the docs-backed traced planning corpus.
- Treat the initiative index and initiative tracker as derived rendered surfaces, not as the authoritative source for artifact content or task state.
- Treat the initiative layer as a compact rendered surface, not as the canonical deep-planning join for one trace now that the planning catalog exists.
- Keep `initiative_tracking.md` compact and scan-first. Prefer brief zero-state text and linked key surfaces over repeated explanatory scaffolding.
- Use `plan/.wt/indexes/coordination_index.json` as the live machine start-here path for repo-level planning state.
- Use `watchtower-core query coordination --format json` when you need the live machine-readable start-here coordination payload.
- Use the authority map when you need to confirm whether initiative lookup, coordination, traceability, or the planning catalog is canonical for a specific planning question.
- Keep the initiative layer compact enough that the coordination index can project from it without becoming a second planning authority.
- Use the unified traceability index as the authoritative machine join for durable artifact links and initiative closeout state.
- Use the task index and task records as the authoritative source for active owners, open tasks, blockers, and execution status.
- Publish one initiative entry per shared `trace_id`.
- Keep active initiatives explicitly task-backed; do not leave an initiative active without durable task linkage.
- Active initiatives should usually be explicitly owned through non-terminal task records.
- The allowed exception is active `closeout`, where all linked tasks may already be terminal and initiative closeout is the only remaining step.
- Every initiative entry must make these questions easy to answer:
  - what this initiative is
  - whether it is active or closed
  - what phase it is currently in
  - who is actively working on it
  - what the next expected step is
  - which surface the next contributor should open
- Use only these initiative phase values:
  - `implementation_planning`
  - `execution`
  - `closeout`
  - `closed`
- Derive `primary_owner` only when exactly one active owner is present on non-terminal task records for the initiative.
- Publish `active_owners` and `active_task_ids` when open task records exist.
- Publish compact `active_task_summaries` for active initiatives with non-terminal tasks so machines can see task names and actionability without reparsing the task index first.
- Allow active `closeout` entries to publish historical `task_ids` without `active_task_ids` when no non-terminal tasks remain and initiative closeout is the only next action.
- Active initiatives outside `closeout` should carry linked task IDs and active-task rendered detail instead of relying on implied execution ownership.
- Use `closed` as the initiative phase for terminal initiative states rather than overloading `current_phase` with `completed`, `superseded`, `cancelled`, or `abandoned`.
- For terminal initiatives, project entry `updated_at` from the later of traceability `updated_at` and `closed_at`.
- Publish initiative-entry lifecycle as `artifact_status` and initiative outcome as `initiative_status`; do not collapse those meanings into one generic entry-level `status` field.
- Make `next_action` specific enough that the next contributor can act without re-deriving the lifecycle state from several trackers.
- Make `next_surface_path` point to the repo-local surface the next contributor should open first.

## Structure or Data Model
### Source-of-truth layers
| Layer | Role |
|---|---|
| Traceability index | Authoritative machine join for trace-linked artifact IDs and initiative closeout status |
| Task records and task index | Authoritative source for active ownership, blockers, and execution state |
| Initiative index | Derived machine-readable live initiative-family surface |
| `initiative_tracking.md` | Derived human-readable initiative board |

### Initiative phase expectations
| Phase | Meaning | Typical Next Step |
|---|---|---|
| `implementation_planning` | Capture, review, or approval work is still in progress before execution starts. | Finish capture, pass validation, and approve readiness. |
| `execution` | Execution or blocking work is active for the initiative. | Continue, unblock, review, or close the active task set. |
| `closeout` | Execution is complete and closeout or promotion work is underway. | Finalize closeout, evidence, and promotion decisions. |
| `closed` | The initiative has reached a terminal closeout state. | No further default action. |

## Process or Workflow
1. Keep authored planning artifacts and task records current in their family directories.
2. Rebuild the family-specific indexes and the unified traceability index when traced artifacts or tasks change materially.
3. Rebuild the initiative index after those source surfaces change.
4. Rebuild the human initiative tracker from the initiative index in the same change set.
5. Use the initiative tracker as the deeper docs-backed initiative-family view beneath the live `plan/**` entrypoints and `coordination_tracking.md`.

## Operationalization
- `Modes`: `documentation`; `artifact`
- `Operational Surfaces`: `docs/planning/initiatives/`; `plan/.wt/indexes/initiative_index.json`; `plan/plan_overview.md`; `docs/planning/prds/`

## Validation
- Every initiative entry should correspond to one current traceability entry.
- Every initiative entry should publish `current_phase`, `next_action`, and `next_surface_path`.
- Active initiative owner and active-task rendered detail should agree with the current open task corpus whenever non-terminal tasks exist.
- Active initiatives should not remain in the index without linked task IDs.
- Active initiatives outside `closeout` should not remain in the index without non-terminal task ownership.
- Initiative closeout state should agree with the traceability index rather than competing with it.
- Terminal initiative entries should not publish `updated_at` earlier than `closed_at`.
- Reviewers should reject initiative views that hide ambiguity by inventing owners, tasks, or progress that the source surfaces do not publish.

## Change Control
- Update this standard when the repository changes initiative phase vocabulary, initiative authority boundaries, or the start-here planning experience.
- Update the initiative-index schema, initiative sync logic, initiative tracker, and affected planning README surfaces in the same change set when initiative tracking changes structurally.

## References
- [traceability_standard.md](/docs/standards/governance/traceability_standard.md)
- [initiative_closeout_standard.md](/docs/standards/governance/initiative_closeout_standard.md)
- [coordination_tracking_standard.md](/docs/standards/governance/coordination_tracking_standard.md)
- [task_tracking_standard.md](/docs/standards/governance/task_tracking_standard.md)
- [initiative_index_standard.md](/docs/standards/data_contracts/initiative_index_standard.md)
- [README.md](/docs/planning/initiatives/README.md)

## Updated At
- `2026-03-17T06:08:09Z`
