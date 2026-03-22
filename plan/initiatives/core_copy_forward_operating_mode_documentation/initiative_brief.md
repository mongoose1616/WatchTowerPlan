# Core Copy Forward Operating Mode Documentation

## Summary
Document that downstream WatchTower repositories may consume the shared core by copying core/ alone or alongside one or more hosted packs.

## Identity
- `initiative_id`: `initiative.core_copy_forward_operating_mode_documentation`
- `trace_id`: `trace.core_copy_forward_operating_mode_documentation`
- `scope_type`: `pack_wide`

## Problem Statement
The current shared-core docs explain the core-host-pack split and pack portability, but they do not state one important operating mode directly enough: downstream WatchTower repositories may adopt the shared runtime by copying `core/` alone during integration bring-up or by copying `core/` together with one or more hosted packs. Without that explicit statement, current `watchtower_plan` examples can be misread as reusable-core defaults instead of current-repository facts.

## Goals
- State clearly that `WatchTowerPlan` is the canonical authored source for the shared `core/` tree.
- State clearly that downstream WatchTower repositories may consume `core/` alone or `core/` plus selected hosted packs.
- Reinforce that shared-core policy, workspace guidance, and pack-boundary docs must stay donor-neutral even when this repository currently hosts `watchtower_plan`.
- Point maintainers at the right ownership boundary: pack selection, registry entries, and shared-workspace package wiring are repo-local decisions for the consuming repository.

## In Scope
- Shared foundation docs that define current repository ownership and future product relationship.
- Shared engineering guidance that describes the Python workspace contract and host-pack portability boundary.
- Shared contributor-facing Python workspace docs that currently use `watchtower_plan` as the current internal example.
- Shared pack-authoring guidance that should describe the supported copy-forward operating modes directly.

## Out Of Scope
- Python runtime, loader, registry, or CLI behavior changes.
- Downstream repository-specific integration work inside `WatchTowerOversight` or future consuming repos.
- Registry or workspace metadata changes for any repository other than the documentation and derived surfaces in `WatchTowerPlan`.

## Success Criteria
- Shared docs explicitly say downstream WatchTower repositories may consume `core/` alone or together with one or more hosted packs.
- Shared-core guidance makes it clear that `watchtower_plan` is the current internal pack example in this repository, not a reusable-core invariant.
- The updated docs validate cleanly, mirrored foundations stay byte-identical, and the derived foundation index stays current.

## Initial Task Set
- `task.core_copy_forward_operating_mode_documentation.bootstrap_core_copy_forward_operating_mode_documentation`: Bootstrap Core Copy Forward Operating Mode Documentation live initiative package.
