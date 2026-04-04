# `.githooks`

## Description
`This directory holds optional repository-local Git hooks that call the shared verification scripts under core/python/tools/.`

## Files
| Path | Description |
|---|---|
| `.githooks/README.md` | Describes the purpose of the repository-local hook directory. |
| `.githooks/pre-push` | Optional pre-push hook that runs the configured local verification mode. |

## Notes
- Install this hook path with `cd core/python && ./tools/install_git_hooks.sh`.
- Add `--fail-fast` during installation when you want the hook-driven pytest checks to stop on the first failure.
- The hook reads `watchtower.verifyMode`, optional `watchtower.verifyPack`, and optional `watchtower.verifyFailFast` from local Git config.
- Set `WATCHTOWER_SKIP_VERIFY=1` for one push when you need to bypass the local hook intentionally.
