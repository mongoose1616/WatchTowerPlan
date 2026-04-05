# `core/control_plane/registries`

## Description
`This directory holds canonical lookup data owned by core. Use registries when stable identifiers need a governed machine-readable catalog. Registry artifacts now live as flat files at this root rather than inside per-family subdirectories.`

## Paths
| Path | Description |
|---|---|
| `core/control_plane/registries/README.md` | Describes the purpose of the registries directory and its main registry families. |
| `core/control_plane/registries/authority_map.json` | Canonical authored registry of supported planning, governance, and engineering questions, preferred commands, and fallback surfaces. |
| `core/control_plane/registries/governance_surface_map.json` | Governance surface map for non-artifact core surfaces. |
| `core/control_plane/registries/path_pattern_registry.json` | Path pattern registry for reusable core surfaces. |
| `core/control_plane/registries/status_registry.json` | Global status vocabulary for validation and enforcement. |
| `core/control_plane/registries/actor_registry.json` | Actor registry for audit and actor-ref validation. |
| `core/control_plane/registries/schema_catalog.json` | Maps schema identifiers, versions, and canonical paths. |
| `core/control_plane/registries/validator_registry.json` | Catalogs validator identities, capabilities, and selection metadata. |
| `core/control_plane/registries/validation_suite_registry.json` | Catalogs declared validation suites and their ordered validation steps. |
| `core/control_plane/registries/benchmark_suite_registry.json` | Catalogs governed reusable-core benchmark suites and their serialized command definitions. |
| `core/control_plane/registries/rendered_surface_registry.json` | Catalogs governed rendered Markdown surfaces for compact human trackers. |
| `core/control_plane/registries/workflow_metadata_registry.json` | Publishes authored workflow retrieval metadata consumed by workflow indexing and route preview. |
| `core/control_plane/registries/route_overlay_registry.json` | Publishes governed route-intent metadata for workflow modifiers and companion routes during route preview. |
| `core/control_plane/registries/route_merge_policy_registry.json` | Publishes governed route-suppression and normalization rules applied after route scoring and overlay attachment. |

## Notes
- The reusable-core startup set currently loads from `pack_settings.json` and centers on `schema_catalog.json`, `governance_surface_map.json`, `path_pattern_registry.json`, `status_registry.json`, `actor_registry.json`, `validator_registry.json`, `validation_suite_registry.json`, `benchmark_suite_registry.json`, `authority_map.json`, `rendered_surface_registry.json`, `workflow_metadata_registry.json`, `route_overlay_registry.json`, and `route_merge_policy_registry.json`.
- `route_overlay_registry.json` now carries explicit intent metadata such as `intent_kind`, `dominant_route_retention_mode`, `exclude_attached_task_types_from_base_scoring`, and `suppresses_intent_ids` so route preview does not have to infer companion-route behavior from ad hoc Python heuristics.
- The earlier structural-rewrite artifact type and artifact role registries were retired after consumer audit confirmed they no longer drove any live reusable-core or repo-local behavior.
