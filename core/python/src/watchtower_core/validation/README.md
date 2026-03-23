# `watchtower_core.validation`

## Summary
Export-safe validation services, suite orchestration, aggregate baseline helpers, result models, generic pack-target enumeration, and namespace guardrails. Reusable-core validation orchestration now loads pack-owned semantic rule providers through the declared pack-integration contract instead of hard-importing pack code.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.validation` for exported validators and result types, plus explicit reusable submodules such as `acceptance`, `all`, `artifact`, and `front_matter`.
- `Non-Goals`: Direct export of pack-local document semantics implementations such as `DocumentSemanticsValidationService`; those stay under the owning `watchtower_<pack>.validation` package even when reusable-core orchestration invokes them, plus pack-flavored duplicates of reusable validator helpers.

## Key Surfaces
- `acceptance.py`, `artifact.py`, `front_matter.py`, and `pack_contract.py`: Exported validator services.
- `all.py`: Aggregate validation helper that runs a selected suite baseline plus acceptance reconciliation.
- `suite.py`: Registry-backed reusable-core suite orchestration that resolves pack-owned document semantics through `watchtower_core.pack_integration.runtime`.
- `pack_targets.py`: Generic pack-target enumeration over validator and workflow contracts for hosted packs.
- `context.py`, `models.py`, and `errors.py`: Pack-aware context helpers, shared validation result models, and error types.
- `__init__.py`: Namespace guardrail for helpers that stay out of the package root, including repo-local semantic validators and submodule-only aggregate orchestration.

## Related Surfaces
- `core/docs/commands/core_python/watchtower_core_validate.md`

## Notes
- Keep reusable suite orchestration, result models, and generic validators here.
- Keep pack-owned validation packages such as `watchtower_<pack>.validation` narrow and limited to pack-local semantic validation rules.
- Do not reintroduce pack-flavored duplicates of reusable validator helpers or suite orchestration under reusable core.
