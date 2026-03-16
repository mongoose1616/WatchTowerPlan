# `watchtower_core.validation`

## Summary
Export-safe validation services, suite orchestration, aggregate baseline helpers, result models, and namespace guardrails that keep repo-local semantic rule providers under `repo_ops.validation`.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.validation` for exported validators and result types, plus explicit reusable submodules such as `acceptance`, `all`, `artifact`, and `front_matter`.
- `Non-Goals`: Direct export of repo-local document semantics implementations such as `DocumentSemanticsValidationService`; those stay under `watchtower_core.repo_ops.validation` even when reusable-core orchestration invokes them.

## Key Surfaces
- `acceptance.py`, `artifact.py`, `front_matter.py`, and `pack_contract.py`: Exported validator services.
- `all.py`: Aggregate validation helper that runs a selected suite baseline plus acceptance reconciliation.
- `suite.py`: Registry-backed reusable-core suite orchestration.
- `context.py`, `models.py`, and `errors.py`: Pack-aware context helpers, shared validation result models, and error types.
- `__init__.py`: Namespace guardrail for helpers that stay out of the package root, including repo-local semantic validators and submodule-only aggregate orchestration.

## Related Surfaces
- `core/python/src/watchtower_core/repo_ops/validation/README.md`
- `docs/commands/core_python/watchtower_core_validate.md`
