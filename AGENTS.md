# AGENTS.md

## Role
- Treat this file as the repository-wide instruction layer.
- Apply these rules across the repository unless a more-specific `AGENTS.md` adds tighter local constraints.
- Use routed workflow modules for task behavior and nested `AGENTS.md` files for subtree-local rules.
- Keep this file focused on repository-wide authority, routing, and path ownership. Put detailed procedures in workflow modules and local subtree rules in nested `AGENTS.md` files.

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

## Repository Map
- `core/` is the shared implementation and authored machine-governed asset root.
- `core/control_plane/` is the canonical authored machine-readable authority for schemas, registries, contracts, policies, examples, indexes, and retained records.
- `core/docs/` is the shared and core-owned durable documentation root, including the authored foundations source under `core/docs/foundations/`.
- `core/python/` is the canonical shared Python workspace for reusable package code, tests, tooling, and the local virtual environment.
- `plan/` is the live plan-domain workspace.
- `plan/.wt/` is the machine-state root for the live plan pack. Keep it machine-only.
- `plan/docs/` is the durable plan-domain documentation root plus the required mirror of `core/docs/foundations/`.
- `plan/python/` is the approved plan-owned Python boundary for plan-specific code that should not live in reusable core.
- `plan/tracking/` and `plan/plan_overview.md` are derived human planning surfaces, not manual authority.

## Local Rules
- Treat the authored foundations under [core/docs/foundations/](/core/docs/foundations/), repository-wide standards under [core/docs/standards/](/core/docs/standards/), plan-domain standards under [plan/docs/standards/](/plan/docs/standards/), and authored machine-readable authority under [core/control_plane](/core/control_plane/README.md) plus `plan/.wt/**` as the current repository contract.
- When guidance disagrees, prefer this precedence order: current machine-readable authority for deterministic state and rules, then current foundations and standards, then supporting references and helper docs.
- When the main question is which surface is canonical, use `watchtower-core query authority` first, then the narrow index-backed query command for the resolved family, then the exact canonical doc or registry, and only then raw repo search such as `rg` when no governed lookup surface exists or when verifying unindexed implementation detail.
- Before drafting or materially restructuring a governed document, use `watchtower-core query templates` plus the relevant family standard or catalog entry instead of inventing document shape from scratch.
- Distinguish observed current-state facts from inference, local policy, and open questions when writing analysis, standards, references, workflow outputs, or closeout guidance.
- If work is happening under [core/docs](/core/docs), also apply [core/docs/AGENTS.md](/core/docs/AGENTS.md).
- If work is happening under [plan/docs](/plan/docs), also apply [plan/docs/AGENTS.md](/plan/docs/AGENTS.md).
- If work is happening under [plan](/plan), also apply [plan/AGENTS.md](/plan/AGENTS.md).
- If work is happening under [core/python](/core/python), also apply [core/python/AGENTS.md](/core/python/AGENTS.md).
- Use the nearest applicable [README.md](/README.md) as the quick reference for directory purpose and file inventory before doing broader scans.
- Keep durable documentation only in `core/docs/` and `plan/docs/` according to ownership. Treat `core/docs/foundations/` as the authored foundations source and `plan/docs/foundations/` as its required mirror.
- Treat `plan/**` as the only live planning workspace. The old docs-backed planning corpus has been purged; do not recreate separate purge-history ledgers for removed traces.
- Treat [core/control_plane](/core/control_plane/README.md) as the authored, versioned machine-readable authority. Treat `plan/.wt/**` as live machine state for the plan pack. Do not blur those roles.
- Treat `core/python/` as the canonical shared Python tooling, test, and local virtual-environment workspace. Use `plan/python/**` only for plan-specific code that should not live in reusable core.
- Treat `watchtower-core pack export` as the canonical customer-release and customer-bootstrap handoff path. Do not treat a raw worktree or a manually cleaned working repository as a shippable artifact.
- Keep human-readable and machine-readable companion surfaces aligned in the same change set when one depends on the other. Examples include planning docs plus tracking indexes, command docs plus command indexes, and schema changes plus examples, schema catalog, validator registry entries, and tests.
- Prefer machine-readable control-plane surfaces for deterministic lookup when they exist, and use prose docs for narrative context, rationale, and operator guidance.
- When the main question is live planning state, next work, or repo coordination, start with `plan/.wt/indexes/coordination_index.json` and the derived `plan/plan_overview.md`.
- Use `plan/docs/**` and `plan/tracking/**` for retained planning guidance and human trackers. Do not recreate docs-backed planning families or separate purge-history ledgers.
- When a question is about reusable behavior, loaders, schemas, validators, or generic tooling, start in `core/**`. When it is about plan-specific workflows, initiative packages, or plan-owned orchestration, start in `plan/**`.
- During any non-documentation workflow, if a documentation gap is discovered, update adjacent docs in the same change when needed for coherence, otherwise load the minimum documentation workflow needed to close the gap or record explicit follow-up work if it is deferred.
- When code, commands, schemas, or governed artifacts may have drifted from companion docs or machine-readable lookup surfaces, use the documentation-implementation reconciliation workflow or record why no explicit reconciliation pass was needed.
- When traced planning or governance artifacts may have drifted from their companion trackers, family-specific indexes, or unified traceability joins, use the traceability reconciliation workflow or record why no explicit reconciliation pass was needed.
- When schema-backed governed artifacts may have drifted from companion schemas, examples, indexes, registries, or loader and validator assumptions, use the governed artifact reconciliation workflow or record why no explicit reconciliation pass was needed.

## Do
- Follow the routed workflow modules for task execution.
- Keep implementation choices aligned to the current foundations, standards, and machine-readable authority surfaces when companion guidance disagrees or is incomplete.
- Use the nearest applicable [README.md](/README.md) as the quick reference before broader scans.
- Use governed lookup surfaces and template-catalog data before reopening large directory trees or rediscovering already-indexed repository facts manually.
- Apply [core/docs/AGENTS.md](/core/docs/AGENTS.md) when work falls under `core/docs/**`.
- Apply [plan/docs/AGENTS.md](/plan/docs/AGENTS.md) when work falls under `plan/docs/**`.
- Apply [plan/AGENTS.md](/plan/AGENTS.md) when work falls anywhere under `plan/**`.
- Prefer structured command output such as `--format json` for agent or workflow use when a command supports it.
- Use the live `plan/**` coordination index and rendered overview as the default repo-level planning entrypoints before opening deeper planning families.
- Update adjacent indexes, trackers, examples, and validation surfaces when a governed document or control-plane artifact changes materially.
- Keep reusable core behavior in `core/**` and plan-only behavior in `plan/**`. Consolidate duplicated logic instead of creating parallel implementations.

## Do Not
- Do not bypass the domain-owned routing tables under [core/workflows/ROUTING_TABLE.md](/core/workflows/ROUTING_TABLE.md) and [plan/workflows/ROUTING_TABLE.md](/plan/workflows/ROUTING_TABLE.md) when selecting workflow modules.
- Do not treat retained history, supporting references, or older planning docs as authority when current foundations, standards, or machine-readable control-plane surfaces already publish the living rule.
- Do not use raw repo search to rediscover authority, command, standards, workflow, reference, or template answers that current governed lookup surfaces already publish.
- Do not improvise governed document structure when an active template, registry entry, or family standard already defines the required shape.
- Do not present inference, recommendation, or open questions as if they were observed current-state facts.
- Do not place durable documentation outside `core/docs/` and `plan/docs/`, or workflow procedures outside `core/workflows/` and `plan/workflows/`.
- Do not store mutable runtime state, caches, or transient event streams under `core/control_plane/`.
- Do not add unapproved parallel Python package roots or alternate virtual-environment conventions outside `core/python/`. The approved exception is the plan-domain package root under `plan/python/**`.
- Do not put hand-maintained prose, workflow guidance, or Python source inside `.wt/` trees.
- Do not duplicate generic reusable logic into `plan/python/**` just to make it plan-flavored.
- Do not treat a live portability scan over an actively used workspace as a substitute for a fresh staged export when the intent is customer handoff.
- Do not leave companion machine-readable lookup or validation surfaces stale when their governing human or machine authority changed in the same task.
