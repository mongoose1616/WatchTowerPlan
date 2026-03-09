---
id: "std.data_contracts.command_index"
title: "Command Index Standard"
summary: "This standard defines the role, structure, and boundary rules for machine-readable command indexes stored under `core/control_plane/indexes/commands/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "data_contracts"
  - "command_index"
owner: "repository_maintainer"
updated_at: "2026-03-09T23:02:08Z"
audience: "shared"
authority: "authoritative"
---

# Command Index Standard

## Summary
This standard defines the role, structure, and boundary rules for machine-readable command indexes stored under `core/control_plane/indexes/commands/`.

## Purpose
Provide a compact lookup surface that maps available commands and subcommands to their human-readable command pages and implementation surfaces without forcing command discovery to scan Markdown or package code directly.

## Scope
- Applies to machine-readable command index artifacts stored under `core/control_plane/indexes/commands/`.
- Covers placement, entry shape, update expectations, and the relationship between the index, command docs, and implementation surfaces.
- Does not replace command-page documentation or the authoritative implementation surface for command behavior.

## Use When
- Adding a new durable repository command or subcommand.
- Refreshing command lookup data after command docs or implementation surfaces change.
- Reviewing whether command lookup metadata belongs in an index or a registry.

## Related Standards and Sources
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [schema_catalog_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_catalog_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/commands/README.md): family entrypoint and inventory surface this standard should stay aligned with.
## Guidance
- Model command lookup as an index, not as a registry.
- Treat the command index as a machine-readable routing aid rather than the authoritative definition of command behavior.
- Keep human-readable command semantics in `docs/commands/**`.
- Keep implementation authority in the actual command code surface.
- Store published command indexes under `core/control_plane/indexes/commands/`.
- Keep the companion artifact schema under `core/control_plane/schemas/artifacts/`.
- Use JSON for the published command index artifact.
- Catalog only durable repository commands or subcommands that have stable command pages.
- Treat the authored command pages under `docs/commands/` as the primary human source for the derived command index.
- Every command index entry must point to a command page under `docs/commands/`.
- Every entry should point to the owning implementation surface when one exists.
- Use a stable `command_id` per command or subcommand.
- Represent subcommands as separate entries rather than embedding them only inside parent records.
- Keep the index modular: add one entry per command surface and let future code load or filter only the relevant command family.
- When a command supports structured machine output, record the supported output formats and default format in the command index entry.
- Update the command index in the same change set whenever a command page or command surface changes materially.

## Structure or Data Model
### Root artifact fields
| Field | Requirement | Notes |
|---|---|---|
| `$schema` | Required | Use the published schema identifier for the command-index artifact family. |
| `id` | Required | Stable identifier for the command index artifact. |
| `title` | Required | Human-readable title for the index artifact. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `workspace` | Required | Stable workspace label such as `core_python`. |
| `entries` | Required | Array of command records. |

### Command entry fields
| Field | Requirement | Notes |
|---|---|---|
| `command_id` | Required | Stable machine-usable command identifier. |
| `command` | Required | Literal command invocation label. |
| `summary` | Required | Concise description of the command purpose. |
| `kind` | Required | Use `root_command` or `subcommand`. |
| `status` | Required | Use the governed lifecycle vocabulary. |
| `workspace` | Required | Stable workspace label such as `core_python`. |
| `doc_path` | Required | Repository-relative path to the command page under `docs/commands/`. |
| `synopsis` | Required | Short usage form for quick lookup. |
| `implementation_path` | Optional | Repository-relative owning implementation surface. |
| `package_entrypoint` | Optional | Import-style entrypoint when one exists. |
| `parent_command_id` | Required for subcommands | Stable parent command identifier. |
| `output_formats` | Optional | Supported output formats such as `human` and `json`. |
| `default_output_format` | Optional | Default output format when the command supports multiple modes. |
| `aliases` | Optional | Alternate lookup terms that materially improve retrieval. |
| `tags` | Optional | Controlled or semi-controlled query terms when useful. |
| `notes` | Optional | Short lookup or operator notes. |

## Process or Workflow
1. Add or update the command page under `docs/commands/`.
2. Rebuild the command index from the current command pages and review the derived output in the same change set.
3. Validate that every entry points to an existing command page and any listed implementation path exists.
4. Update related command-family READMEs, repository path indexes, and schemas in the same change set when the command surface changes structurally.
5. Validate the command index artifact against its published schema before treating the change as complete.

## Examples
- `watchtower-core` should appear as a `root_command` entry with a command page and package entrypoint.
- `watchtower-core doctor` should appear as a `subcommand` entry linked to the root command and its own command page.
- A general Python workspace README is not a command-index entry because it is not a command surface.

## Validation
- The command index should validate against its published artifact schema.
- Every `doc_path` should exist and point to a command page under `docs/commands/`.
- Every listed `implementation_path` should exist.
- Subcommand entries should name a valid `parent_command_id`.
- When `default_output_format` is present, it should match one of the listed `output_formats`.
- Reviewers should reject command-index entries that point to stale docs, stale implementation paths, or commands that do not exist in the current surface.

## Change Control
- Update this standard when the repository changes how commands are indexed or looked up.
- Update the companion artifact schema, examples, and live command index in the same change set when the command-index family changes structurally.
- Update command docs, command-family READMEs, and relevant path indexes in the same change set when command lookup surfaces change materially.

## References
- [command_md_standard.md](/home/j/WatchTowerPlan/docs/standards/documentation/command_md_standard.md)
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md)
- [python_workspace_standard.md](/home/j/WatchTowerPlan/docs/standards/engineering/python_workspace_standard.md)
- [README.md](/home/j/WatchTowerPlan/core/control_plane/indexes/commands/README.md)

## Notes
- The command index is intentionally small and lookup-oriented. It should not duplicate the full content of the command pages.
- The repository path index remains the broader navigation surface. The command index is the targeted command-lookup surface.

## Updated At
- `2026-03-09T23:02:08Z`
