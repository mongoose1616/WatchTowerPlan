---
id: task.planning_semantics_and_decision_contract_alignment.shared_heading_semantics.001
trace_id: trace.planning_semantics_and_decision_contract_alignment
title: Enforce shared heading-separation semantics across governed docs
summary: Centralize the heading-after-list blank-line rule and apply it across
  governed planning, workflow, and companion sync parsing paths.
type: task
status: active
task_status: done
task_kind: bug
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T20:49:38Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/documentation/documentation_semantics_standard.md
- core/python/src/watchtower_core/repo_ops/markdown_semantics.py
- core/python/src/watchtower_core/repo_ops/planning_documents.py
- core/python/src/watchtower_core/repo_ops/validation/document_semantics.py
- core/python/src/watchtower_core/repo_ops/sync/decision_index.py
- core/python/src/watchtower_core/repo_ops/sync/foundation_index.py
- core/python/src/watchtower_core/repo_ops/sync/reference_index.py
- core/python/src/watchtower_core/repo_ops/sync/standard_index.py
- core/python/src/watchtower_core/repo_ops/sync/workflow_index.py
- core/python/tests/unit/test_decision_index_sync.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/unit/test_workflow_index_sync.py
related_ids:
- prd.planning_semantics_and_decision_contract_alignment
- design.features.planning_semantics_and_decision_contract_alignment
- design.implementation.planning_semantics_and_decision_contract_alignment
- decision.planning_semantics_and_decision_contract_alignment_direction
- contract.acceptance.planning_semantics_and_decision_contract_alignment
---

# Enforce shared heading-separation semantics across governed docs

## Summary
Centralize the heading-after-list blank-line rule and apply it across governed
planning, workflow, and companion sync parsing paths.

## Scope
- Introduce one shared helper for the published heading-separation semantics
  rule.
- Wire the helper through governed planning loaders, workflow parsing, and the
  sync builders that parse authored Markdown directly.
- Add focused regressions for planning-document and workflow failures.

## Done When
- Invalid heading-after-list Markdown fails consistently across the affected
  governed document and workflow paths.
- Validation and sync coverage protect the shared helper behavior.
- Companion planning and acceptance surfaces are refreshed.
