---
id: task.foundation_index_family_contract_alignment.documentation.001
trace_id: trace.foundation_index_family_contract_alignment
title: Align foundation-index family standards and command surfaces
summary: Update the foundation-index standard and adjacent family docs so standards
  lookup covers the full foundations index family.
type: task
status: active
task_status: done
task_kind: documentation
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T23:17:39Z'
audience: shared
authority: authoritative
applies_to:
- docs/standards/data_contracts/foundation_index_standard.md
- core/control_plane/indexes/foundations/README.md
- docs/commands/core_python/watchtower_core_query_foundations.md
- docs/commands/core_python/watchtower_core_sync_foundation_index.md
- core/python/src/watchtower_core/repo_ops/query/foundations.py
- core/python/src/watchtower_core/repo_ops/sync/foundation_index.py
related_ids:
- prd.foundation_index_family_contract_alignment
- design.features.foundation_index_family_contract_alignment
- decision.foundation_index_family_contract_alignment_direction
depends_on:
- task.foundation_index_family_contract_alignment.bootstrap.001
---

# Align foundation-index family standards and command surfaces

## Summary
Update the foundation-index standard and adjacent family docs so standards lookup covers the full foundations index family.

## Scope
- Add the missing sync, query, command-doc, and family-README operationalization coverage to the foundation-index standard.
- Align adjacent command or family documentation surfaces that materially participate in the foundation-index family contract.
- Add regression coverage that fails closed if foundations family standards lookup loses these surfaces again.

## Done When
- The foundation-index standard operationalizes the full bounded foundations index family surfaces.
- Standards lookup resolves the governing data-contract standard from the affected foundations code and command surfaces.
- Targeted regression coverage protects the repair.
