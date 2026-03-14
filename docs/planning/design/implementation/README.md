# `docs/planning/design/implementation`

## Description
`This directory contains implementation-plan documents that translate approved feature designs into concrete engineering work for this repository. Use it for plans that are detailed enough to guide execution but still remain above commit-by-commit notes.`

## Files
| Path | Description |
|---|---|
| `docs/planning/design/implementation/README.md` | Describes the purpose of the implementation-plan directory, its current plans, and the standards that govern them. |
| `docs/planning/design/implementation/control_plane_loaders_and_schema_store.md` | Implementation plan for the first control-plane loader and SchemaStore slice in the core Python workspace. |
| `docs/planning/design/implementation/structural_rewrite_artifact_role_registry_pilot.md` | Implementation plan for the bounded artifact-role registry pilot that opens Phase 2 with one additive read-only slice. |
| `docs/planning/design/implementation/structural_rewrite_phase3_command_authority_entry.md` | Entry package for the bounded Phase 3 command-authority normalization checkpoint. |
| `docs/planning/design/implementation/structural_rewrite_phase3_command_companion_source_surface_normalization.md` | Implementation plan for the first bounded Phase 3 slice that reconciles command-doc source surfaces to the current family-owned command authority model. |
| `docs/planning/design/implementation/structural_rewrite_phase4_shared_projection_entry.md` | Entry package for the bounded Phase 4 shared-projection and private internal-planning-graph checkpoint. |
| `docs/planning/design/implementation/structural_rewrite_phase4_planning_projection_snapshot.md` | Implementation plan for the first bounded Phase 4 slice that introduces one private planning projection snapshot behind initiative-index and planning-catalog sync. |
| `docs/planning/design/implementation/structural_rewrite_program.md` | Implementation plan for the structural rewrite program through the closed Phase 4 entry review and handoff into the first bounded Phase 4 slice. |
| `docs/planning/design/implementation/template_and_output_efficiency_execution.md` | Implementation plan for compact authoring rules, tracker compaction, and workflow-guidance tightening. |

## Notes
- Documents in this directory should follow [implementation_plan_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/implementation_plan_md_standard.md).
- Start new documents from [implementation_plan_template.md](/home/j/WatchTowerPlan/docs/templates/implementation_plan_template.md).
- Governed implementation plans in this directory should use the implementation-plan front matter profile.
- Human-readable tracking for this family lives in [design_tracking.md](/home/j/WatchTowerPlan/docs/planning/design/design_tracking.md).
- Use this directory when the main deliverable is engineering execution breakdown. If the main deliverable is architectural recommendation and tradeoff analysis, use `docs/planning/design/features/` instead.
- Rewrite-specific phase plans, checkpoints, and entry-review packages should live here rather than in a separate rewrite-only directory.
