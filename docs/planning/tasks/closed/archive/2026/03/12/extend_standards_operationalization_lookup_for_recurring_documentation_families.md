---
id: task.documentation_family_lookup_and_readme_template_alignment.operationalization_lookup.001
trace_id: trace.documentation_family_lookup_and_readme_template_alignment
title: Extend standards operationalization lookup for recurring documentation families
summary: Add bounded glob-pattern support for standard operationalization surfaces
  and align the affected family standards and query docs.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T00:57:22Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/standards.py
- core/python/src/watchtower_core/repo_ops/query/standards.py
- core/python/tests/unit/
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/unit/test_document_semantics_validation.py
- docs/commands/core_python/watchtower_core_query_standards.md
- docs/standards/data_contracts/standard_index_standard.md
- docs/standards/documentation/standard_md_standard.md
- docs/standards/documentation/readme_md_standard.md
- docs/standards/documentation/agents_md_standard.md
- docs/standards/documentation/reference_md_standard.md
related_ids:
- prd.documentation_family_lookup_and_readme_template_alignment
- design.features.documentation_family_lookup_and_readme_template_alignment
- design.implementation.documentation_family_lookup_and_readme_template_alignment
- decision.documentation_family_lookup_and_readme_template_alignment_direction
- contract.acceptance.documentation_family_lookup_and_readme_template_alignment
---

# Extend standards operationalization lookup for recurring documentation families

## Summary
Add bounded glob-pattern support for standard operationalization surfaces and align the affected family standards and query docs.

## Scope
- Allow operationalization metadata to preserve bounded repo-relative glob patterns that match live surfaces.
- Update standards query matching so concrete governed files resolve through exact, directory, and glob operationalization entries.
- Align the AGENTS, README, reference, and standard family standards plus standards-query docs with the new lookup model.

## Done When
- Standards sync, semantics, and query behavior accept the new operationalization model.
- Representative concrete AGENTS, README, reference, and standard docs resolve to their governing standards.
