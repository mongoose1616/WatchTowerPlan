# `docs`

## Description
`This directory contains repository-native documentation. Use it for durable repo guidance, command pages, standards, references, and reusable templates. Authored shared foundations live under core/docs/foundations/ and are mirrored into plan/docs/foundations/.`

## Paths
| Path | Description |
|---|---|
| `docs/README.md` | Describes the purpose of the docs directory and the documentation surfaces stored here. |
| `docs/AGENTS.md` | Defines documentation-specific instructions for the docs subtree. |
| `docs/commands/` | Holds human-readable command pages for repository commands and subcommands. |
| `docs/references/` | Holds external references and local working-reference mappings. |
| `docs/standards/` | Holds normative repository standards. |
| `docs/templates/` | Holds reusable templates for repository documents. |

## Notes
- Authored foundations live under `core/docs/foundations/`, with the required mirror under `plan/docs/foundations/`.
- This root no longer owns a separate `docs/foundations/` compatibility family.
- Live planning authority does not live under `docs/`; use `plan/**` and `core/control_plane/**` for operational planning state.
