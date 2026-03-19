# Plan Duplicated Foundations Corpus Bootstrap Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_duplicated_foundations_corpus_bootstrap`
- `trace_id`: `trace.plan_duplicated_foundations_corpus_bootstrap`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-17T19:21:00Z`

## Scope and Non-Goals
Duplicates the current foundations corpus into core/docs/foundations and plan/docs/foundations so both roots carry the same guiding context required by requirements.md.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Copy foundations corpus into both roots: Duplicate the current foundations documents into both the core and plan docs roots without changing their shared guidance content.
- Seed duplicated foundations roots: Prepare the core/docs/foundations and plan/docs/foundations roots and align their README surfaces.
- Validate duplicated foundations discovery: Refresh derived indexes and confirm the duplicated foundations roots are discoverable without breaking current guidance lookup.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_duplicated_foundations_corpus_bootstrap.copy_foundations_corpus_into_both_roots](/plan/initiatives/plan_duplicated_foundations_corpus_bootstrap/.wt/tasks/copy_foundations_corpus_into_both_roots/task.json) | `completed` | `high` | `repository_maintainer` | Duplicate the current foundations documents into both the core and plan docs roots without changing their shared guidance content. | task.plan_duplicated_foundations_corpus_bootstrap.seed_duplicated_foundations_roots |
| [task.plan_duplicated_foundations_corpus_bootstrap.seed_duplicated_foundations_roots](/plan/initiatives/plan_duplicated_foundations_corpus_bootstrap/.wt/tasks/seed_duplicated_foundations_roots/task.json) | `completed` | `high` | `repository_maintainer` | Prepare the core/docs/foundations and plan/docs/foundations roots and align their README surfaces. | - |
| [task.plan_duplicated_foundations_corpus_bootstrap.validate_duplicated_foundations_discovery](/plan/initiatives/plan_duplicated_foundations_corpus_bootstrap/.wt/tasks/validate_duplicated_foundations_discovery/task.json) | `completed` | `high` | `repository_maintainer` | Refresh derived indexes and confirm the duplicated foundations roots are discoverable without breaking current guidance lookup. | task.plan_duplicated_foundations_corpus_bootstrap.seed_duplicated_foundations_roots, task.plan_duplicated_foundations_corpus_bootstrap.copy_foundations_corpus_into_both_roots |

## Dependencies and Risks
- Task `task.plan_duplicated_foundations_corpus_bootstrap.copy_foundations_corpus_into_both_roots` depends on `task.plan_duplicated_foundations_corpus_bootstrap.seed_duplicated_foundations_roots`.
- Task `task.plan_duplicated_foundations_corpus_bootstrap.validate_duplicated_foundations_discovery` depends on `task.plan_duplicated_foundations_corpus_bootstrap.seed_duplicated_foundations_roots`, `task.plan_duplicated_foundations_corpus_bootstrap.copy_foundations_corpus_into_both_roots`.

## Validation or Completion Gates
- `capture_complete`: `True`
- `machine_valid`: `True`
- `approval_status`: `approved`
- `ready_for_execution`: `False`
- `blocking_reasons`: `none`
- Task count: `3`
- Evidence bundle count: `1`
- Closeout shell count: `1`
- Promotion shell count: `1`
- Acceptance contract refs: `0`

## Linked Outputs
- Authored input: [initiative_brief.md](/plan/initiatives/plan_duplicated_foundations_corpus_bootstrap/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_duplicated_foundations_corpus_bootstrap/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_duplicated_foundations_corpus_bootstrap/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/plan_duplicated_foundations_corpus_bootstrap/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_duplicated_foundations_corpus_bootstrap/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_duplicated_foundations_corpus_bootstrap/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_duplicated_foundations_corpus_bootstrap/summary.md)
