---
id: "std.data_contracts.coordination_index"
title: "Coordination Index Standard"
summary: "This standard defines the role, structure, and boundary rules for machine-readable coordination indexes stored under `core/control_plane/indexes/coordination/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "coordination_index"
  - "planning_index_family"
owner: "repository_maintainer"
updated_at: "2026-03-13T20:01:23Z"
audience: "shared"
authority: "authoritative"
---

# Coordination Index Standard

## Summary
This standard defines the role, structure, and boundary rules for machine-readable coordination indexes stored under `core/control_plane/indexes/coordination/`.

## Purpose
- Provide one always-useful machine start-here surface for current planning state.
- Project actionable work, blockers, recent closeouts, and bootstrap-ready guidance without reopening multiple planning families on the first pass.
- Keep the coordination layer derived so it does not compete with initiative, task, or traceability authority.

## Scope
- Applies to machine-readable coordination index artifacts stored under `core/control_plane/indexes/coordination/`.
- Covers placement, root artifact fields, coordination-mode semantics, and the projected initiative and task summaries carried by this family.
- Does not replace initiative, task, or traceability indexes as their family authorities.

## Use When
- Building agent or automation entrypoints that need one deterministic current-state surface.
- Refreshing coordination state after initiative, task, or traceability surfaces change.
- Reviewing whether the repository is actively executing work, blocked, or ready for one new initiative.

## Related Standards and Sources
- [planning_index_family_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_index_family_standard.md): defines the shared derived-index baseline and discoverability contract this family-specific standard narrows.
- [initiative_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/initiative_index_standard.md): defines the initiative-family projection that this coordination layer reads from.
- [task_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/task_index_standard.md): defines the task authority layer behind actionable work and blockers.
- [traceability_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/traceability_index_standard.md): defines the durable trace join that initiative state still mirrors.
- [coordination_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/coordination_tracking_standard.md): defines the compact human companion tracker derived from this index.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): defines the human initiative coordination layer that remains available beneath this machine-first view.
- [schema_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_catalog_standard.md): defines the schema-catalog update expectations for this artifact family.
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md): defines the timestamp format used by coordination records.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/coordination/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Apply the shared planning-index-family baseline in [planning_index_family_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/planning_index_family_standard.md).
- Build the coordination index from the initiative index and its task-backed active-task projection rather than reparsing human trackers.
- Publish one repo-level coordination mode and one recommended next action plus next surface path at the root of the artifact.
- Keep `entries` limited to the active current-state initiative set that the coordination start-here experience is summarizing.
- Carry actionable-task summaries only when they improve the first machine coordination pass.
- Carry recent closeout summaries as compact context rather than reproducing the full closed-history corpus.
- Preserve explicit historical lookup through initiative-family query paths instead of expanding the default coordination payload.
- Keep the coordination index smaller than the combined family indexes it summarizes.
- Do not invent owners, blockers, or status beyond what the initiative and task surfaces already publish.
- Keep embedded initiative summaries aligned with initiative-index explicit field naming, including `artifact_status` for lifecycle and `initiative_status` for outcome.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the coordination-index artifact family. |
| `id` | Required | Stable identifier for the coordination index artifact. |
| `title` | Required | Human-readable title for the index artifact. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `updated_at` | Required | Latest timestamp mirrored from the current initiative corpus. |
| `coordination_mode` | Required | Use one of `active_work`, `blocked_work`, or `ready_for_bootstrap`. |
| `summary` | Required | Concise explanation of the current coordination state. |
| `recommended_next_action` | Required | Short next-step statement for the default current state. |
| `recommended_surface_path` | Required | Repository-relative path to open first for the recommended next step. |
| `active_initiative_count` | Required | Number of active initiative entries currently projected. |
| `blocked_task_count` | Required | Number of blocked active tasks across active initiatives. |
| `actionable_task_count` | Required | Number of actionable active tasks across active initiatives. |
| `entries` | Required | Active initiative summaries used by the default coordination query path. |
| `actionable_tasks` | Required | Compact actionable-task summaries when present. Use an empty array when none are actionable. |
| `recent_closed_initiatives` | Required | Compact closeout context. Use an empty array when none are available. |

### Coordination expectations
| Field | Expectation |
|---|---|
| `coordination_mode` | `active_work` means active work exists, `blocked_work` means active execution exists but no actionable task is available, `ready_for_bootstrap` means no active initiatives remain. |
| `entries` | Keep initiative-shaped summaries compact, derived from the initiative index, and limited to active current-state initiatives. |
| `actionable_tasks` | Include trace context so a caller can jump directly to the right initiative and task surface. |
| `recent_closed_initiatives` | Publish only compact summaries needed for recent context and review handoff. Do not duplicate full closed-history initiative entries here. |
| Initiative entry status fields | Use `artifact_status` for lifecycle and `initiative_status` for initiative outcome. |

## Operationalization
- `Modes`: `schema`; `artifact`
- `Operational Surfaces`: `core/control_plane/schemas/artifacts/`; `core/control_plane/indexes/coordination/`; `core/control_plane/indexes/coordination/README.md`; `core/control_plane/examples/valid/indexes/coordination_index*.example.json`; `core/control_plane/examples/invalid/indexes/coordination_index*.example.json`

## Validation
- In addition to the shared planning-index-family validation contract:
- Every entry in the coordination index should correspond to one active initiative-index entry.
- `active_initiative_count` should equal the number of `entries`.
- Root counts should agree with the projected active initiatives and actionable-task summaries.
- `recommended_next_action` and `recommended_surface_path` should stay useful when the repo has no active initiative.
- The coordination index should remain compact enough that it improves machine navigation instead of recreating family-authority detail.

## Change Control
- In addition to the shared planning-index-family change-control contract:
- Update this standard when the repository changes the coordination-mode model or the projected coordination root fields.
- Update the coordination query docs, coordination-tracking companion surface, and nearby planning guidance when the coordination start-here experience changes materially.

## References
- [initiative_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/initiative_index_standard.md)
- [task_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/task_index_standard.md)
- [traceability_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/traceability_index_standard.md)
- [coordination_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/coordination_tracking_standard.md)

## Updated At
- `2026-03-13T20:01:23Z`
