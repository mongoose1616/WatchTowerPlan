# `core/workflows`

## Description
`This directory is the human entrypoint for future core-owned workflow guidance. In the current tranche it exists as a governed router surface while the canonical workflow backend still lives at the repository root.`

## Paths
| Path | Description |
|---|---|
| `core/workflows/README.md` | Describes the purpose of the core workflow root and its current migration boundary. |
| `core/workflows/AGENTS.md` | Defines local instructions for future core-owned workflow guidance. |
| `core/workflows/ROUTING_TABLE.md` | Thin router surface that points to the current canonical routing backend. |
| `core/workflows/modules/README.md` | Explains the current status of core-owned workflow-module migration. |

## Notes
- `requirements.md` and `decisions.md` remain authoritative while the workflow-root split is still incomplete.
- The canonical routing backend remains `workflows/ROUTING_TABLE.md` plus `workflows/modules/` until a later slice explicitly moves that authority.
- Treat this root as a deliberate human-surface contract, not as a duplicate backend.
