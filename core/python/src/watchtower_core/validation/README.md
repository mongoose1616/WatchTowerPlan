# `watchtower_core.validation`

## Summary
Export-safe validation services, suite orchestration, result models, and namespace guardrails that keep repo-local semantic rule providers under `repo_ops.validation`.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.validation` for exported validators and result types, plus explicit reusable submodules such as `acceptance`, `artifact`, and `front_matter`.
- `Non-Goals`: Direct export of repo-local document semantics implementations such as `DocumentSemanticsValidationService`; those stay under `watchtower_core.repo_ops.validation` even when reusable-core orchestration invokes them.

## Key Surfaces
- `acceptance.py`, `artifact.py`, `front_matter.py`, and `pack_contract.py`: Exported validator services.
- `suite.py`: Registry-backed reusable-core suite orchestration.
- `context.py`, `models.py`, and `errors.py`: Pack-aware context helpers, shared validation result models, and error types.
- `__init__.py`: Namespace guardrail for repo-local validation helpers that do not belong in the export-safe surface.

## Related Surfaces
- `core/python/src/watchtower_core/repo_ops/validation/README.md`
- `docs/commands/core_python/watchtower_core_validate.md`
