---
id: "std.data_contracts.route_index"
title: "Route Index Standard"
summary: "This standard defines the role, structure, and boundary rules for machine-readable route indexes stored under `core/control_plane/indexes/routes/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "route_index"
owner: "repository_maintainer"
updated_at: "2026-03-11T06:00:00Z"
audience: "shared"
authority: "authoritative"
---

# Route Index Standard

## Summary
This standard defines the role, structure, and boundary rules for machine-readable route indexes stored under `core/control_plane/indexes/routes/`.

## Purpose
Provide a compact machine-readable projection of the routing table so route-preview tooling can resolve task types and required workflow modules without reparsing `workflows/ROUTING_TABLE.md` on every lookup.

## Scope
- Applies to machine-readable route index artifacts stored under `core/control_plane/indexes/routes/`.
- Covers route entry shape, derivation boundaries, and how route-preview consumers should treat the index.
- Does not replace `AGENTS.md`, `workflows/ROUTING_TABLE.md`, or the workflow modules as the procedural authority.

## Use When
- Updating `workflows/ROUTING_TABLE.md`.
- Adding or reviewing route-preview tooling.
- Auditing whether routed task types still point to the correct workflow modules.

## Related Standards and Sources
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): defines the higher-level routing semantics that the route index mirrors for machine use.
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md): defines the companion workflow lookup surface referenced by route entries.
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md): published route indexes use JSON as the governed machine-readable format.
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md): canonical authored routing source that the route index derives from.

## Guidance
- Model route lookup as a derived index, not as an authored registry.
- Rebuild the route index deterministically from `workflows/ROUTING_TABLE.md`.
- Store published route indexes under `core/control_plane/indexes/routes/`.
- Keep the companion artifact schema under `core/control_plane/schemas/artifacts/`.
- Use JSON for the published route-index artifact.
- Every route entry must point only to workflow modules under `workflows/modules/`.
- Carry stable `route_id` values derived from the routed task-type label.
- Publish both required workflow identifiers and required workflow paths so loaders can validate integrity without reparsing Markdown.
- Treat the route index as advisory lookup data for tools such as `watchtower-core route preview`; the routing table and workflow docs remain the human and procedural authority.
- Keep the route index aligned with the routing table in the same change set.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the route-index artifact family. |
| `id` | Required | Stable identifier for the route index artifact. |
| `title` | Required | Human-readable title for the index artifact. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `entries` | Required | Array of route records. |

### Route entry fields
| Field | Requirement | Notes |
|---|---|---|
| `route_id` | Required | Stable route identifier derived from the task-type label. |
| `task_type` | Required | Human-readable routed task-type label from the routing table. |
| `trigger_keywords` | Required | Example trigger phrases published in the routing table. |
| `required_workflow_ids` | Required | Stable workflow identifiers required by the route. |
| `required_workflow_paths` | Required | Repository-relative workflow module paths required by the route. |

## Operationalization
- `Modes`: `artifact`; `schema`; `workflow`
- `Operational Surfaces`: `core/control_plane/indexes/routes/`; `core/control_plane/schemas/artifacts/`; `workflows/modules/`; `workflows/ROUTING_TABLE.md`

## Validation
- The route index should validate against its published artifact schema.
- Every `required_workflow_path` should exist under `workflows/modules/`.
- Every `required_workflow_id` should resolve to a companion workflow-index entry.
- Every route should publish at least one trigger keyword and one required workflow.
- Reviewers should reject route-index changes that introduce behavior not present in the authored routing table.

## Change Control
- Update this standard when the repository changes how task routing is indexed or previewed.
- Update the companion artifact schema, examples, live route index, command docs, and routing guidance in the same change set when the route-index family changes structurally.

## References
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md)
- [workflow_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/workflow_index_standard.md)
- [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md)

## Updated At
- `2026-03-11T06:00:00Z`
