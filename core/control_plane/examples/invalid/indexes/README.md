# `core/control_plane/examples/invalid/indexes`

## Description
`This directory holds canonical invalid examples of index artifacts that should fail validation against their published artifact schemas.`

## Files
| Path | Description |
|---|---|
| `core/control_plane/examples/invalid/indexes/README.md` | Describes the purpose of the invalid index examples directory. |
| `core/control_plane/examples/invalid/indexes/command_index_subcommand_missing_parent.v1.example.json` | Invalid command index example with a subcommand parent reference omitted. |
| `core/control_plane/examples/invalid/indexes/decision_index_missing_decision_status.v1.example.json` | Invalid decision index example missing a required decision outcome status. |
| `core/control_plane/examples/invalid/indexes/design_document_index_plan_missing_sources.v1.example.json` | Invalid design-document index example with an implementation plan entry missing required source paths. |
| `core/control_plane/examples/invalid/indexes/prd_index_missing_trace_id.v1.example.json` | Invalid PRD index example missing a required trace ID. |
| `core/control_plane/examples/invalid/indexes/repository_path_index_missing_summary.v1.example.json` | Invalid repository path index example with a required entry field omitted. |
| `core/control_plane/examples/invalid/indexes/traceability_index_missing_updated_at.v1.example.json` | Invalid traceability index example missing the required updated-at timestamp. |
