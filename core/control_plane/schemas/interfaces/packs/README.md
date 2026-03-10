# `core/control_plane/schemas/interfaces/packs`

## Description
`This directory holds generic pack-facing interface schemas for future domain packs. Use these schemas for pack-owned notes, manifests, extraction outputs, promoted knowledge, promotion records, and pack-local indexes without storing the pack-owned artifacts in core.`

## Files
| Path | Description |
|---|---|
| `core/control_plane/schemas/interfaces/packs/README.md` | Describes the purpose of the generic pack-facing interface schema directory. |
| `core/control_plane/schemas/interfaces/packs/pack_work_item_note.v1.schema.json` | Schema for one pack-owned work-item note. |
| `core/control_plane/schemas/interfaces/packs/workspace_artifact_manifest.v1.schema.json` | Schema for one metadata-only manifest of pack-local workspace artifacts. |
| `core/control_plane/schemas/interfaces/packs/extraction_output_envelope.v1.schema.json` | Schema for one structured extraction workflow output envelope. |
| `core/control_plane/schemas/interfaces/packs/promoted_knowledge.v1.schema.json` | Schema for one reviewed and promoted reusable knowledge item. |
| `core/control_plane/schemas/interfaces/packs/promotion_record.v1.schema.json` | Schema for one reviewable promotion decision that links extraction output to promoted knowledge. |
| `core/control_plane/schemas/interfaces/packs/pack_work_index.v1.schema.json` | Schema for one pack-local work index over work items and their primary note surfaces. |
| `core/control_plane/schemas/interfaces/packs/knowledge_index.v1.schema.json` | Schema for one pack-local knowledge index over promoted reusable knowledge items. |
