---
trace_id: trace.rendered_surface_contract_enforcement
id: decision.rendered_surface_contract_enforcement_direction
title: Rendered Surface Contract Enforcement Direction Decision
summary: Records the decision to use governed rendered-surface contracts and retire live projection terminology on active derived outputs.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-16T17:34:52Z'
audience: shared
authority: supporting
applies_to:
- core/python/src/watchtower_core/repo_ops/
- core/control_plane/
- docs/standards/
- docs/planning/
---

# Rendered Surface Contract Enforcement Direction Decision

## Record Metadata
- `Trace ID`: `trace.rendered_surface_contract_enforcement`
- `Decision ID`: `decision.rendered_surface_contract_enforcement_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.rendered_surface_contract_enforcement`
- `Linked Designs`: `design.features.rendered_surface_contract_enforcement`
- `Linked Implementation Plans`: `design.implementation.rendered_surface_contract_enforcement`
- `Updated At`: `2026-03-16T17:34:52Z`

## Summary
Records the decision to use governed rendered-surface contracts and retire live projection terminology on active derived outputs.

## Decision Statement
Active derived-output surfaces will use `rendered` terminology, and index-backed Markdown trackers will be emitted from a governed rendered-surface registry through a generic renderer instead of handwritten per-service layout logic.

## Trigger or Source Request
- User request to replace projection phrasing with rendered surface terminology and move derived Markdown rendering to a schema-driven style.

## Current Context and Constraints
- Active runtime code and current docs still use `projection` terminology for live derived outputs even where the concern is explicitly rendering compact human or machine-facing surfaces.
- The current tracker family duplicates Markdown section and table assembly across multiple sync services even though the underlying content already lives in authoritative indexes or task records.
- The repository wants slimmer, more reusable active surfaces and does not want to preserve new compatibility wrappers or duplicate render paths in this slice.
- Retained historical traces and ledgers remain historical records, so this initiative must improve live surfaces without rewriting archived evidence indiscriminately.

## Applied References and Implications
- [engineering_design_principles.md](/docs/foundations/engineering_design_principles.md): readable outputs should remain derived from stronger machine state, which favors a rendered contract over ad hoc handwritten docs.
- [repository_standards_posture.md](/docs/foundations/repository_standards_posture.md): canonical machine and human surfaces must stay synchronized, so terminology and render logic should move together.
- [compact_document_authoring_standard.md](/docs/standards/documentation/compact_document_authoring_standard.md): compact rendered outputs should stay thin because machine authority already lives elsewhere.
- [schema_standard.md](/docs/standards/data_contracts/schema_standard.md): the new rendered-surface contract should be schema-backed and governed like other reusable control-plane surfaces.

## Affected Surfaces
- core/python/src/watchtower_core/repo_ops/
- core/control_plane/
- docs/standards/
- docs/planning/

## Options Considered
### Option 1
- Rename active docs only and leave the runtime helpers and rendered trackers unchanged.
- Low implementation cost.
- Rejected because the runtime seams and handwritten layout duplication would remain, so the term change would be superficial.

### Option 2
- Add a generic renderer but keep `projection` terminology and compatibility wrappers in active code.
- Reduces some duplicated string assembly.
- Rejected because it preserves the terminology split and leaves a larger active surface area than the repository wants.

### Option 3
- Publish a governed rendered-surface contract, render tracker Markdown from that contract, and rename active derived-output helpers from `projection` to `rendered` without compatibility shims.
- Aligns terminology, runtime seams, and machine-readable contracts in one slice.
- Chosen because it best matches the repository goal of being slimmer, more concise, and more reusable.

## Chosen Outcome
- Add a rendered-surface registry and schema under `core/control_plane/`, plus any typed model or loader support needed to load it cleanly.
- Refactor the tracker sync services so they shape source data in code but render final Markdown through the governed rendered-surface contract.
- Rename active `planning_projection_*` and query-handler boundaries to `planning_rendered_*` and matching rendered terminology.
- Update current standards, command docs, and planning entrypoint guidance in the same change set, with no active compatibility alias left behind in scope.

## Rationale and Tradeoffs
- This keeps the canonical machine state where it already belongs while making the rendered layer more generic and configurable.
- It removes duplicate layout logic and terminology drift together instead of solving only one side of the problem.
- It deliberately stops short of historical rewrites, which keeps the slice bounded and avoids mutating archived evidence for cosmetic reasons.

## Consequences and Follow-Up Impacts
- Tracker layout changes now require updating the governed rendered-surface registry instead of silently editing handwritten sync strings.
- Active current docs, standards, and command pages need the same-change terminology update to stay aligned with the runtime rename.
- Historical retained traces may still mention `projection`, but they are explicitly out of scope for this live-surface contract slice.

## Risks, Dependencies, and Assumptions
- The rendered-surface contract must stay intentionally constrained; otherwise it becomes an opaque templating language.
- Renaming runtime boundaries requires disciplined same-change updates across imports, tests, and command docs.
- The decision assumes source shaping logic stays in code and only the render contract moves to governed data.

## References
- [rendered_surface_contract_enforcement.md](/docs/planning/prds/rendered_surface_contract_enforcement.md)
- [rendered_surface_contract_enforcement.md](/docs/planning/design/features/rendered_surface_contract_enforcement.md)
- [compact_document_authoring_and_tracking.md](/docs/planning/design/features/compact_document_authoring_and_tracking.md)
- [core_export_ready_architecture.md](/docs/planning/design/features/core_export_ready_architecture.md)
- [repository_standards_posture.md](/docs/foundations/repository_standards_posture.md)
