# AGENTS.md

## Role
- Treat this file as the instruction layer for `core/workflows/**`.
- Use it for authoritative reusable-core workflow docs and shared workflow modules.

## Scope
- Applies to `core/workflows/**`.
- Inherit [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md) first.

## Routing
- Use [ROUTING_TABLE.md](/home/j/WatchTowerPlan/core/workflows/ROUTING_TABLE.md) for reusable-core and generic engineering route selection.

## Local Rules
- Treat `requirements.md` and `decisions.md` as the authoritative contract for workflow-root migration.
- Keep this subtree focused on reusable-core shared workflow guidance.
- Keep shared modules stable enough for plan-domain routes to reference without duplicating them.

## Do
- Keep reusable shared workflow modules authoritative here when they are not plan-specific.

## Do Not
- Do not reintroduce repo-root `/workflows` as the authoritative backend for modules owned here.
