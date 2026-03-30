# `core/`

## Description
`This directory is the shared implementation and machine-contract workspace for repository-wide reusable behavior. Use it for the canonical control-plane tree, the canonical Python workspace, the authored foundations source, and the authoritative shared workflow root.`

## Paths
| Path | Description |
|---|---|
| `core/README.md` | Describes the purpose of the core root and its main subtrees. |
| `core/control_plane/` | Holds authoritative machine-readable schemas, registries, contracts, indexes, examples, and retained records. |
| `core/python/` | Holds the canonical Python workspace for `watchtower_core` code, tests, and tooling. |
| `core/docs/` | Holds authored core-only guidance surfaces, including the authored shared foundations corpus. |
| `core/workflows/` | Holds the authoritative shared workflow guidance and routing surfaces. |

## Notes
- Current repository contract lives in the authored foundations under `core/docs/foundations/`, the shared standards under `core/docs/standards/`, and the authored machine-readable authority under `core/control_plane/`.
- Use `core/control_plane/README.md` for machine-contract orientation and `core/python/README.md` for executable implementation entrypoints.
- Pack-owned foundations mirrors or promoted pack-local guidance belong under the owning pack docs root and must be kept aligned by the owning pack contract rather than hard-coded into shared-core path rules.
- `core/workflows/` is the only shared workflow root; do not add new routed workflow guidance back under repo-root `workflows/`.
