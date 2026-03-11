# `watchtower_core.adapters`

## Summary
Shared helpers for parsing and normalizing governed front matter and Markdown content.

## Boundary
- `Classification`: `reusable_core`
- `Supported Imports`: `watchtower_core.adapters`
- `Non-Goals`: Repo-wide planning joins, task lifecycle logic, or CLI command registration.

## Key Surfaces
- `front_matter.py`: Parse, render, and replace governed YAML front matter.
- `markdown.py`: Extract sections, links, metadata bullets, and repo-path references from governed Markdown.

## Related Surfaces
- `core/python/src/watchtower_core/control_plane/README.md`
- `core/python/src/watchtower_core/repo_ops/README.md`
