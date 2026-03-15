# `docs/planning/design/features`

## Description
`This directory holds feature-level technical designs that are specific enough for implementation planning but remain above task breakdown and direct code changes. Use it to capture recommended architecture, tradeoffs, affected surfaces, and the guardrails that later implementation plans should preserve.`

## Files
| Path | Description |
|---|---|
| `docs/planning/design/features/README.md` | Describes the purpose of the feature-design directory, its current documents, and the standards that govern them. |
| `docs/planning/design/features/acceptance_evidence_reconciliation.md` | Feature design for a future reusable acceptance and validation-evidence reconciliation phase. |
| `docs/planning/design/features/command_documentation_and_lookup.md` | Feature design for human-readable command pages and machine-readable command lookup. |
| `docs/planning/design/features/compact_document_authoring_and_tracking.md` | Feature design for compact default templates, compact planning trackers, and proportional authoring guidance. |
| `docs/planning/design/features/core_python_workspace_and_harness.md` | Feature design for the consolidated core Python workspace and the first helper-harness package boundaries. |
| `docs/planning/design/features/github_collaboration_scaffolding.md` | Feature design for GitHub issue forms, pull request expectations, and the hosted project field model. |
| `docs/planning/design/features/github_task_push_sync.md` | Feature design for push-only GitHub sync from local task records to issues and optional project items. |
| `docs/planning/design/features/initiative_closeout_and_planning_trackers.md` | Feature design for initiative closeout state and the generated planning trackers that mirror it. |
| `docs/planning/design/features/python_validator_execution.md` | Feature design for the Python validator execution layer driven by the control-plane validator registry. |
| `docs/planning/design/features/schema_resolution_and_index_search.md` | Feature design for deterministic local schema resolution and index-backed repository search. |
| `docs/planning/design/features/structural_rewrite_program.md` | Feature design for executing the guarded structural rewrite program through the closed final Phase 4 outcome review and explicit program closeout decision. |

## Notes
- Documents in this directory should follow [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md).
- Start new documents from [feature_design_template.md](/home/j/WatchTowerPlan/docs/templates/feature_design_template.md).
- Governed feature designs in this directory should use the feature-design front matter profile.
- Human-readable tracking for this family lives in [design_tracking.md](/home/j/WatchTowerPlan/docs/planning/design/design_tracking.md).
- Use this directory when the main deliverable is a recommended design. If the main deliverable is concrete execution breakdown, use `docs/planning/design/implementation/` instead.
