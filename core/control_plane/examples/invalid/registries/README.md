# `core/control_plane/examples/invalid/registries`

## Description
`This directory holds canonical invalid examples of registry artifacts that should fail validation against their published artifact schemas.`

## Files
| Path | Description |
|---|---|
| `core/control_plane/examples/invalid/registries/README.md` | Describes the purpose of the invalid registry examples directory. |
| `core/control_plane/examples/invalid/registries/artifact_role_registry_missing_retention_reasons.v1.example.json` | Invalid artifact-role registry example with required retention reasons omitted for a compatibility surface. |
| `core/control_plane/examples/invalid/registries/schema_catalog_missing_canonical_path.v1.example.json` | Invalid schema catalog example with a required canonical path omitted. |
| `core/control_plane/examples/invalid/registries/validator_registry_missing_schema_ids.v1.example.json` | Invalid validator registry example with required schema references omitted. |
| `core/control_plane/examples/invalid/registries/workflow_metadata_registry_missing_phase_type.v1.example.json` | Invalid workflow metadata registry example missing the required phase type. |
