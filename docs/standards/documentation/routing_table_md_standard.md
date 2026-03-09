---
id: "std.documentation.routing_table_md"
title: "ROUTING_TABLE.md Standard"
summary: "This standard defines the structure and expected content of `ROUTING_TABLE.md` as the canonical task-to-workflow routing surface for the repository."
type: "standard"
status: "active"
tags:
  - "standard"
  - "documentation"
  - "routing_table_md"
owner: "repository_maintainer"
updated_at: "2026-03-09T23:02:08Z"
audience: "shared"
authority: "authoritative"
---

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

## Related Standards and Sources
- [agents_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/agents_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [routing_table_template.md](/home/j/WatchTowerPlan/docs/templates/routing_table_template.md): authoring scaffold that should stay aligned with this standard.
## Guidance
- `ROUTING_TABLE.md` must be the canonical routing index for workflow selection.
- The file should stay compact and table-first rather than turning into a long narrative document.
- Each row should represent one task type with one clear routing outcome.
- Trigger keywords should be broad enough to be useful but specific enough to avoid frequent false matches.
- Trigger keywords are examples, not the only allowed routing surface. Routing may infer the nearest task type from the full prompt context.
- Required workflows should list only the minimum modules needed for the task type.
- The routing table should always include the shared core workflow module in routed task sets.
- Workflow modules that are not selected by routing remain available but inactive.
- If a task spans multiple task types, routing should union only the minimum relevant module sets.
- The short instruction block may include compact merge rules for common compound cases such as commit intent, documentation gaps, or reconciliation routes, as long as the file stays table-first.
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
- Common compound requests such as `implement and commit` or `refresh docs and commit` should have an unambiguous merge outcome without requiring one custom row per combination.

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

## Updated At
- `2026-03-09T23:02:08Z`
