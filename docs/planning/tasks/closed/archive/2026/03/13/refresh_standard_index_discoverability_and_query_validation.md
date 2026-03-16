---
id: task.data_contract_index_family_baseline_alignment.standard_index_discoverability.003
trace_id: trace.data_contract_index_family_baseline_alignment
title: Refresh standard-index discoverability and query validation
summary: Refresh the governed standard index, query-standards command docs, and regression
  tests around the planning-index family tag and discoverability path.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T20:07:34Z'
audience: shared
authority: authoritative
applies_to:
- core/control_plane/indexes/standards/standard_index.v1.json
- docs/commands/core_python/watchtower_core_query_standards.md
- core/python/tests/unit/test_standard_index_sync.py
- core/python/tests/unit/test_cli_knowledge_query_commands.py
related_ids:
- prd.data_contract_index_family_baseline_alignment
- design.features.data_contract_index_family_baseline_alignment
- design.implementation.data_contract_index_family_baseline_alignment
- decision.data_contract_index_family_baseline_alignment_direction
- contract.acceptance.data_contract_index_family_baseline_alignment
depends_on:
- task.data_contract_index_family_baseline_alignment.family_baseline.002
---

# Refresh standard-index discoverability and query validation

## Summary
Refresh the governed standard index, query-standards command docs, and regression tests around the planning-index family tag and discoverability path.

## Scope
- Refresh standard-index projections and command documentation for the new planning-index family discoverability path.
- Add or update regression coverage for standard-index sync output and query-standards lookup by the shared family tag.

## Done When
- The standard index, query-standards command docs, and direct regression tests all expose and verify the planning-index family discovery path.
- No runtime behavior change beyond authored metadata and documentation is needed, or any required change is explicitly justified and validated.
