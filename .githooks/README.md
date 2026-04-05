# `.githooks`

## Description
`This directory holds optional repository-local Git hooks that run lightweight lint and type checks before pushing.`

## Files
| Path | Description |
|---|---|
| `.githooks/README.md` | Describes the purpose of the repository-local hook directory. |
| `.githooks/pre-push` | Lightweight pre-push hook that runs mypy and ruff (~0.2 s). |

## Notes
- This directory is tracked in the repository. After cloning, activate it once with `cd core/python && ./tools/install_git_hooks.sh` (sets `core.hooksPath`).
- The hook runs only mypy and ruff — full test suites are run manually via `verify.sh`.
- Set `WATCHTOWER_SKIP_VERIFY=1` for one push when you need to bypass the hook intentionally.
