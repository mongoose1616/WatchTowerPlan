# Plan Python Package Dependency Cleanup Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_python_package_dependency_cleanup`
- `trace_id`: `trace.plan_python_package_dependency_cleanup`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-20T01:51:19Z`

## Scope and Non-Goals
Make plan/python an installable workspace package and remove the last repo-local import shim from reusable core.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Bootstrap Plan Python Package Dependency Cleanup: Bootstrap, author, confirm, and approve the installable-package cleanup initiative.
- Make plan/python installable: Add package metadata for plan/python and install watchtower_plan through the shared core/python workspace without a second environment.
- Remove repo-local bootstrap from watchtower_core: Delete repo-local path bootstrapping from watchtower_core and rely on the installed watchtower_plan package boundary instead.
- Validate workspace package split and close out: Validate the installable-package cutover, repeat the boundary residue pass, and close the initiative on the final green tree.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary |
| --- | --- | --- | --- | --- |
| [task.plan_python_package_dependency_cleanup.make_plan_python_installable](/plan/initiatives/plan_python_package_dependency_cleanup/.wt/tasks/make_plan_python_installable/task.json) | `completed` | `critical` | `repository_maintainer` | Add package metadata for plan/python and install watchtower_plan through the shared core/python workspace without a second environment. |
| [task.plan_python_package_dependency_cleanup.remove_repo_local_bootstrap](/plan/initiatives/plan_python_package_dependency_cleanup/.wt/tasks/remove_repo_local_bootstrap_from_watchtower_core/task.json) | `completed` | `critical` | `repository_maintainer` | Delete repo-local path bootstrapping from watchtower_core and rely on the installed watchtower_plan package boundary instead. |
| [task.plan_python_package_dependency_cleanup.bootstrap](/plan/initiatives/plan_python_package_dependency_cleanup/.wt/tasks/bootstrap_plan_python_package_dependency_cleanup/task.json) | `completed` | `high` | `repository_maintainer` | Bootstrap, author, confirm, and approve the installable-package cleanup initiative. |
| [task.plan_python_package_dependency_cleanup.validate_workspace_closeout](/plan/initiatives/plan_python_package_dependency_cleanup/.wt/tasks/validate_workspace_package_split_and_close_out/task.json) | `completed` | `high` | `repository_maintainer` | Validate the installable-package cutover, repeat the boundary residue pass, and close the initiative on the final green tree. |

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_python_package_dependency_cleanup/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_python_package_dependency_cleanup/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_python_package_dependency_cleanup/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_python_package_dependency_cleanup/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_python_package_dependency_cleanup/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_python_package_dependency_cleanup/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_python_package_dependency_cleanup/summary.md)
