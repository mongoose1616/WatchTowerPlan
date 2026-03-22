# Core Copy Forward Operating Mode Documentation Design Record

## Summary
Document that downstream WatchTower repositories may consume the shared core by copying core/ alone or alongside one or more hosted packs.

## Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/core_copy_forward_operating_mode_documentation/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation before approval.
- The implementation should clarify repository ownership and supported operating modes without changing runtime contracts, pack registries, or shared-workspace behavior.

## Design Decisions
- Put the operating-mode statement in [repository_scope.md](/core/docs/foundations/repository_scope.md) so the current repository charter explicitly covers downstream `core/` copy-forward use.
- Put the future-facing version of the same statement in [product_direction.md](/core/docs/foundations/product_direction.md) so product planning does not imply that consuming repos must integrate the shared runtime some other way.
- Put the pack-neutral rule in [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md) so shared workspace wiring is documented as repo-local configuration rather than donor-repo inheritance.
- Put the contributor-facing explanation in [README.md](/core/python/README.md) so current `watchtower_plan` examples remain usable here without being mistaken for universal shared-core defaults.
- Put the worked operating-mode examples in [domain_pack_authoring_reference.md](/core/docs/references/domain_pack_authoring_reference.md) so future pack authors and downstream maintainers can see the supported adoption patterns in one place.

## Risks and Controls
- Risk: the new wording could imply that copying `core/` automatically makes another repository usable without updating pack registry or workspace metadata.
- Control: keep the guidance explicit that pack selection, registry entries, and shared-workspace dependency wiring remain repo-local responsibilities in the consuming repository.
