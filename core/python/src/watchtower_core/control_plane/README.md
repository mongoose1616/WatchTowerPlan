# `watchtower_core.control_plane`

## Summary
Reusable control-plane helpers for governed pack/runtime loading, policy and family resolution, typed artifact models, and workspace-aware filesystem access.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.control_plane` and explicit helper or model submodules such as `loader`, `pack_context`, `governance_surfaces`, `terminology`, `template_catalog`, `schemas`, and `workspace`.
- `Non-Goals`: Pack-local lifecycle semantics, Markdown document rules, task orchestration policy, or live pack machine state that belongs under a pack workspace.

## Key Surfaces
- Load and workspace helpers: `loader.py`, `pack_context.py`, `workspace.py`, `paths.py`, `errors.py`, and `schemas.py` provide governed artifact loading, workspace configuration, filesystem abstraction, and schema-store support.
- Policy and family helpers: `artifact_family.py`, `documentation_family.py`, `promotion_policy.py`, `project_surface_policy.py`, `human_surface_policy.py`, and `retention_policy.py` resolve governed family and policy decisions from machine-readable authority.
- Runtime lookup helpers: `actors.py`, `discrepancy.py`, `event_stream.py`, `extraction_output.py`, `governance_surfaces.py`, `path_ids.py`, `template_catalog.py`, `terminology.py`, and `workflow_catalog.py` expose reusable pack-runtime helpers without importing repo-local orchestration.
- `models/`: Typed artifact and contract models grouped by family, including the pack-facing contract surfaces used by `PackContext`, artifact indexes, and extraction-output envelopes.

## Related Surfaces
- `core/docs/standards/engineering/python_code_design_standard.md`
- `core/python/src/watchtower_core/adapters/README.md`
- `core/control_plane/README.md`

## Notes
- Keep authored machine authority in `core/control_plane/**` and live pack machine state in pack workspaces rather than in reusable core.
- Keep generic pack/runtime helpers here and push pack-local behavior back out to the owning `watchtower_<pack>` package when it depends on a pack-specific workspace.
- Keep repo-local pack behavior out of this namespace when it depends on initiative lifecycle rules, pack tracking semantics, or pack-owned rendered surfaces.
- Treat pack-aware loading as a two-step contract: activate the effective pack settings first, then build the full `PackContext` only when the caller needs pack-governed surfaces beyond runtime identity and owned roots.
- Minimal copied-pack or synthetic runtime fixtures may satisfy runtime-manifest and integration loading without declaring every governance surface required by `PackContext`. Do not force the heavy context into seams that only need the active pack identity.
