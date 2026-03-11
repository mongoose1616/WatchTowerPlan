# `watchtower_core.utils`

## Summary
Small shared helpers that keep low-level cross-package utilities out of higher-level orchestration modules.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: Explicit low-coupling helpers such as `watchtower_core.utils.utc_timestamp_now`.
- `Non-Goals`: New home for repo policy, orchestration, or convenience re-exports.

## Key Surfaces
- `timestamps.py`: RFC 3339 UTC timestamp helper.

## Related Surfaces
- `core/python/src/watchtower_core/control_plane/README.md`
- `core/python/src/watchtower_core/repo_ops/README.md`
