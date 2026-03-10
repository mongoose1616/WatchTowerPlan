# `docs/planning/prds`

## Description
`This directory holds product requirements documents for durable product and planning intent. Use it when scope, goals, requirements, and acceptance criteria need to be reviewed before design or implementation planning begins.`

## Files
| Path | Description |
|---|---|
| `docs/planning/prds/README.md` | Describes the purpose of the PRD directory, its current contents, and the standards that govern it. |
| `docs/planning/prds/core_python_foundation.md` | PRD for the core Python workspace, control-plane loading, validation, query, and traceability foundation. |
| `docs/planning/prds/template_and_output_efficiency.md` | PRD for compact template defaults, compact tracker outputs, and proportional workflow guidance. |
| `docs/planning/prds/prd_tracking.md` | Human-readable tracker for the current PRD corpus. |

## Notes
- Start with `docs/planning/initiatives/initiative_tracking.md` when you need cross-family phase, owner, or next-step visibility for a PRD-backed initiative.
- PRDs in this directory should follow [prd_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/prd_md_standard.md).
- Start new documents from [prd_template.md](/home/j/WatchTowerPlan/docs/templates/prd_template.md).
- Keep the machine-readable companion index aligned under `core/control_plane/indexes/prds/`.
- Add or update a companion acceptance contract under `core/control_plane/contracts/acceptance/` when a PRD publishes durable machine-consumable acceptance criteria.
