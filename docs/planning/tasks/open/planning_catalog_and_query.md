---
id: task.planning_authority_unification.planning_catalog.001
trace_id: trace.planning_authority_unification
title: Publish planning catalog and canonical planning query
summary: Build the planning-catalog artifact family and make it the canonical machine planning join through a dedicated query command.
type: task
status: active
task_status: backlog
task_kind: feature
priority: high
owner: repository_maintainer
updated_at: '2026-03-11T01:48:43Z'
audience: shared
authority: authoritative
related_ids:
  - prd.planning_authority_unification
  - design.features.planning_authority_unification
  - design.implementation.planning_authority_unification
  - decision.planning_authority_unification_direction
applies_to:
  - core/control_plane/
  - core/python/
  - docs/commands/core_python/
---

# Publish planning catalog and canonical planning query

## Summary
Build the planning-catalog artifact family and make it the canonical machine planning join through a dedicated query command.

## Scope
- Add the planning-catalog schema, canonical artifact, examples, schema-catalog entry, artifact-type entry, validator entry, typed model, and loader support.
- Add the planning-catalog sync service plus `watchtower-core sync planning-catalog`.
- Add `watchtower-core query planning` with explicit planning-status semantics and linked planning, task, acceptance, evidence, and coordination sections.
- Update companion command docs and tests.

## Done When
- The repo publishes a canonical planning-catalog artifact under `core/control_plane/indexes/planning/`.
- `watchtower-core query planning --format json` returns explicit canonical planning records.
- Companion schemas, registries, command docs, and tests are aligned and green.

## Links
- [planning_authority_unification.md](/home/j/WatchTowerPlan/docs/planning/prds/planning_authority_unification.md)
- [planning_authority_unification.md](/home/j/WatchTowerPlan/docs/planning/design/features/planning_authority_unification.md)
