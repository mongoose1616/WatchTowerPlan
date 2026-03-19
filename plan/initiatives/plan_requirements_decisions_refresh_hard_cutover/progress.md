# Requirements And Decisions Hard Cutover Refresh Progress

## Current Status
- `lifecycle_stage`: `in_progress`
- `review_status`: `approved`
- `approval_status`: `approved`
- `ready_for_execution`: `True`
- `updated_at`: `2026-03-19T05:19:21Z`

## Recent Events or Changes
| Recorded At | Event | Actor | Summary |
| --- | --- | --- | --- |
| `2026-03-19T05:10:14Z` | `execution_started` | `actor.watchtower_core` | Execution started after task task.plan_requirements_decisions_refresh_hard_cutover.cut_over_root_entrypoints_and_foundations entered in_progress. |
| `2026-03-19T05:09:16Z` | `ready_for_execution_marked` | `actor.watchtower_core` | The initiative package entered ready_for_execution after approval. |
| `2026-03-19T05:09:16Z` | `ready_for_execution_approved` | `actor.repository_maintainer` | An authorized maintainer approved the initiative package for execution. |
| `2026-03-19T05:08:35Z` | `authored_inputs_confirmed` | `actor.repository_maintainer` | An authorized maintainer confirmed the authored intake documents into machine state. |
| `2026-03-19T05:02:21Z` | `ready_for_review_marked` | `actor.watchtower_core` | The initiative package passed capture validation and is ready for review. |

## Active Tasks
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_requirements_decisions_refresh_hard_cutover.remove_repo_root_workflows_and_commit_routing_gaps](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/.wt/tasks/remove_repo_root_workflows_and_commit_routing_gaps/task.json) | `in_progress` | `high` | `repository_maintainer` | Delete the compatibility workflows tree after repointing every route, workflow reference, and closeout instruction to core/workflows or plan/workflows. | - |
| [task.plan_requirements_decisions_refresh_hard_cutover.eliminate_repo_ops_namespace](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/.wt/tasks/eliminate_repo_ops_namespace/task.json) | `planned` | `critical` | `repository_maintainer` | Redistribute surviving repo_ops behavior into explicit runtime packages and remove the catch-all namespace. | - |
| [task.plan_requirements_decisions_refresh_hard_cutover.retire_legacy_planning_corpus_and_indexes](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/.wt/tasks/retire_legacy_planning_corpus_and_indexes/task.json) | `planned` | `critical` | `repository_maintainer` | Move human tracking under plan/, promote or distill durable guidance, and delete docs/planning-backed indexes and trackers. | - |
| [task.plan_requirements_decisions_refresh_hard_cutover.eliminate_domain_packs_fixture_path](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/.wt/tasks/eliminate_domain_packs_fixture_path/task.json) | `planned` | `high` | `repository_maintainer` | Rework fixture materialization, examples, and guards so tests use temp pack roots and never recreate repo-root domain_packs/. | - |
| [task.plan_requirements_decisions_refresh_hard_cutover.run_assessment_pass_one](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/.wt/tasks/run_assessment_pass_one/task.json) | `planned` | `high` | `repository_maintainer` | Run the first full repository assessment after the initial cutover slices and fix any newly found gaps. | task.plan_requirements_decisions_refresh_hard_cutover.cut_over_root_entrypoints_and_foundations, task.plan_requirements_decisions_refresh_hard_cutover.retire_legacy_planning_corpus_and_indexes, task.plan_requirements_decisions_refresh_hard_cutover.remove_repo_root_workflows_and_commit_routing_gaps |
| [task.plan_requirements_decisions_refresh_hard_cutover.run_assessment_pass_two](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/.wt/tasks/run_assessment_pass_two/task.json) | `planned` | `high` | `repository_maintainer` | Repeat the full repository assessment after the purge and runtime refactor and close any remaining gaps. | task.plan_requirements_decisions_refresh_hard_cutover.eliminate_repo_ops_namespace, task.plan_requirements_decisions_refresh_hard_cutover.eliminate_domain_packs_fixture_path, task.plan_requirements_decisions_refresh_hard_cutover.run_assessment_pass_one |

## Blockers
- Task `task.plan_requirements_decisions_refresh_hard_cutover.run_assessment_pass_one` depends on `task.plan_requirements_decisions_refresh_hard_cutover.cut_over_root_entrypoints_and_foundations`, `task.plan_requirements_decisions_refresh_hard_cutover.retire_legacy_planning_corpus_and_indexes`, `task.plan_requirements_decisions_refresh_hard_cutover.remove_repo_root_workflows_and_commit_routing_gaps`.
- Task `task.plan_requirements_decisions_refresh_hard_cutover.run_assessment_pass_two` depends on `task.plan_requirements_decisions_refresh_hard_cutover.eliminate_repo_ops_namespace`, `task.plan_requirements_decisions_refresh_hard_cutover.eliminate_domain_packs_fixture_path`, `task.plan_requirements_decisions_refresh_hard_cutover.run_assessment_pass_one`.

## Next Actions
- Start the highest-priority ready task from the initiative package.
- Next surface: [plan.md](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/plan.md)

## Evidence or Validation State
- `machine_valid`: `True`
- Evidence bundles: `1`
- Acceptance contract refs: `1`
- Trace-linked evidence refs: `1`
- `evidence.plan_requirements_decisions_refresh_hard_cutover.bootstrap_validation_bundle`: `planned`
