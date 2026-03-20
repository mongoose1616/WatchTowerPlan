# `core/docs`

## Description
`This directory is the durable home for shared command docs, references, templates, shared or core-owned standards, and other human-authored material that should not live in the live plan workspace.`

## Paths
| Path | Description |
|---|---|
| `core/docs/README.md` | Describes the purpose of the core docs root and its owned documentation families. |
| `core/docs/AGENTS.md` | Defines documentation-specific instructions for the `core/docs/**` subtree. |
| `core/docs/commands/` | Holds canonical CLI command pages. |
| `core/docs/foundations/` | Holds the authored foundations source for shared guidance roots. |
| `core/docs/references/` | Holds external references and local working-reference mappings. |
| `core/docs/standards/` | Holds shared and core-owned standards. |
| `core/docs/templates/` | Holds reusable templates for governed human-authored documents. |

## Notes
- `requirements.md` and `decisions.md` are the authoritative contract for documentation roots and endstate behavior.
- `core/docs/foundations/` is the authored foundations source and `plan/docs/foundations/` is the required byte-identical mirror.
- Do not place live initiative state or plan-domain execution artifacts here.
- Root `docs/` is retired; keep shared or core-owned durable documentation here instead.
