---
trace_id: trace.post_rewrite_core_cleanup_and_surface_reduction
id: design.features.post_rewrite_core_cleanup_and_surface_reduction
title: Post-Rewrite Core Cleanup and Surface Reduction Feature Design
summary: Defines the technical design boundary for Post-Rewrite Core Cleanup and Surface
  Reduction.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-16T06:28:27Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/repo_ops/validation/
- docs/standards/engineering/python_workspace_standard.md
---

# Post-Rewrite Core Cleanup and Surface Reduction Feature Design

## Record Metadata
- `Trace ID`: `trace.post_rewrite_core_cleanup_and_surface_reduction`
- `Design ID`: `design.features.post_rewrite_core_cleanup_and_surface_reduction`
- `Design Status`: `active`
- `Linked PRDs`: `prd.post_rewrite_core_cleanup_and_surface_reduction`
- `Linked Decisions`: `decision.post_rewrite_core_cleanup_and_surface_reduction_direction`
- `Linked Implementation Plans`: `design.implementation.post_rewrite_core_cleanup_and_surface_reduction`
- `Updated At`: `2026-03-16T06:28:27Z`

## Summary
Defines the technical design boundary for Post-Rewrite Core Cleanup and Surface Reduction.

## Source Request
- Full repository review focused on code and rewrite leftovers after the core-pack restructuring.

## Scope and Feature Boundary
- Covers the broken workspace-standard integration contract, the declaration-driven `PackContext` startup defect, and the first proven-unused inventory-only governed family found in the current review loop.
- Excludes a wholesale planning-system replacement, broader ledger removal beyond the first proven-unused family, and terminology changes made only to match STEP1 naming.

## Current-State Context
- The current repository review confirmed that full `pytest` fails on a stale documentation assertion and that the new pack startup path is only generic for repository-default surface paths.
- The cleanup must preserve the current default repository behavior while reducing maintenance on no-value retained surfaces rather than adding more compatibility scaffolding.

## Foundations References Applied
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md): temporary migration aids should retire once the intended boundary is clear.
- [repository_standards_posture.md](/home/j/WatchTowerPlan/docs/foundations/repository_standards_posture.md): code, docs, schemas, registries, and tests must move together when a governed boundary changes.

## Internal Standards and Canonical References Applied
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): the rewritten workspace contract must stay consistent with default validation entrypoints and current runtime-boundary wording.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/README.md): pack settings are the reusable-core startup root, so required-surface loading must follow declared paths.
- [all.py](/home/j/WatchTowerPlan/core/python/src/watchtower_core/repo_ops/validation/all.py): aggregate validation is the active enforcement path for governed artifact families and should not keep dead surfaces alive without runtime value.

## Design Goals and Constraints
- Keep the current default repository behavior green while repairing the rewrite regressions.
- Retire only surfaces that a code-and-consumer audit proves unused; do not delete broader retained families opportunistically.
- Preserve fail-closed startup and validation behavior when declared pack surfaces are missing, wrong-typed, or otherwise invalid.

## Options Considered
### Option 1
- Keep the current loader constants and patch around them with more default-path assumptions.
- Minimizes immediate code churn.
- Keeps the reusable-core startup story repo-specific and does not reduce rewrite leftovers.

### Option 2
- Introduce one declaration-driven typed-surface resolution path and pair it with explicit retirement of the first proven-unused governed family.
- Aligns the runtime boundary with pack settings and reduces maintenance load at the same time.
- Requires coordinated updates across code, tests, registries, schemas, and docs.

## Recommended Design
### Architecture
- Reconcile the workspace-standard wording and the integration test so the current guardrail boundary is asserted consistently.
- Route required `PackContext` surfaces through one typed resolution path keyed by declaration metadata instead of by repository-default path alone.
- Audit the repository-manifest family for runtime consumers and retire it when the audit stays empty, repairing validator, schema-catalog, documentation, and derived-surface references in the same slice.

### Data and Interface Impacts
- `core/python/src/watchtower_core/control_plane/loader.py` and `pack_context.py` gain the generic typed-surface loading path.
- `core/python/tests/integration/test_control_plane_loader_and_foundation_contracts.py` and `core/python/tests/unit/test_pack_context.py` become the primary regression guards for the repaired boundary.
- `core/control_plane/manifests/`, `core/control_plane/registries/`, and companion docs or indexes change if the inventory-only manifest family is retired.

### Execution Flow
1. Repair the stale workspace-standard integration contract and re-establish a green `pytest` baseline.
2. Generalize required pack-surface loading and add a regression that proves relocated declared paths still materialize typed artifacts.
3. Audit, retire, and repair the first proven-unused inventory-only governed family, then rerun full validation and a confirmation-pass review.

### Invariants and Failure Cases
- The current default `pack_settings.json` must continue to load successfully without changing its declared paths.
- If a required declared surface cannot be materialized as the expected typed model, startup must still fail closed with a clear error.

## Affected Surfaces
- core/python/src/watchtower_core/control_plane/
- core/python/src/watchtower_core/repo_ops/validation/
- docs/standards/engineering/python_workspace_standard.md

## Design Guardrails
- Do not add new compatibility wrappers or alternate path aliases just to preserve dead assumptions.
- Do not retire a governed family unless the slice also removes or repairs every live validator, doc, schema, index, and test reference to it.

## Risks
- A hidden consumer could still depend on the repository-manifest family even if no in-repo code path currently references it.
- A typed-surface resolution refactor could accidentally bypass existing loader caches or validation steps if it is implemented too narrowly.

## References
- [post_rewrite_core_cleanup_and_surface_reduction.md](/home/j/WatchTowerPlan/docs/planning/prds/post_rewrite_core_cleanup_and_surface_reduction.md)
- [post_rewrite_core_cleanup_and_surface_reduction.md](/home/j/WatchTowerPlan/docs/planning/design/implementation/post_rewrite_core_cleanup_and_surface_reduction.md)
