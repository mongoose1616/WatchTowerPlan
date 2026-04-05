# `plan/workflows`

## Description
`This directory is the authoritative workflow root for the live plan domain. Use it for initiative, project, promotion, traceability, and plan-specific task procedures, while reusing shared modules from core/workflows where appropriate.`

## Paths
| Path | Description |
|---|---|
| `plan/workflows/README.md` | Describes the purpose of the plan workflow entrypoint and its owned workflow surfaces. |
| `plan/workflows/AGENTS.md` | Defines local instructions for plan-domain workflow guidance surfaces. |
| `plan/workflows/ROUTING_TABLE.md` | Defines plan-domain task routes and the required workflow documents for those routes. |
| `plan/workflows/modules/README.md` | Explains the authoritative plan-owned workflow-module set. |
| `plan/workflows/roles/README.md` | Explains the authoritative plan-owned workflow-role set. |

## Notes
- Start here when the main question is how live plan work should be routed or narrated for humans.
- Shared reusable workflow modules remain under `core/workflows/modules/`.
- Shared reusable workflow roles remain under `core/workflows/roles/`.
- Plan-specific routing, workflow modules, and workflow roles are authoritative here.
- `plan/.wt/registries/workflow_metadata_registry.json` is the plan-owned machine companion for these authored workflow docs and keeps shared workflow indexing plus route preview pack-aware.
- The active plan-owned role set currently includes `planning_author.md`, `task_coordinator.md`, and `traceability_steward.md`.
- Narrow module-first routes remain authoritative for specific planning tasks, and broad role routes now cover end-to-end planning authoring, task coordination, and traceability governance when one request spans multiple plan modules.
