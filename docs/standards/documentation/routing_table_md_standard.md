# ROUTING_TABLE.md Standard

## Summary
This standard defines the structure and expected content of `ROUTING_TABLE.md` as the canonical task-to-workflow routing surface for the repository.

## Purpose
Keep routing deterministic, minimal, and easy to maintain by giving the repository one compact table that maps request types to the minimum required workflow modules.

## Scope
- Applies to the canonical routing table file at `workflows/ROUTING_TABLE.md`.
- Covers the table structure, row design, path conventions, and routing intent.
- Does not define the detailed behavior of context loading beyond what is needed to structure the routing table itself.

## Use When
- Creating the repository routing table.
- Adding a new task type or workflow module.
- Reviewing whether routing entries are too broad, duplicated, or ambiguous.

## Guidance
- `ROUTING_TABLE.md` must be the canonical routing index for workflow selection.
- The file should stay compact and table-first rather than turning into a long narrative document.
- Each row should represent one task type with one clear routing outcome.
- Trigger keywords should be broad enough to be useful but specific enough to avoid frequent false matches.
- Required workflows should list only the minimum modules needed for the task type.
- The routing table should always include the shared core workflow module in routed task sets.
- If a task spans multiple task types, routing should union only the minimum relevant module sets.
- If a task type cannot be routed clearly in one row, it should usually be split into smaller task types.

## Structure or Data Model
- Title and one short instruction block.
- Table with these columns:
  - `Task Type`
  - `Trigger Keywords (Examples)`
  - `Required Workflows`
- Workflow paths should be written relative to the routing table location.
- For this repo, workflow module entries should use `modules/<name>.md`.

## Validation
- Every listed workflow must exist at the referenced path.
- New workflow modules that are intended for routing should be represented in the table.
- Rows should not route to a larger set of modules than the task actually needs.
- Task types with overlapping triggers should still produce clear routing behavior.

## Change Control
- Update the routing table whenever a routed workflow module is added, renamed, removed, or materially re-scoped.
- Update this standard and the routing behavior standard together if routing semantics change.

## References
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md)
- [routing_table_template.md](/home/j/WatchTowerPlan/docs/templates/routing_table_template.md)
- [agents_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/agents_md_standard.md)

## Notes
- The routing table should answer "what should be loaded?" and not "how should the task be executed?"
- Detailed logic belongs in workflow modules, not in routing rows.

## Last Synced
- `2026-03-08`
