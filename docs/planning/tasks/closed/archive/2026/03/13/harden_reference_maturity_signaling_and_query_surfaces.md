---
id: task.reference_and_reserved_surface_maturity_signaling.reference_maturity_signaling.002
trace_id: trace.reference_and_reserved_surface_maturity_signaling
title: Harden reference maturity signaling and query surfaces
summary: Add deterministic reference maturity classification, meaningful touchpoint
  accounting, and aligned reference query/docs/test coverage across the governed reference
  family.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T16:08:13Z'
audience: shared
authority: authoritative
applies_to:
- docs/references/
- core/control_plane/indexes/references/
- core/control_plane/schemas/artifacts/reference_index.v1.schema.json
- core/control_plane/examples/valid/indexes/reference_index.v1.example.json
- core/control_plane/examples/invalid/indexes/reference_index_missing_upstream.v1.example.json
- core/python/src/watchtower_core/repo_ops/sync/reference_index.py
- core/python/src/watchtower_core/repo_ops/query/references.py
- core/python/src/watchtower_core/control_plane/models/planning.py
- core/python/src/watchtower_core/repo_ops/validation/document_semantics.py
- core/python/src/watchtower_core/cli/query_knowledge_family.py
- core/python/src/watchtower_core/cli/query_knowledge_handlers.py
- core/python/tests/unit/test_reference_index_sync.py
- core/python/tests/unit/
- core/python/tests/unit/test_document_semantics_validation.py
- docs/commands/core_python/watchtower_core_query_references.md
related_ids:
- trace.reference_and_reserved_surface_maturity_signaling
- prd.reference_and_reserved_surface_maturity_signaling
- design.features.reference_and_reserved_surface_maturity_signaling
- design.implementation.reference_and_reserved_surface_maturity_signaling
- decision.reference_and_reserved_surface_maturity_signaling_direction
- contract.acceptance.reference_and_reserved_surface_maturity_signaling
---

# Harden reference maturity signaling and query surfaces

## Summary
Add deterministic reference maturity classification, meaningful touchpoint accounting, and aligned reference query/docs/test coverage across the governed reference family.

## Scope
- Review and update the reference family guidance for approved repository-status vocabulary and touchpoint rules.
- Update the reference index schema, examples, sync, model, query, and CLI surfaces so repository status and related-path behavior are deterministic.
- Add or refresh regression coverage and command docs for the reference sync/query behavior.

## Done When
- The reference index publishes deterministic repository status and candidate references no longer appear as internal support because of README-only backlinks.
- watchtower-core query references exposes status-aware output and directory touchpoint lookup with aligned docs and tests.
