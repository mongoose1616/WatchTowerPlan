# Task Tracking

## Open Tasks
| Task | Status | Priority | Owner | Trace ID | Summary |
| --- | --- | --- | --- | --- | --- |
| [task.plan_domain_pack_core_validation.pack_aware_loading.002](/docs/planning/tasks/open/implement_pack_aware_schema_and_validator_loading.md) | `in_progress` | `high` | `repository_maintainer` | `trace.plan_domain_pack_core_validation` | Adds pack-aware schema catalog merge and pack-declared validator selection to reusable core validation. |
| [task.plan_domain_pack_core_validation.core_suite_runtime.003](/docs/planning/tasks/open/add_core_validation_suite_runtime_and_pack_contract_validation.md) | `backlog` | `high` | `repository_maintainer` | `trace.plan_domain_pack_core_validation` | Publishes the validation suite registry, reusable-core suite runtime, and pack-contract validator. |
| [task.plan_domain_pack_core_validation.plan_fixture_pack.004](/docs/planning/tasks/open/add_plan_fixture_pack_and_end_to_end_suite_coverage.md) | `backlog` | `high` | `repository_maintainer` | `trace.plan_domain_pack_core_validation` | Adds the plan pack test fixture, temp-repo materialization, and end-to-end suite validation coverage. |
| [task.plan_domain_pack_core_validation.repo_migration.005](/docs/planning/tasks/open/migrate_repo_validation_onto_core_suite_runtime.md) | `backlog` | `high` | `repository_maintainer` | `trace.plan_domain_pack_core_validation` | Routes the WatchTowerPlan validation entrypoints and docs through the reusable-core suite runtime. |
| [task.plan_domain_pack_core_validation.validation_closeout.006](/docs/planning/tasks/open/validate_and_close_plan_domain_pack_core_validation.md) | `backlog` | `medium` | `repository_maintainer` | `trace.plan_domain_pack_core_validation` | Refreshes derived surfaces, runs the final validation stack, updates evidence, and closes the trace. |

## Closed Task Summary
- `done`: 253
- `cancelled`: 3

Use `docs/planning/tasks/closed/archive/` for canonical terminal task records, `watchtower-core query tasks --task-status done --format json` for completed-task lookup, or `watchtower-core query tasks --task-status cancelled --format json` for cancelled-task lookup.

## Recently Closed Tasks
| Task | Status | Priority | Owner | Trace ID | Summary |
| --- | --- | --- | --- | --- | --- |
| [task.plan_domain_pack_core_validation.bootstrap.001](/docs/planning/tasks/closed/archive/2026/03/16/plan_domain_pack_core_validation_bootstrap.md) | `done` | `high` | `repository_maintainer` | `trace.plan_domain_pack_core_validation` | Bootstraps the initial planning chain for Plan Domain Pack Core Validation. |
| [task.transition_surface_retirement.validation_closeout.003](/docs/planning/tasks/closed/archive/2026/03/16/validate_and_close_transition_surface_retirement.md) | `done` | `high` | `repository_maintainer` | `trace.transition_surface_retirement` | Refreshes derived surfaces, runs the full validation stack, and closes the trace once no transition leftovers remain in scope. |
| [task.transition_surface_retirement.implementation.002](/docs/planning/tasks/closed/archive/2026/03/16/retire_remaining_transition_modules_and_marker_tests.md) | `done` | `high` | `repository_maintainer` | `trace.transition_surface_retirement` | Removes the remaining compatibility facades, re-export bridges, and marker-only test files and repairs direct consumers. |
| [task.transition_surface_retirement.bootstrap.001](/docs/planning/tasks/closed/archive/2026/03/16/transition_surface_retirement_bootstrap.md) | `done` | `high` | `repository_maintainer` | `trace.transition_surface_retirement` | Bootstraps the initial planning chain for Transition Surface Retirement. |
| [task.governed_filename_canonicalization.validation_and_closeout.003](/docs/planning/tasks/closed/archive/2026/03/16/validate_and_close_governed_filename_canonicalization.md) | `done` | `high` | `repository_maintainer` | `trace.governed_filename_canonicalization` | Refreshes derived surfaces, validates the versionless governed-filename migration, and closes the trace after the renamed repository state is clean. |
| [task.governed_filename_canonicalization.rename_and_repair.002](/docs/planning/tasks/closed/archive/2026/03/16/rename_governed_artifact_filenames_and_repair_consumers.md) | `done` | `high` | `repository_maintainer` | `trace.governed_filename_canonicalization` | Renames the governed `.v1` file set to versionless paths and updates runtime, tests, docs, registries, and planning references to the new canonical names. |
| [task.governed_filename_canonicalization.bootstrap.001](/docs/planning/tasks/closed/archive/2026/03/16/governed_filename_canonicalization_bootstrap.md) | `done` | `high` | `repository_maintainer` | `trace.governed_filename_canonicalization` | Bootstraps the initial planning chain for Versionless Governed Artifact Filenames. |
| [task.rendered_surface_contract_enforcement.validation_and_closeout.003](/docs/planning/tasks/closed/archive/2026/03/16/validate_and_close_rendered_surface_contract_enforcement.md) | `done` | `high` | `repository_maintainer` | `trace.rendered_surface_contract_enforcement` | Refreshes rendered and machine-readable surfaces, validates the rendered-surface initiative, and closes the trace after a clean confirmation pass. |
| [task.rendered_surface_contract_enforcement.rendered_registry_and_runtime_alignment.002](/docs/planning/tasks/closed/archive/2026/03/16/implement_governed_rendered_surfaces_and_retire_live_projection_boundaries.md) | `done` | `high` | `repository_maintainer` | `trace.rendered_surface_contract_enforcement` | Adds the rendered-surface contract, refactors rendered trackers onto it, and retires live projection terminology in active runtime and authority surfaces. |
| [task.rendered_surface_contract_enforcement.bootstrap.001](/docs/planning/tasks/closed/archive/2026/03/16/rendered_surface_contract_enforcement_bootstrap.md) | `done` | `high` | `repository_maintainer` | `trace.rendered_surface_contract_enforcement` | Bootstraps the initial planning chain for Rendered Surface Contract Enforcement. |

_Updated At: `2026-03-16T20:37:39Z`_
