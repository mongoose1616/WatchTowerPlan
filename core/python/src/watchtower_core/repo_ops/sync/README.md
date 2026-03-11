# `watchtower_core.repo_ops.sync`

## Summary
Authoritative repository sync services for derived indexes, trackers, route data, and GitHub task mirrors.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: Explicit sync services and family modules such as `all`, `command_index`, `standard_index`, and `github_tasks`.
- `Non-Goals`: Stable public export surface through `watchtower_core.sync`.

## Key Surfaces
- `all.py`: Aggregate sync orchestration.
- `*_index.py` and `*_tracking.py`: Family-specific rebuild logic for governed indexes and trackers.
- `github_tasks.py`: GitHub task mirror sync.

## Related Surfaces
- `core/python/src/watchtower_core/sync/README.md`
- `core/python/src/watchtower_core/integrations/github/README.md`
- `docs/commands/core_python/watchtower_core_sync.md`
