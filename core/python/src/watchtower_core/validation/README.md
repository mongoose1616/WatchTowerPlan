# `watchtower_core.validation`

## Summary
Export-safe validation services, result models, and compatibility guards around repo-specific aggregate validation.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.validation` for exported validators and result types, plus explicit submodules such as `acceptance`, `artifact`, and `front_matter`.
- `Non-Goals`: Direct export of aggregate repo validation families such as `ValidationAllService`; those stay under `watchtower_core.repo_ops.validation`.

## Key Surfaces
- `acceptance.py`, `artifact.py`, `document_semantics.py`, and `front_matter.py`: Exported validator services.
- `models.py` and `errors.py`: Shared validation result and error types.
- `__init__.py`: Namespace guardrail for repo-local aggregate validation helpers.

## Related Surfaces
- `core/python/src/watchtower_core/repo_ops/validation/README.md`
- `docs/commands/core_python/watchtower_core_validate.md`
