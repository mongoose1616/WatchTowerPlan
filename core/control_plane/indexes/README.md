# `core/control_plane/indexes`

## Description
`This directory holds deliberate denormalized lookup files when a concrete consumer benefits from them. Keep indexes derived and reviewable, and do not let them become a parallel source of truth.`

## Paths
| Path | Description |
|---|---|
| `core/control_plane/indexes/README.md` | Describes the purpose of the indexes directory and its main index families. |
| `core/control_plane/indexes/commands/` | Machine-readable command indexes for command lookup and routing to command pages. |
| `core/control_plane/indexes/coordination/` | Machine-readable coordination indexes for one current-state start-here view above the family-specific planning indexes. |
| `core/control_plane/indexes/decisions/` | Machine-readable indexes for durable decision records and their trace links. |
| `core/control_plane/indexes/design_documents/` | Machine-readable indexes for tracking feature designs and implementation plans. |
| `core/control_plane/indexes/foundations/` | Machine-readable indexes for governed foundation documents and their downstream citation or application use. |
| `core/control_plane/indexes/initiatives/` | Machine-readable initiative indexes that project current phase, ownership, and next-step status across traced planning surfaces. |
| `core/control_plane/indexes/planning/` | Canonical machine-readable planning catalogs that join trace-linked planning, task, acceptance, evidence, and per-trace coordination state. |
| `core/control_plane/indexes/prds/` | Machine-readable indexes for PRDs and their traceability anchors. |
| `core/control_plane/indexes/references/` | Machine-readable indexes for reference docs, their upstream authority, and local touchpoints. |
| `core/control_plane/indexes/repository_paths/` | Generated repository path indexes for retrieval and navigation. |
| `core/control_plane/indexes/routes/` | Machine-readable indexes for routed task types and their required workflow modules. |
| `core/control_plane/indexes/standards/` | Machine-readable indexes for governed standards and best-practice documents. |
| `core/control_plane/indexes/tasks/` | Machine-readable indexes for local task records and task lookup. |
| `core/control_plane/indexes/workflows/` | Machine-readable indexes for workflow modules and their governing sources. |
| `core/control_plane/indexes/schemas/` | Lookup indexes over published schemas. |
| `core/control_plane/indexes/registries/` | Lookup indexes over governed registries. |
| `core/control_plane/indexes/traceability/` | Unified traceability indexes that join planning, contract, validator, and evidence surfaces. |
