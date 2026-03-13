# `docs/standards/data_contracts`

## Description
`This directory holds standards for structured data used by the planning repository. Use it for rules that define formats, schemas, registries, and status-tracking expectations for machine-readable or strongly structured content.`

## Families
### Planning and Traceability Index Family
| Path | Description |
|---|---|
| `docs/standards/data_contracts/planning_index_family_standard.md` | Defines the shared baseline for the planning-related derived index standards and the family-level discoverability contract. |
| `docs/standards/data_contracts/coordination_index_standard.md` | Defines the family-specific contract for the machine-readable coordination index. |
| `docs/standards/data_contracts/initiative_index_standard.md` | Defines the family-specific contract for machine-readable initiative indexes. |
| `docs/standards/data_contracts/planning_catalog_standard.md` | Defines the family-specific contract for the canonical machine-readable planning catalog. |
| `docs/standards/data_contracts/prd_index_standard.md` | Defines the family-specific contract for machine-readable PRD indexes. |
| `docs/standards/data_contracts/decision_index_standard.md` | Defines the family-specific contract for machine-readable decision indexes. |
| `docs/standards/data_contracts/design_document_index_standard.md` | Defines the family-specific contract for machine-readable design-document indexes. |
| `docs/standards/data_contracts/task_index_standard.md` | Defines the family-specific contract for machine-readable task indexes. |
| `docs/standards/data_contracts/traceability_index_standard.md` | Defines the family-specific contract for the unified machine-readable traceability index. |

### Other Data-Contract Standards
| Path | Description |
|---|---|
| `docs/standards/data_contracts/README.md` | Describes the purpose of the data contracts standards directory and the standards stored here. |
| `docs/standards/data_contracts/acceptance_contract_standard.md` | Defines the standard for machine-readable acceptance contracts. |
| `docs/standards/data_contracts/authority_map_standard.md` | Defines the standard for the authored authority-map registry. |
| `docs/standards/data_contracts/command_index_standard.md` | Defines the standard for machine-readable command indexes. |
| `docs/standards/data_contracts/foundation_index_standard.md` | Defines the standard for machine-readable foundation indexes. |
| `docs/standards/data_contracts/format_selection_standard.md` | Defines how to choose the right data format for a planning-repo artifact. |
| `docs/standards/data_contracts/reference_index_standard.md` | Defines the standard for machine-readable reference indexes. |
| `docs/standards/data_contracts/repository_path_index_standard.md` | Defines the standard for generated repository path indexes. |
| `docs/standards/data_contracts/route_index_standard.md` | Defines the standard for machine-readable route indexes. |
| `docs/standards/data_contracts/schema_catalog_standard.md` | Defines the standard for the authored schema catalog registry. |
| `docs/standards/data_contracts/schema_standard.md` | Defines schema expectations for governed structured data. |
| `docs/standards/data_contracts/standard_index_standard.md` | Defines the standard for machine-readable standard indexes. |
| `docs/standards/data_contracts/status_tracking_standard.md` | Defines how status values should be represented and maintained. |
| `docs/standards/data_contracts/validation_evidence_standard.md` | Defines the standard for durable validation-evidence ledger artifacts. |
| `docs/standards/data_contracts/workflow_index_standard.md` | Defines the standard for machine-readable workflow indexes. |

## Notes
- Use `docs/standards/data_contracts/planning_index_family_standard.md` first when the question is what the planning-related derived index standards share as one governed family.
- Use `cd core/python && ./.venv/bin/watchtower-core query standards --category data_contracts --tag planning_index_family --format json` when you want the shared family baseline plus the member standards in one machine-readable result set.
- Use the member standards when you need family-specific entry fields, invariants, validation checks, or change-control deltas that go beyond the shared baseline.
