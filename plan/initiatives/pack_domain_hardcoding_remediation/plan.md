# Pack Domain Hardcoding Remediation Plan

## Initiative Identity
- `initiative_id`: `initiative.pack_domain_hardcoding_remediation`
- `trace_id`: `trace.pack_domain_hardcoding_remediation`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `in_progress`
- `review_status`: `approved`
- `updated_at`: `2026-03-20T00:16:10Z`

## Scope and Non-Goals
Verify and remove remaining pack-domain hardcoding, reorganize lingering legacy artifacts, and prove the pack-driven endstate.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Bootstrap Pack Domain Hardcoding Remediation: Bootstrap Pack Domain Hardcoding Remediation live initiative package.
- Pack-drive runtime roots and validation selection: Remove remaining fixed pack-root assumptions from runtime helpers, CLI defaults, and validation selection.
- Re-root governed contracts and generated surfaces: Move remaining plan-specific governed contracts out of shared-core assumptions and bind them through pack-owned declarations.
- Recover rich human docs and guidance from pack-driven state: Review main-branch patterns and restore rich human-facing documentation and navigation without reintroducing hardcoded domain roots.
- Run assessment pass one: Run the first full repository assessment after the main hardcoding fixes land and convert any new gaps into tracked remediation work.
- Run assessment pass two: Run the final full repository assessment after cleanup and confirm the pack-driven endstate has no remaining actionable gaps.
- Split core and plan Python boundary: Move residual plan-domain runtime out of watchtower_core.plan_runtime and behind a plan-owned Python boundary under plan/**.
- Verify report findings and map pack roots: Validate the hardcoding assessment against the current repository and map the actual pack-root authority seams.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary |
| --- | --- | --- | --- | --- |
| [task.pack_domain_hardcoding_remediation.split_core_and_plan_python_boundary](/plan/initiatives/pack_domain_hardcoding_remediation/.wt/tasks/split_core_and_plan_python_boundary/task.json) | `ready` | `critical` | `repository_maintainer` | Move residual plan-domain runtime out of watchtower_core.plan_runtime and behind a plan-owned Python boundary under plan/**. |
| [task.pack_domain_hardcoding_remediation.run_assessment_pass_two](/plan/initiatives/pack_domain_hardcoding_remediation/.wt/tasks/run_assessment_pass_two/task.json) | `in_progress` | `high` | `repository_maintainer` | Run the final full repository assessment after cleanup and confirm the pack-driven endstate has no remaining actionable gaps. |
| [task.pack_domain_hardcoding_remediation.pack_drive_runtime_roots_and_validation](/plan/initiatives/pack_domain_hardcoding_remediation/.wt/tasks/pack_drive_runtime_roots_and_validation_selection/task.json) | `completed` | `critical` | `repository_maintainer` | Remove remaining fixed pack-root assumptions from runtime helpers, CLI defaults, and validation selection. |
| [task.pack_domain_hardcoding_remediation.re_root_control_plane_and_governed_contracts](/plan/initiatives/pack_domain_hardcoding_remediation/.wt/tasks/re_root_governed_contracts_and_generated_surfaces/task.json) | `completed` | `critical` | `repository_maintainer` | Move remaining plan-specific governed contracts out of shared-core assumptions and bind them through pack-owned declarations. |
| [task.pack_domain_hardcoding_remediation.verify_report_and_map_pack_roots](/plan/initiatives/pack_domain_hardcoding_remediation/.wt/tasks/verify_report_findings_and_map_pack_roots/task.json) | `completed` | `critical` | `repository_maintainer` | Validate the hardcoding assessment against the current repository and map the actual pack-root authority seams. |
| [task.pack_domain_hardcoding_remediation.recover_rich_human_docs_and_guidance](/plan/initiatives/pack_domain_hardcoding_remediation/.wt/tasks/recover_rich_human_docs_and_guidance_from_pack_driven_state/task.json) | `completed` | `high` | `repository_maintainer` | Review main-branch patterns and restore rich human-facing documentation and navigation without reintroducing hardcoded domain roots. |
| [task.pack_domain_hardcoding_remediation.run_assessment_pass_one](/plan/initiatives/pack_domain_hardcoding_remediation/.wt/tasks/run_assessment_pass_one/task.json) | `completed` | `high` | `repository_maintainer` | Run the first full repository assessment after the main hardcoding fixes land and convert any new gaps into tracked remediation work. |
| [task.pack_domain_hardcoding_remediation.bootstrap_pack_domain_hardcoding_remediation](/plan/initiatives/pack_domain_hardcoding_remediation/.wt/tasks/bootstrap_pack_domain_hardcoding_remediation/task.json) | `completed` | `medium` | `repository_maintainer` | Bootstrap Pack Domain Hardcoding Remediation live initiative package. |

## Dependencies and Risks
- No current blockers, dependencies, or open discrepancy risks are recorded.

## Validation or Completion Gates
- `capture_complete`: `True`
- `machine_valid`: `True`
- `approval_status`: `approved`
- `ready_for_execution`: `True`
- `blocking_reasons`: `none`
- Task count: `8`
- Evidence bundle count: `1`
- Closeout shell count: `1`
- Promotion shell count: `1`
- Acceptance contract refs: `0`

## Linked Outputs
- Authored input: [initiative_brief.md](/plan/initiatives/pack_domain_hardcoding_remediation/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/pack_domain_hardcoding_remediation/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/pack_domain_hardcoding_remediation/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/pack_domain_hardcoding_remediation/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/pack_domain_hardcoding_remediation/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/pack_domain_hardcoding_remediation/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/pack_domain_hardcoding_remediation/summary.md)
