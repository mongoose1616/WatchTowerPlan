# `watchtower_plan.testing`

## Description
`This package holds plan-owned test-support helpers and shared case modules. Keep helpers here when multiple plan tests need live-pack materialization, initiative/package setup, or other plan-specific support that should not live in core/python/tests/.`

## Notes
- This package is test support, not production runtime API.
- Shared-core tests must not import this package.
- Prefer synthetic fixture-pack support in `core/python/tests/` when a shared-core test only needs generic pack context.
