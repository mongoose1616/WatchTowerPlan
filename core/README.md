# `core/`

## Description
`This directory is the shared implementation and machine-contract workspace for repository-wide reusable behavior. Use it for the canonical control-plane tree, the canonical Python workspace, and the future core-owned docs and workflow roots.`

## Paths
| Path | Description |
|---|---|
| `core/README.md` | Describes the purpose of the core root and its main subtrees. |
| `core/control_plane/` | Holds authoritative machine-readable schemas, registries, contracts, indexes, examples, and ledgers. |
| `core/python/` | Holds the canonical Python workspace for `watchtower_core` code, tests, and tooling. |
| `core/docs/` | Holds durable core-only guidance surfaces. |
| `core/workflows/` | Holds the human entrypoint for future core-owned workflow guidance and routing surfaces. |

## Notes
- `requirements.md` and `decisions.md` remain the authoritative implementation contract while the repository is still converging on the target split.
- Use `core/control_plane/README.md` for machine-contract orientation and `core/python/README.md` for executable implementation entrypoints.
- `core/docs/` and `core/workflows/` are seeded in this tranche as governed human roots even though deeper content migration remains in progress.
