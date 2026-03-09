# `docs/design`

## Description
`This directory holds repository-native design documents. Use it for technical design work that bridges repository foundations to later implementation. Store feature-level solution designs in docs/design/features/ and concrete engineering execution plans in docs/design/implementation/.`

## Paths
| Path | Description |
|---|---|
| `docs/design/README.md` | Describes the purpose of the design directory, its document families, and the standards that govern them. |
| `docs/design/design_tracking.md` | Human-readable tracker for the current feature designs, implementation plans, and their main relationships. |
| `docs/design/features/` | Holds feature-level technical design documents that define recommended solution direction before implementation planning. |
| `docs/design/implementation/` | Holds implementation-plan documents that break approved designs into concrete engineering work. |

## Notes
- Documents under `docs/design/features/**` should follow [feature_design_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/feature_design_md_standard.md) and start from [feature_design_template.md](/home/j/WatchTowerPlan/docs/templates/feature_design_template.md).
- Documents under `docs/design/implementation/**` should follow [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md) and start from [implementation_plan_template.md](/home/j/WatchTowerPlan/docs/templates/implementation_plan_template.md).
- Keep the human tracking view in [design_tracking.md](/home/j/WatchTowerPlan/docs/design/design_tracking.md) aligned with the machine-readable index under `core/control_plane/indexes/design_documents/`.
- Keep workflow execution procedure in `workflows/**` and normative repository rules in `docs/standards/**`; `docs/design/**` is for recommended designs and executable planning, not for authority surfaces that replace those families.
