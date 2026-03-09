# `docs/planning/design`

## Description
`This directory holds repository-native design documents. Use it for technical design work that bridges repository foundations to later implementation. Store feature-level solution designs in docs/planning/design/features/ and concrete engineering execution plans in docs/planning/design/implementation/.`

## Paths
| Path | Description |
|---|---|
| `docs/planning/design/README.md` | Describes the purpose of the design directory, its document families, and the standards that govern them. |
| `docs/planning/design/design_tracking.md` | Human-readable tracker for the current feature designs, implementation plans, and their main relationships. |
| `docs/planning/design/features/` | Holds feature-level technical design documents that define recommended solution direction before implementation planning. |
| `docs/planning/design/implementation/` | Holds implementation-plan documents that break approved designs into concrete engineering work. |

## Notes
- Documents under `docs/planning/design/features/**` should follow [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md) and start from [feature_design_template.md](/home/j/WatchTowerPlan/docs/templates/feature_design_template.md).
- Documents under `docs/planning/design/implementation/**` should follow [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md) and start from [implementation_plan_template.md](/home/j/WatchTowerPlan/docs/templates/implementation_plan_template.md).
- Governed feature designs and implementation plans should use front matter that validates against their published design-family profiles.
- Keep the human tracking view in [design_tracking.md](/home/j/WatchTowerPlan/docs/planning/design/design_tracking.md) aligned with the machine-readable index under `core/control_plane/indexes/design_documents/`.
- Keep workflow execution procedure in `workflows/**` and normative repository rules in `docs/standards/**`; `docs/planning/design/**` is for recommended designs and executable planning, not for authority surfaces that replace those families.
