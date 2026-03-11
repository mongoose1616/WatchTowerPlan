# `watchtower_core`

## Summary
`watchtower_core` is the in-repo Python package for control-plane loading, governed validation, repo-local orchestration, and the `watchtower-core` CLI.

## Boundary
- `Classification`: `runtime_architecture_start_here`
- `Supported Imports`: Start with the package-specific READMEs below before importing from a new namespace.
- `Non-Goals`: This file does not define a stable wildcard import surface for the whole package.

## Package Map
| Package | Classification | Use It For |
|---|---|---|
| `adapters/` | `reusable_core` | Parsing and normalizing governed front matter and Markdown surfaces. |
| `control_plane/` | `reusable_core` | Workspace-aware schema, artifact, and loader primitives. |
| `validation/` | `reusable_core` | Export-safe validation services and result models. |
| `query/` | `boundary_layer` | Compatibility namespace for explicit query wrappers, not repo-local query orchestration. |
| `sync/` | `boundary_layer` | Compatibility namespace for explicit sync wrappers, not repo-local sync orchestration. |
| `integrations/` | `boundary_layer` | External-system integration clients such as GitHub. |
| `repo_ops/` | `repo_local_orchestration` | WatchTowerPlan-specific planning, query, sync, and validation behavior. |
| `cli/` | `repo_local_orchestration` | CLI parser wiring and command-family registration. |
| `closeout/` | `repo_local_orchestration` | Initiative closeout services and future release/report closeout helpers. |
| `evidence/` | `reusable_core` | Validation-evidence recording helpers. |
| `utils/` | `reusable_core` | Small shared helpers with low coupling. |

## Related Surfaces
- `core/python/README.md`
- `core/python/src/watchtower_core/repo_ops/README.md`
- `docs/planning/design/features/core_export_ready_architecture.md`
