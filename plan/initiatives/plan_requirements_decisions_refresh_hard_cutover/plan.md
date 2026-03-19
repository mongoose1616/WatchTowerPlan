# Requirements And Decisions Hard Cutover Refresh Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_requirements_decisions_refresh_hard_cutover`
- `trace_id`: `trace.plan_requirements_decisions_refresh_hard_cutover`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `in_progress`
- `review_status`: `approved`
- `updated_at`: `2026-03-19T05:19:21Z`

## Scope and Non-Goals
Tracks the hard-cutover refresh that retires legacy planning history, workflow compatibility roots, repo_ops, and domain_packs while aligning the repo to requirements.md and decisions.md.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Cut over root entrypoints and foundations: Rewrite root and foundation authority surfaces around core/docs, plan/docs mirrors, and split workflow roots.
- Eliminate domain_packs fixture path: Rework fixture materialization, examples, and guards so tests use temp pack roots and never recreate repo-root domain_packs/.
- Eliminate repo_ops namespace: Redistribute surviving repo_ops behavior into explicit runtime packages and remove the catch-all namespace.
- Remove repo-root workflows and commit routing gaps: Delete the compatibility workflows tree after repointing every route, workflow reference, and closeout instruction to core/workflows or plan/workflows.
- Bootstrap Requirements And Decisions Hard Cutover Refresh planning chain: Bootstraps the initial planning chain for Requirements And Decisions Hard Cutover Refresh.
- Retire legacy planning corpus and indexes: Move human tracking under plan/, promote or distill durable guidance, and delete docs/planning-backed indexes and trackers.
- Run assessment pass one: Run the first full repository assessment after the initial cutover slices and fix any newly found gaps.
- Run assessment pass two: Repeat the full repository assessment after the purge and runtime refactor and close any remaining gaps.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_requirements_decisions_refresh_hard_cutover.remove_repo_root_workflows_and_commit_routing_gaps](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/.wt/tasks/remove_repo_root_workflows_and_commit_routing_gaps/task.json) | `in_progress` | `high` | `repository_maintainer` | Delete the compatibility workflows tree after repointing every route, workflow reference, and closeout instruction to core/workflows or plan/workflows. | - |
| [task.plan_requirements_decisions_refresh_hard_cutover.eliminate_repo_ops_namespace](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/.wt/tasks/eliminate_repo_ops_namespace/task.json) | `planned` | `critical` | `repository_maintainer` | Redistribute surviving repo_ops behavior into explicit runtime packages and remove the catch-all namespace. | - |
| [task.plan_requirements_decisions_refresh_hard_cutover.retire_legacy_planning_corpus_and_indexes](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/.wt/tasks/retire_legacy_planning_corpus_and_indexes/task.json) | `planned` | `critical` | `repository_maintainer` | Move human tracking under plan/, promote or distill durable guidance, and delete docs/planning-backed indexes and trackers. | - |
| [task.plan_requirements_decisions_refresh_hard_cutover.eliminate_domain_packs_fixture_path](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/.wt/tasks/eliminate_domain_packs_fixture_path/task.json) | `planned` | `high` | `repository_maintainer` | Rework fixture materialization, examples, and guards so tests use temp pack roots and never recreate repo-root domain_packs/. | - |
| [task.plan_requirements_decisions_refresh_hard_cutover.run_assessment_pass_one](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/.wt/tasks/run_assessment_pass_one/task.json) | `planned` | `high` | `repository_maintainer` | Run the first full repository assessment after the initial cutover slices and fix any newly found gaps. | task.plan_requirements_decisions_refresh_hard_cutover.cut_over_root_entrypoints_and_foundations, task.plan_requirements_decisions_refresh_hard_cutover.retire_legacy_planning_corpus_and_indexes, task.plan_requirements_decisions_refresh_hard_cutover.remove_repo_root_workflows_and_commit_routing_gaps |
| [task.plan_requirements_decisions_refresh_hard_cutover.run_assessment_pass_two](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/.wt/tasks/run_assessment_pass_two/task.json) | `planned` | `high` | `repository_maintainer` | Repeat the full repository assessment after the purge and runtime refactor and close any remaining gaps. | task.plan_requirements_decisions_refresh_hard_cutover.eliminate_repo_ops_namespace, task.plan_requirements_decisions_refresh_hard_cutover.eliminate_domain_packs_fixture_path, task.plan_requirements_decisions_refresh_hard_cutover.run_assessment_pass_one |
| [task.plan_requirements_decisions_refresh_hard_cutover.cut_over_root_entrypoints_and_foundations](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/.wt/tasks/cut_over_root_entrypoints_and_foundations/task.json) | `completed` | `high` | `repository_maintainer` | Rewrite root and foundation authority surfaces around core/docs, plan/docs mirrors, and split workflow roots. | - |
| [task.plan_requirements_decisions_refresh_hard_cutover.bootstrap.001](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/.wt/tasks/requirements_and_decisions_hard_cutover_refresh_bootstrap/task.json) | `completed` | `medium` | `repository_maintainer` | Bootstraps the initial planning chain for Requirements And Decisions Hard Cutover Refresh. | - |

## Dependencies and Risks
- Task `task.plan_requirements_decisions_refresh_hard_cutover.run_assessment_pass_one` depends on `task.plan_requirements_decisions_refresh_hard_cutover.cut_over_root_entrypoints_and_foundations`, `task.plan_requirements_decisions_refresh_hard_cutover.retire_legacy_planning_corpus_and_indexes`, `task.plan_requirements_decisions_refresh_hard_cutover.remove_repo_root_workflows_and_commit_routing_gaps`.
- Task `task.plan_requirements_decisions_refresh_hard_cutover.run_assessment_pass_two` depends on `task.plan_requirements_decisions_refresh_hard_cutover.eliminate_repo_ops_namespace`, `task.plan_requirements_decisions_refresh_hard_cutover.eliminate_domain_packs_fixture_path`, `task.plan_requirements_decisions_refresh_hard_cutover.run_assessment_pass_one`.

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
- Acceptance contract refs: `1`

## Linked Outputs
- Authored input: [initiative_brief.md](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_requirements_decisions_refresh_hard_cutover/summary.md)
