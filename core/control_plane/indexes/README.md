# `core/control_plane/indexes`

## Description
`This directory holds deliberate denormalized lookup files when a concrete consumer benefits from them. Keep indexes derived and reviewable, and do not let them become a parallel source of truth.`

## Paths
| Path | Description |
|---|---|
| `core/control_plane/indexes/README.md` | Describes the purpose of the indexes directory and its main index families. |
| `core/control_plane/indexes/commands/` | Machine-readable command indexes for command lookup and routing to command pages. |
| `core/control_plane/indexes/design_documents/` | Machine-readable indexes for tracking feature designs and implementation plans. |
| `core/control_plane/indexes/repository_paths/` | Generated repository path indexes for retrieval and navigation. |
| `core/control_plane/indexes/schemas/` | Lookup indexes over published schemas. |
| `core/control_plane/indexes/registries/` | Lookup indexes over governed registries. |
