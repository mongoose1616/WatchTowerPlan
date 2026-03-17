# `watchtower_core.control_plane`

## Summary
Workspace-aware artifact loading, schema validation, typed models, PackContext loading, and filesystem abstraction for governed control-plane data.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.control_plane` and explicit submodules such as `loader`, `schemas`, and `workspace`.
- `Non-Goals`: Repo-local planning semantics, Markdown document rules, or task orchestration policy.

## Key Surfaces
- `loader.py`: High-level governed artifact loader, including generic typed loading and pack-settings-driven context loading.
- `pack_context.py`: PackContext materialization from pack settings and declared governed surfaces.
- `artifact_family.py`: Pack-local artifact-family resolution for placement, status, visibility, and renderability rules.
- `documentation_family.py`: Pack-local documentation-family resolution for governed authored guidance families, allowed roots, and mirror rules.
- `event_stream.py`: Append-only event stream helpers for governed initiative and task event records.
- `planning_vocabulary.py`: Pack-local lifecycle, review, and provenance vocabulary resolution for plan-runtime helpers.
- `project_surface_policy.py`: Pack-local project-root surface policy resolution for required machine and rendered project surfaces.
- `template_catalog.py`: Pack-local template-catalog resolution for governed template assets, section-spec contracts, and fail-closed template-heading validation.
- `governance_surfaces.py`: Cross-surface resolution helper for governed surface path, authority, rebuildability, and declared dependencies.
- `schemas.py`: Schema store and supplemental-schema registration.
- `workspace.py`: Workspace configuration, artifact source, and artifact store abstractions.
- `models/`: Typed artifact models grouped by artifact family, including the pack-facing contract surfaces used by PackContext.

## Related Surfaces
- `core/python/src/watchtower_core/adapters/README.md`
- `core/python/src/watchtower_core/repo_ops/README.md`
- `core/control_plane/README.md`
