---
id: task.planning_semantics_and_decision_contract_alignment.decision_contract_alignment.001
trace_id: trace.planning_semantics_and_decision_contract_alignment
title: Align planning authoring contracts with live enforcement
summary: Update the decision-record, feature-design, and implementation-plan
  standards, templates, and regression coverage so authoring guidance matches the
  live required applied-reference sections.
type: task
status: active
task_status: done
task_kind: documentation
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T20:49:38Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/documentation/decision_record_md_standard.md
- docs/standards/documentation/feature_design_md_standard.md
- docs/standards/documentation/implementation_plan_md_standard.md
- docs/templates/decision_record_template.md
- docs/templates/feature_design_template.md
- docs/templates/implementation_plan_template.md
- core/python/src/watchtower_core/repo_ops/planning_documents.py
- core/python/tests/integration/test_control_plane_artifacts.py
related_ids:
- prd.planning_semantics_and_decision_contract_alignment
- design.features.planning_semantics_and_decision_contract_alignment
- design.implementation.planning_semantics_and_decision_contract_alignment
- decision.planning_semantics_and_decision_contract_alignment_direction
- contract.acceptance.planning_semantics_and_decision_contract_alignment
---

# Align planning authoring contracts with live enforcement

## Summary
Update the decision-record, feature-design, and implementation-plan standards,
templates, and regression coverage so authoring guidance matches the live
required applied-reference sections.

## Scope
- Make the live applied-reference sections required in the decision-record,
  feature-design, and implementation-plan standards and templates.
- Add regression checks that fail if those planning authoring contracts drift
  back to optional treatment for the governed sections.

## Done When
- Planning authoring guidance no longer claims the governed applied-reference
  sections are optional.
- Regression coverage protects the required planning authoring contracts.
- Companion planning surfaces are refreshed.
