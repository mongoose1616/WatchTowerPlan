---
trace_id: trace.core_split_compatibility_wrapper_retirement
id: design.features.core_split_compatibility_wrapper_retirement
title: Core Split Compatibility Wrapper Retirement Feature Design
summary: Defines the technical design boundary for retiring repo-specific compatibility
  wrappers before splitting out reusable core surfaces.
type: feature_design
status: active
owner: repository_maintainer
updated_at: '2026-03-16T02:06:53Z'
audience: shared
authority: authoritative
applies_to:
- core/python/src/watchtower_core/query/
- core/python/src/watchtower_core/sync/
- core/python/src/watchtower_core/validation/
- core/python/src/watchtower_core/README.md
- core/python/src/watchtower_core/query/README.md
- core/python/src/watchtower_core/sync/README.md
- core/python/src/watchtower_core/validation/README.md
- core/python/src/watchtower_core/cli/
- core/python/README.md
- core/python/tests/unit/test_repo_ops_compatibility.py
---

# Core Split Compatibility Wrapper Retirement Feature Design

## Record Metadata
- `Trace ID`: `trace.core_split_compatibility_wrapper_retirement`
- `Design ID`: `design.features.core_split_compatibility_wrapper_retirement`
- `Design Status`: `active`
- `Linked PRDs`: `prd.core_split_compatibility_wrapper_retirement`
- `Linked Decisions`: `decision.core_split_compatibility_wrapper_retirement_direction`
- `Linked Implementation Plans`: `design.implementation.core_split_compatibility_wrapper_retirement`
- `Updated At`: `2026-03-16T02:06:53Z`

## Summary
Defines the technical design boundary for retiring repo-specific compatibility wrappers before splitting out reusable core surfaces.

## Source Request
- Turn the split-prep recommendation into a concrete traced slice that removes repo-specific compatibility wrappers from export-safe namespaces.

## Scope and Feature Boundary
- Covers the repo-specific leaf wrapper modules under `watchtower_core.query`, `watchtower_core.sync`, and repo-wide aggregate validation compatibility paths.
- Covers internal import cleanup, package-boundary docs, and regression tests needed to prove the new boundary.
- Does not extract a separate package, rename `watchtower_core`, or change CLI command names.
- Does not reopen broader export-readiness architecture work beyond the compatibility-wrapper seam.

## Current-State Context
- `docs/planning/prds/core_export_readiness_and_optimization.md` and `docs/planning/prds/core_export_hardening_followup.md` both closed with the reusable-versus-`repo_ops` boundary made explicit, but they intentionally left compatibility wrappers available.
- The live package still documents `watchtower_core.query` and `watchtower_core.sync` as boundary-layer compatibility namespaces, and the directory trees still include multiple wrapper modules that forward directly to `repo_ops`.
- Representative examples remain one-line re-exports: `core/python/src/watchtower_core/query/commands.py`, `core/python/src/watchtower_core/sync/command_index.py`, and `core/python/src/watchtower_core/validation/all.py`.
- `core/python/tests/unit/test_repo_ops_compatibility.py` still asserts that those legacy wrapper imports remain available, which preserves extraction debt instead of proving a clean split-ready boundary.

## Foundations References Applied
- `docs/foundations/repository_scope.md`: reusable-core and repo-local behavior must stay explicitly separated.
- `docs/foundations/product_direction.md`: future product work should inherit a clean shared substrate instead of repo-specific forwarding surfaces.
- `docs/foundations/engineering_design_principles.md`: the boundary should be explicit, inspectable, and deterministic.

## Internal Standards and Canonical References Applied
- `docs/standards/engineering/python_workspace_standard.md`: the cleanup stays inside the canonical Python workspace and updates workspace guidance when import expectations change.
- `docs/standards/engineering/engineering_best_practices_standard.md`: use thin boundaries, explicit imports, and targeted regression coverage.
- `docs/standards/governance/task_tracking_standard.md`: record the wrapper-retirement slice as bounded task work instead of implied cleanup.
- `docs/standards/governance/traceability_standard.md`: link the new boundary proof back to the PRD, design, plan, and tasks explicitly.

## Design Goals and Constraints
- Remove repo-specific forwarding surfaces from top-level namespaces before extraction pressure increases.
- Preserve the reusable validation API that genuinely belongs at top level.
- Avoid introducing a second compatibility package or another long-lived deprecation layer inside `watchtower_core`.

## Options Considered
### Option 1
- Keep the current compatibility wrappers indefinitely and rely on docs to explain that they are legacy-only.
- Strength: no internal import churn now.
- Tradeoff: the extracted package would still carry repo-specific forwarding debt or require another cleanup pass immediately before split-out.

### Option 2
- Split out reusable core first and keep the wrappers as deprecation shims inside the extracted package.
- Strength: defers cleanup until extraction time.
- Tradeoff: publishes the wrong public surface and makes the first extracted package boundary intentionally muddy.

### Option 3
- Retire the repo-specific leaf wrappers now, update internal imports to `repo_ops`, and leave only reusable services or explicit guardrails at top level.
- Strength: creates the cleanest pre-extraction boundary with the smallest conceptual ambiguity.
- Tradeoff: requires coordinated import, test, and doc cleanup in one bounded slice.

## Recommended Design
### Architecture
- Keep `watchtower_core.query` and `watchtower_core.sync` only as guardrail package roots if those roots still serve value; remove repo-specific leaf wrapper modules beneath them.
- Keep `watchtower_core.validation` as the reusable validation namespace, but retire `watchtower_core.validation.all` and any repo-local document-semantics forwarding that does not belong in the extracted core surface.
- Move all repo-local callers and tests to direct `watchtower_core.repo_ops.*` imports or to genuinely reusable validator modules.
- Replace the legacy compatibility test with boundary-proof coverage that fails when repo-specific wrapper modules or re-exports come back.

### Data and Interface Impacts
- Internal import paths change for repo-local callers and tests.
- Package README guidance changes from “compatibility wrappers exist” to “repo-local behavior imports from `repo_ops` directly.”
- No CLI payload, control-plane schema, or command ID changes are intended.

### Execution Flow
1. Inventory the remaining repo-specific wrapper modules and direct callers that still depend on them.
2. Update repo-local code and tests to use `repo_ops` or reusable validation surfaces directly.
3. Remove the retired wrapper modules, tighten package-boundary docs, and add fail-closed boundary tests before validation closeout.

### Invariants and Failure Cases
- Repo-specific behavior must not remain reachable through an export-safe leaf module after the refactor.
- Reusable validation services that are actually cross-repo must stay importable from `watchtower_core.validation`.
- Boundary tests must fail if a future refactor reintroduces repo-specific forwarding into top-level query, sync, or aggregate-validation surfaces.

## Affected Surfaces
- `core/python/src/watchtower_core/query/`
- `core/python/src/watchtower_core/sync/`
- `core/python/src/watchtower_core/validation/`
- `core/python/src/watchtower_core/README.md`
- `core/python/src/watchtower_core/query/README.md`
- `core/python/src/watchtower_core/sync/README.md`
- `core/python/src/watchtower_core/validation/README.md`
- `core/python/src/watchtower_core/cli/`
- `core/python/README.md`
- `core/python/tests/unit/test_repo_ops_compatibility.py`

## Design Guardrails
- Do not add a new compatibility namespace just to preserve the old import paths.
- Do not move truly reusable validation services under `repo_ops` by accident while retiring repo-specific wrappers.
- Do not broaden this slice into package extraction, release engineering, or command-surface redesign.

## Risks
- Hidden internal imports may still depend on the wrapper paths and only show up during targeted test runs.
- Boundary docs can drift if the code cleanup and README changes land separately.
- Retiring `validation.document_semantics` or similar wrappers may expose disagreement about which validators are actually reusable.

## References
- `docs/planning/prds/core_split_compatibility_wrapper_retirement.md`
- `docs/planning/prds/core_export_hardening_followup.md`
- `docs/planning/design/features/core_export_ready_architecture.md`
- `docs/planning/design/features/core_export_hardening.md`
- `core/python/src/watchtower_core/README.md`
