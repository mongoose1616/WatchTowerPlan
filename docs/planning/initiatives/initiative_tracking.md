# Initiative Tracking

## Summary
This document provides the human-readable start-here view for traced initiatives across PRDs, decisions, designs, implementation plans, tasks, validation, and closeout. Use it when the main question is what phase an initiative is in, who is currently working on it, and what should happen next.

## Active Initiatives
| Trace ID | Phase | Owners | Open Tasks | Key Surface | Next Surface | Next Action |
|---|---|---|---|---|---|---|
| `trace.acceptance_evidence_reconciliation` | `design` | unassigned | `0` | `docs/planning/design/features/acceptance_evidence_reconciliation.md` | `docs/planning/design/implementation/` | Create or update an implementation plan so the approved design becomes executable work. |
| `trace.command_documentation_and_lookup` | `design` | unassigned | `0` | `docs/planning/design/features/command_documentation_and_lookup.md` | `docs/planning/design/implementation/` | Create or update an implementation plan so the approved design becomes executable work. |
| `trace.github_collaboration` | `design` | unassigned | `0` | `docs/planning/design/features/github_collaboration_scaffolding.md` | `docs/planning/design/implementation/` | Create or update an implementation plan so the approved design becomes executable work. |
| `trace.initiative_closeout` | `design` | unassigned | `0` | `docs/planning/design/features/initiative_closeout_and_planning_trackers.md` | `docs/planning/design/implementation/` | Create or update an implementation plan so the approved design becomes executable work. |
| `trace.core_python_foundation` | `closeout` | unassigned | `0` | `docs/planning/prds/core_python_foundation.md` | `docs/commands/core_python/watchtower_core_closeout_initiative.md` | Run initiative closeout or create explicit follow-up tasks before marking the initiative complete. |

## Closed Initiatives
| Trace ID | Initiative Status | Key Surface | Closed At | Closure Reason |
|---|---|---|---|---|
| `trace.local_task_tracking` | `completed` | `docs/planning/design/features/github_task_push_sync.md` | `2026-03-09T16:14:50Z` | Delivered and validated |

## Update Rules
- Treat the unified traceability index, family-specific planning indexes, and task index as the authoritative source surfaces for this tracker.
- Rebuild this tracker in the same change set when traced planning, task, validation, or closeout state changes materially.
- Use this tracker as the start-here cross-family initiative view, and use the PRD, decision, design, and task trackers as local family views.
- Keep the machine-readable companion index at [initiative_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/initiatives/initiative_index.v1.json) aligned with this tracker.

## References
- [README.md](/home/j/WatchTowerPlan/docs/planning/initiatives/README.md)
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md)
- [initiative_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/initiative_index_standard.md)
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md)

## Updated At
- `2026-03-10T02:30:31Z`
