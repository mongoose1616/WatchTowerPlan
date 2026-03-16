# `core/control_plane/registries`

## Description
`This directory holds canonical lookup data owned by core. Use registries when stable identifiers need a governed machine-readable catalog. Registry artifacts now live as flat files at this root rather than inside per-family subdirectories.`

## Paths
| Path | Description |
|---|---|
| `core/control_plane/registries/README.md` | Describes the purpose of the registries directory and its main registry families. |
| `core/control_plane/registries/artifact_role_registry.json` | Retained repo-local artifact-role catalog from the structural rewrite classification slice. |
| `core/control_plane/registries/artifact_type_registry.json` | Retained repo-local catalog of governed artifact kinds, schemas, and canonical paths. |
| `core/control_plane/registries/authority_map.json` | Canonical authored registry of supported planning and governance questions, preferred commands, and fallback surfaces. |
| `core/control_plane/registries/governance_surface_map.json` | Governance surface map for non-artifact core surfaces. |
| `core/control_plane/registries/path_pattern_registry.json` | Path pattern registry for reusable core surfaces. |
| `core/control_plane/registries/status_registry.json` | Global status vocabulary for validation and enforcement. |
| `core/control_plane/registries/actor_registry.json` | Actor registry for audit and actor-ref validation. |
| `core/control_plane/registries/schema_catalog.json` | Maps schema identifiers, versions, and canonical paths. |
| `core/control_plane/registries/validator_registry.json` | Catalogs validator identities, capabilities, and selection metadata. |
| `core/control_plane/registries/workflow_metadata_registry.json` | Publishes authored workflow retrieval metadata consumed by workflow indexing and route preview. |

## Notes
- The reusable-core startup set currently loads from `pack_settings.json` and centers on `schema_catalog.json`, `governance_surface_map.json`, `path_pattern_registry.json`, `status_registry.json`, `actor_registry.json`, `validator_registry.json`, `authority_map.json`, and `workflow_metadata_registry.json`.
- `artifact_type_registry.json` and `artifact_role_registry.json` remain retained repo-local registries while the broader pack-facing contract cutover continues.
