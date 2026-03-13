---
trace_id: trace.query_family_source_surface_alignment
id: design.features.query_family_source_surface_alignment
title: Query Family Source Surface Alignment Feature Design
summary: Defines the technical design boundary for Query Family Source Surface Alignment.
type: feature_design
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

# Query Family Source Surface Alignment Feature Design

## Record Metadata
- `Trace ID`: `trace.query_family_source_surface_alignment`
- `Design ID`: `design.features.query_family_source_surface_alignment`
- `Design Status`: `active`
- `Linked PRDs`: `prd.query_family_source_surface_alignment`
- `Linked Decisions`: `decision.query_family_source_surface_alignment_direction`
- `Linked Implementation Plans`: `design.implementation.query_family_source_surface_alignment`
- `Updated At`: `2026-03-13T22:02:13Z`

## Summary
Defines the technical design boundary for Query Family Source Surface Alignment.

## Source Request
- Comprehensive refactor review slice for query-family source-surface authority, command docs, and command index drift.

## Scope and Feature Boundary
- Covers registry-backed CLI parser introspection, query command registration families,
  command-index derivation, affected query command pages, command discovery output, and the
  direct unit or CLI consumers that assert those surfaces.
- Excludes CLI behavior changes, output-schema changes, non-query command families, and any
  runtime refactor beyond the query-family source-surface authority problem unless a later
  confirmation pass proves it is necessary.

## Current-State Context
- `query_family.py` is now only the umbrella group registrar, while live leaf registration is
  split across `query_discovery_family.py`, `query_knowledge_family.py`,
  `query_records_family.py`, and `query_coordination_family.py`.
- `core/python/src/watchtower_core/cli/introspection.py` still derives command
  `implementation_path` from the top-level family token only, so every `watchtower-core query`
  leaf command is published as if `query_family.py` owns it.
- The command index and `watchtower-core query commands` therefore reported stale
  implementation paths for query leaf commands, and many command pages still pointed all the
  way back to `main.py` or to the umbrella `query_family.py` path.
- Re-review of `query_coordination_handlers.py` shows a 591-line family boundary with shared
  initiative and planning output helpers already extracted; the live concrete drift in this
  slice is source-surface authority, not a confirmed runtime behavior split failure.

## Foundations References Applied
- `docs/foundations/engineering_design_principles.md`: keep the authority change local and
  deterministic at the registry-backed CLI metadata boundary instead of scattering per-command
  heuristics through docs and tests.
- `docs/foundations/repository_standards_posture.md`: human-readable docs and machine-readable
  lookup surfaces must move together in the same change set when one depends on the other.

## Internal Standards and Canonical References Applied
- `docs/standards/data_contracts/command_index_standard.md`: the command index must point to
  the owning implementation surface and must be updated in the same change set as command
  surface changes.
- `docs/standards/documentation/command_md_standard.md`: command pages must record the current
  source surface so engineers can route directly to the owning code path.
- `docs/standards/engineering/python_workspace_standard.md`: implementation and regression work
  stays inside the canonical Python workspace.

## Design Goals and Constraints
- Publish precise leaf-command implementation paths for the query family without changing how
  commands are registered or executed.
- Preserve the `watchtower-core query` group command as the umbrella entrypoint and keep leaf
  help text, command IDs, synopsis text, and output-format metadata stable.
- Keep the fix durable by putting subcommand ownership in the same registry-backed metadata
  system that the parser introspection already trusts.

## Options Considered
### Option 1
- Add a query-only subcommand mapping directly inside `introspection.py`.
- Smallest possible code change with no registry shape expansion.
- Hides authoritative ownership data away from the registry metadata that already declares top-
  level family boundaries.

### Option 2
- Extend `CommandGroupSpec` with optional per-subcommand implementation-path overrides and let
  introspection consume that registry-backed metadata for the query family.
- Keeps command-family ownership in one authoritative registry layer and makes the resulting
  command index and docs deterministic.
- Adds a small metadata structure that future split families must maintain deliberately.

## Recommended Design
### Architecture
- `core/python/src/watchtower_core/cli/registry.py` remains the authority for top-level command
  groups and gains optional leaf-command implementation ownership for split families.
- `core/python/src/watchtower_core/cli/introspection.py` stays the only place that derives
  parser-backed command specs, but it now consults registry-backed per-subcommand overrides
  before falling back to the top-level family file.
- Command docs and the derived command index are treated as companion surfaces that must align
  with that same mapping.

### Data and Interface Impacts
- No CLI arguments, command IDs, payload schemas, or help text contracts change.
- `core/control_plane/indexes/commands/command_index.v1.json` changes its
  `implementation_path` values for query leaf entries.
- The affected query command pages change only in their source-surface metadata and related
  routing guidance.

### Execution Flow
1. The registry declares which query leaf commands belong to discovery, knowledge, records, or
   coordination family files.
2. Parser introspection builds command specs from the live parser tree and resolves
   `implementation_path` through those leaf overrides before falling back to the umbrella family
   path.
3. Command-index sync, command docs, loader expectations, and command-discovery queries all
   consume the same resulting source-surface authority.

### Invariants and Failure Cases
- The root `watchtower-core query` group command must continue to resolve to
  `core/python/src/watchtower_core/cli/query_family.py`.
- If a family has no per-subcommand override for a leaf command, introspection must fail safe
  by falling back to the top-level family path rather than crashing or inventing a heuristic.
- Command pages should be rejected in review if they still point to stale `main.py` or umbrella
  paths for split query leaf commands after the index and tests have been reconciled.

## Affected Surfaces
- core/python/src/watchtower_core/cli/
- docs/commands/core_python/
- core/control_plane/indexes/commands/

## Design Guardrails
- Do not add ad hoc string-matching rules in command docs or tests to compensate for stale
  metadata; fix the registry-backed authority instead.
- Do not split `query_coordination_handlers.py` in this trace unless a later confirmation pass
  surfaces a concrete new correctness or maintainability defect beyond file size alone.

## Risks
- The main risk is omission: one query leaf command could be left on the fallback family path,
  producing a partial command-index or doc reconciliation that still looks superficially valid.
- A secondary risk is future drift if additional split query leaves are added without extending
  the registry override table and regression coverage.

## References
- REFACTOR.md RF-PY-004
