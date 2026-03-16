---
id: task.decision_supersession_and_regression_evidence_alignment.supersession.001
trace_id: trace.decision_supersession_and_regression_evidence_alignment
title: Add explicit decision supersession support
summary: Extend decision governance, sync, query, and live decision records so superseded
  decisions link explicitly to replacement decisions.
type: task
status: active
task_status: cancelled
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T03:30:46Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/governance/decision_capture_standard.md
- docs/standards/documentation/decision_record_md_standard.md
- docs/templates/decision_record_template.md
- docs/standards/data_contracts/decision_index_standard.md
- core/control_plane/schemas/artifacts/decision_index.v1.schema.json
- core/python/src/watchtower_core/control_plane/models/planning.py
- core/python/src/watchtower_core/repo_ops/sync/decision_index.py
- core/python/src/watchtower_core/repo_ops/query/decisions.py
- core/python/src/watchtower_core/cli/query_records_handlers.py
- docs/commands/core_python/watchtower_core_query_decisions.md
- docs/planning/decisions/preimplementation_machine_coordination_entrypoint.md
- docs/planning/decisions/machine_first_coordination_entry_surface.md
- docs/planning/decisions/planning_authority_unification_direction.md
related_ids:
- trace.decision_supersession_and_regression_evidence_alignment
---

# Add explicit decision supersession support

## Summary
Extend decision governance, sync, query, and live decision records so superseded decisions link explicitly to replacement decisions.

## Scope
- Update the decision record standard/template, decision index standard/schema/models/sync/query surfaces, and the affected live planning-authority decision records so supersession is explicit and machine-readable.

## Done When
- Decision supersession links are governed, indexed, queryable, covered by regression tests, and the currently affected live decisions are aligned.
