# `watchtower_core.repo_ops.validation`

## Summary
Repo-wide aggregate validation orchestration and repository-specific validation families.

## Boundary
- `Classification`: `repo_local_orchestration`
- `Supported Imports`: Explicit aggregate or repo-specific validation modules such as `all` and `document_semantics`.
- `Non-Goals`: Direct export of aggregate repo validation through `watchtower_core.validation`.

## Key Surfaces
- `all.py`: Aggregate validation family orchestration.
- `document_semantics.py`: Repo-native Markdown semantic validation.
- `example_artifacts.py`: Schema resolution helpers for governed control-plane examples.

## Related Surfaces
- `core/python/src/watchtower_core/validation/README.md`
- `docs/commands/core_python/watchtower_core_validate.md`
