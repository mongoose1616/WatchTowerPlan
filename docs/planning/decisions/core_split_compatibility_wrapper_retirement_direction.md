---
trace_id: trace.core_split_compatibility_wrapper_retirement
id: decision.core_split_compatibility_wrapper_retirement_direction
title: Core Split Compatibility Wrapper Retirement Direction Decision
summary: Records the direction decision for retiring repo-specific compatibility
  wrappers before splitting out reusable core surfaces.
type: decision_record
status: active
owner: repository_maintainer
updated_at: '2026-03-16T02:06:53Z'
audience: shared
authority: supporting
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
- core/python/tests/unit/test_repo_ops_boundary.py
---

# Core Split Compatibility Wrapper Retirement Direction Decision

## Record Metadata
- `Trace ID`: `trace.core_split_compatibility_wrapper_retirement`
- `Decision ID`: `decision.core_split_compatibility_wrapper_retirement_direction`
- `Record Status`: `active`
- `Decision Status`: `accepted`
- `Linked PRDs`: `prd.core_split_compatibility_wrapper_retirement`
- `Linked Designs`: `design.features.core_split_compatibility_wrapper_retirement`
- `Linked Implementation Plans`: `design.implementation.core_split_compatibility_wrapper_retirement`
- `Updated At`: `2026-03-16T02:06:53Z`

## Summary
Records the direction decision for retiring repo-specific compatibility wrappers before splitting out reusable core surfaces.

## Decision Statement
Retire repo-specific leaf compatibility wrappers from top-level `watchtower_core` query, sync, and aggregate-validation namespaces now, so a future reusable-core split inherits only explicit reusable surfaces and `repo_ops` remains the sole home for `WatchTowerPlan`-specific behavior.

## Trigger or Source Request
- Turn the core-split refactor recommendation into a concrete traced slice and task chain.

## Current Context and Constraints
- The earlier export-readiness traces established the `repo_ops` boundary and tightened top-level package exports, but they intentionally preserved explicit compatibility wrapper modules.
- The live code still carries representative wrappers such as `watchtower_core.query.commands`, `watchtower_core.sync.command_index`, and `watchtower_core.validation.all`.
- The cleanup must preserve genuinely reusable validation services and avoid drifting into package extraction or release engineering.

## Applied References and Implications
- `docs/planning/prds/core_export_readiness_and_optimization.md`: the reusable-versus-repo-local split is already an accepted architecture goal, so this slice should finish the leftover compatibility debt instead of reopening the broader architecture decision.
- `docs/planning/prds/core_export_hardening_followup.md`: the previous hardening slice made the public boundary more honest, which now makes wrapper retirement the right next bounded follow-up.
- `docs/foundations/repository_scope.md`: repo-specific behavior must stay explicit in this repository rather than hiding behind reusable-looking namespaces.
- `docs/foundations/product_direction.md`: future product consumers should see a clean shared core surface when extraction eventually happens.

## Affected Surfaces
- core/python/src/watchtower_core/query/
- core/python/src/watchtower_core/sync/
- core/python/src/watchtower_core/validation/
- core/python/src/watchtower_core/README.md
- core/python/src/watchtower_core/query/README.md
- core/python/src/watchtower_core/sync/README.md
- core/python/src/watchtower_core/validation/README.md
- core/python/src/watchtower_core/cli/
- core/python/README.md
- core/python/tests/unit/test_repo_ops_boundary.py

## Options Considered
### Option 1
- Keep the compatibility wrappers indefinitely and rely on docs to explain that they are not part of the future reusable boundary.
- Strength: avoids import churn now.
- Tradeoff: preserves extraction debt and keeps the wrong package surface alive.

### Option 2
- Delay wrapper retirement until the actual package split and ship the extracted package with temporary shims.
- Strength: pushes the cleanup closer to the real extraction event.
- Tradeoff: makes the first extracted boundary intentionally muddy and couples extraction work to cleanup work.

### Option 3
- Retire the wrappers now, move callers to direct `repo_ops` or reusable imports, and prove the package boundary with docs and tests.
- Strength: gives the cleanest split-ready boundary before extraction starts.
- Tradeoff: requires coordinated import, test, and doc cleanup in one bounded slice.

## Chosen Outcome
Adopt option 3. The compatibility wrappers should be retired in-repo now so the eventual reusable-core split starts from an explicit, already-proven package boundary.

## Rationale and Tradeoffs
- The architecture work that justified `repo_ops` is already complete enough that the wrappers now preserve ambiguity instead of providing migration value.
- Doing the cleanup before extraction reduces risk because it keeps the boundary work testable inside the current repository.
- The main cost is bounded internal import churn, which is smaller than coupling extraction to last-minute wrapper retirement.

## Consequences and Follow-Up Impacts
- Internal code and tests will import repo-local behavior from `watchtower_core.repo_ops.*` directly.
- Top-level package READMEs and workspace guidance will describe a smaller export-safe surface.
- If a future extracted package still needs external deprecation shims, that should be a later explicit release decision rather than an accidental carry-over from the current repo.

## Risks, Dependencies, and Assumptions
- Risk: one or more hidden callers still rely on the wrappers.
- Dependency: package-boundary tests must distinguish reusable validation exports from repo-local aggregate validation correctly.
- Assumption: the earlier `repo_ops` split is structurally strong enough that wrappers are no longer required for internal clarity.

## References
- `docs/planning/prds/core_split_compatibility_wrapper_retirement.md`
- `docs/planning/prds/core_export_hardening_followup.md`
- `docs/planning/design/features/core_export_ready_architecture.md`
