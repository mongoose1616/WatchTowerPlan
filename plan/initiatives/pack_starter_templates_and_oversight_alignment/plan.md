# Pack Starter Templates And Oversight Alignment Plan

## Initiative Identity
- `initiative_id`: `initiative.pack_starter_templates_and_oversight_alignment`
- `trace_id`: `trace.pack_starter_templates_and_oversight_alignment`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `in_progress`
- `review_status`: `approved`
- `updated_at`: `2026-03-21T01:54:51Z`

## Scope and Non-Goals
Publishes reusable hosted-pack starter templates and aligns WatchTowerOversight to the shared core-host-pack contract.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Align WatchTowerOversight to the shared pack contract: Aligns the oversight pack to the shared core-host-pack contract in its own repository.
- Bootstrap Pack Starter Templates And Oversight Alignment: Bootstrap Pack Starter Templates And Oversight Alignment live initiative package.
- Publish hosted-pack starter templates: Adds governed starter templates and guidance for new hosted packs.
- Validate starter templates and oversight adoption: Proves the starter templates and real oversight alignment through validation and closeout evidence.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.pack_starter_templates_and_oversight_alignment.publish_hosted_pack_starter_templates](/plan/initiatives/pack_starter_templates_and_oversight_alignment/.wt/tasks/publish_hosted_pack_starter_templates/task.json) | `ready` | `high` | `repository_maintainer` | Adds governed starter templates and guidance for new hosted packs. | - |
| [task.pack_starter_templates_and_oversight_alignment.align_watchtower_oversight_to_shared_pack_contract](/plan/initiatives/pack_starter_templates_and_oversight_alignment/.wt/tasks/align_watchtoweroversight_to_the_shared_pack_contract/task.json) | `planned` | `high` | `repository_maintainer` | Aligns the oversight pack to the shared core-host-pack contract in its own repository. | task.pack_starter_templates_and_oversight_alignment.publish_hosted_pack_starter_templates |
| [task.pack_starter_templates_and_oversight_alignment.validate_pack_starter_and_oversight_adoption](/plan/initiatives/pack_starter_templates_and_oversight_alignment/.wt/tasks/validate_starter_templates_and_oversight_adoption/task.json) | `planned` | `medium` | `repository_maintainer` | Proves the starter templates and real oversight alignment through validation and closeout evidence. | task.pack_starter_templates_and_oversight_alignment.publish_hosted_pack_starter_templates, task.pack_starter_templates_and_oversight_alignment.align_watchtower_oversight_to_shared_pack_contract |
| [task.pack_starter_templates_and_oversight_alignment.bootstrap_pack_starter_templates_and_oversight_alignment](/plan/initiatives/pack_starter_templates_and_oversight_alignment/.wt/tasks/bootstrap_pack_starter_templates_and_oversight_alignment/task.json) | `completed` | `high` | `repository_maintainer` | Bootstrap Pack Starter Templates And Oversight Alignment live initiative package. | - |

## Dependencies and Risks
- Discrepancy `discrepancy.pack_starter_templates_and_oversight_alignment.artifact_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/artifact_index.json.
- Discrepancy `discrepancy.pack_starter_templates_and_oversight_alignment.progress_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/initiatives/pack_starter_templates_and_oversight_alignment/progress.md.
- Discrepancy `discrepancy.pack_starter_templates_and_oversight_alignment.review_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/review_index.json.
- Task `task.pack_starter_templates_and_oversight_alignment.align_watchtower_oversight_to_shared_pack_contract` depends on `task.pack_starter_templates_and_oversight_alignment.publish_hosted_pack_starter_templates`.
- Task `task.pack_starter_templates_and_oversight_alignment.validate_pack_starter_and_oversight_adoption` depends on `task.pack_starter_templates_and_oversight_alignment.publish_hosted_pack_starter_templates`, `task.pack_starter_templates_and_oversight_alignment.align_watchtower_oversight_to_shared_pack_contract`.

## Validation or Completion Gates
- `capture_complete`: `True`
- `machine_valid`: `True`
- `approval_status`: `approved`
- `ready_for_execution`: `True`
- `blocking_reasons`: `none`
- Task count: `4`
- Evidence bundle count: `1`
- Closeout shell count: `1`
- Promotion shell count: `1`
- Acceptance contract refs: `0`

## Linked Outputs
- Authored input: [initiative_brief.md](/plan/initiatives/pack_starter_templates_and_oversight_alignment/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/pack_starter_templates_and_oversight_alignment/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/pack_starter_templates_and_oversight_alignment/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/pack_starter_templates_and_oversight_alignment/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/pack_starter_templates_and_oversight_alignment/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/pack_starter_templates_and_oversight_alignment/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/pack_starter_templates_and_oversight_alignment/summary.md)
