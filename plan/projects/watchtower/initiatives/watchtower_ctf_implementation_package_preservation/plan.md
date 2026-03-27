# WatchTower CTF Implementation Package Preservation Plan

## Initiative Identity
- `initiative_id`: `initiative.watchtower_ctf_implementation_package_preservation`
- `trace_id`: `trace.watchtower_ctf_implementation_package_preservation`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `ready_for_execution`
- `review_status`: `approved`
- `updated_at`: `2026-03-27T22:21:04Z`

## Scope and Non-Goals
Captures the full CTF implementation package inside the governed WatchTower initiative so WatchTower implementation no longer depends on /home/j/mvp_reference/CTF_implementation.
- Scope type: `project_scoped`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Bootstrap WatchTower CTF Implementation Package Preservation: Bootstrap placeholder retired after the phase-aligned execution chain replaced it.
- Phase 0 Shared Contract Adoption And Alignment: Revalidate the live baseline, donor and recipient split, and current-compatible identity before target-repo mutation.
- Phase 1 Recipient Scaffold And Bootstrap: Export shared core, scaffold the offsec pack, bootstrap it in the recipient repo, and replace starter workflow metadata.
- Phase 2 Pack Machine Contract: Author the offsec schemas, registries, policies, validation suite, and human-surface starter contract.
- Phase 3 Runtime Query Sync And Workflow Seam: Implement the pack runtime seam, query and sync surfaces, workflow docs, and rendered visibility outputs.
- Phase 4 Challenge Artifacts And Closeout: Implement challenge-local artifacts, evidence capture, discrepancy handling, and closeout behavior.
- Phase 5 Knowledge Promotion And Retrieval: Implement reusable knowledge families, promotion policy, relation governance, and deterministic retrieval.
- Phase 6 Environment Adapters And Safety: Implement environment adapters, transfer governance, confirmation rules, and safety-enforcement policy.
- Phase 7 Release And Portability Proof: Prove staged export, bootstrap, validation, and release portability for the finished offsec pack.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.watchtower_ctf_implementation_package_preservation.phase_0_shared_contract_adoption_and_alignment](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/phase_0_shared_contract_adoption_and_alignment/task.json) | `ready` | `high` | `repository_maintainer` | Revalidate the live baseline, donor and recipient split, and current-compatible identity before target-repo mutation. | - |
| [task.watchtower_ctf_implementation_package_preservation.phase_1_recipient_scaffold_and_bootstrap](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/phase_1_recipient_scaffold_and_bootstrap/task.json) | `planned` | `high` | `repository_maintainer` | Export shared core, scaffold the offsec pack, bootstrap it in the recipient repo, and replace starter workflow metadata. | task.watchtower_ctf_implementation_package_preservation.phase_0_shared_contract_adoption_and_alignment |
| [task.watchtower_ctf_implementation_package_preservation.phase_2_pack_machine_contract](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/phase_2_pack_machine_contract/task.json) | `planned` | `high` | `repository_maintainer` | Author the offsec schemas, registries, policies, validation suite, and human-surface starter contract. | task.watchtower_ctf_implementation_package_preservation.phase_1_recipient_scaffold_and_bootstrap |
| [task.watchtower_ctf_implementation_package_preservation.phase_3_runtime_query_sync_and_workflow_seam](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/phase_3_runtime_query_sync_and_workflow_seam/task.json) | `planned` | `high` | `repository_maintainer` | Implement the pack runtime seam, query and sync surfaces, workflow docs, and rendered visibility outputs. | task.watchtower_ctf_implementation_package_preservation.phase_2_pack_machine_contract |
| [task.watchtower_ctf_implementation_package_preservation.phase_4_challenge_artifacts_and_closeout](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/phase_4_challenge_artifacts_and_closeout/task.json) | `planned` | `high` | `repository_maintainer` | Implement challenge-local artifacts, evidence capture, discrepancy handling, and closeout behavior. | task.watchtower_ctf_implementation_package_preservation.phase_3_runtime_query_sync_and_workflow_seam |
| [task.watchtower_ctf_implementation_package_preservation.phase_5_knowledge_promotion_and_retrieval](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/phase_5_knowledge_promotion_and_retrieval/task.json) | `planned` | `high` | `repository_maintainer` | Implement reusable knowledge families, promotion policy, relation governance, and deterministic retrieval. | task.watchtower_ctf_implementation_package_preservation.phase_4_challenge_artifacts_and_closeout |
| [task.watchtower_ctf_implementation_package_preservation.phase_6_environment_adapters_and_safety](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/phase_6_environment_adapters_and_safety/task.json) | `planned` | `high` | `repository_maintainer` | Implement environment adapters, transfer governance, confirmation rules, and safety-enforcement policy. | task.watchtower_ctf_implementation_package_preservation.phase_5_knowledge_promotion_and_retrieval |
| [task.watchtower_ctf_implementation_package_preservation.phase_7_release_and_portability_proof](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/phase_7_release_and_portability_proof/task.json) | `planned` | `high` | `repository_maintainer` | Prove staged export, bootstrap, validation, and release portability for the finished offsec pack. | task.watchtower_ctf_implementation_package_preservation.phase_6_environment_adapters_and_safety |
| [task.watchtower_ctf_implementation_package_preservation.bootstrap_watchtower_ctf_implementation_package_preservation](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/bootstrap_watchtower_ctf_implementation_package_preservation/task.json) | `cancelled` | `high` | `repository_maintainer` | Bootstrap placeholder retired after the phase-aligned execution chain replaced it. | - |

## Dependencies and Risks
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.artifact_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/artifact_index.json.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.artifact_index_project_drift`: `high` `stale_aggregate_index` / `resolved`. Project aggregate index drift detected for plan/.wt/indexes/artifact_index.json.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.closeout_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/closeout_index.json.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.coordination_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/coordination_index.json.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.decision_notes_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/decision_notes.md; machine confirmation is required.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.design_record_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/design_record.md; machine confirmation is required.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.discrepancy_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/discrepancy_index.json.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.evidence_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/evidence_index.json.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.guidance_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/guidance_index.json.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.implementation_slice_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/implementation_slice.md; machine confirmation is required.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.initiative_brief_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/initiative_brief.md; machine confirmation is required.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.initiative_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/initiative_index.json.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.plan_overview_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/plan_overview.md.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.plan_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/plan.md.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.progress_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/progress.md.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.project_index_project_drift`: `high` `stale_aggregate_index` / `resolved`. Project aggregate index drift detected for plan/.wt/indexes/project_index.json.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.project_project_drift`: `high` `stale_rendered_surface` / `resolved`. Project rendered surface drift detected for plan/projects/watchtower/project.md.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.promotion_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/promotion_index.json.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.readiness_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/readiness_index.json.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.review_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/review_index.json.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.summary_project_drift`: `high` `stale_rendered_surface` / `resolved`. Project rendered surface drift detected for plan/projects/watchtower/summary.md.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.summary_surface_drift`: `high` `stale_rendered_surface` / `resolved`. Rendered surface drift detected for plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/summary.md.
- Discrepancy `discrepancy.watchtower.watchtower_ctf_implementation_package_preservation.task_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/task_index.json.
- Task `task.watchtower_ctf_implementation_package_preservation.phase_1_recipient_scaffold_and_bootstrap` depends on `task.watchtower_ctf_implementation_package_preservation.phase_0_shared_contract_adoption_and_alignment`.
- Task `task.watchtower_ctf_implementation_package_preservation.phase_2_pack_machine_contract` depends on `task.watchtower_ctf_implementation_package_preservation.phase_1_recipient_scaffold_and_bootstrap`.
- Task `task.watchtower_ctf_implementation_package_preservation.phase_3_runtime_query_sync_and_workflow_seam` depends on `task.watchtower_ctf_implementation_package_preservation.phase_2_pack_machine_contract`.
- Task `task.watchtower_ctf_implementation_package_preservation.phase_4_challenge_artifacts_and_closeout` depends on `task.watchtower_ctf_implementation_package_preservation.phase_3_runtime_query_sync_and_workflow_seam`.
- Task `task.watchtower_ctf_implementation_package_preservation.phase_5_knowledge_promotion_and_retrieval` depends on `task.watchtower_ctf_implementation_package_preservation.phase_4_challenge_artifacts_and_closeout`.
- Task `task.watchtower_ctf_implementation_package_preservation.phase_6_environment_adapters_and_safety` depends on `task.watchtower_ctf_implementation_package_preservation.phase_5_knowledge_promotion_and_retrieval`.
- Task `task.watchtower_ctf_implementation_package_preservation.phase_7_release_and_portability_proof` depends on `task.watchtower_ctf_implementation_package_preservation.phase_6_environment_adapters_and_safety`.

## Validation or Completion Gates
- `capture_complete`: `True`
- `machine_valid`: `True`
- `approval_status`: `approved`
- `ready_for_execution`: `True`
- `blocking_reasons`: `none`
- Task count: `9`
- Evidence bundle count: `1`
- Closeout shell count: `1`
- Promotion shell count: `1`
- Acceptance contract refs: `1`

## Linked Outputs
- Authored input: [initiative_brief.md](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/initiative_brief.md)
- Authored input: [design_record.md](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/design_record.md)
- Authored input: [implementation_slice.md](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/decision_notes.md)
- Rendered plan: [plan.md](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/plan.md)
- Rendered progress: [progress.md](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/progress.md)
- Rendered summary: [summary.md](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/summary.md)
- Project surface: [project.md](/plan/projects/watchtower/project.md)
- Project repositories: [repositories.md](/plan/projects/watchtower/repositories.md)
- Project summary: [summary.md](/plan/projects/watchtower/summary.md)
