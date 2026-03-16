# `core/control_plane/registries`

## Description
`This directory holds canonical lookup data owned by core. Use registries when stable identifiers need a governed machine-readable catalog. Registry artifacts now live as flat files at this root rather than inside per-family subdirectories.`

## Paths
| Path | Description |
|---|---|
| `core/control_plane/registries/README.md` | Describes the purpose of the registries directory and its main registry families. |
| `core/control_plane/registries/artifact_role_registry.json` | Artifact-role registry for the bounded structural rewrite classification slice. |
| `core/control_plane/registries/artifact_type_registry.json` | Registry of active governed artifact kinds, their families, schemas, and canonical paths. |
| `core/control_plane/registries/authority_map.json` | Canonical authored registry of supported planning and governance questions, preferred commands, and fallback surfaces. |
| `core/control_plane/registries/governance_surface_map.json` | Governance surface map for non-artifact core surfaces. |
| `core/control_plane/registries/path_pattern_registry.json` | Path pattern registry for reusable core surfaces. |
| `core/control_plane/registries/status_registry.json` | Global status vocabulary for validation and enforcement. |
| `core/control_plane/registries/actor_registry.json` | Actor registry for audit and actor-ref validation. |
| `core/control_plane/registries/schema_catalog.json` | Maps schema identifiers, versions, and canonical paths. |
| `core/control_plane/registries/validator_registry.json` | Catalogs validator identities, capabilities, and selection metadata. |
| `core/control_plane/registries/workflow_metadata_registry.json` | Publishes authored workflow retrieval metadata consumed by workflow indexing and route preview. |
