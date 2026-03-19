---
id: "std.governance.initiative_tracking"
title: "Initiative Tracking Standard"
summary: "This standard defines the repository's live initiative tracking model over plan/.wt indexes with richer human companion trackers."
type: "standard"
status: "active"
tags:
  - "standard"
  - "governance"
  - "initiative_tracking"
owner: "repository_maintainer"
updated_at: "2026-03-18T14:00:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "plan/tracking/initiative_tracking.md"
  - "plan/.wt/indexes/initiative_index.json"
aliases:
  - "initiative tracking"
  - "initiative coordination"
  - "cross-family planning status"
---

# Initiative Tracking Standard

## Summary
This standard defines the repository's live initiative tracking model so one trace can be followed from PRD through design, planning, execution, validation, and closeout through `plan/.wt` machine authority plus richer human companion trackers.

## Purpose
- Give humans one family-specific initiative view for "what is this initiative, who owns it, what phase is it in, what is next, and what already closed?"
- Preserve the artifact-family split for PRDs, decisions, designs, plans, and tasks instead of collapsing everything into one mixed tracker.
- Publish one machine-readable initiative surface under `plan/.wt/indexes/initiative_index.json` so coordination and family workflows do not reconstruct phase and ownership by hand.
- Keep the human initiative tracker rich enough for real browsing instead of collapsing terminal history into count-only summaries.

## Scope
- Applies to the human-readable initiative tracker under `plan/tracking/initiative_tracking.md`.
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
- [task_tracking_standard.md](/docs/standards/governance/task_tracking_standard.md): defines the authoritative live task layer that initiative owner and active-task detail must read from.
- [initiative_index_standard.md](/docs/standards/data_contracts/initiative_index_standard.md): defines the machine-readable initiative rendered-surface contract.
- [README.md](/plan/tracking/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Keep the live initiative package split by responsibility:
  - initiative capture in `initiative_brief.md`
  - durable rationale in `decision_notes.md` when needed
  - technical design in `design_record.md`
  - implementation sequencing in `implementation_slice.md`
  - engineer-sized execution tasks in live `plan/**/.wt/tasks/**`
- Use the initiative layer as the cross-family coordination view, not as a replacement for those authored surfaces.
- Use `plan/plan_overview.md` as the live human start-here surface for current planning state.
- Use `plan/tracking/coordination_tracking.md` as the richer human coordination companion beneath the summary-first overview.
- Treat the initiative index and initiative tracker as derived rendered surfaces, not as the authoritative source for artifact content or task state.
- Keep `initiative_tracking.md` summary-first, but retain full active and terminal initiative tables so humans can browse history without relying on machine output for ordinary review.
- Use `plan/.wt/indexes/coordination_index.json` as the live machine start-here path for repo-level planning state.
- Use the unified traceability index as the authoritative machine join for durable artifact links and initiative closeout state.
- Use the live task index and task records as the authoritative source for active owners, open tasks, blockers, and execution status.
- Publish one initiative entry per shared `trace_id`.
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

## Structure or Data Model
### Source-of-truth layers
| Layer | Role |
|---|---|
| Traceability index | Authoritative machine join for trace-linked artifact IDs and initiative closeout status |
| Live task records and task index | Authoritative source for active ownership, blockers, and execution state |
| Initiative index | Derived machine-readable live initiative-family surface |
| `initiative_tracking.md` | Derived human-readable initiative board with browseable active and terminal tables |

## Process or Workflow
1. Keep authored planning artifacts and live task records current in their family roots.
2. Rebuild the family-specific indexes and the unified traceability index when traced artifacts or tasks change materially.
3. Rebuild the initiative index after those source surfaces change.
4. Rebuild the human initiative tracker from the initiative index in the same change set.
5. Use the initiative tracker as the deeper human initiative-family view beneath the live `plan/**` entrypoints and `coordination_tracking.md`.

## Operationalization
- `Modes`: `documentation`; `artifact`
- `Operational Surfaces`: `plan/tracking/initiative_tracking.md`; `plan/.wt/indexes/initiative_index.json`; `plan/plan_overview.md`

## Validation
- Every initiative entry should correspond to one current traceability entry.
- Every initiative entry should publish `current_phase`, `next_action`, and `next_surface_path`.
- Active initiative owner and active-task detail should agree with the current live task corpus whenever non-terminal tasks exist.
- Initiative closeout state should agree with the traceability index rather than competing with it.
- Reviewers should reject initiative views that hide ambiguity by inventing owners, tasks, or progress that the source surfaces do not publish.
- Reviewers should also reject initiative views that collapse terminal history into count-only summaries when the generated tracker can show the underlying rows directly.

## Change Control
- Update this standard when the repository changes initiative phase vocabulary, initiative authority boundaries, or the start-here planning experience.
- Update the initiative-index schema, initiative sync logic, initiative tracker, and affected planning README surfaces in the same change set when initiative tracking changes structurally.

## References
- [traceability_standard.md](/docs/standards/governance/traceability_standard.md)
- [initiative_closeout_standard.md](/docs/standards/governance/initiative_closeout_standard.md)
- [coordination_tracking_standard.md](/docs/standards/governance/coordination_tracking_standard.md)
- [task_tracking_standard.md](/docs/standards/governance/task_tracking_standard.md)
- [initiative_index_standard.md](/docs/standards/data_contracts/initiative_index_standard.md)
- [README.md](/plan/tracking/README.md)

## Updated At
- `2026-03-18T14:00:00Z`
