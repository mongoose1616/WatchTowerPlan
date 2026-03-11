---
id: "std.engineering.cli_help_text"
title: "CLI Help Text Standard"
summary: "This standard defines the minimum detail, structure, and example quality for repository CLI help text so new engineers, operators, and agents can discover commands without reading implementation code first."
type: "standard"
status: "active"
tags:
  - "standard"
  - "engineering"
  - "cli_help"
owner: "repository_maintainer"
updated_at: "2026-03-11T06:00:00Z"
audience: "shared"
authority: "authoritative"
aliases:
  - "command help standard"
  - "cli usage help"
  - "argparse help guidance"
applies_to:
  - "core/python/src/watchtower_core/cli"
  - "docs/commands"
---

# CLI Help Text Standard

## Summary
This standard defines the minimum detail, structure, and example quality for repository CLI help text so new engineers, operators, and agents can discover commands without reading implementation code first.

## Purpose
Keep CLI help useful as the first-stop operator surface instead of treating `--help` as a bare parser dump that only existing contributors can navigate.

## Scope
- Applies to repository-native CLI help text implemented in code, including root commands, command groups, and leaf commands.
- Applies to the `watchtower-core` CLI family under `core/python/`.
- Covers descriptions, option help text, examples, and command-group behavior.
- Does not replace the fuller command pages under `docs/commands/`.

## Use When
- Adding a new root command, command group, or leaf command.
- Revising parser help text after command behavior changes.
- Reviewing whether CLI help is readable enough for new engineers or occasional users.

## Related Standards and Sources
- [engineering_best_practices_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/engineering_best_practices_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [command_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/command_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.

## Guidance
- Write CLI help for a new engineer first, then for a frequent operator, and only then for an already-context-loaded maintainer.
- Use plain task-oriented language such as `Search documented commands` or `Rebuild the repository path index`; avoid short internal shorthand that assumes prior knowledge.
- Root command help should explain what the command family is for, where it is expected to run, and what the main subcommand families are.
- Command-group help should explain how to choose among the leaf commands in that family.
- Leaf-command help should state what the command does, what the safest default behavior is, and what output mode or side effects matter.
- Prefer one short descriptive block and a small runnable example set over long narrative help text.
- Use real repository examples that a new engineer can run without guessing hidden setup beyond the documented workspace contract.
- When structured output exists, explain that `json` is the preferred mode for workflows, scripts, or agent calls.
- Use help text to surface safe behavior. If a command defaults to dry run or non-mutating behavior, say so explicitly.
- Keep per-option help concrete. Describe the field or filter the flag affects rather than repeating the flag name in prose.
- Do not force users to open source code to learn which subcommands exist or what common invocations look like.

## Structure or Data Model
### Root-command help
| Element | Requirement | Notes |
|---|---|---|
| Description | Required | One concise explanation of the command family and workspace expectations. |
| Commands list | Required | Let the parser show available subcommands. |
| Examples | Required | Include 2-4 runnable examples that reflect common first steps. |

### Command-group help
| Element | Requirement | Notes |
|---|---|---|
| Description | Required | Explain how to choose among the leaf commands. |
| Group-specific help on bare invocation | Required | `command group` with no leaf should print that group's help, not the root help. |
| Examples | Required | Include 2-3 examples that cover browsing and one structured-output case when applicable. |

### Leaf-command help
| Element | Requirement | Notes |
|---|---|---|
| Description | Required | State the command purpose in plain language. |
| Safe/default behavior note | Required when relevant | Call out dry-run defaults, read-only behavior, or other important defaults. |
| Option help | Required | Keep each option explanation concrete and action-oriented. |
| Examples | Required | Include 1-3 runnable examples. |
| Structured-output note | Required when relevant | Explain when to use `--format json`. |

## Examples
- `watchtower-core --help` should show a short orientation paragraph plus common examples such as `doctor`, `query commands`, and `sync repository-paths`.
- `watchtower-core query --help` should explain the difference between `paths`, `commands`, and `trace` instead of only listing them.
- `watchtower-core sync repository-paths --help` should state that the command is dry-run by default and that `--write` updates the canonical artifact.

## Operationalization
- `Modes`: `documentation`; `runtime`
- `Operational Surfaces`: `docs/commands`; `core/python/src/watchtower_core/cli`; `docs/commands/`; `docs/commands/core_python/watchtower_core.md`

## Validation
- Root and command-group `--help` output should be understandable without opening the implementation file first.
- Root help should include at least one onboarding-friendly example.
- Command-group help should stay scoped to that group rather than falling back to the root parser.
- Leaf commands that support structured output should explain when `--format json` is appropriate.
- Example commands should match the actual workspace contract and current CLI surface.

## Change Control
- Update this standard when the repository changes the expected help-text shape or operator experience.
- Update command docs and the command index in the same change set when help-surface changes materially affect how commands are discovered or used.

## References
- [core/python/README.md](/home/j/WatchTowerPlan/core/python/README.md)
- [docs/commands/core_python/watchtower_core.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core.md)
- [docs/templates/command_reference_template.md](/home/j/WatchTowerPlan/docs/templates/command_reference_template.md)

## Updated At
- `2026-03-11T06:00:00Z`
