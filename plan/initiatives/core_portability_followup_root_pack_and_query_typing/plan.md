# Core Portability Follow-up Root Pack And Query Typing Plan

## Initiative Identity
- `initiative_id`: `initiative.core_portability_followup_root_pack_and_query_typing`
- `trace_id`: `trace.core_portability_followup_root_pack_and_query_typing`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-23T01:51:41Z`

## Scope and Non-Goals
Cleans up copied-core portability debt in shared help, command docs, tests, and host query typing without changing WatchTowerPlan's current steady-state plan workspace contract.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Align shared core tests with root pack defaults: Moves generic shared-core portability tests to first-party root-pack defaults while preserving explicit externalization coverage.
- Bootstrap Core Portability Follow-up Root Pack And Query Typing: Bootstrap Core Portability Follow-up Root Pack And Query Typing live initiative package.
- Clear host query type backlog and validate slice: Introduces typed helper boundaries for host query handlers and runs the bounded validation gate for the initiative.
- Refresh root pack help and docs: Makes shared core help and command docs root-pack-first while keeping externalized packs supported.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary |
| --- | --- | --- | --- | --- |
| [task.core_portability_followup_root_pack_and_query_typing.align_shared_core_tests_with_root_pack_defaults](/plan/initiatives/core_portability_followup_root_pack_and_query_typing/.wt/tasks/align_shared_core_tests_with_root_pack_defaults/task.json) | `completed` | `high` | `implementation_engineer` | Moves generic shared-core portability tests to first-party root-pack defaults while preserving explicit externalization coverage. |
| [task.core_portability_followup_root_pack_and_query_typing.bootstrap_core_portability_follow_up_root_pack_and_query_typing](/plan/initiatives/core_portability_followup_root_pack_and_query_typing/.wt/tasks/bootstrap_core_portability_follow_up_root_pack_and_query_typing/task.json) | `completed` | `high` | `repository_maintainer` | Bootstrap Core Portability Follow-up Root Pack And Query Typing live initiative package. |
| [task.core_portability_followup_root_pack_and_query_typing.clear_host_query_type_backlog_and_validate](/plan/initiatives/core_portability_followup_root_pack_and_query_typing/.wt/tasks/clear_host_query_type_backlog_and_validate_slice/task.json) | `completed` | `high` | `implementation_engineer` | Introduces typed helper boundaries for host query handlers and runs the bounded validation gate for the initiative. |
| [task.core_portability_followup_root_pack_and_query_typing.refresh_root_pack_help_and_docs](/plan/initiatives/core_portability_followup_root_pack_and_query_typing/.wt/tasks/refresh_root_pack_help_and_docs/task.json) | `completed` | `high` | `implementation_engineer` | Makes shared core help and command docs root-pack-first while keeping externalized packs supported. |

## Dependencies and Risks
- No current blockers, dependencies, or open discrepancy risks are recorded.

## Validation or Completion Gates
- `capture_complete`: `True`
- `machine_valid`: `True`
- `approval_status`: `approved`
- `ready_for_execution`: `False`
- `blocking_reasons`: `none`
- Task count: `4`
- Evidence bundle count: `1`
- Closeout shell count: `1`
- Promotion shell count: `1`
- Acceptance contract refs: `0`

## Linked Outputs
- Authored input: [initiative_brief.md](/plan/initiatives/core_portability_followup_root_pack_and_query_typing/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/core_portability_followup_root_pack_and_query_typing/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/core_portability_followup_root_pack_and_query_typing/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/core_portability_followup_root_pack_and_query_typing/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/core_portability_followup_root_pack_and_query_typing/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/core_portability_followup_root_pack_and_query_typing/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/core_portability_followup_root_pack_and_query_typing/summary.md)
