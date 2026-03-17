# AGENTS.md

## Role
- Treat this file as the instruction layer for `core/workflows/**`.
- Use it for core-owned workflow entrypoint docs and migration guidance only.

## Scope
- Applies to `core/workflows/**`.
- Inherit [AGENTS.md](/home/j/WatchTowerPlan/AGENTS.md) first.

## Routing
- Use [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md) for actual route selection until workflow authority moves here.
- Do not duplicate the canonical workflow modules in this subtree during the current migration step.

## Local Rules
- Treat `requirements.md` and `decisions.md` as the authoritative contract for workflow-root migration.
- Keep this subtree focused on core-owned workflow entrypoint guidance and router surfaces.
- Point to the canonical backend under `workflows/` until a later slice moves that authority explicitly.

## Do
- Keep migration status explicit when a core workflow surface is a router instead of the backend source of truth.

## Do Not
- Do not treat `core/workflows/**` as the canonical routing backend until the migration explicitly moves that authority.
