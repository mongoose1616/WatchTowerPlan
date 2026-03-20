# `watchtower_core.pack_integration`

## Purpose
This package holds the reusable contracts and helpers that let `watchtower_host` load one or more hosted packs without hard-coding pack-specific behavior into reusable core.

## Contents
| Path | Purpose |
|---|---|
| `core/python/src/watchtower_core/pack_integration/__init__.py` | Typed pack-integration contracts and runtime descriptors. |
| `core/python/src/watchtower_core/pack_integration/runtime.py` | Generic pack runtime loading and runtime-shape validation helpers. |
| `core/python/src/watchtower_core/pack_integration/docs.py` | Canonical helpers for pack-owned command-doc roots and namespace entry pages. |

## Guidance
- Keep this package reusable-core only.
- Put pack-owned implementation details in the owning `watchtower_<pack>` package.
- Put host-only parser composition in `watchtower_host`.
- Use the helpers here when host code, validation code, and command-index sync all need the same pack-contract path rules.
