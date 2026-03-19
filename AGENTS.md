# AGENTS.md

## Role
- Treat this file as the repository-wide instruction layer.
- Apply these rules across the repository unless a more-specific `AGENTS.md` adds tighter local constraints.
- Use routed workflow modules for task behavior and nested `AGENTS.md` files for subtree-local rules.

## Scope
- Applies to the entire repository unless a more-specific `AGENTS.md` exists below the current path.
- A nested `AGENTS.md` adds local guidance for its subtree rather than replacing this file.
- More-specific `AGENTS.md` files must not weaken repository-wide safety, governance, or framing rules.

## Routing
- Read this file first.
- Select workflow modules from the domain-owned routing tables under [core/workflows/ROUTING_TABLE.md](/core/workflows/ROUTING_TABLE.md) and [plan/workflows/ROUTING_TABLE.md](/plan/workflows/ROUTING_TABLE.md).
- For reusable-core or generic engineering work, start with `core/workflows/ROUTING_TABLE.md` and always load `core/workflows/modules/core.md` plus only the additional modules required by the matched task type.
- For live planning, initiative, project, promotion, or plan-pack governance work, use `plan/workflows/ROUTING_TABLE.md` and merge any shared reusable modules referenced from `core/workflows/modules/`.
- Workflow modules are repository-available building blocks, but they are not active unless routing selects them or the active task explicitly merges them.
- Route from the full prompt context rather than exact keyword matching alone. If multiple task types or domain roots apply, load the minimum union of their module sets.
- If the request explicitly includes commit creation or closeout intent, merge `core/workflows/modules/commit_closeout.md` into the dominant route or use the Commit Closeout route alone when commit creation is the only requested task.
- If the request explicitly includes the keyword `no_route`, bypass routing-table lookup and handle the task directly with only the immediately relevant local context.
- Do not turn this file into a second routing table.

## Local Rules
- Treat [requirements.md](/requirements.md) and [decisions.md](/decisions.md) as the authoritative implementation directions and details until that contract is fully implemented.
- Use existing standards, references, and helper docs only where they support or conform to [requirements.md](/requirements.md) and [decisions.md](/decisions.md); do not let them materially change what those two files decided.
- If work is happening under [core/docs](/core/docs), also apply [core/docs/AGENTS.md](/core/docs/AGENTS.md).
- If work is happening under [plan/docs](/plan/docs), also apply [plan/docs/AGENTS.md](/plan/docs/AGENTS.md).
- If work is happening under [core/python](/core/python), also apply [core/python/AGENTS.md](/core/python/AGENTS.md).
- Use the nearest applicable [README.md](/README.md) as the quick reference for directory purpose and file inventory before doing broader scans.
- Keep durable documentation only in `core/docs/` and `plan/docs/` according to ownership. Treat `core/docs/foundations/` as the authored foundations source and `plan/docs/foundations/` as its required mirror.
- Treat `plan/**` as the only live planning workspace. The old docs-backed planning corpus has been purged; use `core/control_plane/ledgers/purges/**` only when you need the machine purge history for removed traces.
- Treat [core/control_plane](/core/control_plane/README.md) as the canonical, versioned, machine-readable authority. Keep authored schemas, registries, contracts, policies, indexes, examples, and ledgers there rather than in ad hoc JSON or Python constants.
- Treat `core/python/` as the canonical Python workspace for package code, tests, tooling, and local virtual-environment usage.
- Keep human-readable and machine-readable companion surfaces aligned in the same change set when one depends on the other. Examples include planning docs plus tracking indexes, command docs plus command indexes, and schema changes plus examples, schema catalog, validator registry entries, and tests.
- Prefer machine-readable control-plane surfaces for deterministic lookup when they exist, and use prose docs for narrative context, rationale, and operator guidance.
- When the main question is live planning state, next work, or repo coordination, start with `plan/.wt/indexes/coordination_index.json` and the derived `plan/plan_overview.md`.
- Use `plan/docs/**`, `plan/tracking/**`, and `core/control_plane/ledgers/purges/**` for retained planning guidance, human trackers, and purge history. Do not recreate docs-backed planning families.
- During any non-documentation workflow, if a documentation gap is discovered, update adjacent docs in the same change when needed for coherence, otherwise load the minimum documentation workflow needed to close the gap or record explicit follow-up work if it is deferred.
- When code, commands, schemas, or governed artifacts may have drifted from companion docs or machine-readable lookup surfaces, use the documentation-implementation reconciliation workflow or record why no explicit reconciliation pass was needed.
- When traced planning or governance artifacts may have drifted from their companion trackers, family-specific indexes, or unified traceability joins, use the traceability reconciliation workflow or record why no explicit reconciliation pass was needed.
- When schema-backed governed artifacts may have drifted from companion schemas, examples, indexes, registries, or loader and validator assumptions, use the governed artifact reconciliation workflow or record why no explicit reconciliation pass was needed.

## Do
- Follow the routed workflow modules for task execution.
- Keep implementation choices aligned to [requirements.md](/requirements.md) and [decisions.md](/decisions.md) when companion guidance disagrees or is incomplete.
- Use the nearest applicable [README.md](/README.md) as the quick reference before broader scans.
- Apply [core/docs/AGENTS.md](/core/docs/AGENTS.md) when work falls under `core/docs/**`.
- Apply [plan/docs/AGENTS.md](/plan/docs/AGENTS.md) when work falls under `plan/docs/**`.
- Prefer structured command output such as `--format json` for agent or workflow use when a command supports it.
- Use the live `plan/**` coordination index and rendered overview as the default repo-level planning entrypoints before opening deeper planning families.
- Update adjacent indexes, trackers, examples, and validation surfaces when a governed document or control-plane artifact changes materially.

## Do Not
- Do not bypass the domain-owned routing tables under [core/workflows/ROUTING_TABLE.md](/core/workflows/ROUTING_TABLE.md) and [plan/workflows/ROUTING_TABLE.md](/plan/workflows/ROUTING_TABLE.md) when selecting workflow modules.
- Do not treat older supporting standards, references, or legacy planning docs as authority when they conflict materially with [requirements.md](/requirements.md) or [decisions.md](/decisions.md).
- Do not place durable documentation outside `core/docs/` and `plan/docs/`, or workflow procedures outside `core/workflows/` and `plan/workflows/`.
- Do not store mutable runtime state, caches, or transient event streams under `core/control_plane/`.
- Do not add parallel Python package roots or alternate virtual-environment conventions outside `core/python/`.
- Do not leave companion machine-readable lookup or validation surfaces stale when their governing human or machine authority changed in the same task.
