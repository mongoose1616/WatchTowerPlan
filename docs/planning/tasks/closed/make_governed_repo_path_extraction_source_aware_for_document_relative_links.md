---
id: task.internal_project_standards_review_and_hardening.document_relative_reference_extraction.001
trace_id: trace.internal_project_standards_review_and_hardening
title: Make governed repo-path extraction source-aware for document-relative links
summary: Resolve document-relative repo-local Markdown links in governed sync and
  citation-audit extraction paths.
type: task
status: active
task_status: done
task_kind: bug
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T18:00:40Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/
- core/python/src/watchtower_core/adapters/markdown.py
- core/python/src/watchtower_core/repo_ops/planning_documents.py
- core/python/src/watchtower_core/repo_ops/sync/
- core/python/tests/
related_ids:
- prd.internal_project_standards_review_and_hardening
- design.features.internal_project_standards_review_and_hardening
- design.implementation.internal_project_standards_review_and_hardening
- decision.internal_project_standards_review_and_hardening_direction
- contract.acceptance.internal_project_standards_review_and_hardening
---

# Make governed repo-path extraction source-aware for document-relative links

## Summary
Resolve document-relative repo-local Markdown links in governed sync and citation-audit extraction paths.

## Scope
- Add source-document context to Markdown repo-path normalization and extraction helpers.
- Update planning, decision, standard, reference, foundation, workflow, and citation-audit call sites to pass source-document paths.
- Add regression coverage proving derived machine-readable surfaces capture document-relative repo-local links, including normalized decision `Affected Surfaces`.

## Done When
- Derived repo-path extraction normalizes document-relative links to repo-relative paths.
- Standard, decision, reference, workflow, and planning helper tests cover document-relative examples.
- Affected planning and acceptance surfaces are refreshed.
