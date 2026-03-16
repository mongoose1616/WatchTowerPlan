# `core/control_plane/schemas/artifacts`

## Description
`This directory holds schemas for artifacts authored and owned by the control plane itself, such as registries, indexes, contracts, and retained record families. Pack-facing startup interfaces live under core/control_plane/schemas/interfaces/packs/.`

## Paths
| Path | Description |
|---|---|
| `core/control_plane/schemas/artifacts/README.md` | Describes the purpose of the artifact schema directory and its current contents. |
| `core/control_plane/schemas/artifacts/acceptance_contract.schema.json` | Schema for the machine-readable acceptance-contract artifact family. |
| `core/control_plane/schemas/artifacts/authority_map.schema.json` | Schema for the authored authority-map registry artifact family. |
| `core/control_plane/schemas/artifacts/command_index.schema.json` | Schema for the machine-readable command-index artifact family. |
| `core/control_plane/schemas/artifacts/coordination_index.schema.json` | Schema for the machine-readable coordination-index artifact family. |
| `core/control_plane/schemas/artifacts/decision_index.schema.json` | Schema for the machine-readable decision-index artifact family. |
| `core/control_plane/schemas/artifacts/design_document_index.schema.json` | Schema for the machine-readable design-document index artifact family. |
| `core/control_plane/schemas/artifacts/foundation_index.schema.json` | Schema for the machine-readable foundation-index artifact family. |
| `core/control_plane/schemas/artifacts/initiative_index.schema.json` | Schema for the machine-readable initiative-index artifact family. |
| `core/control_plane/schemas/artifacts/migration_record.schema.json` | Schema for the machine-readable migration-record artifact family. |
| `core/control_plane/schemas/artifacts/planning_catalog.schema.json` | Schema for the canonical machine-readable planning-catalog artifact family. |
| `core/control_plane/schemas/artifacts/prd_index.schema.json` | Schema for the machine-readable PRD-index artifact family. |
| `core/control_plane/schemas/artifacts/reference_index.schema.json` | Schema for the machine-readable reference-index artifact family. |
| `core/control_plane/schemas/artifacts/release_record.schema.json` | Schema for the machine-readable release-record artifact family. |
| `core/control_plane/schemas/artifacts/rendered_surface_registry.schema.json` | Schema for the authored rendered-surface registry artifact family. |
| `core/control_plane/schemas/artifacts/repository_path_index.schema.json` | Schema for the generated repository path index artifact family. |
| `core/control_plane/schemas/artifacts/route_index.schema.json` | Schema for the machine-readable route-index artifact family. |
| `core/control_plane/schemas/artifacts/schema_catalog.schema.json` | Schema for the authored schema catalog registry artifact family. |
| `core/control_plane/schemas/artifacts/standard_index.schema.json` | Schema for the machine-readable standard-index artifact family. |
| `core/control_plane/schemas/artifacts/task_index.schema.json` | Schema for the machine-readable task-index artifact family. |
| `core/control_plane/schemas/artifacts/trace_purge_record.schema.json` | Schema for the machine-readable trace-purge ledger artifact family. |
| `core/control_plane/schemas/artifacts/traceability_index.schema.json` | Schema for the unified machine-readable traceability-index artifact family. |
| `core/control_plane/schemas/artifacts/validation_evidence.schema.json` | Schema for the durable validation-evidence artifact family. |
| `core/control_plane/schemas/artifacts/validator_registry.schema.json` | Schema for the authored validator registry artifact family. |
| `core/control_plane/schemas/artifacts/workflow_metadata_registry.schema.json` | Schema for the authored workflow-metadata registry artifact family. |
| `core/control_plane/schemas/artifacts/workflow_index.schema.json` | Schema for the machine-readable workflow-index artifact family. |

## Notes
- `core/control_plane/schemas/interfaces/packs/` holds the pack-facing startup contracts such as `pack_settings`, `governance_surface_map`, `path_pattern_registry`, `status_registry`, `actor_registry`, and `artifact_index`.
- This directory carries the active control-plane artifact schemas plus the current migration and evidence record schemas consumed by the internal planning-and-implementation pack.
