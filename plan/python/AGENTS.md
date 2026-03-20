# AGENTS.md

## Role
- This file applies to the [plan/python](/plan/python) subtree.
- Use it for plan-domain Python instructions that sit on top of the repository and plan-root instruction layers.

## Scope
- Applies to `plan/python/**`.
- Inherit the repository root [AGENTS.md](/AGENTS.md), [plan/AGENTS.md](/plan/AGENTS.md), and [core/python/AGENTS.md](/core/python/AGENTS.md) first.

## Local Rules
- Treat `plan/python/src/watchtower_plan/**` as the approved plan-owned Python boundary for repo-local planning behavior.
- Keep this boundary narrow. Only place code here when it is truly plan-specific and should not live in reusable core.
- Import shared loaders, validators, query helpers, and utilities from `core/python/src/watchtower_core/**` instead of copying them into `watchtower_plan`.
- Keep reusable logic out of `watchtower_plan` when it fits a reusable-core boundary under `core/python/src/watchtower_core/**`.
- Use the shared environment and tooling rooted at `core/python/`; do not create a separate `plan/python/.venv`.
- Keep `plan/python/README.md` and package-level READMEs aligned when plan-domain module ownership changes materially.
- Keep plan-domain source out of `.wt/`; that tree is reserved for machine state, not runtime implementation.

## Do Not
- Do not reintroduce plan-domain runtime under `watchtower_core.plan_runtime`.
- Do not put pack-agnostic helpers in `watchtower_plan` just because the immediate caller is plan-owned.
- Do not mirror `watchtower_core` structure under `watchtower_plan` just to create plan-flavored duplicates.
