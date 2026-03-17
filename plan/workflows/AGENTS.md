# AGENTS.md

## Role
- Treat this file as the instruction layer for `plan/workflows/**`.
- Use it for plan-domain workflow entrypoint docs and migration guidance only.

## Scope
- Applies to `plan/workflows/**`.
- Inherit [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md) and [AGENTS.md](/home/j/WatchTowerPlan/plan/AGENTS.md) first.

## Routing
- Use [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md) for actual route selection.
- Do not duplicate the routing table or workflow module bodies here.

## Local Rules
- Use [README.md](/home/j/WatchTowerPlan/plan/workflows/README.md) as the quick reference before broader scans.
- Keep this subtree focused on plan-domain workflow entrypoint guidance and migration notes.
- Point to the canonical workflow modules under `workflows/modules/` until a later slice moves them.
- Keep [ROUTING_TABLE.md](/home/j/WatchTowerPlan/plan/workflows/ROUTING_TABLE.md) and `modules/README.md` aligned with the current migration boundary when this subtree changes.

## Do
- Route readers toward the current canonical routing backend and the live `plan/**` authority surfaces together.
- Keep migration status explicit when a plan workflow surface is an entrypoint rather than the backend source of truth.

## Do Not
- Do not copy workflow module content into this subtree just to mirror `workflows/modules/`.
- Do not treat `plan/workflows/**` as the canonical routing backend until the migration explicitly moves that authority.
