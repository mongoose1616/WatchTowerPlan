# `watchtower_core`

## Summary
`watchtower_core` is the reusable-core Python package for loader, schema, validation, query, sync, rebuild, routing, and workflow primitives. Host-owned CLI composition now lives under `watchtower_host`, and pack-native orchestration belongs under `watchtower_<pack>`.

## Boundary
- `Classification`: `runtime_architecture_start_here`
- `Supported Imports`: Start with the package-specific READMEs below before importing from a new namespace.
- `Non-Goals`: This file does not define a stable wildcard import surface for the whole package, and `watchtower_core` is not a catch-all home for pack-owned logic that should stay under the owning `watchtower_<pack>` package.

## Governing Foundations
- [repository_scope.md](/core/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/core/docs/foundations/engineering_design_principles.md)
- [engineering_stack_direction.md](/core/docs/foundations/engineering_stack_direction.md)

## Governing Standards
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md)
- [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md)
- [core_host_pack_python_boundary_standard.md](/core/docs/standards/engineering/core_host_pack_python_boundary_standard.md)
- [pack_interface_contract_standard.md](/core/docs/standards/data_contracts/pack_interface_contract_standard.md)
- [engineering_best_practices_standard.md](/core/docs/standards/engineering/engineering_best_practices_standard.md)

## Package Map
| Package | Classification | Use It For |
|---|---|---|
| `adapters/` | `reusable_core` | Parsing and normalizing governed front matter and Markdown surfaces. |
| `control_plane/` | `reusable_core` | Workspace-aware schema, artifact, and loader primitives. |
| `documentation/` | `reusable_core` | Repo-shared governed-document semantics, front-matter path normalization, and standard/reference helper logic used by validation and sync services. |
| `benchmarking/` | `reusable_core` | Governed benchmark suite execution, telemetry-on versus telemetry-off comparison, retained benchmark record generation, and fail-closed benchmarking helpers. |
| `validation/` | `reusable_core` | Export-safe validation services, pack-target enumeration, and result models; pack-owned semantic validators stay under the owning `watchtower_<pack>.validation` package. |
| `query/` | `reusable_core` | Export-safe generic query services over governed command, workflow, route, surface, and artifact-family metadata; pack-local lifecycle or coordination queries stay under the owning `watchtower_<pack>.query` package. |
| `sync/` | `reusable_core` | Export-safe sync harness and repo-shared command, route, and repository-path index rebuild services; pack-local sync orchestration stays under the owning `watchtower_<pack>.sync` package. |
| `telemetry/` | `reusable_core` | Local runtime telemetry session creation, nested operation timing, JSONL sinks, and fail-open stderr summaries for CLI execution. |
| `rebuild/` | `reusable_core` | Export-safe rebuild harness primitives plus registry-backed rendered-view building and markdown reconciliation; pack-owned output shaping stays outside the reusable-core package root. |
| `routing/` | `reusable_core` | Export-safe route-selection runtime over the governed route and workflow indexes; CLI formatting and repo-local route handlers stay out of the package root. |
| `workflow_execution/` | `reusable_core` | Export-safe workflow execution harness built on routed workflow selection and callback-based execution hooks; repo-local workflow behavior stays out of the package root. |
| `integrations/` | `boundary_layer` | External-system integration clients such as GitHub. |
| `cli/` | `boundary_guard` | Thin compatibility shim plus reusable CLI support helpers that pack namespaces may import without depending on host composition. |
| `closeout/` | `boundary_guard` | Fail-closed compatibility guard; pack-owned closeout services live under the owning `watchtower_<pack>.closeout` package. |
| `evidence/` | `reusable_core` | Validation-evidence records plus pack-local evidence-bundle helpers for readiness, review, and closeout flows. |
| `utils/` | `reusable_core` | Small shared helpers with low coupling. |

## Related Surfaces
- `core/python/README.md`
- `core/python/src/watchtower_host/README.md`
- `core/docs/standards/engineering/python_code_design_standard.md`
- `core/docs/standards/engineering/core_host_pack_python_boundary_standard.md`
- The owning pack Python README for pack-native runtime behavior

## Notes
- Keep new generic loaders, validators, query helpers, sync helpers, rebuild helpers, adapters, and utilities in `watchtower_core`.
- Reach pack-owned behavior through the owning `watchtower_<pack>` package only when the behavior is truly tied to a pack-local workspace.
- Do not pull pack-owned logic back into reusable core when the behavior still depends on pack-local lifecycle rules, rendered surfaces, or workspace state.
- Runtime telemetry is an active reusable-core baseline. Use `watchtower_core.telemetry` for per-command sessions and nested operation timing instead of ad hoc stderr timers or pack-local JSONL writers.
- Deliberate retained performance measurement belongs in `watchtower_core.benchmarking`, not in the default-on telemetry package.
