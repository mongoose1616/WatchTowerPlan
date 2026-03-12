---
id: task.foundations_docs_boundary_alignment.documentation.001
trace_id: trace.foundations_docs_boundary_alignment
title: Align foundations-adjacent command and standards docs
summary: Update command docs, README inventories, standards, and references to reflect
  current foundations-adjacent documentation coverage and repo_ops ownership boundaries.
type: task
status: active
task_status: done
task_kind: documentation
priority: high
owner: repository_maintainer
updated_at: '2026-03-12T22:08:55Z'
audience: shared
authority: authoritative
applies_to:
- docs/commands/core_python/
- docs/standards/
- docs/references/
related_ids:
- prd.foundations_docs_boundary_alignment
- design.features.foundations_docs_boundary_alignment
- decision.foundations_docs_boundary_alignment_direction
---

# Align foundations-adjacent command and standards docs

## Summary
Update command docs, README inventories, standards, and references to reflect current foundations-adjacent documentation coverage and repo_ops ownership boundaries.

## Scope
- Repair the core Python command-doc README so it accurately routes foundations, query, and sync pages without a misleading partial inventory.
- Replace compatibility-wrapper source-surface references in current command docs with the authoritative repo_ops owners where that boundary is now canonical.
- Align active engineering and governance standards plus GitHub collaboration reference surfaces with the current query/sync ownership model.

## Done When
- Current authoritative docs and references describe the repo_ops boundary consistently with core/python/README.md and package READMEs.
- Foundations-adjacent command discovery surfaces expose the relevant query and sync pages clearly.
