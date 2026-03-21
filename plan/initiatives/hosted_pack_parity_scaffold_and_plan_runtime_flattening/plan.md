# Hosted Pack Parity, Scaffolding, and Plan Runtime Flattening Plan

## Initiative Identity
- `initiative_id`: `initiative.hosted_pack_parity_scaffold_and_plan_runtime_flattening`
- `trace_id`: `trace.hosted_pack_parity_scaffold_and_plan_runtime_flattening`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-21T03:56:17Z`

## Scope and Non-Goals
Brings WatchTowerOversight to host-layer parity, turns pack starter templates into scaffoldable operator surfaces, and flattens remaining plan runtime adapters.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Align WatchTowerOversight to host-layer parity: Moves WatchTowerOversight CLI composition behind a host layer and aligns its core-host-pack runtime boundaries with WatchTowerPlan.
- Bootstrap Hosted Pack Parity, Scaffolding, and Plan Runtime Flattening: Bootstrap Hosted Pack Parity, Scaffolding, and Plan Runtime Flattening live initiative package.
- Flatten plan runtime into feature-owned modules: Reorganizes watchtower_plan so remaining adapter-style package families collapse into feature-owned plan services and minimal host-facing adapters.
- Turn pack starter templates into a scaffold command surface: Adds an operator-facing scaffold path that renders the hosted-pack starter templates into a validated pack skeleton.
- Validate and close out the hosted-pack tranche: Runs the explicit cross-repo validation bundle for host parity, scaffold output, and plan runtime flattening, then closes the initiative.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.hosted_pack_parity_scaffold_and_plan_runtime_flattening.align_watchtower_oversight_to_host_layer_parity](/plan/initiatives/hosted_pack_parity_scaffold_and_plan_runtime_flattening/.wt/tasks/align_watchtoweroversight_to_host_layer_parity/task.json) | `completed` | `high` | `repository_maintainer` | Moves WatchTowerOversight CLI composition behind a host layer and aligns its core-host-pack runtime boundaries with WatchTowerPlan. | - |
| [task.hosted_pack_parity_scaffold_and_plan_runtime_flattening.bootstrap_hosted_pack_parity_scaffolding_and_plan_runtime_flattening](/plan/initiatives/hosted_pack_parity_scaffold_and_plan_runtime_flattening/.wt/tasks/bootstrap_hosted_pack_parity_scaffolding_and_plan_runtime_flattening/task.json) | `completed` | `high` | `repository_maintainer` | Bootstrap Hosted Pack Parity, Scaffolding, and Plan Runtime Flattening live initiative package. | - |
| [task.hosted_pack_parity_scaffold_and_plan_runtime_flattening.flatten_plan_runtime_into_feature_owned_modules](/plan/initiatives/hosted_pack_parity_scaffold_and_plan_runtime_flattening/.wt/tasks/flatten_plan_runtime_into_feature_owned_modules/task.json) | `completed` | `high` | `repository_maintainer` | Reorganizes watchtower_plan so remaining adapter-style package families collapse into feature-owned plan services and minimal host-facing adapters. | - |
| [task.hosted_pack_parity_scaffold_and_plan_runtime_flattening.turn_pack_starter_templates_into_a_scaffold_command_surface](/plan/initiatives/hosted_pack_parity_scaffold_and_plan_runtime_flattening/.wt/tasks/turn_pack_starter_templates_into_a_scaffold_command_surface/task.json) | `completed` | `high` | `repository_maintainer` | Adds an operator-facing scaffold path that renders the hosted-pack starter templates into a validated pack skeleton. | - |
| [task.hosted_pack_parity_scaffold_and_plan_runtime_flattening.validate_and_closeout_the_tranche](/plan/initiatives/hosted_pack_parity_scaffold_and_plan_runtime_flattening/.wt/tasks/validate_and_close_out_the_hosted_pack_tranche/task.json) | `completed` | `medium` | `repository_maintainer` | Runs the explicit cross-repo validation bundle for host parity, scaffold output, and plan runtime flattening, then closes the initiative. | task.hosted_pack_parity_scaffold_and_plan_runtime_flattening.align_watchtower_oversight_to_host_layer_parity, task.hosted_pack_parity_scaffold_and_plan_runtime_flattening.turn_pack_starter_templates_into_a_scaffold_command_surface, task.hosted_pack_parity_scaffold_and_plan_runtime_flattening.flatten_plan_runtime_into_feature_owned_modules |

## Dependencies and Risks
- Discrepancy `discrepancy.hosted_pack_parity_scaffold_and_plan_runtime_flattening.artifact_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/artifact_index.json.
- Discrepancy `discrepancy.hosted_pack_parity_scaffold_and_plan_runtime_flattening.progress_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/hosted_pack_parity_scaffold_and_plan_runtime_flattening/progress.md.
- Discrepancy `discrepancy.hosted_pack_parity_scaffold_and_plan_runtime_flattening.review_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/review_index.json.
- Task `task.hosted_pack_parity_scaffold_and_plan_runtime_flattening.validate_and_closeout_the_tranche` depends on `task.hosted_pack_parity_scaffold_and_plan_runtime_flattening.align_watchtower_oversight_to_host_layer_parity`, `task.hosted_pack_parity_scaffold_and_plan_runtime_flattening.turn_pack_starter_templates_into_a_scaffold_command_surface`, `task.hosted_pack_parity_scaffold_and_plan_runtime_flattening.flatten_plan_runtime_into_feature_owned_modules`.

## Validation or Completion Gates
- `capture_complete`: `True`
- `machine_valid`: `True`
- `approval_status`: `approved`
- `ready_for_execution`: `False`
- `blocking_reasons`: `none`
- Task count: `5`
- Evidence bundle count: `1`
- Closeout shell count: `1`
- Promotion shell count: `1`
- Acceptance contract refs: `0`

## Linked Outputs
- Authored input: [initiative_brief.md](/plan/initiatives/hosted_pack_parity_scaffold_and_plan_runtime_flattening/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/hosted_pack_parity_scaffold_and_plan_runtime_flattening/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/hosted_pack_parity_scaffold_and_plan_runtime_flattening/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/hosted_pack_parity_scaffold_and_plan_runtime_flattening/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/hosted_pack_parity_scaffold_and_plan_runtime_flattening/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/hosted_pack_parity_scaffold_and_plan_runtime_flattening/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/hosted_pack_parity_scaffold_and_plan_runtime_flattening/summary.md)
