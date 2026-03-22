# First-Party Root Pack Roots Design Record

## Summary
Implement first-party root-pack discovery and default-pack resolution so copied repositories can host packs at <slug>/ without donor assumptions.

## Design Boundary
- The initiative package is machine-first and local to `plan/initiatives/first_party_root_pack_roots/.wt/`.
- Authored intake docs remain editable inputs but require explicit machine confirmation.
- Readiness must fail closed on missing capture, blocking deferred items, open discrepancies, or missing approval.

## Design Decisions
- Keep the manifest marker authoritative. A pack is discoverable because it publishes `<pack>/.wt/manifests/pack_settings.json`, not because it lives under one special directory name.
- Prefer direct repository child pack roots such as `plan/` or `oversight/` ahead of `packs/<slug>/` when fallback discovery is needed. This matches the current first-party layout while preserving the nested convention for copied or multi-pack repos.
- Prefer the explicit shared registry default over all filesystem discovery when `pack_registry.json` declares one valid `default_repo_pack`.
- Keep this slice focused on pack-settings discovery and default selection. Do not couple it to package-import changes or `core/python/pyproject.toml` donor cleanup in the same change set.
- Use `plan` as the proof pack for the root-pack path because it is the current first-party pack in this repository and exercises the real core-host-pack interaction.

## Risks and Controls
- Risk: changing discovery order could change which pack becomes the implicit default in fixture repos that omit an explicit registry default.
- Control: add deterministic tests for direct-root versus `packs/*` precedence and keep the registry default path authoritative whenever present.
- Risk: moving discovery helpers carelessly could create a control-plane to pack-integration import cycle.
- Control: keep the new discovery helper path-oriented and dependency-light so both loader and pack-integration helpers can use it safely.
