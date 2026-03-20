# `watchtower_core.validation`

## Summary
Export-safe validation services, suite orchestration, aggregate baseline helpers, result models, and namespace guardrails. Reusable-core validation orchestration now loads pack-owned semantic rule providers through the declared pack-integration contract instead of hard-importing plan code.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.validation` for exported validators and result types, plus explicit reusable submodules such as `acceptance`, `all`, `artifact`, and `front_matter`.
- `Non-Goals`: Direct export of repo-local document semantics implementations such as `DocumentSemanticsValidationService`; those stay under `watchtower_plan.validation` even when reusable-core orchestration invokes them, and plan-flavored duplicates of reusable validator helpers.

## Key Surfaces
- `acceptance.py`, `artifact.py`, `front_matter.py`, and `pack_contract.py`: Exported validator services.
- `all.py`: Aggregate validation helper that runs a selected suite baseline plus acceptance reconciliation.
- `suite.py`: Registry-backed reusable-core suite orchestration that resolves pack-owned document semantics through `watchtower_core.pack_integration.runtime`.
- `context.py`, `models.py`, and `errors.py`: Pack-aware context helpers, shared validation result models, and error types.
- `__init__.py`: Namespace guardrail for helpers that stay out of the package root, including repo-local semantic validators and submodule-only aggregate orchestration.

## Related Surfaces
- `plan/python/src/watchtower_plan/validation/README.md`
- `core/docs/commands/core_python/watchtower_core_validate.md`

## Notes
- Keep reusable suite orchestration, result models, and generic validators here.
- Keep `watchtower_plan.validation` narrow and limited to repo-local semantic validation rules and target enumeration.
