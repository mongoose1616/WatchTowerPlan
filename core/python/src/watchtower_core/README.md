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
| `documentation/` | `reusable_core` | Repo-shared governed-document semantics, front-matter path normalization, and standard/reference helper logic used by validation and sync services. |
| `validation/` | `reusable_core` | Export-safe validation services and result models; plan-domain document semantics and aggregate validation stay under `watchtower_plan.validation`. |
| `query/` | `reusable_core` | Export-safe generic query services over governed command, workflow, route, surface, and artifact-family metadata; live planning queries stay under `watchtower_plan.query`. |
| `sync/` | `reusable_core` | Export-safe sync harness and repo-shared command, route, and repository-path index rebuild services; plan-domain sync registries and orchestration stay under `watchtower_plan.sync`. |
| `rebuild/` | `reusable_core` | Export-safe rebuild harness primitives plus registry-backed rendered-view building and markdown reconciliation; plan-owned output shaping stays outside the reusable-core package root. |
| `routing/` | `reusable_core` | Export-safe route-selection runtime over the governed route and workflow indexes; CLI formatting and repo-local route handlers stay out of the package root. |
| `workflow_execution/` | `reusable_core` | Export-safe workflow execution harness built on routed workflow selection and callback-based execution hooks; repo-local workflow behavior stays out of the package root. |
| `integrations/` | `boundary_layer` | External-system integration clients such as GitHub. |
| `cli/` | `repo_local_orchestration` | CLI parser wiring and command-family registration. |
| `closeout/` | `boundary_guard` | Fail-closed compatibility guard; plan-domain closeout services live under `watchtower_plan.closeout`. |
| `evidence/` | `reusable_core` | Validation-evidence ledgers plus pack-local evidence-bundle helpers for readiness, review, and closeout flows. |
| `utils/` | `reusable_core` | Small shared helpers with low coupling. |

## Related Surfaces
- `core/python/README.md`
- `core/docs/standards/engineering/python_code_design_standard.md`
- `plan/python/src/watchtower_plan/README.md`
- `requirements.md`
- `decisions.md`
