# `core/control_plane/ledgers`

## Description
`This directory holds committed append-only history for governed changes. Use it for reviewable migration and release history, not for mutable runtime logs or transient event streams.`

## Paths
| Path | Description |
|---|---|
| `core/control_plane/ledgers/README.md` | Describes the purpose of the ledgers directory and its main ledger families. |
| `core/control_plane/ledgers/migrations/` | Append-only history of schema and contract migrations. |
| `core/control_plane/ledgers/releases/` | Append-only history of releases and their evidence pointers. |
| `core/control_plane/ledgers/validation_evidence/` | Committed validation evidence linked to traced initiatives, validators, and acceptance items. |
