---
id: task.internal_project_code_review_followup.bootstrap_decision_scaffold_hardening.001
trace_id: trace.internal_project_code_review_followup
title: Harden bootstrap decision scaffold output
summary: Make plan bootstrap and scaffolded decision records publish the governed
  applied-reference section by default and enforce that same rule in repo semantic
  validation.
type: task
status: active
task_status: done
task_kind: bug
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T17:13:25Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/planning_scaffold_support.py
- core/python/src/watchtower_core/repo_ops/planning_documents.py
- core/python/src/watchtower_core/repo_ops/validation/document_semantics.py
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/unit/test_planning_scaffolds.py
- core/python/tests/integration/test_control_plane_artifacts.py
related_ids:
- prd.internal_project_code_review_followup
- decision.internal_project_code_review_followup_direction
- design.features.internal_project_code_review_followup
- design.implementation.internal_project_code_review_followup
---

# Harden bootstrap decision scaffold output

## Summary
Make plan bootstrap and scaffolded decision records publish the governed applied-reference section by default and enforce that same rule in repo semantic validation.

## Scope
- Add the missing Applied References and Implications decision section to generated planning scaffolds.
- Validate scaffolded decision docs against the governed section expectations before writing.
- Align document-semantics validation so `validate all` rejects the same missing or unexplained decision section.

## Done When
- Scaffolded decision docs include the governed applied-reference section with explained bullets.
- Targeted decision-semantic validation and `validate all` both fail when the section is missing or unexplained.
- Bootstrap and decision scaffold regression coverage fails before the fix and passes after it.
