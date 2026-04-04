# `watchtower_core.utils`

## Summary
Small shared helpers that keep low-level cross-package utilities out of higher-level orchestration modules.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: Explicit low-coupling helpers such as `watchtower_core.utils.utc_timestamp_now`.
- `Non-Goals`: New home for repo policy, orchestration, or convenience re-exports.

## Key Surfaces
- `exception_formatting.py`: Shared helper for stable human-readable exception detail strings in operator and validation output.
- `git_hygiene.py`: Local git branch and worktree evaluation helpers used by hygiene-oriented CLI commands.
- `module_exports.py`: Shared package-root lazy-export and fail-closed guard helpers used by runtime namespace `__init__` modules.
- `timestamps.py`: RFC 3339 UTC timestamp helper.

## Related Surfaces
- `core/python/src/watchtower_core/control_plane/README.md`
- `core/python/src/watchtower_core/README.md`
