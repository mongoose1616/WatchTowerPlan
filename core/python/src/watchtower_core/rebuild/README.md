# `watchtower_core.rebuild`

## Summary
Export-safe rebuild harness primitives for deterministic regeneration of derived JSON indexes and rendered Markdown views from stronger authority.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.rebuild` plus explicit reusable rebuild modules such as `rendered_views`, `harness`, and related target helpers.
- `Non-Goals`: Pack-specific rebuild target catalogs, pack-local output shaping, or pack-flavored rebuild wrappers that belong under the owning pack package.

## Key Surfaces
- `harness.py`: Reusable rebuild target contracts and deterministic dry-run or write orchestration.
- `rendered_views.py`: Registry-backed rendered Markdown builders and reconciliation helpers for governed human surfaces.
- Target helpers: Reusable JSON and Markdown rebuild paths that do not need pack-local orchestration services.

## Notes
- Keep reusable rebuild primitives here.
- Keep pack-specific output shaping and pack-local target catalogs out of this namespace.
