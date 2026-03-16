---
trace_id: trace.rendered_surface_contract_enforcement
id: design.implementation.rendered_surface_contract_enforcement
title: Rendered Surface Contract Enforcement Implementation Plan
summary: Breaks the rendered-surface registry, tracker refactor, and live terminology enforcement into one bounded implementation slice.
type: implementation_plan
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

# Rendered Surface Contract Enforcement Implementation Plan

## Record Metadata
- `Trace ID`: `trace.rendered_surface_contract_enforcement`
- `Plan ID`: `design.implementation.rendered_surface_contract_enforcement`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.rendered_surface_contract_enforcement`
- `Linked Decisions`: `decision.rendered_surface_contract_enforcement_direction`
- `Source Designs`: `design.features.rendered_surface_contract_enforcement`
- `Linked Acceptance Contracts`: `contract.acceptance.rendered_surface_contract_enforcement`
- `Updated At`: `2026-03-16T17:34:52Z`

## Summary
Breaks the rendered-surface registry, tracker refactor, and live terminology enforcement into one bounded implementation slice.

## Source Request or Design
- User request to replace projection phrasing with rendered surface terminology and move derived Markdown rendering to a schema-driven style.

## Scope Summary
- Covers the governed rendered-surface contract, loader-model wiring, generic Markdown renderer, tracker refactor, active terminology rename, and companion docs or standards updates required to keep the repo coherent.
- Covers the active code and current authority surfaces that still expose `projection` terminology for live derived outputs.
- Excludes historical trace rewrites, purge-ledger cleanup, and changes that would move canonical machine authority into Markdown.

## Assumptions and Constraints
- `core/control_plane/` remains the canonical versioned machine-readable authority for authored rendered-surface contracts.
- `core/python/` remains the only Python workspace and the place where runtime rendering and sync refactors land.
- Tracker source selection, filtering, and sort policy remain code-owned; only the rendered layout contract moves to governed machine-readable data.
- No compatibility wrappers for old `projection` names should survive in active runtime or current command and standards guidance after the slice lands.

## Internal Standards and Canonical References Applied
- [schema_standard.md](/docs/standards/data_contracts/schema_standard.md): the registry and schema additions must update catalog, validators, and tests in the same change set.
- [compact_document_authoring_standard.md](/docs/standards/documentation/compact_document_authoring_standard.md): rendered trackers must stay compact and scan-first after the refactor.
- [coordination_tracking_standard.md](/docs/standards/governance/coordination_tracking_standard.md): the start-here tracker remains a rendered view over the coordination index.
- [python_workspace_standard.md](/docs/standards/engineering/python_workspace_standard.md): all runtime, tests, and command execution changes stay under `core/python/`.
- [engineering_best_practices_standard.md](/docs/standards/engineering/engineering_best_practices_standard.md): keep the implementation modular, explicit, and aligned across code plus companion docs.

## Proposed Technical Approach
- Add the rendered-surface registry artifact and schema first so the runtime refactor has a governed contract to target.
- Add typed model and loader support for the new registry so rendered surfaces can be loaded through the same deterministic control-plane path as other governed registries.
- Implement a generic rendered Markdown adapter plus repo-local tracker section shapers, then refactor the six tracker sync services onto that adapter.
- Rename the active planning-rendered runtime helpers and query handlers in the same slice so the contract, code, and command docs all use the same live term.
- Refresh current standards, README entrypoints, and command docs after the code move so current authority and runtime agree before final validation.

## Work Breakdown
1. Author the rendered-surface schema and registry, then update schema catalog, validator registry, pack settings, and any typed loader-model surfaces needed to load the registry deterministically.
2. Add the generic rendered Markdown adapter and refactor the tracker sync services to emit rendered Markdown from governed surface definitions rather than handwritten layout strings.
3. Rename active `projection` runtime boundaries to `rendered`, update current docs and standards guidance, refresh derived surfaces, and close the slice through targeted plus full validation.

## Risks
- The schema and registry could be under-specified and force layout logic back into Python helpers.
- The runtime rename can leave stale imports or command-doc references if the same-change update set misses one active surface.
- Tracker output regressions can surface late if tests only assert strings and not section or column behavior through the new rendered contract.

## Validation Plan
- Add or update focused unit tests for the rendered Markdown adapter, rendered-surface registry loading, and tracker output behavior.
- Run `./.venv/bin/watchtower-core sync all --write --format json` after authoritative contract and tracker changes so derived surfaces refresh in one deterministic slice.
- Run `./.venv/bin/watchtower-core validate acceptance --trace-id trace.rendered_surface_contract_enforcement --format json`.
- Run `./.venv/bin/watchtower-core validate all --format json`.
- Run `./.venv/bin/pytest -q`, `./.venv/bin/mypy src`, and `./.venv/bin/ruff check .`.
- Do not close the initiative until a confirmation pass finds no remaining active `projection` terminology inside the bounded live scope.

## References
- [rendered_surface_contract_enforcement.md](/docs/planning/prds/rendered_surface_contract_enforcement.md)
- [rendered_surface_contract_enforcement.md](/docs/planning/design/features/rendered_surface_contract_enforcement.md)
- [compact_document_authoring_and_tracking.md](/docs/planning/design/features/compact_document_authoring_and_tracking.md)
- [core_export_ready_architecture.md](/docs/planning/design/features/core_export_ready_architecture.md)
- [repository_standards_posture.md](/docs/foundations/repository_standards_posture.md)
