# AGENTS.md

> Use this template for root-level or nested `AGENTS.md` files.
> Keep the file concise.
> Use it as a thin instruction layer for the current directory, not as a full operating manual.
> Root files should point to the canonical routing surface.
> Nested files should add only subtree-local rules and must not weaken parent instructions.
> When instantiating this template, remove template-authoring language and rewrite the file as active instructions for the current scope.
> Every retained bullet should be a live rule for the current scope. Replace generic filler with scope-specific instructions or delete the section.
> Delete any section that does not help the current scope.

## Role
- This file applies to `<scope>`.
- Describe what this scope governs and what instructions always apply here.
- Put detailed task behavior in workflow modules, standards, or companion docs instead of expanding this file.

## Scope
- Applies to `<directory>/**`.
- If a more-specific `AGENTS.md` exists below this path, treat it as a more local overlay.
- If a parent `AGENTS.md` exists above this path, inherit it first and do not weaken it here.

## Routing
- Read this file before working in this scope.
- Use `<path/to/ROUTING_TABLE.md>` to select the minimum workflow modules required for the task.
- If this scope does not own a routing table, inherit routing from `<parent routing surface>`.
- Do not turn this file into a second routing table.

## Local Rules
- Keep rules specific to this directory and its contents.
- Use the nearest applicable `README.md` as the quick reference for directory purpose and file inventory.
- Prefer rules about scope, local paths, generated files, validation, naming, or safety boundaries.
- Reference companion standards, runbooks, or templates when they already define the detailed behavior.

## Do
- `<specific required behavior that should be followed in this scope>`
- `<specific local expectation or operating habit that should remain true after instantiation>`

## Do Not
- `<specific prohibited behavior for this scope>`
- `<specific local anti-pattern or boundary that must not be crossed>`
