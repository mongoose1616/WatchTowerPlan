# `watchtower_plan.validation`

## Summary
Repo-local document-semantic validators plus WatchTowerPlan-specific validation-target enumeration.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: Explicit repo-local semantic validators and target-enumeration helpers such as `document_semantics` and `targets`.
- `Non-Goals`: Owning reusable validation-suite orchestration or aggregate validate-all services.

## Key Surfaces
- `document_semantics.py`: Repo-local validator wiring over reusable documentation helpers plus plan-owned workflow and validator target rules.
- `targets.py`: WatchTowerPlan-specific target enumeration for the repo baseline validation suite.

## Related Surfaces
- `core/python/src/watchtower_core/validation/README.md`
- `core/docs/commands/core_python/watchtower_core_validate.md`
