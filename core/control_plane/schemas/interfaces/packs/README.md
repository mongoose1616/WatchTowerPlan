# `core/control_plane/schemas/interfaces/packs`

## Description
`This directory holds generic pack-facing interface schemas for future domain packs. Use these schemas for STEP1-style pack settings, governance surfaces, indexes, notes, and extraction outputs without storing pack-owned artifacts in core.`

## Files
| Path | Description |
|---|---|
| `core/control_plane/schemas/interfaces/packs/README.md` | Describes the purpose of the generic pack-facing interface schema directory. |
| `core/control_plane/schemas/interfaces/packs/pack_settings.schema.json` | Schema for one pack settings load root. |
| `core/control_plane/schemas/interfaces/packs/governance_surface_map.schema.json` | Schema for one governance surface map over non-artifact governed surfaces. |
| `core/control_plane/schemas/interfaces/packs/path_pattern_registry.schema.json` | Schema for one path pattern registry. |
| `core/control_plane/schemas/interfaces/packs/status_registry.schema.json` | Schema for one global status registry. |
| `core/control_plane/schemas/interfaces/packs/actor_registry.schema.json` | Schema for one actor registry. |
| `core/control_plane/schemas/interfaces/packs/artifact_index.schema.json` | Schema for one STEP1-style artifact index. |
| `core/control_plane/schemas/interfaces/packs/pack_work_item_note.v1.schema.json` | Schema for one pack-owned work-item note. |
| `core/control_plane/schemas/interfaces/packs/workspace_artifact_manifest.v1.schema.json` | Schema for one metadata-only manifest of pack-local workspace artifacts. |
| `core/control_plane/schemas/interfaces/packs/extraction_output_envelope.v1.schema.json` | Schema for one structured extraction workflow output envelope. |
| `core/control_plane/schemas/interfaces/packs/promoted_knowledge.v1.schema.json` | Schema for one reviewed and promoted reusable knowledge item. |
| `core/control_plane/schemas/interfaces/packs/promotion_record.v1.schema.json` | Schema for one reviewable promotion decision that links extraction output to promoted knowledge. |
| `core/control_plane/schemas/interfaces/packs/pack_work_index.v1.schema.json` | Schema for one pack-local work index over work items and their primary note surfaces. |
| `core/control_plane/schemas/interfaces/packs/knowledge_index.v1.schema.json` | Schema for one pack-local knowledge index over promoted reusable knowledge items. |
