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
| `validation/` | `reusable_core` | Export-safe validation services and result models; repo-local document semantics and aggregate validation stay under `repo_ops.validation`. |
| `query/` | `reusable_core` | Export-safe generic query services over governed command, workflow, route, surface, and artifact-family metadata; live planning queries stay under `repo_ops.query`. |
| `sync/` | `reusable_core` | Export-safe sync harness and target contracts; repo-local sync target registries and orchestration live under `repo_ops.sync`. |
| `rebuild/` | `reusable_core` | Export-safe rebuild harness primitives plus registry-backed rendered-view building and markdown reconciliation; repo-local output shaping stays under `repo_ops`. |
| `routing/` | `reusable_core` | Export-safe route-selection runtime over the governed route and workflow indexes; CLI formatting and repo-local route handlers stay out of the package root. |
| `workflow_execution/` | `reusable_core` | Export-safe workflow execution harness built on routed workflow selection and callback-based execution hooks; repo-local workflow behavior stays out of the package root. |
| `integrations/` | `boundary_layer` | External-system integration clients such as GitHub. |
| `repo_ops/` | `repo_local_orchestration` | Residual WatchTowerPlan-specific orchestration that remains after reusable-core extraction; shrink it rather than adding new generic behavior. |
| `cli/` | `repo_local_orchestration` | CLI parser wiring and command-family registration. |
| `closeout/` | `repo_local_orchestration` | Traced closeout services plus pack-level initiative-package closeout coordination helpers. |
| `evidence/` | `reusable_core` | Validation-evidence ledgers plus pack-local evidence-bundle helpers for readiness, review, and closeout flows. |
| `utils/` | `reusable_core` | Small shared helpers with low coupling. |

## Related Surfaces
- `core/python/README.md`
- `docs/standards/engineering/python_code_design_standard.md`
- `core/python/src/watchtower_core/repo_ops/README.md`
- `docs/planning/design/features/core_export_ready_architecture.md`
