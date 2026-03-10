---
trace_id: "trace.core_export_hardening_followup"
id: "design.features.core_export_hardening"
title: "Core Export Hardening Design"
summary: "Defines the follow-up architecture needed to make output-directory sync runs dependency-correct, restore accurate command implementation metadata, and tighten the public export-safe boundary around repo-specific services."
type: "feature_design"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T15:24:07Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/python/src/watchtower_core/"
  - "docs/planning/design/"
aliases:
  - "export hardening design"
---

# Core Export Hardening Design

## Record Metadata
- `Trace ID`: `trace.core_export_hardening_followup`
- `Design ID`: `design.features.core_export_hardening`
- `Design Status`: `active`
- `Linked PRDs`: `prd.core_export_hardening_followup`
- `Linked Decisions`: `None`
- `Linked Implementation Plans`: `design.implementation.core_export_hardening_execution`
- `Updated At`: `2026-03-10T15:24:07Z`

## Summary
Defines the follow-up architecture needed to make output-directory sync runs dependency-correct, restore accurate command implementation metadata, and tighten the public export-safe boundary around repo-specific services.

## Source Request
- User request to turn the repo review findings into a new traced feature process and complete the related work.

## Scope and Feature Boundary
- Covers sync output-directory consistency for deterministic derived artifacts.
- Covers command implementation metadata published through the command index.
- Covers the public package boundary for repo-specific query, sync, and aggregate validation services.
- Does not reopen the prior export-readiness initiative or add new product capabilities.

## Current-State Context
- [all.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/repo_ops/sync/all.py) materializes output-directory targets but keeps every sync service bound to the canonical repo loader.
- [introspection.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/cli/introspection.py) hardcodes `cli/main.py` as the implementation path for every command.
- [query/__init__.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/query/__init__.py) and [sync/__init__.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/sync/__init__.py) still advertise repo-specific services as top-level exports.
- [validation/all.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/validation/all.py) still embeds repo-specific planning and document-semantic behavior in the public aggregate validation surface.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): fix hidden coupling instead of adding more implicit behavior.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): keep indexes, docs, and tests aligned as the boundary tightens.
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md): hardening remains at the shared-substrate layer.

## Internal Standards and Canonical References Applied
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): favor explicit boundaries, thin entrypoints, and targeted regression coverage.
- [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md): command metadata should remain trustworthy as a machine-readable navigation surface.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): this work belongs to a new bounded initiative instead of reopening a closed trace.

## Design Goals and Constraints
- Keep the hardening work bounded to the three review findings.
- Preserve current CLI behavior and validation semantics while tightening internal boundaries.
- Avoid introducing a second authoritative sync path or a new convenience compatibility layer that recreates the same leak.

## Options Considered
### Option 1
- Fix each issue locally without a new trace.
- Would be faster in the short term.
- Was not chosen because the review findings affect architecture and public boundary expectations across multiple governed surfaces.

### Option 2
- Reopen the prior export-readiness initiative.
- Would reuse the existing trace.
- Was not chosen because that initiative is explicitly closed and the follow-up work is a new bounded hardening pass.

### Option 3
- Create a new hardening initiative with one bounded task per finding.
- Chosen because it keeps the review findings durable, traceable, and separately closeable from the broader export-readiness work.

## Recommended Design
### Output-Directory Sync Overlay
- Add an overlay artifact source that prefers already-written files from `--output-dir` and falls back to the canonical repo for untouched source surfaces.
- Keep canonical Markdown and governed-source reads pointed at the real repo while letting later sync targets resolve earlier generated JSON artifacts from the materialized snapshot.
- Reuse the same service orchestration order; change the loader behavior rather than duplicating sync logic for snapshot mode.

### Command Implementation Metadata
- Let parser metadata carry an explicit implementation path for each command family.
- Derive command-index implementation paths from the parser tree rather than hardcoding the thin root CLI entrypoint.
- Keep the root command on the root surface, but point family and subcommand entries at the command-family module that defines their CLI contract.

### Public Boundary Hardening
- Move repo-specific consumers such as the CLI and repo-maintenance tests to `watchtower_core.repo_ops.*` imports directly.
- Stop advertising repo-specific query, sync, and aggregate validation services from top-level export-safe namespaces.
- Keep genuinely reusable validation services exported from `watchtower_core.validation`, but move the aggregate repo-wide validation surface under `watchtower_core.repo_ops.validation`.

## Affected Surfaces
- `core/python/src/watchtower_core/control_plane/workspace.py`
- `core/python/src/watchtower_core/repo_ops/sync/`
- `core/python/src/watchtower_core/cli/`
- `core/python/src/watchtower_core/query/`
- `core/python/src/watchtower_core/sync/`
- `core/python/src/watchtower_core/validation/`
- `core/python/tests/`

## Design Guardrails
- Do not introduce a second sync code path that duplicates the registered sync orchestration.
- Do not point command metadata back at the thin root entrypoint once family modules exist.
- Do not keep repo-specific services in top-level export-safe namespaces just for convenience.

## Implementation-Planning Handoff Notes
- Land output-directory sync consistency first because it is the only correctness bug from the review.
- Land command metadata next because it is localized and updates machine-readable docs without broad API churn.
- Land the public-boundary hardening last because it is the only intentionally breaking internal API cleanup in this follow-up.

## Dependencies
- The existing export-readiness refactor and repo-ops package split.
- The current command-index and sync orchestration machinery.
- The current planning and traceability trackers under `docs/planning/` and `core/control_plane/indexes/`.

## Risks
- Overlay reads could accidentally mask missing generated outputs if the fallback behavior is not explicit.
- Tightening the top-level boundary may require wider internal import cleanup than the current review suggests.
- Command metadata could remain only partially useful if family registration and handler ownership diverge further later.

## References
- [core_export_hardening_followup.md](/home/j/WatchTowerPlan/docs/planning/prds/core_export_hardening_followup.md)
- [core_export_ready_architecture.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_ready_architecture.md)

## Updated At
- `2026-03-10T15:24:07Z`
