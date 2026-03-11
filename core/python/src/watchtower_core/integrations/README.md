# `watchtower_core.integrations`

## Summary
External-system integration boundary for clients that speak to hosted services from the Python workspace.

## Boundary
- `Classification`: `boundary_layer`
- `Supported Imports`: Explicit provider subpackages such as `watchtower_core.integrations.github`.
- `Non-Goals`: Repo-local planning behavior or direct CLI orchestration.

## Key Surfaces
- `github/`: GitHub API client and related integration helpers.

## Related Surfaces
- `core/python/src/watchtower_core/integrations/github/README.md`
- `docs/standards/governance/github_collaboration_standard.md`
