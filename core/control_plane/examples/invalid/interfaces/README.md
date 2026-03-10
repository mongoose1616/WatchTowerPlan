# `core/control_plane/examples/invalid/interfaces`

## Description
`This directory holds canonical invalid examples of generic pack-facing interface artifacts that should fail validation against the published interface schemas.`

## Files
| Path | Description |
|---|---|
| `core/control_plane/examples/invalid/interfaces/README.md` | Describes the purpose of the invalid generic interface examples directory. |
| `core/control_plane/examples/invalid/interfaces/pack_work_item_note_missing_work_item_id.v1.example.json` | Invalid work-item note example missing required work-item provenance. |
| `core/control_plane/examples/invalid/interfaces/workspace_artifact_manifest_missing_role.v1.example.json` | Invalid workspace artifact manifest example missing an artifact role. |
| `core/control_plane/examples/invalid/interfaces/extraction_output_envelope_missing_trace_id.v1.example.json` | Invalid extraction output example missing the required trace identifier. |
| `core/control_plane/examples/invalid/interfaces/promoted_knowledge_missing_promotion_record_id.v1.example.json` | Invalid promoted knowledge example missing the promotion record link. |
| `core/control_plane/examples/invalid/interfaces/promotion_record_approved_missing_promoted_ids.v1.example.json` | Invalid promotion record example that approves promotion without naming promoted knowledge. |
| `core/control_plane/examples/invalid/interfaces/pack_work_index_missing_note_path.v1.example.json` | Invalid pack work index example missing the primary note path for an indexed work item. |
| `core/control_plane/examples/invalid/interfaces/knowledge_index_missing_promotion_record_id.v1.example.json` | Invalid knowledge index example missing the promotion record link for an indexed knowledge item. |
