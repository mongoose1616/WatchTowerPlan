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
- Start with `docs/planning/coordination_tracking.md` when you need the current repo-level planning state before opening design-specific surfaces.
- Use `docs/planning/initiatives/initiative_tracking.md` when you need the deeper initiative-family view behind a design.
- Treat `design_tracking.md` as an active-first tracker. Use `uv run watchtower-core query initiatives --initiative-status <status> --format json` for terminal trace browsing and `uv run watchtower-core query designs --trace-id <trace_id>` for one known design trace.
- Use `uv run watchtower-core query planning --trace-id <trace_id> --format json` when a closed design trace needs the canonical joined planning record rather than the compact family tracker.
- Documents under `docs/planning/design/features/**` should follow [feature_design_md_standard.md](/docs/standards/documentation/feature_design_md_standard.md) and start from [feature_design_template.md](/docs/templates/feature_design_template.md).
- Documents under `docs/planning/design/implementation/**` should follow [implementation_plan_md_standard.md](/docs/standards/documentation/implementation_plan_md_standard.md) and start from [implementation_plan_template.md](/docs/templates/implementation_plan_template.md).
- Governed feature designs and implementation plans should use front matter that validates against their published design-family profiles.
- Keep the human tracking view in [design_tracking.md](/docs/planning/design/design_tracking.md) aligned with the machine-readable index under `core/control_plane/indexes/design_documents/`.
- Keep workflow execution procedure in `workflows/**` and normative repository rules in `docs/standards/**`; `docs/planning/design/**` is for recommended designs and executable planning, not for authority surfaces that replace those families.
