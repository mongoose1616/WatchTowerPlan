# `core/control_plane/records`

## Description
`This directory holds committed append-only history for governed changes. Use it for reviewable migration and release history, not for mutable runtime logs or transient event streams. These records are internal retained history by default, not automatic customer-bootstrap content.`

## Paths
| Path | Description |
|---|---|
| `core/control_plane/records/README.md` | Describes the purpose of the records directory and its main record families. |
| `core/control_plane/records/migrations/` | Append-only history of schema and contract migrations. |
| `core/control_plane/records/releases/` | Append-only history of releases and their evidence pointers. |
| `core/control_plane/records/validation_evidence/` | Committed validation evidence linked to traced initiatives, validators, and acceptance items. |

## Notes
- Treat this directory as donor-repository history unless a recipient explicitly needs governance lineage.
- Portable customer releases should exclude these record families by default rather than inheriting them through a raw repository snapshot.
