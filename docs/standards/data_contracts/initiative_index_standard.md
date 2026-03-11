---
id: "std.data_contracts.initiative_index"
title: "Initiative Index Standard"
summary: "This standard defines the role, structure, and boundary rules for machine-readable initiative indexes stored under `core/control_plane/indexes/initiatives/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "initiative_index"
owner: "repository_maintainer"
updated_at: "2026-03-11T06:21:01Z"
audience: "shared"
authority: "authoritative"
---

# Initiative Index Standard

## Summary
This standard defines the role, structure, and boundary rules for machine-readable initiative indexes stored under `core/control_plane/indexes/initiatives/`.

## Purpose
- Provide one compact machine-readable initiative-family view over the current traced initiative corpus.
- Let agents and engineers answer "what phase is this initiative in, who is working on it, and what is next?" without reparsing multiple family trackers or raw Markdown documents.
- Keep the initiative view derived so it does not compete with the traceability index, family indexes, or task records as authoritative sources.
- Keep the initiative layer distinct from the repo-level coordination index that now sits above it as the default machine start-here surface.

## Scope
- Applies to machine-readable initiative index artifacts stored under `core/control_plane/indexes/initiatives/`.
- Covers placement, root artifact fields, initiative entry shape, and update expectations.
- Does not replace the unified traceability index, family-specific indexes, or task records.

## Use When
- Building lookup or review tooling that needs a single initiative-centric view.
- Refreshing derived initiative coordination data after PRDs, decisions, designs, plans, tasks, evidence, or closeout state change.
- Reviewing whether the current initiative phase and ownership are explicit enough for another contributor to continue the work.

## Related Standards and Sources
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): defines the coordination boundary, phase vocabulary, and authority model this index must preserve.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): defines the traced artifact relationships the initiative index projects from.
- [initiative_closeout_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_closeout_standard.md): defines initiative closeout state that this index must mirror.
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md): defines the task authority layer this index must use for owner and open-task projection.
- [coordination_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/coordination_index_standard.md): defines the repo-level coordination overlay that projects from this initiative-family view.
- [schema_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_catalog_standard.md): defines the schema-catalog update expectations for this artifact family.
- [timestamp_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/timestamp_standard.md): defines the timestamp format used by initiative records.
- [initiative_tracking.md](/home/j/WatchTowerPlan/docs/planning/initiatives/initiative_tracking.md): companion human-readable initiative view that should remain aligned with this index.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/initiatives/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Model initiative coordination as an index, not as a registry.
- Treat the initiative index as a derived machine-readable projection over traced planning and task surfaces.
- Keep the initiative index focused on initiative-family detail rather than repo-level bootstrap or recent-closeout summary state.
- Store published initiative indexes under `core/control_plane/indexes/initiatives/`.
- Keep the companion artifact schema under `core/control_plane/schemas/artifacts/`.
- Use JSON for the published initiative index artifact.
- Build the initiative index from the traceability index plus current planning and task indexes rather than scanning human trackers.
- Carry `current_phase`, `next_action`, and `next_surface_path` in every active initiative entry.
- Carry active owner and open-task projection for every active initiative with non-terminal tasks.
- Carry compact `active_task_summaries` for active initiatives with non-terminal tasks so the first machine coordination pass can see task titles, status, priority, ownership, and actionability without reopening the task index immediately.
- Do not publish an active initiative entry without linked task IDs.
- Mirror terminal initiative closeout state from traceability rather than inventing a second closeout authority.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the initiative-index artifact family. |
| `id` | Required | Stable identifier for the initiative index artifact. |
| `title` | Required | Human-readable title for the index artifact. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `entries` | Required | Array of initiative records. |

### Initiative entry fields
| Field | Requirement | Notes |
|---|---|---|
| `trace_id` | Required | Shared umbrella identifier for the initiative. |
| `title` | Required | Human-readable initiative title. |
| `summary` | Required | Concise description of the initiative. |
| `artifact_status` | Required | Use the governed lifecycle vocabulary mirrored from traceability for the projected governing artifact. |
| `initiative_status` | Required | Use the initiative closeout vocabulary mirrored from traceability. |
| `current_phase` | Required | Use the governed initiative-phase vocabulary. |
| `updated_at` | Required | RFC 3339 UTC timestamp matching the latest governing source. |
| `open_task_count` | Required | Number of non-terminal tasks currently linked to the initiative. |
| `blocked_task_count` | Required | Number of active tasks currently blocked or carrying blockers. |
| `key_surface_path` | Required | Primary planning surface to open for understanding the initiative. |
| `next_action` | Required | Short human-readable statement of the next expected step. |
| `next_surface_path` | Required | Repository-relative path to the next surface a contributor should open first. |
| `primary_owner` | Conditionally required | Use when exactly one active owner is present. |
| `active_owners` | Conditionally required | Current owners of open tasks when present and especially when more than one owner is active. |
| `active_task_ids` | Conditionally required | Non-terminal local task IDs for active initiatives. Required for active initiatives outside `validation` and `closeout`. |
| `active_task_summaries` | Conditionally required | Compact active-task summaries for active initiatives outside `validation` and `closeout`, including task title, status, priority, owner, doc path, and actionability. |
| `blocked_by_task_ids` | Optional | Blocking task IDs referenced by current active tasks when present. |
| `prd_ids` | Optional | Linked PRD IDs for the initiative. |
| `decision_ids` | Optional | Linked decision IDs for the initiative. |
| `design_ids` | Optional | Linked feature-design IDs for the initiative. |
| `plan_ids` | Optional | Linked implementation-plan IDs for the initiative. |
| `task_ids` | Conditionally required | All linked task IDs for the initiative; active initiatives should not omit this field. |
| `acceptance_ids` | Optional | Linked acceptance IDs for the initiative. |
| `acceptance_contract_ids` | Optional | Linked acceptance-contract IDs for the initiative. |
| `evidence_ids` | Optional | Linked validation-evidence IDs for the initiative. |
| `closed_at` | Optional | Required when `initiative_status` is terminal. |
| `closure_reason` | Optional | Required when `initiative_status` is terminal. |
| `superseded_by_trace_id` | Optional | Required when `initiative_status` is `superseded`. |
| `related_paths` | Optional | Related repository paths strongly associated with the initiative. |
| `tags` | Optional | Retrieval-oriented tags when useful. |
| `notes` | Optional | Short coordination notes carried forward from source surfaces. |

## Operationalization
- `Modes`: `schema`; `artifact`; `documentation`
- `Operational Surfaces`: `core/control_plane/schemas/artifacts/`; `core/control_plane/indexes/initiatives/`; `core/control_plane/indexes/initiatives/README.md`; `docs/planning/initiatives/initiative_tracking.md`

## Validation
- The initiative index should validate against its published artifact schema.
- Every initiative entry should correspond to one current traceability entry.
- `current_phase` should agree with the current planning and task state implied by the authoritative source surfaces.
- Active initiative `task_ids` should agree with the current linked task corpus.
- Active initiatives outside `validation` and `closeout` should also keep `primary_owner` or `active_owners` plus `active_task_ids` and `active_task_summaries` aligned with the current non-terminal task corpus.
- Active `validation` and `closeout` entries may have only historical `task_ids` when no non-terminal tasks remain and validation or initiative closeout is the only next action.
- Terminal initiative entries should also publish the required closeout fields.
- Entry payloads should use `artifact_status` rather than a generic `status` field so initiative outcome and artifact lifecycle remain distinct.

## Change Control
- Update this standard when the repository changes the initiative-phase projection model or initiative-index entry shape.
- Update the companion artifact schema, examples, and live initiative index in the same change set when the initiative-index family changes structurally.
- Update the human-readable initiative tracker in the same change set when indexed initiative coordination changes materially.

## References
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md)
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md)
- [task_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/task_tracking_standard.md)
- [initiative_tracking.md](/home/j/WatchTowerPlan/docs/planning/initiatives/initiative_tracking.md)

## Updated At
- `2026-03-11T06:21:01Z`
