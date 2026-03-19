# Plan Extraction Output Envelope Alignment Plan

## Initiative Identity
- `initiative_id`: `initiative.plan_extraction_output_envelope_alignment`
- `trace_id`: `trace.plan_extraction_output_envelope_alignment`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-18T02:20:00Z`

## Scope and Non-Goals
Adds a typed extraction-output envelope helper and aligns guidance promotion with an explicit extraction stage instead of schema-only coverage.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Add typed extraction output envelope helper: Publish reusable typed models and helper methods for the pack-facing extraction output envelope contract.
- Validate extraction output alignment: Add focused tests and requirements reconciliation proving the extraction envelope now aligns with promotion flows.
- Wire guidance promotion through extraction stage: Refactor guidance promotion so extraction is an explicit validated stage before durable promotion output is written.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.plan_extraction_output_envelope_alignment.add_typed_extraction_output_helper](/plan/initiatives/plan_extraction_output_envelope_alignment/.wt/tasks/add_typed_extraction_output_helper/task.json) | `completed` | `high` | `repository_maintainer` | Publish reusable typed models and helper methods for the pack-facing extraction output envelope contract. | - |
| [task.plan_extraction_output_envelope_alignment.validate_extraction_output_alignment](/plan/initiatives/plan_extraction_output_envelope_alignment/.wt/tasks/validate_extraction_output_alignment/task.json) | `completed` | `high` | `repository_maintainer` | Add focused tests and requirements reconciliation proving the extraction envelope now aligns with promotion flows. | task.plan_extraction_output_envelope_alignment.wire_guidance_promotion_through_extraction_stage |
| [task.plan_extraction_output_envelope_alignment.wire_guidance_promotion_through_extraction_stage](/plan/initiatives/plan_extraction_output_envelope_alignment/.wt/tasks/wire_guidance_promotion_through_extraction_stage/task.json) | `completed` | `high` | `repository_maintainer` | Refactor guidance promotion so extraction is an explicit validated stage before durable promotion output is written. | task.plan_extraction_output_envelope_alignment.add_typed_extraction_output_helper |

## Dependencies and Risks
- Task `task.plan_extraction_output_envelope_alignment.validate_extraction_output_alignment` depends on `task.plan_extraction_output_envelope_alignment.wire_guidance_promotion_through_extraction_stage`.
- Task `task.plan_extraction_output_envelope_alignment.wire_guidance_promotion_through_extraction_stage` depends on `task.plan_extraction_output_envelope_alignment.add_typed_extraction_output_helper`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/plan_extraction_output_envelope_alignment/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/plan_extraction_output_envelope_alignment/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/plan_extraction_output_envelope_alignment/implementation_slice.md)
- Rendered plan: [plan.md](/plan/initiatives/plan_extraction_output_envelope_alignment/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/plan_extraction_output_envelope_alignment/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/plan_extraction_output_envelope_alignment/summary.md)
