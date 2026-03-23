# AGENTS.md

## Role
- Treat this file as the local instruction layer for `core/control_plane/**`.
- Use it for authored machine-governed artifact boundaries and control-plane-specific reconciliation expectations.
- Keep detailed procedures in workflow modules, schemas, registries, and standards rather than expanding this file into a process catalog.

## Scope
- Applies to `core/control_plane/**`.
- Inherit the repository root [AGENTS.md](/AGENTS.md) first and do not weaken it here.

## Routing
- Read this file before working in `core/control_plane/**`.
- Use [ROUTING_TABLE.md](/core/workflows/ROUTING_TABLE.md) for governed-artifact reconciliation, documentation refresh, validation, and shared engineering routes.
- Use a pack-owned routing table only when a pack-domain route explicitly depends on shared control-plane artifact updates.
- Do not turn this file into a second routing table.

## Local Rules
- Treat `core/control_plane/**` as the authored, versioned machine-readable authority for shared core artifacts.
- Keep authored schemas, registries, manifests, contracts, templates, indexes, and retained records here according to their owned families.
- Treat the owning pack machine root such as `<pack>/.wt/**` as live pack machine state, not as a substitute for authored control-plane assets.
- Keep reusable core artifacts here and keep pack-owned runtime or initiative-local state out of this tree.
- When a schema-backed artifact family changes, update its companion schemas, examples, registries, indexes, validators, and affected docs in the same change set.
- Use [README.md](/core/control_plane/README.md) as the quick reference for directory purpose and family inventory before broader scans.

## Do
- Keep this tree reviewable, deterministic, and versioned.
- Prefer explicit governed artifacts here over ad hoc JSON blobs, Python constants, or hidden sidecar files elsewhere in the repository.

## Do Not
- Do not store mutable runtime state, caches, or transient event streams under `core/control_plane/**`.
- Do not move pack-owned live state out of the owning pack machine root into this tree.
- Do not place repo-local Python business logic under `core/control_plane/**`.
