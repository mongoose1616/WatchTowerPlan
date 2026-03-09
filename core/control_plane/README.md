# `core/control_plane`

## Description
`This directory is the canonical, versioned, machine-readable authority for the shared core substrate. Keep authored schemas, manifests, registries, contracts, policies, examples, indexes, and committed ledgers here.`

## Boundaries
- Keep domain-pack content out of this tree.
- Validate external content against published interfaces and contracts rather than storing pack-owned artifacts here.
- Do not store mutable runtime state, caches, or transient event streams here.

## Paths
| Path | Description |
|---|---|
| `core/control_plane/README.md` | Describes the purpose, boundaries, and main artifact families in the control-plane tree. |
| `core/control_plane/schemas/` | JSON Schemas for governed core artifacts and external validation interfaces. |
| `core/control_plane/manifests/` | Authored machine-readable declarations owned by core. |
| `core/control_plane/registries/` | Canonical lookup data owned by core. |
| `core/control_plane/contracts/` | Versioned intake and compatibility boundaries. |
| `core/control_plane/policies/` | Machine-readable guardrails for validation, execution, and release behavior. |
| `core/control_plane/examples/` | Canonical valid and invalid sample artifacts. |
| `core/control_plane/indexes/` | Deliberate denormalized lookup files when a concrete consumer exists. |
| `core/control_plane/ledgers/` | Committed append-only history for governed changes such as migrations and releases. |
