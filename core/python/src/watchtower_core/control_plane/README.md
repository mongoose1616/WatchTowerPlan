# `watchtower_core.control_plane`

## Summary
Reusable control-plane helpers for governed pack/runtime loading, policy and family resolution, typed artifact models, and workspace-aware filesystem access.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.control_plane` and explicit helper or model submodules such as `loader`, `pack_context`, `governance_surfaces`, `terminology`, `template_catalog`, `schemas`, and `workspace`.
- `Non-Goals`: Repo-local planning semantics, Markdown document rules, or task orchestration policy.

## Key Surfaces
- Load and workspace helpers: `loader.py`, `pack_context.py`, `workspace.py`, `paths.py`, `errors.py`, and `schemas.py` provide governed artifact loading, workspace configuration, filesystem abstraction, and schema-store support.
- Policy and family helpers: `artifact_family.py`, `documentation_family.py`, `promotion_policy.py`, `project_surface_policy.py`, `human_surface_policy.py`, and `retention_policy.py` resolve governed family and policy decisions from machine-readable authority.
- Runtime lookup helpers: `actors.py`, `discrepancy.py`, `event_stream.py`, `extraction_output.py`, `governance_surfaces.py`, `path_ids.py`, `template_catalog.py`, `terminology.py`, and `workflow_catalog.py` expose reusable pack-runtime helpers without importing repo-local orchestration.
- `models/`: Typed artifact and contract models grouped by family, including the pack-facing contract surfaces used by `PackContext`, artifact indexes, and extraction-output envelopes.

## Related Surfaces
- `core/docs/standards/engineering/python_code_design_standard.md`
- `core/python/src/watchtower_core/adapters/README.md`
- `plan/python/src/watchtower_plan/README.md`
- `core/control_plane/README.md`
