# AGENTS.md

## Role
- Treat this file as the instruction layer for `plan/**`.
- Use it for live plan-domain work, plan-root navigation, and plan-scoped authority boundaries.

## Scope
- Applies to `plan/**` unless a more-specific `AGENTS.md` exists below this path.
- Inherit the repository root [AGENTS.md](/AGENTS.md) first and do not weaken it here.

## Routing
- Read this file after the repository root [AGENTS.md](/AGENTS.md) when working under `plan/**`.
- Use [ROUTING_TABLE.md](/plan/workflows/ROUTING_TABLE.md) to select plan-domain workflow modules.
- Shared reusable modules referenced by plan routes live under `core/workflows/modules/`; plan-specific modules live under `plan/workflows/modules/`.
- Do not turn this file into a second routing table.

## Local Rules
- Treat the mirrored foundations under [plan/docs/foundations/](/plan/docs/foundations/), promoted plan standards under [plan/docs/standards/](/plan/docs/standards/), and live plan-pack machine authority under `plan/.wt/**` as the authoritative implementation directions for live `plan/**` work.
- Use standards, references, promoted guidance, and purge history only where they remain consistent with those current authority surfaces.
- Use [README.md](/plan/README.md) as the quick reference for plan-root purpose and entrypoints before broader scans.
- Treat `plan/.wt/` as the authoritative machine root for live plan-pack state.
- Treat `plan/docs/**` as durable promoted guidance, not live execution state.
- Treat `plan/plan_overview.md` and initiative-local rendered views as derived human surfaces, not manual authority.
- Treat `plan/tracking/**` as the browsable derived tracker family for live planning state.
- Use `plan/python/**` only for plan-specific code that should not live in reusable core.
- Treat `plan/workflows/README.md` as the human workflow entrypoint for live plan-domain procedures.
- Treat `.wt/` trees as machine-state roots only. Do not place Python source, workflow prose, or other hand-maintained runtime code inside them.
- Use promoted guidance, closed initiative packages, and purge records for historical context. The legacy docs-backed planning corpus no longer exists as a working repository surface.

## Do
- Keep new live plan work under `plan/initiatives/**` or `plan/projects/**/initiatives/**` as appropriate.
- Keep authored and machine-readable plan surfaces aligned in the same change when one depends on the other.
- Apply the nested instruction files under `plan/docs/**` and `plan/python/**` when work enters those owned boundaries.

## Do Not
- Do not recreate the legacy docs-backed planning corpus or any other docs-backed planning authority surface.
- Do not place `README.md` or `AGENTS.md` files inside machine-only `.wt/` trees.
- Do not duplicate generic reusable logic into `plan/**` when `core/**` already owns the reusable boundary.
