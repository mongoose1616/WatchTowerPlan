# PRD Tracking

## Summary
This document provides the human-readable tracking view for PRDs under `docs/planning/prds/`.

## Current PRDs
| Trace ID | PRD ID | Initiative Status | Path | Summary | Linked Designs and Plans |
|---|---|---|---|---|---|
| `trace.core_export_hardening_followup` | `prd.core_export_hardening_followup` | `active` | `docs/planning/prds/core_export_hardening_followup.md` | Defines the follow-up work needed to make export-oriented sync snapshots dependency-correct, repair command implementation metadata, and harden the public boundary around repo-specific services. | `design.features.core_export_hardening; design.implementation.core_export_hardening_execution` |
| `trace.core_export_readiness_and_optimization` | `prd.core_export_readiness_and_optimization` | `completed` | `docs/planning/prds/core_export_readiness_and_optimization.md` | Defines the product and engineering requirements for making WatchTowerPlan core export-ready, lower-fan-out to maintain, and prepared to publish generic pack-facing contracts for future WatchTower work. | `design.features.core_export_ready_architecture; design.implementation.core_export_readiness_execution` |
| `trace.core_python_foundation` | `prd.core_python_foundation` | `completed` | `docs/planning/prds/core_python_foundation.md` | Defines the planning intent for the core Python workspace, control-plane loaders, validation, and query foundations. | `design.features.core_python_workspace_and_harness; design.features.python_validator_execution; design.features.schema_resolution_and_index_search; design.implementation.control_plane_loaders_and_schema_store` |

## Update Rules
- Rebuild this tracker in the same change set when a PRD is added, renamed, removed, materially retargeted, or when a trace initiative changes closeout state.
- Keep the machine-readable companion index at [prd_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/prds/prd_index.v1.json) aligned with this tracker.
- Treat the unified traceability index at [traceability_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/traceability/traceability_index.v1.json) as the source for initiative closeout status.

## References
- [README.md](/home/j/WatchTowerPlan/docs/planning/prds/README.md)
- [prd_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/prd_md_standard.md)
- [prd_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/prd_index_standard.md)

## Updated At
- `2026-03-10T15:24:07Z`
