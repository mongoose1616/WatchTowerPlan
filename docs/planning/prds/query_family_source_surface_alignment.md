---
trace_id: trace.query_family_source_surface_alignment
id: prd.query_family_source_surface_alignment
title: Query Family Source Surface Alignment PRD
summary: Hardens query-family implementation-path authority so command docs and command
  index surfaces resolve to the correct split query families.
type: prd
status: active
owner: repository_maintainer
updated_at: '2026-03-13T22:02:13Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/cli/
- docs/commands/core_python/
- core/control_plane/indexes/commands/
aliases:
- query source surface alignment
---

# Query Family Source Surface Alignment PRD

## Record Metadata
- `Trace ID`: `trace.query_family_source_surface_alignment`
- `PRD ID`: `prd.query_family_source_surface_alignment`
- `Status`: `active`
- `Linked Decisions`: `decision.query_family_source_surface_alignment_direction`
- `Linked Designs`: `design.features.query_family_source_surface_alignment`
- `Linked Implementation Plans`: `design.implementation.query_family_source_surface_alignment`
- `Updated At`: `2026-03-13T22:02:13Z`

## Summary
Hardens query-family implementation-path authority so command docs and command index surfaces resolve to the correct split query families.

## Problem Statement
The `query` CLI family has already been split into discovery, knowledge, record, and
coordination registration modules, but parser-backed command metadata still collapses every
query leaf command to the umbrella `query_family.py` surface. That coarse authority leaked
into the command index, `query commands` discovery output, and many leaf command pages, which
still pointed at either `query_family.py` or the older `main.py` entrypoint instead of the
owning family modules and handlers. The result is a deterministic lookup surface that routes
engineers and agents to stale implementation files even though the live command family is
already modularized.

## Goals
- Make parser-backed command metadata resolve each query leaf command to the correct split
  query family implementation path while preserving the `watchtower-core query` group entry
  at `query_family.py`.
- Reconcile affected query command pages, the command index, and command discovery output to
  the same source-surface model.
- Close the slice only after targeted validation, full repo validation, and repeated
  confirmation passes find no new actionable query-family source-surface issue.

## Non-Goals
- Change CLI flags, output payloads, command IDs, or command help behavior.
- Rename the split query family modules or move query business logic out of the current CLI and
  `repo_ops/query/` boundaries.
- Split `query_coordination_handlers.py` further unless confirmation work proves that the
  remaining file shape is itself a new actionable issue.

## Requirements
- `req.query_family_source_surface_alignment.001`: The trace must publish the fully-authored
  PRD, accepted direction decision, active feature design, active implementation plan,
  refreshed acceptance contract, refreshed evidence ledger, and bounded closed task set with
  the explicit coverage map and findings ledger for the query-family source-surface slice.
- `req.query_family_source_surface_alignment.002`: Parser-backed command metadata and the
  derived command index must map query leaf commands to their owning split query family files
  while keeping the `watchtower-core query` group command at `query_family.py`.
- `req.query_family_source_surface_alignment.003`: Affected query command pages and command
  discovery output must point to the correct family, handler, query service, and governed index
  or contract surfaces instead of stale umbrella or root-entrypoint files.
- `req.query_family_source_surface_alignment.004`: Direct consumers must gain regression
  coverage for discovery, knowledge, records, and coordination query-family implementation
  paths, and the review must record the accepted bounded recommendation for the
  `query_coordination_handlers.py` family boundary.
- `req.query_family_source_surface_alignment.005`: The trace closes only after targeted and
  full validation plus repeated confirmation passes show no remaining actionable issue under
  the same query-family source-surface theme.

## Acceptance Criteria
- `ac.query_family_source_surface_alignment.001`: The bootstrap flow publishes the PRD, design,
  implementation plan, decision record, acceptance contract, evidence ledger, and bounded task
  chain for `trace.query_family_source_surface_alignment`.
- `ac.query_family_source_surface_alignment.002`: Representative query command specs and the
  rebuilt command index resolve discovery, knowledge, records, and coordination leaf commands
  to `query_discovery_family.py`, `query_knowledge_family.py`, `query_records_family.py`, and
  `query_coordination_family.py` respectively, while the root `query` group remains at
  `query_family.py`.
- `ac.query_family_source_surface_alignment.003`: The affected query command pages no longer
  point at stale `main.py` or umbrella `query_family.py` paths except where the root query
  group intentionally remains authoritative, and command discovery returns the same family
  ownership model.
- `ac.query_family_source_surface_alignment.004`: The decision record and implementation
  ledger explain the accepted bounded recommendation for `query_coordination_handlers.py`
  after re-review.
- `ac.query_family_source_surface_alignment.005`: Targeted validation, full repo validation,
  and repeated confirmation or adversarial probes pass on the final closed state with no new
  actionable issue under the theme.

## Risks and Dependencies
- Future query leaf commands could drift again if new family-specific registrations are added
  without updating the registry-backed implementation-path metadata.
- Over-correcting the slice into a runtime handler split would expand churn without improving
  the actual lookup-authority problem this trace is fixing.

## References
- REFACTOR.md RF-PY-004
