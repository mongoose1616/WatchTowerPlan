# `core/control_plane/indexes/workflows`

## Description
`This directory holds the machine-readable workflow index used to look up workflow modules and any task-specific extra files they require beyond the routing baseline, using companion authored metadata from `core/control_plane/registries/`.`

## Files
| Path | Description |
|---|---|
| `core/control_plane/indexes/workflows/README.md` | Describes the purpose of the workflow-index directory and its current artifact. |
| `core/control_plane/indexes/workflows/workflow_index.json` | Canonical machine-readable workflow index rebuilt from shared and pack-owned workflow module roots. |
