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
| `core/control_plane/examples/invalid/indexes/foundation_index_external_without_urls.v1.example.json` | Invalid foundation index example with external-reference usage declared but no external URLs published. |
| `core/control_plane/examples/invalid/indexes/prd_index_missing_trace_id.v1.example.json` | Invalid PRD index example missing a required trace ID. |
| `core/control_plane/examples/invalid/indexes/reference_index_missing_upstream.v1.example.json` | Invalid reference index example missing required canonical upstream URLs. |
| `core/control_plane/examples/invalid/indexes/repository_path_index_missing_summary.v1.example.json` | Invalid repository path index example with a required entry field omitted. |
| `core/control_plane/examples/invalid/indexes/standard_index_external_without_urls.v1.example.json` | Invalid standard index example with external-reference usage declared but no external URLs published. |
| `core/control_plane/examples/invalid/indexes/task_index_open_task_with_done_status.v1.example.json` | Invalid task index example with an open task document path and a terminal task status. |
| `core/control_plane/examples/invalid/indexes/traceability_index_missing_updated_at.v1.example.json` | Invalid traceability index example missing the required updated-at timestamp. |
| `core/control_plane/examples/invalid/indexes/workflow_index_missing_summary.v1.example.json` | Invalid workflow index example missing a required entry summary. |
