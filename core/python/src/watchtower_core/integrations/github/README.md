# `watchtower_core.integrations.github`

## Summary
GitHub API client support for task sync and other hosted collaboration flows.

## Boundary
- `Classification`: `boundary_layer`
- `Supported Imports`: `watchtower_core.integrations.github.client`
- `Non-Goals`: Repo-local task-mirror policy or planning-document authority rules.

## Key Surfaces
- `client.py`: GitHub REST and GraphQL client helpers used by task sync.

## Related Surfaces
- `core/python/src/watchtower_core/repo_ops/sync/README.md`
- `docs/standards/governance/github_task_sync_standard.md`
