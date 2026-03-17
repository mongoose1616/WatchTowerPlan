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
| `core/control_plane/README.md` | Describes the purpose, boundaries, and main artifact families in the control-plane tree. |
| `core/control_plane/schemas/` | JSON Schemas for governed core artifacts and external validation interfaces. |
| `core/control_plane/templates/` | Governed reusable template assets for core-owned human surfaces and mirrored foundations. |
| `core/control_plane/manifests/` | Authored startup and descriptive declarations owned by core. |
| `core/control_plane/registries/` | Canonical lookup data and pack-startup registries owned by core. |
| `core/control_plane/contracts/` | Versioned machine-readable contract families, currently the acceptance-contract set. |
| `core/control_plane/indexes/` | Deliberate derived lookup files when a concrete consumer exists. |
| `core/control_plane/ledgers/` | Retained governed record families for migrations, releases, purge records, and validation evidence. |
