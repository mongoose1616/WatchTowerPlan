# Core Copy Forward Operating Mode Documentation Implementation Slice

## Summary
Document that downstream WatchTower repositories may consume the shared core by copying core/ alone or alongside one or more hosted packs.

## Work Breakdown
- Update [repository_scope.md](/core/docs/foundations/repository_scope.md) to state that `WatchTowerPlan` is the canonical authored shared-core source and that downstream WatchTower repositories may consume `core/` alone or with selected hosted packs.
- Update [product_direction.md](/core/docs/foundations/product_direction.md) to describe copy-forward consumption as one valid downstream delivery and adoption mode.
- Update [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md) to state that shared-workspace dependency wiring is repo-local configuration, even when this repository currently installs `watchtower_plan`.
- Update [README.md](/core/python/README.md) to explain that `watchtower_plan` examples reflect the current internal pack in this repository and must not be treated as donor defaults in downstream repos.
- Update [domain_pack_authoring_reference.md](/core/docs/references/domain_pack_authoring_reference.md) with an explicit operating-mode table for `core/` only, `core/` plus one pack, and `core/` plus multiple packs.
- Mirror any changed foundation docs into `plan/docs/foundations/`, rebuild the foundation index, validate the changed docs, and close the initiative once the doc set is coherent.

## Gate
- No execution starts until the initiative package is approved and marked `ready_for_execution`.

## Planned Change Set
- `core/docs/foundations/repository_scope.md`
- `plan/docs/foundations/repository_scope.md`
- `core/docs/foundations/product_direction.md`
- `plan/docs/foundations/product_direction.md`
- `core/docs/standards/engineering/python_workspace_standard.md`
- `core/docs/references/domain_pack_authoring_reference.md`
- `core/python/README.md`
