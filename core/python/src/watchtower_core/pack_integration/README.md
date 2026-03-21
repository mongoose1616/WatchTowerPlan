# `watchtower_core.pack_integration`

## Purpose
This package holds the reusable contracts and helpers that let `watchtower_host` load one or more hosted packs without hard-coding pack-specific behavior into reusable core.

## Contents
| Path | Purpose |
|---|---|
| `core/python/src/watchtower_core/pack_integration/__init__.py` | Typed pack-integration contracts and runtime descriptors. |
| `core/python/src/watchtower_core/pack_integration/bootstrap.py` | Shared host-wiring bootstrap that updates registry and workspace metadata together. |
| `core/python/src/watchtower_core/pack_integration/runtime.py` | Generic pack runtime loading and runtime-shape validation helpers. |
| `core/python/src/watchtower_core/pack_integration/docs.py` | Canonical helpers for pack-owned command-doc roots and namespace entry pages. |
| `core/python/src/watchtower_core/pack_integration/scaffold.py` | Reusable starter-generation helpers that render hosted-pack template bundles without hard-coding pack specifics into host handlers. |
| `core/python/src/watchtower_core/pack_integration/workspace_registration.py` | Shared `core/python/pyproject.toml` registration helpers for hosted pack distributions and source paths. |

## Guidance
- Keep this package reusable-core only.
- Put pack-owned implementation details in the owning `watchtower_<pack>` package.
- Put host-only parser composition in `watchtower_host`.
- Use the helpers here when host code, validation code, and command-index sync all need the same pack-contract path rules.
- Prefer `watchtower-core pack scaffold` for pack-owned starter generation and `watchtower-core pack bootstrap` for shared registry plus workspace wiring.
