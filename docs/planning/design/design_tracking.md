# Design Tracking

## Summary
This document provides the human-readable tracking view for the current design documents under `docs/planning/design/`. Use it to see which feature designs exist, which implementation plans are active, and how those documents relate to one another.

## Feature Designs
| Trace ID | Initiative Status | Path | Summary | Linked Plans | Notes |
|---|---|---|---|---|---|
| `trace.acceptance_evidence_reconciliation` | `completed` | `docs/planning/design/features/acceptance_evidence_reconciliation.md` | Defines the feature-level design for the acceptance and evidence reconciliation flow that keeps acceptance contracts, validator expectations, validation evidence, and traceability joins aligned. | `None` | None |
| `trace.command_documentation_and_lookup` | `completed` | `docs/planning/design/features/command_documentation_and_lookup.md` | Defines the feature-level design for a human-readable command-page family under docs/commands and a machine-readable command index under core/control_plane/indexes/commands. | `None` | None |
| `trace.core_export_readiness_and_optimization` | `active` | `docs/planning/design/features/core_export_ready_architecture.md` | Defines the in-repo architecture needed to separate reusable core behavior from WatchTowerPlan repo-operations, reduce maintenance fan-out, and publish generic pack-facing contracts. | `docs/planning/design/implementation/core_export_readiness_execution.md` | None |
| `trace.core_python_foundation` | `completed` | `docs/planning/design/features/core_python_workspace_and_harness.md` | Defines the feature-level technical design for the consolidated Python workspace under core/python and the first functional boundaries of the core helper and harness package. | `docs/planning/design/implementation/control_plane_loaders_and_schema_store.md` | None |
| `trace.github_collaboration` | `completed` | `docs/planning/design/features/github_collaboration_scaffolding.md` | Defines the hosted GitHub intake, pull request, and project-field scaffolding that complements the repo-local planning and task model. | `None` | None |
| `trace.local_task_tracking` | `completed` | `docs/planning/design/features/github_task_push_sync.md` | Defines the first push-only sync from local task records to GitHub issues and optional project items while preserving local task authority. | `None` | None |
| `trace.initiative_closeout` | `completed` | `docs/planning/design/features/initiative_closeout_and_planning_trackers.md` | Defines the first initiative closeout model, its traceability fields, and the generated planning trackers that mirror initiative outcome for humans. | `None` | None |
| `trace.local_task_tracking` | `completed` | `docs/planning/design/features/local_task_tracking_and_github_sync.md` | Defines the feature-level design for local-first task records, a generated task tracker, a generated task index, and later GitHub sync support. | `None` | None |
| `trace.core_python_foundation` | `completed` | `docs/planning/design/features/python_validator_execution.md` | Defines the feature-level technical design for a Python validation layer that reads the authored validator registry from core/control_plane and executes validators deterministically against governed artifacts. | `docs/planning/design/implementation/control_plane_loaders_and_schema_store.md` | None |
| `trace.core_python_foundation` | `completed` | `docs/planning/design/features/schema_resolution_and_index_search.md` | Defines the feature-level technical design for deterministic local schema resolution and index-backed repository search in the Python helper layer. | `docs/planning/design/implementation/control_plane_loaders_and_schema_store.md` | None |

## Implementation Plans
| Trace ID | Initiative Status | Path | Summary | Source Designs | Notes |
|---|---|---|---|---|---|
| `trace.core_python_foundation` | `completed` | `docs/planning/design/implementation/control_plane_loaders_and_schema_store.md` | Breaks the first executable core/python slice into concrete work for loading governed control-plane artifacts and resolving schemas locally through a reusable SchemaStore. | `docs/planning/design/features/core_python_workspace_and_harness.md; docs/planning/design/features/python_validator_execution.md; docs/planning/design/features/schema_resolution_and_index_search.md` | First executable slice for the core Python helper and harness layer. |
| `trace.core_export_readiness_and_optimization` | `active` | `docs/planning/design/implementation/core_export_readiness_execution.md` | Breaks the export-readiness architecture into concrete in-repo phases that isolate repo-ops, reduce maintenance fan-out, and publish generic pack-facing contracts without extracting the package yet. | `docs/planning/design/features/core_export_ready_architecture.md` | None |

## Update Rules
- Rebuild this tracker in the same change set when a design document or implementation plan is added, renamed, removed, materially retargeted, or when a trace initiative changes closeout state.
- Keep the machine-readable companion index at [design_document_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/design_documents/design_document_index.v1.json) aligned with this tracker.
- Treat the unified traceability index at [traceability_index.v1.json](/home/j/WatchTowerPlan/core/control_plane/indexes/traceability/traceability_index.v1.json) as the source for initiative closeout status.

## References
- [README.md](/home/j/WatchTowerPlan/docs/planning/design/README.md)
- [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md)
- [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md)
- [design_document_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/design_document_index_standard.md)

## Updated At
- `2026-03-10T05:14:33Z`
