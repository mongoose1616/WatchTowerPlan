# Root Pack Schema Catalog Contract Alignment Plan

## Initiative Identity
- `initiative_id`: `initiative.root_pack_schema_catalog_contract_alignment`
- `trace_id`: `trace.root_pack_schema_catalog_contract_alignment`
- `scope_type`: `pack_wide`
- `owner`: `repository_maintainer`
- `lifecycle_stage`: `completed`
- `review_status`: `approved`
- `updated_at`: `2026-03-22T23:08:32Z`

## Scope and Non-Goals
Extends the reusable-core schema catalog canonical-path contract to support first-party root pack machine roots such as <pack>/.wt without donor-specific exceptions.
- Scope type: `pack_wide`.
- No explicit non-goals or deferred scope items are recorded.

## Objectives
- Bootstrap Root Pack Schema Catalog Contract Alignment: Bootstrap Root Pack Schema Catalog Contract Alignment live initiative package.
- Validate And Close Root-Pack Schema Contract Slice: Runs the validation gate for the schema-catalog contract update and closes the initiative cleanly.
- Widen Root-Pack Schema Catalog Contract: Updates reusable-core schema catalog validation so first-party root packs can publish canonical schema paths under <pack>/.wt/schemas/.

## Planned Slices or Workstreams
| Task | Status | Priority | Owner | Summary | Depends On |
| --- | --- | --- | --- | --- | --- |
| [task.root_pack_schema_catalog_contract_alignment.bootstrap_root_pack_schema_catalog_contract_alignment](/plan/initiatives/root_pack_schema_catalog_contract_alignment/.wt/tasks/bootstrap_root_pack_schema_catalog_contract_alignment/task.json) | `completed` | `high` | `repository_maintainer` | Bootstrap Root Pack Schema Catalog Contract Alignment live initiative package. | - |
| [task.root_pack_schema_catalog_contract_alignment.validate_and_close](/plan/initiatives/root_pack_schema_catalog_contract_alignment/.wt/tasks/validate_and_close_root_pack_schema_contract_slice/task.json) | `completed` | `high` | `repository_maintainer` | Runs the validation gate for the schema-catalog contract update and closes the initiative cleanly. | task.root_pack_schema_catalog_contract_alignment.widen_root_pack_schema_catalog_contract |
| [task.root_pack_schema_catalog_contract_alignment.widen_root_pack_schema_catalog_contract](/plan/initiatives/root_pack_schema_catalog_contract_alignment/.wt/tasks/widen_root_pack_schema_catalog_contract/task.json) | `completed` | `high` | `repository_maintainer` | Updates reusable-core schema catalog validation so first-party root packs can publish canonical schema paths under <pack>/.wt/schemas/. | - |

## Dependencies and Risks
- Discrepancy `discrepancy.root_pack_schema_catalog_contract_alignment.decision_notes_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/root_pack_schema_catalog_contract_alignment/decision_notes.md; machine confirmation is required.
- Discrepancy `discrepancy.root_pack_schema_catalog_contract_alignment.design_record_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/root_pack_schema_catalog_contract_alignment/design_record.md; machine confirmation is required.
- Discrepancy `discrepancy.root_pack_schema_catalog_contract_alignment.implementation_slice_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/root_pack_schema_catalog_contract_alignment/implementation_slice.md; machine confirmation is required.
- Discrepancy `discrepancy.root_pack_schema_catalog_contract_alignment.initiative_brief_drift`: `high` `authored_input_drift` / `resolved`. Authored input drift detected for plan/initiatives/root_pack_schema_catalog_contract_alignment/initiative_brief.md; machine confirmation is required.
- Discrepancy `discrepancy.root_pack_schema_catalog_contract_alignment.review_index_index_drift`: `high` `stale_aggregate_index` / `resolved`. Aggregate index drift detected for plan/.wt/indexes/review_index.json.
- Task `task.root_pack_schema_catalog_contract_alignment.validate_and_close` depends on `task.root_pack_schema_catalog_contract_alignment.widen_root_pack_schema_catalog_contract`.

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
- Authored input: [initiative_brief.md](/plan/initiatives/root_pack_schema_catalog_contract_alignment/initiative_brief.md)
- Authored input: [design_record.md](/plan/initiatives/root_pack_schema_catalog_contract_alignment/design_record.md)
- Authored input: [implementation_slice.md](/plan/initiatives/root_pack_schema_catalog_contract_alignment/implementation_slice.md)
- Authored input: [decision_notes.md](/plan/initiatives/root_pack_schema_catalog_contract_alignment/decision_notes.md)
- Rendered plan: [plan.md](/plan/initiatives/root_pack_schema_catalog_contract_alignment/plan.md)
- Rendered progress: [progress.md](/plan/initiatives/root_pack_schema_catalog_contract_alignment/progress.md)
- Rendered summary: [summary.md](/plan/initiatives/root_pack_schema_catalog_contract_alignment/summary.md)
