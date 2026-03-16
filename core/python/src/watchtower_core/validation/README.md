# `watchtower_core.validation`

## Summary
Export-safe validation services, result models, and namespace guardrails that keep repo-local validation orchestration under `repo_ops.validation`.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.validation` for exported validators and result types, plus explicit reusable submodules such as `acceptance`, `artifact`, and `front_matter`.
- `Non-Goals`: Direct export of repo-local document semantics or aggregate validation families such as `DocumentSemanticsValidationService` or `ValidationAllService`; those stay under `watchtower_core.repo_ops.validation`.

## Key Surfaces
- `acceptance.py`, `artifact.py`, and `front_matter.py`: Exported validator services.
- `models.py` and `errors.py`: Shared validation result and error types.
- `__init__.py`: Namespace guardrail for repo-local validation helpers that do not belong in the export-safe surface.

## Related Surfaces
- `core/python/src/watchtower_core/repo_ops/validation/README.md`
- `docs/commands/core_python/watchtower_core_validate.md`
