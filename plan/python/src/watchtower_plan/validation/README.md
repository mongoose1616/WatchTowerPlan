# `watchtower_plan.validation`

## Summary
Repo-local document-semantic validators for plan-owned guidance and workflow semantics that cannot already live under reusable core.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: Explicit repo-local semantic validators such as `document_semantics`.
- `Non-Goals`: Owning reusable validation-suite orchestration, pack-target enumeration, or aggregate validate-all services, or duplicating generic reusable validator helpers.

## Key Surfaces
- `document_semantics.py`: Repo-local validator wiring over reusable documentation helpers plus plan-owned workflow semantics and generic initiative-handoff document rules.
- Generic pack-target enumeration now lives in `watchtower_core.validation.pack_targets`.

## Related Surfaces
- `core/python/src/watchtower_core/validation/README.md`
- `core/docs/commands/core_python/watchtower_core_validate.md`

## Shrink Rules
- Keep reusable suite orchestration, aggregate helpers, and generic validators in `watchtower_core.validation`.
- Keep `watchtower_plan.validation` narrow and limited to repo-local semantic validation rules.
