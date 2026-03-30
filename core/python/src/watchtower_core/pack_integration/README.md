# `watchtower_core.pack_integration`

## Purpose
This package holds the reusable contracts and helpers that let `watchtower_host` load one or more hosted packs without hard-coding pack-specific behavior into reusable core.

## Contents
| Path | Purpose |
|---|---|
| `core/python/src/watchtower_core/pack_integration/__init__.py` | Typed pack-integration contracts and runtime descriptors. |
| `core/python/src/watchtower_core/pack_integration/bootstrap.py` | Shared host-wiring bootstrap that updates registry and workspace metadata together. |
| `core/python/src/watchtower_core/pack_integration/export.py` | Staged export and scrub helpers that build portability-clean customer/bootstrap bundles. |
| `core/python/src/watchtower_core/pack_integration/release_check.py` | Local release-gate orchestration that combines broad validation, schema-definition checks, dirty-worktree protection, and staged export. |
| `core/python/src/watchtower_core/pack_integration/importing.py` | Bounded pack-integration import helpers, including copied-core bootstrap-mode fallback through the declared pack python root. |
| `core/python/src/watchtower_core/pack_integration/runtime.py` | Generic pack runtime loading and runtime-shape validation helpers. |
| `core/python/src/watchtower_core/pack_integration/runtime_registry.py` | Effective runtime hosted-pack view that merges authored registry entries with valid manifest-discovered packs during copied-core bring-up. |
| `core/python/src/watchtower_core/pack_integration/docs.py` | Canonical helpers for pack-owned command-doc roots and namespace entry pages. |
| `core/python/src/watchtower_core/pack_integration/scaffold.py` | Reusable starter-generation helpers that render hosted-pack template bundles without hard-coding pack specifics into host handlers. |
| `core/python/src/watchtower_core/pack_integration/workspace_registration.py` | Shared `core/python/pyproject.toml` registration helpers for hosted pack distributions and source paths. |

## Guidance
- Keep this package reusable-core only.
- Put pack-owned implementation details in the owning `watchtower_<pack>` package.
- Put host-only parser composition in `watchtower_host`.
- Use the helpers here when host code, validation code, and command-index sync all need the same pack-contract path rules.
- Prefer `watchtower-core pack scaffold` for pack-owned starter generation and `watchtower-core pack bootstrap` for shared registry plus workspace wiring.
- Use `watchtower-core pack export` when the deliverable is a curated customer/bootstrap bundle instead of an internal engineering checkout. Add `--pack-only` when you need only the scrubbed hosted-pack roots without shared core.
- Keep pack-specific staged-export cleanup in the owning `watchtower_<pack>` package through the optional `export_cleanup` capability instead of hard-coding pack history rules into reusable core.
- Use `watchtower-core release check` when you want the local fail-closed release gate to enforce dirty-worktree protection, the broad validation baseline, schema-definition checks, and the final staged export in one command.
- Treat runtime-only discovered packs as bootstrap-mode compatibility for copied-core consuming repositories. Shared registry and shared workspace wiring remain the steady-state integration contract once a pack is meant to stay integrated.
