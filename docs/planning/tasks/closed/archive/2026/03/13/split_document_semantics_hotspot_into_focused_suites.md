---
id: task.validation_test_hotspot_rebalancing.document_semantics_suite_split.003
trace_id: trace.validation_test_hotspot_rebalancing
title: Split document-semantics hotspot into focused suites
summary: Replace the remaining mixed-family document-semantics hotspot with focused
  suites, reusable fixture writers, and aligned unit-suite inventory coverage.
type: task
status: active
task_status: done
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-13T19:10:03Z'
audience: shared
authority: authoritative
applies_to:
- core/python/tests/unit/test_document_semantics_validation.py
- core/python/tests/unit/README.md
- core/python/src/watchtower_core/repo_ops/validation/document_semantics.py
- core/python/src/watchtower_core/validation/document_semantics.py
- core/python/src/watchtower_core/repo_ops/validation/all.py
related_ids:
- prd.validation_test_hotspot_rebalancing
- design.features.validation_test_hotspot_rebalancing
- design.implementation.validation_test_hotspot_rebalancing
- decision.validation_test_hotspot_rebalancing_direction
- contract.acceptance.validation_test_hotspot_rebalancing
---

# Split document-semantics hotspot into focused suites

## Summary
Replace the remaining mixed-family document-semantics hotspot with focused suites, reusable fixture writers, and aligned unit-suite inventory coverage.

## Scope
- Split the document-semantics hotspot along real validator-rule families.
- Move repeated fixture writing into small explicit helper modules without hiding fixture intent.
- Refresh unit README inventory coverage for the focused suite layout and compatibility marker.

## Done When
- The old document-semantics hotspot is replaced by focused suites plus reusable fixture helpers.
- Validator-selection, reference, standard, workflow, planning, and canonical-path coverage remain fail-closed.
- The unit README describes the new suite family and the compatibility marker path.
