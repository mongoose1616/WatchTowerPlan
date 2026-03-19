# `core/docs/standards/data_contracts`

## Description
`This directory holds standards for structured data used by the reusable core and the current planning-and-implementation pack. Use it for rules that define formats, schemas, registries, indexes, and retained record families for machine-readable or strongly structured content.`

## Families
### Planning and Traceability Index Family
| Path | Description |
|---|---|
| `plan/docs/standards/data_contracts/planning_index_family_standard.md` | Defines the shared baseline for the planning-related derived index standards and the family-level discoverability contract. |
| `plan/docs/standards/data_contracts/coordination_index_standard.md` | Defines the family-specific contract for the machine-readable coordination index. |
| `plan/docs/standards/data_contracts/initiative_index_standard.md` | Defines the family-specific contract for machine-readable initiative indexes. |
| `plan/docs/standards/data_contracts/task_index_standard.md` | Defines the family-specific contract for machine-readable task indexes. |
| `plan/docs/standards/data_contracts/traceability_index_standard.md` | Defines the family-specific contract for the unified machine-readable traceability index. |

### Other Data-Contract Standards
| Path | Description |
|---|---|
| `core/docs/standards/data_contracts/README.md` | Describes the purpose of the data contracts standards directory and the standards stored here. |
| `plan/docs/standards/data_contracts/acceptance_contract_standard.md` | Defines the standard for machine-readable acceptance contracts. |
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
| `plan/docs/standards/data_contracts/status_tracking_standard.md` | Defines how status values should be represented and maintained. |
| `plan/docs/standards/data_contracts/validation_evidence_standard.md` | Defines the standard for durable validation-evidence records. |
| `core/docs/standards/data_contracts/workflow_index_standard.md` | Defines the standard for machine-readable workflow indexes. |

## Notes
- Use `plan/docs/standards/data_contracts/planning_index_family_standard.md` first when the question is what the planning-related derived index standards share as one governed family.
- Use `cd core/python && ./.venv/bin/watchtower-core query standards --category data_contracts --tag planning_index_family --format json` when you want the shared family baseline plus the member standards in one machine-readable result set.
- Use the member standards when you need family-specific entry fields, invariants, validation checks, or change-control deltas that go beyond the shared baseline.
