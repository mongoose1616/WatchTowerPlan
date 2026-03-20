# `core/control_plane/indexes`

## Description
`This directory holds deliberate denormalized lookup files when a concrete consumer benefits from them. Live planning indexes now live under plan/.wt/indexes/; keep the remaining core indexes derived and reviewable, and do not let them become a parallel source of truth.`

## Paths
| Path | Description |
|---|---|
| `core/control_plane/indexes/README.md` | Describes the purpose of the indexes directory and its main index families. |
| `core/control_plane/indexes/commands/` | Machine-readable command indexes for command lookup and routing to command pages. |
| `core/control_plane/indexes/foundations/` | Machine-readable indexes for governed foundation documents and their downstream citation or application use. |
| `core/control_plane/indexes/references/` | Machine-readable indexes for reference docs, their upstream authority, and local touchpoints. |
| `core/control_plane/indexes/repository_paths/` | Generated repository path indexes for retrieval and navigation. |
| `core/control_plane/indexes/routes/` | Machine-readable indexes for routed task types and their required workflow modules. |
| `core/control_plane/indexes/standards/` | Machine-readable indexes for governed standards and best-practice documents. |
| `core/control_plane/indexes/workflows/` | Machine-readable indexes for workflow modules and their governing sources. |
| `core/control_plane/indexes/traceability/` | Unified traceability indexes that join planning, contract, validator, and evidence surfaces. |
| `plan/.wt/indexes/` | Canonical live plan-workspace indexes for coordination, initiatives, tasks, readiness, discrepancies, evidence, and other execution-state projections. |
