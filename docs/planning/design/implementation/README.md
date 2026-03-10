# `docs/planning/design/implementation`

## Description
`This directory contains implementation-plan documents that translate approved feature designs into concrete engineering work for this repository. Use it for plans that are detailed enough to guide execution but still remain above commit-by-commit notes.`

## Files
| Path | Description |
|---|---|
| `docs/planning/design/implementation/README.md` | Describes the purpose of the implementation-plan directory, its current plans, and the standards that govern them. |
| `docs/planning/design/implementation/control_plane_loaders_and_schema_store.md` | Implementation plan for the first control-plane loader and SchemaStore slice in the core Python workspace. |
| `docs/planning/design/implementation/template_and_output_efficiency_execution.md` | Implementation plan for compact authoring rules, tracker compaction, and workflow-guidance tightening. |

## Notes
- Documents in this directory should follow [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md).
- Start new documents from [implementation_plan_template.md](/home/j/WatchTowerPlan/docs/templates/implementation_plan_template.md).
- Governed implementation plans in this directory should use the implementation-plan front matter profile.
- Human-readable tracking for this family lives in [design_tracking.md](/home/j/WatchTowerPlan/docs/planning/design/design_tracking.md).
- Use this directory when the main deliverable is engineering execution breakdown. If the main deliverable is architectural recommendation and tradeoff analysis, use `docs/planning/design/features/` instead.
