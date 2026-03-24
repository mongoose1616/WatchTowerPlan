# AGENTS.md

## Role
- Treat this file as the instruction layer for `plan/workflows/**`.
- Use it for authoritative plan-domain workflow docs, plan-owned workflow modules, and plan-owned workflow roles.

## Scope
- Applies to `plan/workflows/**`.
- Inherit [AGENTS.md](/AGENTS.md) and [AGENTS.md](/plan/AGENTS.md) first.

## Routing
- Use [ROUTING_TABLE.md](/plan/workflows/ROUTING_TABLE.md) for plan-domain route selection.
- Load shared reusable modules from `core/workflows/modules/` only when a plan route explicitly references them.

## Local Rules
- Use [README.md](/plan/workflows/README.md) as the quick reference before broader scans.
- Keep this subtree focused on plan-domain workflow guidance, route selection, and plan-owned workflow documents.
- Keep [ROUTING_TABLE.md](/plan/workflows/ROUTING_TABLE.md), `modules/README.md`, and `roles/README.md` aligned with the active authoritative workflow set.

## Do
- Route readers toward the live `plan/**` authority surfaces and the authoritative plan routing table together.
- Keep plan-specific workflow modules and workflow roles authoritative here.

## Do Not
- Do not reintroduce repo-root `/workflows` as the plan-domain routing authority.
- Do not duplicate shared reusable modules here when `core/workflows/modules/` already owns them.
- Do not use `plan/workflows/roles/` as a place to hide copied module logic that should stay reusable.
