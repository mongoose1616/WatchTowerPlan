---
id: task.standards_lookup_and_generic_template_alignment.lookup_resolution.001
trace_id: trace.standards_lookup_and_generic_template_alignment
title: Resolve descendant standard lookup for directory-scoped operationalization
  paths
summary: Make standards lookup resolve concrete files under directory-scoped
  operationalization surfaces and add matching CLI regressions.
type: task
status: active
task_status: done
task_kind: governance
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T00:20:44Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/repo_ops/query/standards.py
- core/python/src/watchtower_core/cli/query_knowledge_family.py
- core/python/tests/unit/test_cli_query_commands.py
- docs/commands/core_python/watchtower_core_query_standards.md
depends_on:
- task.standards_lookup_and_generic_template_alignment.bootstrap.001
related_ids:
- prd.standards_lookup_and_generic_template_alignment
- design.features.standards_lookup_and_generic_template_alignment
- design.implementation.standards_lookup_and_generic_template_alignment
- decision.standards_lookup_and_generic_template_alignment_direction
- contract.acceptance.standards_lookup_and_generic_template_alignment
---

# Resolve descendant standard lookup for directory-scoped operationalization paths

## Summary
Make standards lookup resolve concrete files under directory-scoped
operationalization surfaces and add matching CLI regressions.

## Scope
- Update `StandardQueryService` so `operationalization_path` treats indexed
  directories as governing descendants.
- Keep other standards-query path filters exact in this slice.
- Document and test the descendant-match behavior through the CLI surface.

## Done When
- Querying a concrete PRD, decision, or generic-template file returns the
  governing standard instead of zero results when the indexed standard
  operationalizes the containing directory.
- CLI regressions fail closed if standards lookup falls back to exact-match-only
  behavior again.
- The command page documents the descendant-path behavior accurately.
