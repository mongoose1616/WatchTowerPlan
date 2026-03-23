# Copy-Forward Pack Runtime Hardening Plan

## Initiative Identity
- `initiative_id`: `initiative.copy_forward_pack_runtime_hardening`
- `trace_id`: `trace.copy_forward_pack_runtime_hardening`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-23T01:24:34Z`

## Scope and Non-Goals
Hardens reusable core for copied-core host scenarios by discovering unbootstrapped hosted packs from manifests, structuring stale-registry failures, and keeping current shared workspace contracts explicit.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Bootstrap Copy-Forward Pack Runtime Hardening: Bootstrap Copy-Forward Pack Runtime Hardening live initiative package.
- Cover bootstrap-mode copy-forward behavior: Adds reusable-core regression coverage for copied-core repos with valid local packs, stale donor registry metadata, and incomplete local workspace rewiring.
- Harden selected pack commands: Makes pack list, describe, validate, and selected namespace resolution use the effective hosted-pack runtime view and return structured failures for stale authored registry entries.
- Implement effective pack discovery: Adds a runtime-only effective hosted-pack view that supplements valid authored registry entries with manifest-discovered bootstrap-mode packs.
- Refresh docs and close out the slice: Updates shared docs for bootstrap-mode copy-forward behavior, runs the validation gate, and closes the initiative with committed evidence.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.copy_forward_pack_runtime_hardening.bootstrap_copy_forward_pack_runtime_hardening](/plan/initiatives/copy_forward_pack_runtime_hardening/.wt/tasks/bootstrap_copy_forward_pack_runtime_hardening/task.json) | `completed` | `high` | `repository_maintainer` | Bootstrap Copy-Forward Pack Runtime Hardening live initiative package. | - |
| [task.copy_forward_pack_runtime_hardening.cover_copy_forward_bootstrap_mode](/plan/initiatives/copy_forward_pack_runtime_hardening/.wt/tasks/cover_bootstrap_mode_copy_forward_behavior/task.json) | `completed` | `high` | `validation_engineer` | Adds reusable-core regression coverage for copied-core repos with valid local packs, stale donor registry metadata, and incomplete local workspace rewiring. | task.copy_forward_pack_runtime_hardening.harden_selected_pack_commands |
| [task.copy_forward_pack_runtime_hardening.harden_selected_pack_commands](/plan/initiatives/copy_forward_pack_runtime_hardening/.wt/tasks/harden_selected_pack_commands/task.json) | `completed` | `high` | `implementation_engineer` | Makes pack list, describe, validate, and selected namespace resolution use the effective hosted-pack runtime view and return structured failures for stale authored registry entries. | task.copy_forward_pack_runtime_hardening.implement_effective_pack_discovery |
| [task.copy_forward_pack_runtime_hardening.implement_effective_pack_discovery](/plan/initiatives/copy_forward_pack_runtime_hardening/.wt/tasks/implement_effective_pack_discovery/task.json) | `completed` | `high` | `implementation_engineer` | Adds a runtime-only effective hosted-pack view that supplements valid authored registry entries with manifest-discovered bootstrap-mode packs. | - |
| [task.copy_forward_pack_runtime_hardening.refresh_docs_and_closeout](/plan/initiatives/copy_forward_pack_runtime_hardening/.wt/tasks/refresh_docs_and_close_out_the_slice/task.json) | `completed` | `medium` | `repository_maintainer` | Updates shared docs for bootstrap-mode copy-forward behavior, runs the validation gate, and closes the initiative with committed evidence. | task.copy_forward_pack_runtime_hardening.cover_copy_forward_bootstrap_mode |

## Dependencies and Risks
- Task `task.copy_forward_pack_runtime_hardening.cover_copy_forward_bootstrap_mode` depends on `task.copy_forward_pack_runtime_hardening.harden_selected_pack_commands`.
- Task `task.copy_forward_pack_runtime_hardening.harden_selected_pack_commands` depends on `task.copy_forward_pack_runtime_hardening.implement_effective_pack_discovery`.
- Task `task.copy_forward_pack_runtime_hardening.refresh_docs_and_closeout` depends on `task.copy_forward_pack_runtime_hardening.cover_copy_forward_bootstrap_mode`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/copy_forward_pack_runtime_hardening/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/copy_forward_pack_runtime_hardening/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/copy_forward_pack_runtime_hardening/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/copy_forward_pack_runtime_hardening/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/copy_forward_pack_runtime_hardening/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/copy_forward_pack_runtime_hardening/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/copy_forward_pack_runtime_hardening/summary.md)
