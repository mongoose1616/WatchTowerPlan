# WatchTower CTF Implementation Package Preservation Plan

## Initiative Identity
- `initiative_id`: `initiative.watchtower_ctf_implementation_package_preservation`
- `trace_id`: `trace.watchtower_ctf_implementation_package_preservation`
- `scope_type`: `project_scoped`
- `project_id`: `project.watchtower`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `in_progress`
- `review_status`: `approved`
- `updated_at`: `2026-03-28T10:08:34Z`

## Scope and Non-Goals
Captures the full CTF implementation package inside the governed WatchTower initiative so WatchTower implementation no longer depends on /home/j/mvp_reference/CTF_implementation.
- Scope type: `project_scoped`.
- Non-goal: Do not mutate `/home/j/WatchTower` during this preservation initiative.
- Non-goal: Do not alter repo-wide readiness rules, artifact validation behavior, or validator selection.
- Non-goal: Do not replace the transformed mirror with a reauthored summary; the source snapshot remains the frozen provenance layer.
- Locked post-v1 deferral: `decision.workflow_catalog`: defer a richer workflow catalog beyond routing-table plus workflow-metadata baseline.
- Locked post-v1 deferral: `decision.actor_bootstrap_day_one`: reuse shared `actor_registry` and defer actor bootstrap unless needed immediately.
- Locked post-v1 deferral: `decision.public_rebuild_cli`: keep public operator guidance centered on `sync`.
- Locked post-v1 deferral: `decision.pentest_pack_split`: keep one `offensive_security` hosted pack for v1.
- Locked post-v1 deferral: `decision.saved_query_views`: defer saved query views beyond v1, with pack-owned defaults first and user-local views outside the governed pack root later.
- Locked post-v1 deferral: `decision.provenance_review_impact_surface`: defer richer provenance-triggered downstream review tooling beyond v1.

## Objectives
- Phase 0 Shared Contract Adoption And Alignment: Revalidate the live baseline, donor and recipient split, and current-compatible identity before target-repo mutation.
- Phase 1 Recipient Scaffold And Bootstrap: Export shared core, scaffold the offsec pack, bootstrap it in the recipient repo, and replace starter workflow metadata.
- Phase 2 Pack Machine Contract: Author the offsec schemas, registries, policies, validation suite, and human-surface starter contract.
- Phase 3 Runtime Query Sync And Workflow Seam: Implement the pack runtime seam, query and sync surfaces, workflow docs, and rendered visibility outputs.
- Phase 4 Challenge Artifacts And Closeout: Implement challenge-local artifacts, evidence capture, discrepancy handling, and closeout behavior.
- Phase 5 Knowledge Promotion And Retrieval: Implement reusable knowledge families, promotion policy, relation governance, and deterministic retrieval.
- Phase 6 Environment Adapters And Safety: Implement environment adapters, transfer governance, confirmation rules, and safety-enforcement policy.
- Phase 7 Release And Portability Proof: Prove staged export, bootstrap, validation, and release portability for the finished offsec pack.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary |
| --- | --- | --- | --- | --- |
| [task.watchtower_ctf_implementation_package_preservation.phase_0_shared_contract_adoption_and_alignment](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/phase_0_shared_contract_adoption_and_alignment/task.json) | `completed` | `high` | `repository_maintainer` | Revalidate the live baseline, donor and recipient split, and current-compatible identity before target-repo mutation. |
| [task.watchtower_ctf_implementation_package_preservation.phase_1_recipient_scaffold_and_bootstrap](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/phase_1_recipient_scaffold_and_bootstrap/task.json) | `completed` | `high` | `repository_maintainer` | Export shared core, scaffold the offsec pack, bootstrap it in the recipient repo, and replace starter workflow metadata. |
| [task.watchtower_ctf_implementation_package_preservation.phase_2_pack_machine_contract](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/phase_2_pack_machine_contract/task.json) | `completed` | `high` | `repository_maintainer` | Author the offsec schemas, registries, policies, validation suite, and human-surface starter contract. |
| [task.watchtower_ctf_implementation_package_preservation.phase_3_runtime_query_sync_and_workflow_seam](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/phase_3_runtime_query_sync_and_workflow_seam/task.json) | `completed` | `high` | `repository_maintainer` | Implement the pack runtime seam, query and sync surfaces, workflow docs, and rendered visibility outputs. |
| [task.watchtower_ctf_implementation_package_preservation.phase_4_challenge_artifacts_and_closeout](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/phase_4_challenge_artifacts_and_closeout/task.json) | `completed` | `high` | `repository_maintainer` | Implement challenge-local artifacts, evidence capture, discrepancy handling, and closeout behavior. |
| [task.watchtower_ctf_implementation_package_preservation.phase_5_knowledge_promotion_and_retrieval](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/phase_5_knowledge_promotion_and_retrieval/task.json) | `completed` | `high` | `repository_maintainer` | Implement reusable knowledge families, promotion policy, relation governance, and deterministic retrieval. |
| [task.watchtower_ctf_implementation_package_preservation.phase_6_environment_adapters_and_safety](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/phase_6_environment_adapters_and_safety/task.json) | `completed` | `high` | `repository_maintainer` | Implement environment adapters, transfer governance, confirmation rules, and safety-enforcement policy. |
| [task.watchtower_ctf_implementation_package_preservation.phase_7_release_and_portability_proof](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/phase_7_release_and_portability_proof/task.json) | `completed` | `high` | `repository_maintainer` | Prove staged export, bootstrap, validation, and release portability for the finished offsec pack. |
| [task.watchtower_ctf_implementation_package_preservation.bootstrap_watchtower_ctf_implementation_package_preservation](/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation/.wt/tasks/bootstrap_watchtower_ctf_implementation_package_preservation/task.json) | `cancelled` | `high` | `repository_maintainer` | Bootstrap placeholder retired after the phase-aligned execution chain replaced it. |

## Dependencies and Risks
- No current blockers, dependencies, or open discrepancy risks are recorded.

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
