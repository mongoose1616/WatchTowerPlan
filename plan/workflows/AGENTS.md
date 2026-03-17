# AGENTS.md

## Role
- Treat this file as the instruction layer for `plan/workflows/**`.
- Use it for authoritative plan-domain workflow docs and plan-owned workflow modules.

## Scope
- Applies to `plan/workflows/**`.
- Inherit [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md) and [AGENTS.md](/home/j/WatchTowerPlan/plan/AGENTS.md) first.

## Routing
- Use [ROUTING_TABLE.md](/home/j/WatchTowerPlan/plan/workflows/ROUTING_TABLE.md) for plan-domain route selection.
- Load shared reusable modules from `core/workflows/modules/` only when a plan route explicitly references them.

## Local Rules
- Use [README.md](/home/j/WatchTowerPlan/plan/workflows/README.md) as the quick reference before broader scans.
- Keep this subtree focused on plan-domain workflow guidance, route selection, and plan-owned modules.
- Keep [ROUTING_TABLE.md](/home/j/WatchTowerPlan/plan/workflows/ROUTING_TABLE.md) and `modules/README.md` aligned with the active authoritative module set.

## Do
- Route readers toward the live `plan/**` authority surfaces and the authoritative plan routing table together.
- Keep plan-specific workflow modules authoritative here.

## Do Not
- Do not reintroduce repo-root `/workflows` as the plan-domain routing authority.
- Do not duplicate shared reusable modules here when `core/workflows/modules/` already owns them.
