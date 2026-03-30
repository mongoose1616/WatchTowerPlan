# `core/control_plane`

## Description
`This directory is the canonical, versioned, machine-readable authority for the shared core substrate. Keep authored schemas, startup manifests, registries, contracts, indexes, and retained governed record families here.`

## Boundaries
- Keep domain-pack content out of this tree.
- Treat `core/control_plane/manifests/pack_settings.json` as the reusable-core startup root; supporting manifests and retained record families live alongside it.
- Validate external content against published interfaces and contracts rather than storing pack-owned artifacts here.
- Do not store mutable runtime state, caches, or transient event streams here.

## Paths
| Path | Description |
|---|---|
| `core/control_plane/AGENTS.md` | Defines the local instruction layer for authored control-plane artifacts and machine-governed boundary work. |
| `core/control_plane/README.md` | Describes the purpose, boundaries, and main artifact families in the control-plane tree. |
| `core/control_plane/schemas/` | JSON Schemas for governed core artifacts and external validation interfaces. |
| `core/control_plane/templates/` | Governed reusable template assets for core-owned human surfaces and mirrored foundations. |
| `core/control_plane/manifests/` | Authored startup and descriptive declarations owned by core. |
| `core/control_plane/registries/` | Canonical lookup data and pack-startup registries owned by core. |
| `core/control_plane/contracts/` | Versioned machine-readable contract families, currently the acceptance-contract set. |
| `core/control_plane/indexes/` | Deliberate derived lookup files when a concrete consumer exists. |
| `core/control_plane/records/` | Retained governed record families for migrations, releases, validation evidence, and benchmark baselines. |

## Notes
- Keep authored control-plane assets here and keep live pack machine state under the owning pack machine root such as `<pack>/.wt/`.
- Use `core/control_plane/**` for authored machine authority and pack machine roots such as `<pack>/.wt/**` for live pack state. Do not blur those roles.
- Treat retained record families under `core/control_plane/records/**` as internal governed history. They are not portable customer-bootstrap surfaces unless a release contract explicitly includes governance history.
- Benchmark suite definitions belong in the authored registry layer, while captured benchmark results belong in retained benchmark records. Runtime telemetry JSONL remains outside this tree.
