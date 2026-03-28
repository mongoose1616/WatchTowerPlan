# `core/workflows`

## Description
`This directory is the authoritative reusable-core workflow root and shared agent-execution surface. It holds shared routing guidance, reusable workflow modules, and any future shared workflow roles for core implementation, review, validation, documentation, and repository-governance work.`

## Paths
| Path | Description |
|---|---|
| `core/workflows/README.md` | Describes the purpose of the core workflow root and its owned workflow surfaces. |
| `core/workflows/AGENTS.md` | Defines local instructions for core-owned workflow guidance. |
| `core/workflows/ROUTING_TABLE.md` | Defines the reusable-core task routes and shared workflow-module selection rules. |
| `core/workflows/modules/README.md` | Explains the authoritative core workflow-module set. |
| `core/workflows/roles/README.md` | Describes the shared workflow-role root and its current reserved status. |

## Notes
- Workflow-root boundaries and routing behavior are governed by `core/docs/foundations/repository_scope.md`, `core/docs/standards/workflows/routing_and_context_loading_standard.md`, and the authoritative routing tables.
- Shared reusable workflow modules live under `core/workflows/modules/` and should stay donor-neutral enough for multiple WatchTower repos or packs to reuse without local rewrites.
- Shared reusable workflow roles, when they exist, live under `core/workflows/roles/`.
- Pack-owned routing and orchestration live under the owning pack workflow roots and may reference shared modules from this root instead of copying them.
