# Requirements And Decisions Adherence Remediation Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_requirements_decisions_adherence_remediation`
- `trace_id`: `trace.plan_requirements_decisions_adherence_remediation`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-19T18:39:56Z`

## Scope and Non-Goals
Retire the root docs tree, finish the initiative-package hard cutover, and restore rich machine-backed documentation surfaces.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Bootstrap Requirements And Decisions Adherence Remediation: Bootstrap Requirements And Decisions Adherence Remediation live initiative package.
- Enforce the six-section plan overview contract: Make the six-section plan overview template authoritative across template catalog, registry, renderer, tests, and live output.
- Hard-cut planning terminology and phase vocabulary: Replace retired planning-model language and stale initiative phase names on active surfaces with the initiative-package model.
- Harden residue and domain_packs regression guards: Add explicit tests and validation gates that block reintroduction of root docs, domain_packs, and retired planning-model residue.
- Move plan-domain governance and standards into plan/docs: Move plan-domain governance and plan-runtime standards under plan/docs and remove the root docs authority.
- Re-root command, reference, template, and core standard docs: Move shared command pages, references, templates, and core-owned standards from root docs into core/docs and update their governed roots.
- Replace retired planning-document semantics: Remove the remaining pre-cutover planning-document semantic helpers and validate only the live initiative-package authored inputs.
- Restore rich human-facing rendering and navigation: Recover the stronger markdown structure, browseable tables, and summary-plus-detail navigation while keeping machine indexes compact.
- Run full assessment pass one: Run the first full repository assessment after the main cutover slices land and convert any new gaps into tracked remediation work.
- Run full assessment pass two: Run the final repository assessment after cleanup and guards are in place and close any remaining gaps before initiative closeout.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary |
| --- | --- | --- | --- | --- |
| [task.plan_requirements_decisions_adherence_remediation.enforce_plan_overview_contract](/plan/initiatives/plan_requirements_decisions_adherence_remediation/.wt/tasks/enforce_the_six_section_plan_overview_contract/task.json) | `completed` | `critical` | `repository_maintainer` | Make the six-section plan overview template authoritative across template catalog, registry, renderer, tests, and live output. |
| [task.plan_requirements_decisions_adherence_remediation.hard_rename_planning_terms](/plan/initiatives/plan_requirements_decisions_adherence_remediation/.wt/tasks/hard_cut_planning_terminology_and_phase_vocabulary/task.json) | `completed` | `critical` | `repository_maintainer` | Replace retired planning-model language and stale initiative phase names on active surfaces with the initiative-package model. |
| [task.plan_requirements_decisions_adherence_remediation.re_root_core_docs](/plan/initiatives/plan_requirements_decisions_adherence_remediation/.wt/tasks/re_root_command_reference_template_and_core_standard_docs/task.json) | `completed` | `critical` | `repository_maintainer` | Move shared command pages, references, templates, and core-owned standards from root docs into core/docs and update their governed roots. |
| [task.plan_requirements_decisions_adherence_remediation.re_root_plan_docs](/plan/initiatives/plan_requirements_decisions_adherence_remediation/.wt/tasks/move_plan_domain_governance_and_standards_into_plan_docs/task.json) | `completed` | `critical` | `repository_maintainer` | Move plan-domain governance and plan-runtime standards under plan/docs and remove the root docs authority. |
| [task.plan_requirements_decisions_adherence_remediation.bootstrap](/plan/initiatives/plan_requirements_decisions_adherence_remediation/.wt/tasks/bootstrap_requirements_and_decisions_adherence_remediation/task.json) | `completed` | `high` | `repository_maintainer` | Bootstrap Requirements And Decisions Adherence Remediation live initiative package. |
| [task.plan_requirements_decisions_adherence_remediation.harden_residue_guards](/plan/initiatives/plan_requirements_decisions_adherence_remediation/.wt/tasks/harden_residue_and_domain_packs_regression_guards/task.json) | `completed` | `high` | `repository_maintainer` | Add explicit tests and validation gates that block reintroduction of root docs, domain_packs, and retired planning-model residue. |
| [task.plan_requirements_decisions_adherence_remediation.replace_planning_semantics](/plan/initiatives/plan_requirements_decisions_adherence_remediation/.wt/tasks/replace_retired_planning_document_semantics/task.json) | `completed` | `high` | `repository_maintainer` | Remove the remaining pre-cutover planning-document semantic helpers and validate only the live initiative-package authored inputs. |
| [task.plan_requirements_decisions_adherence_remediation.restore_rich_rendering](/plan/initiatives/plan_requirements_decisions_adherence_remediation/.wt/tasks/restore_rich_human_facing_rendering_and_navigation/task.json) | `completed` | `high` | `repository_maintainer` | Recover the stronger markdown structure, browseable tables, and summary-plus-detail navigation while keeping machine indexes compact. |
| [task.plan_requirements_decisions_adherence_remediation.run_assessment_pass_one](/plan/initiatives/plan_requirements_decisions_adherence_remediation/.wt/tasks/run_full_assessment_pass_one/task.json) | `completed` | `medium` | `repository_maintainer` | Run the first full repository assessment after the main cutover slices land and convert any new gaps into tracked remediation work. |
| [task.plan_requirements_decisions_adherence_remediation.run_assessment_pass_two](/plan/initiatives/plan_requirements_decisions_adherence_remediation/.wt/tasks/run_full_assessment_pass_two/task.json) | `completed` | `medium` | `repository_maintainer` | Run the final repository assessment after cleanup and guards are in place and close any remaining gaps before initiative closeout. |

## Dependencies and Risks
- No current blockers, dependencies, or open discrepancy risks are recorded.

## Validation or Completion Gates
- `capture_complete`: `True`
- `machine_valid`: `True`
- `approval_status`: `approved`
- `ready_for_execution`: `False`
- `blocking_reasons`: `none`
- Task count: `10`
- Evidence bundle count: `1`
- Closeout shell count: `1`
- Promotion shell count: `1`
- Acceptance contract refs: `0`

## Linked Outputs
- Authored input: [initiative_brief.md](/plan/initiatives/plan_requirements_decisions_adherence_remediation/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_requirements_decisions_adherence_remediation/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_requirements_decisions_adherence_remediation/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_requirements_decisions_adherence_remediation/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_requirements_decisions_adherence_remediation/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_requirements_decisions_adherence_remediation/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_requirements_decisions_adherence_remediation/summary.md)
