# `core/docs/standards/data_contracts`

## Description
`This directory holds the shared reusable-core standards for structured data. Use it for rules that define formats, schemas, registries, indexes, and retained record families for machine-readable or strongly structured content, and use the owning pack docs root for pack-local planning or evidence families.`

## Families
### Shared Core-Owned Standards In This Directory
| Path | Description |
|---|---|
| `core/docs/standards/data_contracts/README.md` | Describes the purpose of the data contracts standards directory and the standards stored here. |
| `core/docs/standards/data_contracts/authority_map_standard.md` | Defines the standard for the authored authority-map registry. |
| `core/docs/standards/data_contracts/command_index_standard.md` | Defines the standard for machine-readable command indexes. |
| `core/docs/standards/data_contracts/foundation_index_standard.md` | Defines the standard for machine-readable foundation indexes. |
| `core/docs/standards/data_contracts/format_selection_standard.md` | Defines how to choose the right data format for a planning-repo artifact. |
| `core/docs/standards/data_contracts/reference_index_standard.md` | Defines the standard for machine-readable reference indexes. |
| `core/docs/standards/data_contracts/repository_path_index_standard.md` | Defines the standard for generated repository path indexes. |
| `core/docs/standards/data_contracts/route_index_standard.md` | Defines the standard for machine-readable route indexes. |
| `core/docs/standards/data_contracts/schema_catalog_standard.md` | Defines the standard for the authored schema catalog registry. |
| `core/docs/standards/data_contracts/schema_standard.md` | Defines schema expectations for governed structured data. |
| `core/docs/standards/data_contracts/standard_index_standard.md` | Defines the standard for machine-readable standard indexes. |
| `core/docs/standards/data_contracts/workflow_index_standard.md` | Defines the standard for machine-readable workflow indexes. |

### Related Pack-Owned Data-Contract Standards
| Path Pattern | Description |
|---|---|
| `<pack>/docs/standards/data_contracts/planning_index_family_standard.md` | Defines the shared baseline for the pack's planning-related derived index standards and the family-level discoverability contract. |
| `<pack>/docs/standards/data_contracts/coordination_index_standard.md` | Defines the family-specific contract for the pack's machine-readable coordination index. |
| `<pack>/docs/standards/data_contracts/initiative_index_standard.md` | Defines the family-specific contract for pack-owned machine-readable initiative indexes. |
| `<pack>/docs/standards/data_contracts/task_index_standard.md` | Defines the family-specific contract for pack-owned machine-readable task indexes. |
| `<pack>/docs/standards/data_contracts/traceability_index_standard.md` | Defines the family-specific contract for the pack's unified machine-readable traceability index. |
| `<pack>/docs/standards/data_contracts/acceptance_contract_standard.md` | Defines pack-owned machine-readable acceptance-contract expectations. |
| `<pack>/docs/standards/data_contracts/status_tracking_standard.md` | Defines the hosted pack's lifecycle status vocabulary and status-representation rules. |
| `<pack>/docs/standards/data_contracts/validation_evidence_standard.md` | Defines the hosted pack's durable validation-evidence record contract. |

## Notes
- Use `<pack>/docs/standards/data_contracts/planning_index_family_standard.md` first when the question is what a hosted pack's planning-related derived index standards share as one governed family.
- Use `cd core/python && ./.venv/bin/watchtower-core query standards --category data_contracts --tag planning_index_family --format json` when you want the shared family baseline plus the member standards in one machine-readable result set.
- Use the member standards when you need family-specific entry fields, invariants, validation checks, or change-control deltas that go beyond the shared baseline.
