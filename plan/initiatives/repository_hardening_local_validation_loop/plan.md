# Repository Hardening and Local Validation Loop Plan

## Initiative Identity
- `initiative_id`: `initiative.repository_hardening_local_validation_loop`
- `trace_id`: `trace.repository_hardening_local_validation_loop`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-29T00:30:24Z`

## Scope and Non-Goals
Hardens local verification, shared-core boundaries, and parser-module hotspots.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add Local Verification Runner: Add a canonical local verification script, optional git-hook installer, and aligned docs for daily use.
- Bootstrap Repository Hardening and Local Validation Loop: Bootstrap Repository Hardening and Local Validation Loop live initiative package.
- Decompose Plan Query Registration: Split the plan query parser registration surface into smaller modules with clearer ownership boundaries.
- Fix Shared-Core Validation Boundary: Remove live plan coupling from shared-core validation tests and restore the current core lint baseline.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.repository_hardening_local_validation_loop.add_local_verification_runner.002](/plan/initiatives/repository_hardening_local_validation_loop/.wt/tasks/add_local_verification_runner/task.json) | `completed` | `high` | `repository_maintainer` | Add a canonical local verification script, optional git-hook installer, and aligned docs for daily use. | task.repository_hardening_local_validation_loop.fix_shared_core_validation_boundary.001 |
| [task.repository_hardening_local_validation_loop.fix_shared_core_validation_boundary.001](/plan/initiatives/repository_hardening_local_validation_loop/.wt/tasks/fix_shared_core_validation_boundary/task.json) | `completed` | `high` | `repository_maintainer` | Remove live plan coupling from shared-core validation tests and restore the current core lint baseline. | - |
| [task.repository_hardening_local_validation_loop.bootstrap_repository_hardening_and_local_validation_loop](/plan/initiatives/repository_hardening_local_validation_loop/.wt/tasks/bootstrap_repository_hardening_and_local_validation_loop/task.json) | `completed` | `medium` | `repository_maintainer` | Bootstrap Repository Hardening and Local Validation Loop live initiative package. | - |
| [task.repository_hardening_local_validation_loop.decompose_plan_query_registration.003](/plan/initiatives/repository_hardening_local_validation_loop/.wt/tasks/decompose_plan_query_registration/task.json) | `completed` | `medium` | `repository_maintainer` | Split the plan query parser registration surface into smaller modules with clearer ownership boundaries. | task.repository_hardening_local_validation_loop.add_local_verification_runner.002 |

## Dependencies and Risks
- Task `task.repository_hardening_local_validation_loop.add_local_verification_runner.002` depends on `task.repository_hardening_local_validation_loop.fix_shared_core_validation_boundary.001`.
- Task `task.repository_hardening_local_validation_loop.decompose_plan_query_registration.003` depends on `task.repository_hardening_local_validation_loop.add_local_verification_runner.002`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/repository_hardening_local_validation_loop/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/repository_hardening_local_validation_loop/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/repository_hardening_local_validation_loop/implementation_slice.md)
- Governing document: [repository_validation_standard.md](/core/docs/standards/validations/repository_validation_standard.md)
- Governing document: [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md)
- Rendered plan: [plan.md](/plan/initiatives/repository_hardening_local_validation_loop/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/repository_hardening_local_validation_loop/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/repository_hardening_local_validation_loop/summary.md)
