# `core/control_plane/registries`

## Description
`This directory holds canonical lookup data owned by core. Use registries when stable identifiers need a governed machine-readable catalog.`

## Paths
| Path | Description |
|---|---|
| `core/control_plane/registries/README.md` | Describes the purpose of the registries directory and its main registry families. |
| `core/control_plane/registries/governance_surface_map.json` | STEP1-style governance surface map for non-artifact core surfaces. |
| `core/control_plane/registries/path_pattern_registry.json` | STEP1-style path pattern registry for reusable core surfaces. |
| `core/control_plane/registries/status_registry.json` | STEP1-style global status vocabulary for validation and enforcement. |
| `core/control_plane/registries/actor_registry.json` | STEP1-style actor registry for audit and actor-ref validation. |
| `core/control_plane/registries/artifact_roles/` | Publishes bounded rewrite metadata for artifact-role classification without changing runtime authority. |
| `core/control_plane/registries/schema_catalog/` | Maps schema identifiers, versions, and canonical paths. |
| `core/control_plane/registries/artifact_types/` | Defines machine-recognized artifact kinds and their identifiers. |
| `core/control_plane/registries/authority_map/` | Defines canonical planning and governance lookup answers, preferred commands, and fallback surfaces. |
| `core/control_plane/registries/validators/` | Catalogs validator identities, capabilities, and selection metadata. |
| `core/control_plane/registries/workflows/` | Publishes authored workflow retrieval metadata consumed by workflow indexing and route preview. |
| `core/control_plane/registries/policy_catalog/` | Catalogs published policy sets by stable identifier. |
