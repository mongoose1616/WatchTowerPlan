# AGENTS.md

## Role
- Treat this file as the instruction layer for `core/workflows/**`.
- Use it for authoritative reusable-core workflow docs, shared workflow modules, and shared workflow roles.

## Scope
- Applies to `core/workflows/**`.
- Inherit [AGENTS.md](/AGENTS.md) first.

## Routing
- Use [ROUTING_TABLE.md](/core/workflows/ROUTING_TABLE.md) for reusable-core and generic engineering route selection.

## Local Rules
- Treat `core/docs/foundations/repository_scope.md`, `core/docs/standards/workflows/routing_and_context_loading_standard.md`, and the authoritative routing tables as the contract for workflow-root boundaries and routing behavior.
- Keep this subtree focused on reusable-core shared workflow guidance.
- Keep shared modules stable enough for plan-domain routes to reference without duplicating them.

## Do
- Keep reusable shared workflow modules and shared workflow roles authoritative here when they are not plan-specific.

## Do Not
- Do not reintroduce repo-root `/workflows` as the authoritative backend for modules owned here.
