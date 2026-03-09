---
id: "std.documentation.agents_md"
title: "AGENTS.md Standard"
summary: "This standard defines the role, scope, structure, and authoring rules for `AGENTS.md` files used at the repository root and within nested directory subtrees."
type: "standard"
status: "active"
tags:
  - "standard"
  - "documentation"
  - "agents_md"
owner: "repository_maintainer"
updated_at: "2026-03-09T14:40:36Z"
audience: "shared"
authority: "authoritative"
---

# AGENTS.md Standard

## Summary
This standard defines the role, scope, structure, and authoring rules for `AGENTS.md` files used at the repository root and within nested directory subtrees.

## Purpose
Keep `AGENTS.md` files concise, scoped, and trustworthy by making them thin instruction layers for the current directory instead of catch-all manuals, duplicated workflow docs, or meta commentary about how `AGENTS.md` files are written.

## Scope
- Applies to root and nested `AGENTS.md` files in this repository.
- Covers what belongs in `AGENTS.md`, how nested files inherit from parent files, and how `AGENTS.md` should relate to `README.md`, routing tables, workflow modules, standards, and templates.
- Does not define task-specific workflow behavior in detail.

## Use When
- Creating a new root or nested `AGENTS.md`.
- Updating the structure or local rules of an existing `AGENTS.md`.
- Reviewing whether instructions belong in `AGENTS.md`, a `README.md`, a routing table, a workflow module, or a standard.

## Guidance
- `AGENTS.md` must act as a thin instruction layer for the current scope.
- Every retained bullet in an `AGENTS.md` file must be a live rule for that scope.
- `AGENTS.md` must not contain template-authoring language, placeholder text, or generic commentary about how `AGENTS.md` files should be written unless that is itself the local rule being expressed.
- Root `AGENTS.md` files should define repository-wide instruction boundaries and point to the canonical routing surface.
- Nested `AGENTS.md` files should define only subtree-local rules that materially help work in that subtree.
- Nested `AGENTS.md` files inherit parent `AGENTS.md` files and must not weaken parent safety, governance, or framing rules.
- `AGENTS.md` should point to the relevant routing surface rather than embedding full routing logic.
- Use the nearest applicable `README.md` as the quick reference for directory purpose and file inventory.
- Put detailed task behavior in routed workflow modules rather than in `AGENTS.md`.
- Put durable reference material, standards catalogs, templates, or long procedural content in the appropriate companion docs rather than in `AGENTS.md`.
- Keep `AGENTS.md` as plain Markdown by default. Do not add YAML front matter unless a narrower future rule explicitly introduces a governed `AGENTS.md` metadata profile.
- Delete any section from an instantiated `AGENTS.md` file if it does not help the current scope.

## Structure or Data Model
- Title: `# AGENTS.md`
- `## Role`
- `## Scope`
- `## Routing`
- `## Local Rules`
- `## Do`
- `## Do Not`

## Validation
- The file should read as active instructions for the current scope, not as template guidance.
- The file should be concise enough to scan quickly before work begins.
- Each bullet should express a real rule, boundary, or operating expectation for the scope where the file lives.
- The file should point to the routing surface instead of trying to reproduce full routing logic.
- The file should align with the nearest applicable `README.md` and should not contradict directory purpose or ownership boundaries.
- If the file contains large procedural sections, standards catalogs, or generic filler that could apply anywhere, it should be tightened or split.

## Change Control
- Update this standard when the repository-wide `AGENTS.md` model changes.
- Update the `AGENTS.md` template and any affected live `AGENTS.md` files in the same change set when the required structure or authoring rules change materially.
- Update related routing or documentation standards in the same change set when `AGENTS.md` precedence or directory-reference behavior changes.

## References
- [agent_template.md](/home/j/WatchTowerPlan/docs/templates/agent_template.md)
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md)
- [routing_table_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/routing_table_md_standard.md)
- [routing_and_context_loading_standard.md](/home/j/WatchTowerPlan/docs/standards/workflows/routing_and_context_loading_standard.md)

## Notes
- `AGENTS.md` is an instruction surface, not a documentation dump.
- The best `AGENTS.md` files are short, scoped, and obviously tied to the directory they govern.

## Updated At
- `2026-03-09T14:40:36Z`
