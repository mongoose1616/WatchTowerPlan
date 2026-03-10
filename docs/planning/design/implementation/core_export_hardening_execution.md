---
trace_id: "trace.core_export_hardening_followup"
id: "design.implementation.core_export_hardening_execution"
title: "Core Export Hardening Implementation Plan"
summary: "Breaks the export-hardening follow-up into bounded slices for output-directory sync consistency, command metadata repair, and public boundary cleanup."
type: "implementation_plan"
status: "active"
owner: "repository_maintainer"
updated_at: "2026-03-10T15:24:07Z"
audience: "shared"
authority: "supporting"
applies_to:
  - "core/python/src/watchtower_core/"
  - "core/python/tests/"
aliases:
  - "export hardening plan"
---

# Core Export Hardening Implementation Plan

## Record Metadata
- `Trace ID`: `trace.core_export_hardening_followup`
- `Plan ID`: `design.implementation.core_export_hardening_execution`
- `Plan Status`: `active`
- `Linked PRDs`: `prd.core_export_hardening_followup`
- `Source Designs`: `design.features.core_export_hardening`
- `Linked Acceptance Contracts`: `contract.acceptance.core_export_hardening_followup`
- `Updated At`: `2026-03-10T15:24:07Z`

## Summary
Breaks the export-hardening follow-up into bounded slices for output-directory sync consistency, command metadata repair, and public boundary cleanup.

## Source Request or Design
- Feature design: [core_export_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_hardening.md)
- PRD: [core_export_hardening_followup.md](/home/j/WatchTowerPlan/docs/planning/prds/core_export_hardening_followup.md)
- User request to take the repo review findings through the full traced planning and implementation flow.

## Scope Summary
- Fix dependency-correct snapshot materialization for sync output directories.
- Repair command implementation metadata emitted by the command index.
- Tighten the public export-safe boundary around repo-specific services.
- Keep planning, traceability, and validation green throughout.

## Assumptions and Constraints
- The prior export-readiness initiative remains closed.
- No new product-facing features are added in this plan.
- The hardening work should stay bounded to the three review findings.

## Current-State Context
- The repo is currently green and the prior initiative is closed.
- The three follow-up findings are localized enough to land as three bounded tasks.
- The current sync and validation command surfaces already exist, so the main execution risk is coherence rather than missing tooling.

## Internal Standards and Canonical References Applied
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): keep the hardening work modular and regression-tested.
- [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md): command metadata must stay trustworthy as a governed lookup surface.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): track this work as a separate bounded initiative.

## Proposed Technical Approach
- Add an output-directory overlay artifact source and keep sync orchestration otherwise unchanged.
- Add explicit command-family implementation metadata to parser-derived command specs.
- Move repo-specific consumers onto `watchtower_core.repo_ops.*` imports and narrow the top-level export-safe namespaces accordingly.

## Work Breakdown
1. Bootstrap the new traced initiative, acceptance contract, planning evidence, and three implementation tasks.
2. Add output-directory overlay loading for generated artifacts and add regression coverage that fails when later sync targets read stale canonical artifacts.
3. Publish explicit command-family implementation paths through parser metadata and resync the command index.
4. Move repo-specific consumers to `watchtower_core.repo_ops.*`, move aggregate repo-wide validation under `repo_ops.validation`, and stop exporting repo-specific query and sync services from top-level namespaces.
5. Close the tasks, rerun validation, and close the initiative.

## Dependencies
- The existing repo-ops split from the closed export-readiness initiative.
- Current sync orchestration and CLI family registration.
- Current planning and traceability tracking surfaces.

## Risks
- Snapshot overlay behavior must not hide missing-output bugs by silently swallowing load failures.
- Public-boundary cleanup could require broad import updates in tests and CLI wiring.

## Validation Plan
- Run `./.venv/bin/watchtower-core sync all --write --format json` after planning or governed-surface changes.
- Run `./.venv/bin/pytest -q`, `./.venv/bin/mypy src`, `./.venv/bin/ruff check .`, `./.venv/bin/watchtower-core validate all --format json`, and `./.venv/bin/watchtower-core doctor --format json` after each code slice.
- Add targeted tests for stale-canonical snapshot regression, command implementation-path accuracy, and top-level export boundary expectations.

## Rollout or Migration Plan
- Land one commit for the planning bootstrap.
- Land one commit per implementation slice where the change set is coherent on its own.
- Close the initiative in a final planning-only commit after the repo is green.

## References
- [core_export_hardening_followup.md](/home/j/WatchTowerPlan/docs/planning/prds/core_export_hardening_followup.md)
- [core_export_hardening.md](/home/j/WatchTowerPlan/docs/planning/design/features/core_export_hardening.md)

## Updated At
- `2026-03-10T15:24:07Z`
