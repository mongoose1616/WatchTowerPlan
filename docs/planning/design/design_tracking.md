# Design Tracking

## Summary
This document provides the human-readable tracking view for the current design documents under `docs/planning/design/`. Use it to see which feature designs exist, which implementation plans are active, and how those documents relate to one another.

## Feature Designs
| Trace ID | Path | Summary | Linked Plans | Notes |
|---|---|---|---|---|
| `trace.command_documentation_and_lookup` | `docs/planning/design/features/command_documentation_and_lookup.md` | Defines the feature design for human-readable command pages and the machine-readable command index. | None yet. | Governs the command-doc and command-index family shape. |
| `trace.core_python_foundation` | `docs/planning/design/features/core_python_workspace_and_harness.md` | Defines the feature design for the consolidated `core/python/` workspace and the first harness package boundaries. | `docs/planning/design/implementation/control_plane_loaders_and_schema_store.md` | Provides the workspace and package boundary assumptions used by the first implementation slice. |
| `trace.core_python_foundation` | `docs/planning/design/features/python_validator_execution.md` | Defines the feature design for registry-driven validator execution in Python. | `docs/planning/design/implementation/control_plane_loaders_and_schema_store.md` | The current implementation plan depends on its control-plane loading assumptions. |
| `trace.core_python_foundation` | `docs/planning/design/features/schema_resolution_and_index_search.md` | Defines the feature design for schema catalog resolution and index-backed repository search. | `docs/planning/design/implementation/control_plane_loaders_and_schema_store.md` | The current implementation plan is the first execution slice for this design. |

## Implementation Plans
| Trace ID | Path | Summary | Source Designs | Notes |
|---|---|---|---|---|
| `trace.core_python_foundation` | `docs/planning/design/implementation/control_plane_loaders_and_schema_store.md` | Breaks the first `core/python` execution slice into concrete work for control-plane loaders and `SchemaStore`. | `core_python_workspace_and_harness.md`; `python_validator_execution.md`; `schema_resolution_and_index_search.md` | First executable slice for the Python helper and harness layer. |

## Update Rules
- Update this tracker in the same change set when a design document or implementation plan is added, renamed, removed, or materially retargeted.
- Keep the machine-readable companion index at [design_document_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/design_documents/design_document_index.v1.json) aligned with this tracker.
- When a new implementation plan is created for an existing feature design, update both the `Linked Plans` column here and the corresponding `related_paths` in the machine-readable index.

## References
- [README.md](/home/j/WatchTowerPlan/docs/planning/design/README.md)
- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md)
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md)
- [design_document_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/design_document_index_standard.md)
- [design_document_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/design_documents/design_document_index.v1.json)

## Updated At
- `2026-03-09T04:55:49Z`
