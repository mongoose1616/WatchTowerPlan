---
id: "std.documentation.command_md"
title: "Command Document Standard"
summary: "This standard defines how repository-native command reference documents are written under `docs/commands/` so humans can discover available commands, scan usage quickly, and route from a command index to durable command pages."
type: "standard"
status: "active"
tags:
  - "standard"
  - "documentation"
  - "command_md"
owner: "repository_maintainer"
updated_at: "2026-03-09T23:02:08Z"
audience: "shared"
authority: "authoritative"
---

# Command Document Standard

## Summary
This standard defines how repository-native command reference documents are written under `docs/commands/` so humans can discover available commands, scan usage quickly, and route from a command index to durable command pages.

## Purpose
Provide one consistent command-document shape for CLI and operator-facing commands without overloading README files or treating command docs as external references.

## Scope
- Applies to command reference documents stored under `docs/commands/`.
- Covers placement, required sections, naming expectations, and the relationship between command pages and the machine-readable command index.
- Does not define the machine-readable command index schema itself.

## Use When
- Adding a new durable command page for a repository command or subcommand.
- Reviewing whether a command page is structured clearly enough to act as a human-readable man page.
- Updating command docs after a command surface changes.

## Related Standards and Sources
- [readme_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/readme_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [cli_help_text_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/cli_help_text_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [command_reference_template.md](/home/j/WatchTowerPlan/docs/templates/command_reference_template.md): authoring scaffold that should stay aligned with this standard.
- [README.md](/home/j/WatchTowerPlan/docs/commands/README.md): family entrypoint and inventory surface this standard should stay aligned with.

## Guidance
- Store repository-native command docs under `docs/commands/`.
- Do not place command docs under `docs/references/`; they are local command pages, not external references.
- Keep one primary command or subcommand per document.
- Use the literal command name in the title, wrapped in backticks.
- Keep command pages human-readable first, but structured enough that a machine index can route to them reliably.
- Keep command pages as plain Markdown by default. Do not add front matter unless a later command-family rule explicitly requires it.
- Keep command docs focused on stable behavior: invocation shape, arguments, examples, outputs, and source surface.
- Link each durable command page from the machine-readable command index and from the relevant command-family README.
- Use `## Arguments and Options` even when the current command surface is small; state clearly when no command-specific arguments or options exist yet.
- When a command supports both human-readable and structured machine output, document the canonical output-mode flag and supported values explicitly.
- Prefer one `--format` option such as `--format human` or `--format json` over separate bespoke `--human` and `--json` switches.
- Prefer concise examples that match the actual workspace and onboarding contract.
- Record the implementation or source surface so engineers can move from the doc to the responsible code path quickly.
- Keep command families modular: one directory per command family and one page per command or subcommand.

## Structure or Data Model
### Placement rules
| Document Type | Canonical Location | Notes |
|---|---|---|
| Command-family entrypoint README | `docs/commands/**/README.md` | Directory orientation and local command inventory. |
| Root command page | `docs/commands/**/<command_name>.md` | Use snake_case filenames derived from the command name. |
| Subcommand page | `docs/commands/**/<command_name>_<subcommand>.md` | Keep the filename readable and stable. |

### Required sections for command pages
| Section | Requirement | Notes |
|---|---|---|
| `Summary` | Required | One short explanation of the command and its purpose. |
| `Use When` | Required | When an operator or engineer should reach for this command. |
| `Command` | Required | Table describing invocation, kind, workspace, and implementation surface. |
| `Synopsis` | Required | Short usage form in a fenced shell block. |
| `Arguments and Options` | Required | List supported args or state clearly when there are none beyond help. |
| `Examples` | Required | At least one real repository example. |
| `Behavior and Outputs` | Required | Describe the current output shape, side effects, and exit behavior. |
| `Related Commands` | Required | Point to nearby commands or command-family docs. |
| `Source Surface` | Required | Point to the implementation surface that owns the command. |
| `Updated At` | Required | Record the last meaningful content update as an RFC 3339 UTC timestamp in the form `YYYY-MM-DDTHH:MM:SSZ`. |

## Process or Workflow
1. Place the command doc under the correct command-family directory in `docs/commands/`.
2. Draft the page using the command template and required section order.
3. Update the relevant command-family README and the machine-readable command index in the same change set.
4. Verify that the documented command actually exists and that the invocation examples match the current workspace contract.
5. Treat command doc changes as incomplete if the command index or command-family inventory still points to stale paths.

## Examples
- A page for `watchtower-core` belongs under `docs/commands/core_python/watchtower_core.md`.
- A page for `watchtower-core doctor` belongs under `docs/commands/core_python/watchtower_core_doctor.md`.
- A generic Python packaging guide does not belong in `docs/commands/`; it belongs in standards, design, or foundations depending on purpose.

## Validation
- Command pages should contain the required sections in the documented order.
- The documented command should exist in the repository’s current command surface.
- Example invocations should be runnable or clearly marked as illustrative if the command is not yet implemented.
- If a command advertises structured output, the documented output mode should match the actual implementation surface.
- Reviewers should reject command pages that mix multiple unrelated commands into one document or omit the source surface.

## Change Control
- Update this standard when the repository changes the command-doc family shape or required sections.
- Update the command template in the same change set when command page structure changes.
- Update command-family READMEs and the machine-readable command index in the same change set when command pages are added, renamed, or removed.

## References
- [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [command_reference_template.md](/home/j/WatchTowerPlan/docs/templates/command_reference_template.md)
- [README.md](/home/j/WatchTowerPlan/docs/commands/README.md)

## Notes
- Command pages are intended to be the human-readable man-page layer for repository commands.
- The command index exists to route to these pages and support lookup, not to replace the command docs themselves.
- Command pages do not require front matter by default because the command index already carries the structured machine-lookup fields for this document family.
- CLI `--help` output should follow the command-help standard while these command pages remain the fuller human-readable reference layer.

## Updated At
- `2026-03-09T23:02:08Z`
