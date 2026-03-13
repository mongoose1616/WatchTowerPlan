---
trace_id: trace.query_family_source_surface_alignment
id: decision.query_family_source_surface_alignment_direction
title: Query Family Source Surface Alignment Direction Decision
summary: Records the initial direction decision for Query Family Source Surface Alignment.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-13T22:02:13Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/cli/
- docs/commands/core_python/
- core/control_plane/indexes/commands/
aliases:
- query source surface alignment
---

# Query Family Source Surface Alignment Direction Decision

## Record Metadata
- `Trace ID`: `trace.query_family_source_surface_alignment`
- `Decision ID`: `decision.query_family_source_surface_alignment_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.query_family_source_surface_alignment`
- `Linked Designs`: `design.features.query_family_source_surface_alignment`
- `Linked Implementation Plans`: `design.implementation.query_family_source_surface_alignment`
- `Updated At`: `2026-03-13T22:02:13Z`

## Summary
Records the initial direction decision for Query Family Source Surface Alignment.

## Decision Statement
Keep the root `watchtower-core query` group at `query_family.py`, add registry-backed
per-subcommand implementation-path authority for split query leaf commands, reconcile the
command docs and command index to that authority, and treat the current
`query_coordination_handlers.py` file as an acceptable family boundary for this trace.

## Trigger or Source Request
- Comprehensive refactor review slice for query-family source-surface authority, command docs, and command index drift.

## Current Context and Constraints
- The live CLI already registers query leaves through discovery, knowledge, records, and
  coordination family files, but parser introspection still publishes all query leaves as if
  the umbrella `query_family.py` surface owns them.
- Command docs and the derived command index must stay aligned in the same change set, so the
  fix needs one shared implementation-path authority rather than parallel manual updates.
- The coordination query handler file is still large, but the earlier family split plus shared
  planning serializers mean file size alone is not enough evidence to justify further runtime
  splitting in this bounded trace.

## Applied References and Implications
- `docs/standards/data_contracts/command_index_standard.md`: the command index should point to
  the owning implementation surface and must be rebuilt when command surfaces change
  materially.
- `docs/standards/documentation/command_md_standard.md`: command pages must route engineers to
  the current implementation surface, so stale `main.py` and umbrella-family references are
  not acceptable once split leaf families exist.
- `docs/foundations/engineering_design_principles.md`: fix the deterministic local authority
  boundary instead of patching symptoms across several consumers.

## Affected Surfaces
- core/python/src/watchtower_core/cli/
- docs/commands/core_python/
- core/control_plane/indexes/commands/

## Options Considered
### Option 1
- Add a query-only mapping directly inside parser introspection and update the docs and tests
  around it.
- Smallest code delta.
- Keeps the authoritative leaf ownership data outside the command registry metadata.

### Option 2
- Extend `CommandGroupSpec` with per-subcommand implementation-path overrides, consume those
  overrides in parser introspection, and reconcile the command docs and command index to that
  registry-backed authority while deferring further runtime handler splitting.
- Centralizes ownership metadata and aligns all companion surfaces to the same source of truth.
- Requires a small metadata extension and deliberate maintenance when new split query leaves are
  added.

## Chosen Outcome
Choose option 2. The registry already defines the command-family boundary, so it should also
declare the owning leaf family files for split query commands. Parser introspection consumes
that metadata, the command index rebuild becomes precise automatically, and the command pages
can align to the same family and handler surfaces. The runtime handler split is explicitly not
expanded in this trace because re-review did not show a more concrete same-theme defect than
the source-surface drift already being fixed.

## Rationale and Tradeoffs
- The command-index and command-doc drift came from one coarse authority decision, so one
  authoritative metadata fix is lower risk than manual per-surface patching.
- Keeping the handler file boundary intact avoids widening the trace into speculative runtime
  restructuring when the live issue is navigation and lookup fidelity.

## Consequences and Follow-Up Impacts
- Future split query leaves must add their owning family path to the registry-backed override
  table and to regression coverage.
- Command discovery and loader-based tests now become active guards against the same drift.
- A later refactor trace can revisit `query_coordination_handlers.py` only if a fresh review
  finds a concrete new maintainability or correctness failure after this authority fix.

## Risks, Dependencies, and Assumptions
- The main risk is omission if one query leaf is missed in the override table or the doc
  reconciliation.
- The decision assumes the current split query family files remain the intended registration
  boundaries for the medium term.

## References
- REFACTOR.md RF-PY-004
