# Core Host Pack Architecture Hard Cutover Plan

## Initiative Identity
- `initiative_id`: `initiative.core_host_pack_architecture_hard_cutover`
- `trace_id`: `trace.core_host_pack_architecture_hard_cutover`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `in_progress`
- `review_status`: `approved`
- `updated_at`: `2026-03-20T18:08:51Z`

## Scope and Non-Goals
Separates reusable core, host composition, and pack-native runtime behind governed pack contracts, host-owned CLI composition, and pack interface validation.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add governed pack registry and runtime manifest contracts: Defines the core-owned registry, schemas, typed models, and validator hooks for host-pack integration.
- Add pack-interface validation, import-boundary guards, and second-pack proofs: Proves the new architecture with validator coverage, boundary guards, and a synthetic second-pack fixture.
- Bootstrap Core Host Pack Architecture Hard Cutover: Bootstrap Core Host Pack Architecture Hard Cutover live initiative package.
- Introduce watchtower_host and move CLI composition out of reusable core: Moves parser construction and command registration into a host-owned package while preserving the watchtower-core binary name.
- Publish host-pack standards, references, templates, and workflow modules: Documents the final core-host-pack contract and updates workflow routing, command docs, and pack authoring guidance.
- Refactor watchtower_plan into pack-native feature services and namespaced commands: Rebuilds the plan package around pack-native feature seams instead of mirrored core-style families.
- Run boundary stabilization cleanup loop: Performs the first required validation, neighboring-surface expansion, fixes, docs updates, and commit pass after the main implementation slices land.
- Run extensibility and portability hardening loop: Performs the second required validation loop focused on pack portability, extensibility, and surrounding contract cleanup.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.core_host_pack_architecture_hard_cutover.docs_workflows.004](/plan/initiatives/core_host_pack_architecture_hard_cutover/.wt/tasks/publish_host_pack_standards_references_templates_and_workflow_modules/task.json) | `planned` | `high` | `repository_maintainer` | Documents the final core-host-pack contract and updates workflow routing, command docs, and pack authoring guidance. | task.core_host_pack_architecture_hard_cutover.pack_contract.001 |
| [task.core_host_pack_architecture_hard_cutover.pack_tests.005](/plan/initiatives/core_host_pack_architecture_hard_cutover/.wt/tasks/add_pack_interface_validation_import_boundary_guards_and_second_pack_proofs/task.json) | `planned` | `high` | `repository_maintainer` | Proves the new architecture with validator coverage, boundary guards, and a synthetic second-pack fixture. | task.core_host_pack_architecture_hard_cutover.pack_contract.001, task.core_host_pack_architecture_hard_cutover.host_runtime.002 |
| [task.core_host_pack_architecture_hard_cutover.plan_pack.003](/plan/initiatives/core_host_pack_architecture_hard_cutover/.wt/tasks/refactor_watchtower_plan_into_pack_native_feature_services_and_namespaced_commands/task.json) | `planned` | `high` | `repository_maintainer` | Rebuilds the plan package around pack-native feature seams instead of mirrored core-style families. | task.core_host_pack_architecture_hard_cutover.pack_contract.001, task.core_host_pack_architecture_hard_cutover.host_runtime.002 |
| [task.core_host_pack_architecture_hard_cutover.bootstrap_core_host_pack_architecture_hard_cutover](/plan/initiatives/core_host_pack_architecture_hard_cutover/.wt/tasks/bootstrap_core_host_pack_architecture_hard_cutover/task.json) | `planned` | `medium` | `repository_maintainer` | Bootstrap Core Host Pack Architecture Hard Cutover live initiative package. | - |
| [task.core_host_pack_architecture_hard_cutover.cleanup_loop_one.006](/plan/initiatives/core_host_pack_architecture_hard_cutover/.wt/tasks/run_boundary_stabilization_cleanup_loop/task.json) | `planned` | `medium` | `repository_maintainer` | Performs the first required validation, neighboring-surface expansion, fixes, docs updates, and commit pass after the main implementation slices land. | task.core_host_pack_architecture_hard_cutover.plan_pack.003, task.core_host_pack_architecture_hard_cutover.docs_workflows.004, task.core_host_pack_architecture_hard_cutover.pack_tests.005 |
| [task.core_host_pack_architecture_hard_cutover.cleanup_loop_two.007](/plan/initiatives/core_host_pack_architecture_hard_cutover/.wt/tasks/run_extensibility_and_portability_hardening_loop/task.json) | `planned` | `medium` | `repository_maintainer` | Performs the second required validation loop focused on pack portability, extensibility, and surrounding contract cleanup. | task.core_host_pack_architecture_hard_cutover.cleanup_loop_one.006 |
| [task.core_host_pack_architecture_hard_cutover.host_runtime.002](/plan/initiatives/core_host_pack_architecture_hard_cutover/.wt/tasks/introduce_watchtower_host_and_move_cli_composition_out_of_reusable_core/task.json) | `completed` | `high` | `repository_maintainer` | Moves parser construction and command registration into a host-owned package while preserving the watchtower-core binary name. | task.core_host_pack_architecture_hard_cutover.pack_contract.001 |
| [task.core_host_pack_architecture_hard_cutover.pack_contract.001](/plan/initiatives/core_host_pack_architecture_hard_cutover/.wt/tasks/add_governed_pack_registry_and_runtime_manifest_contracts/task.json) | `completed` | `high` | `repository_maintainer` | Defines the core-owned registry, schemas, typed models, and validator hooks for host-pack integration. | - |

## Dependencies and Risks
- Task `task.core_host_pack_architecture_hard_cutover.pack_tests.005` depends on `task.core_host_pack_architecture_hard_cutover.pack_contract.001`, `task.core_host_pack_architecture_hard_cutover.host_runtime.002`.
- Task `task.core_host_pack_architecture_hard_cutover.host_runtime.002` depends on `task.core_host_pack_architecture_hard_cutover.pack_contract.001`.
- Task `task.core_host_pack_architecture_hard_cutover.docs_workflows.004` depends on `task.core_host_pack_architecture_hard_cutover.pack_contract.001`.
- Task `task.core_host_pack_architecture_hard_cutover.plan_pack.003` depends on `task.core_host_pack_architecture_hard_cutover.pack_contract.001`, `task.core_host_pack_architecture_hard_cutover.host_runtime.002`.
- Task `task.core_host_pack_architecture_hard_cutover.cleanup_loop_one.006` depends on `task.core_host_pack_architecture_hard_cutover.plan_pack.003`, `task.core_host_pack_architecture_hard_cutover.docs_workflows.004`, `task.core_host_pack_architecture_hard_cutover.pack_tests.005`.
- Task `task.core_host_pack_architecture_hard_cutover.cleanup_loop_two.007` depends on `task.core_host_pack_architecture_hard_cutover.cleanup_loop_one.006`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/core_host_pack_architecture_hard_cutover/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/core_host_pack_architecture_hard_cutover/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/core_host_pack_architecture_hard_cutover/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/core_host_pack_architecture_hard_cutover/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/core_host_pack_architecture_hard_cutover/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/core_host_pack_architecture_hard_cutover/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/core_host_pack_architecture_hard_cutover/summary.md)
