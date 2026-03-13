# `watchtower_core.control_plane`

## Summary
Workspace-aware artifact loading, schema validation, typed models, and filesystem abstraction for governed control-plane data.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.control_plane` and explicit submodules such as `loader`, `schemas`, and `workspace`.
- `Non-Goals`: Repo-local planning semantics, Markdown document rules, or task orchestration policy.

## Key Surfaces
- `loader.py`: High-level governed artifact loader.
- `schemas.py`: Schema store and supplemental-schema registration.
- `workspace.py`: Workspace configuration, artifact source, and artifact store abstractions.
- `models/`: Typed artifact models grouped by artifact family, with a stable re-export surface in `models/__init__.py`.

## Related Surfaces
- `core/python/src/watchtower_core/adapters/README.md`
- `core/python/src/watchtower_core/repo_ops/README.md`
- `core/control_plane/README.md`
