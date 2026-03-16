# `core/control_plane/manifests`

## Description
`This directory holds authored machine-readable startup and descriptive declarations owned by core. Keep manifest-like documents here when they declare reusable-core load inputs or other shared control-plane facts.`

## Files
| Path | Description |
|---|---|
| `core/control_plane/manifests/README.md` | Describes the purpose of the manifests directory and its current contents. |
| `core/control_plane/manifests/pack_settings.json` | Canonical load root for reusable-core startup and pack-context materialization. |
| `core/control_plane/manifests/repository_manifest.v1.json` | Supporting repository inventory of top-level governed surfaces and command entrypoints. |

## Notes
- `pack_settings.json` is the startup contract consumed by `ControlPlaneLoader.load_pack_settings()` and `ControlPlaneLoader.load_pack_context()`.
- `repository_manifest.v1.json` is descriptive inventory, not the reusable-core load root.
