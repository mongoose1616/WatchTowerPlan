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
- Use [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md) to select the minimum workflow modules required for the task.
- Always load `workflows/modules/core.md` plus only the additional modules required by the matched task type.
- If the request explicitly includes the keyword `no_route`, bypass routing-table lookup and handle the task directly with only the immediately relevant local context.
- Do not turn this file into a second routing table.

## Local Rules
- If work is happening under [docs](/home/j/WatchTowerPlan/docs), also apply [docs/AGENTS.md](/home/j/WatchTowerPlan/docs/AGENTS.md).
- If work is happening under [core/python](/home/j/WatchTowerPlan/core/python), also apply [core/python/AGENTS.md](/home/j/WatchTowerPlan/core/python/AGENTS.md).
- Use the nearest applicable [README.md](/home/j/WatchTowerPlan/README.md) as the quick reference for directory purpose and file inventory before doing broader scans.
- Keep durable documentation in `docs/`, workflow routing and task procedures in `workflows/`, and future shared implementation assets in `core/`.
- Treat `core/python/` as the canonical Python workspace for package code, tests, tooling, and local virtual-environment usage.
- During any non-documentation workflow, if a documentation gap is discovered, update adjacent docs in the same change when needed for coherence, otherwise load the minimum documentation workflow needed to close the gap or record explicit follow-up work if it is deferred.

## Do
- Follow the routed workflow modules for task execution.
- Use the nearest applicable [README.md](/home/j/WatchTowerPlan/README.md) as the quick reference before broader scans.
- Apply [docs/AGENTS.md](/home/j/WatchTowerPlan/docs/AGENTS.md) when work falls under `docs/**`.

## Do Not
- Do not bypass [ROUTING_TABLE.md](/home/j/WatchTowerPlan/workflows/ROUTING_TABLE.md) when selecting workflow modules.
- Do not place durable documentation outside `docs/` or workflow procedures outside `workflows/`.
