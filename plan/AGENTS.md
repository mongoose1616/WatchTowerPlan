# AGENTS.md

## Role
- Treat this file as the instruction layer for `plan/**`.
- Use it for live plan-domain work, plan-root navigation, and plan-scoped authority boundaries.

## Scope
- Applies to `plan/**` unless a more-specific `AGENTS.md` exists below this path.
- Inherit the repository root [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md) first and do not weaken it here.

## Routing
- Read this file after the repository root [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md) when working under `plan/**`.
- Use [ROUTING_TABLE.md](/home/j/WatchTowerPlan/plan/workflows/ROUTING_TABLE.md) to select plan-domain workflow modules.
- Shared reusable modules referenced by plan routes live under `core/workflows/modules/`; plan-specific modules live under `plan/workflows/modules/`.
- Do not turn this file into a second routing table.

## Local Rules
- Treat [requirements.md](/home/j/WatchTowerPlan/requirements.md) and [decisions.md](/home/j/WatchTowerPlan/decisions.md) as the authoritative implementation directions for live `plan/**` work until that contract is fully implemented.
- Use standards, references, and legacy planning docs only where they support or conform to those two files.
- Use [README.md](/home/j/WatchTowerPlan/plan/README.md) as the quick reference for plan-root purpose and entrypoints before broader scans.
- Treat `plan/.wt/` as the authoritative machine root for live plan-pack state.
- Treat `plan/plan_overview.md` and initiative-local rendered views as derived human surfaces, not manual authority.
- Treat `plan/workflows/README.md` as the human workflow entrypoint for live plan-domain procedures.
- Use `docs/planning/**` for traced planning history and legacy corpus lookup, not for new live plan execution.

## Do
- Keep new live plan work under `plan/initiatives/**` or `plan/projects/**/initiatives/**` as appropriate.
- Keep authored and machine-readable plan surfaces aligned in the same change when one depends on the other.

## Do Not
- Do not create new live execution artifacts under `docs/planning/**`.
- Do not place `README.md` or `AGENTS.md` files inside machine-only `.wt/` trees.
