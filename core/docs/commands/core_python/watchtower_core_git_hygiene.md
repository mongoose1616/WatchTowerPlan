# `watchtower-core git hygiene`

## Summary
This command evaluates local branches and worktrees against the repository's old-state cleanup rules and can apply only the cleanup actions marked safe enough for automation.

## Use When
- You need to decide whether a local branch or temporary worktree should be kept, reviewed, merged, deleted, or removed.
- You want the current cleanup policy applied consistently instead of relying on age alone.
- You want a conservative `--apply` path for clearly merged or empty branches and clean removable worktrees.

## Command
| Field | Value |
|---|---|
| Invocation | `watchtower-core git hygiene` |
| Kind | `subcommand` |
| Workspace | `core_python` |
| Source Surface | `core/python/src/watchtower_host/cli/git_handlers.py` |

## Synopsis
```sh
cd core/python
uv run watchtower-core git hygiene [--repo-root <path>] [--base-ref <ref>] [--inactive-days <days>] [--override-path <path>] [--apply] [--format <human|json>]
```

## Arguments and Options
- `--repo-root <path>`: Optional path inside the target git worktree. Defaults to the current working directory.
- `--base-ref <ref>`: Base ref used for merge-state and unique-commit evaluation. Defaults to `main` and falls back to `origin/main` when needed.
- `--inactive-days <days>`: Inactivity threshold used as one old-state signal. Defaults to `14`.
- `--override-path <path>`: Optional JSON file that carries local-only defer, handoff, supersession, or owner metadata. Defaults to `<git-common-dir>/watchtower/git_hygiene_overrides.json`.
- `--apply`: Apply only the conservative cleanup actions marked safe by the evaluation.
- `--format <human|json>`: Select human-readable or structured JSON output. Agents should prefer `json`.
- `-h`, `--help`: Show the command help text.

## Examples
```sh
cd core/python
uv run watchtower-core git hygiene --format json
```

```sh
cd core/python
uv run watchtower-core git hygiene --base-ref origin/main --format json
```

```sh
cd core/python
uv run watchtower-core git hygiene --override-path .git/watchtower/git_hygiene_overrides.json --format json
```

```sh
cd core/python
uv run watchtower-core git hygiene --apply --format json
```

## Behavior and Outputs
- The command evaluates every local branch plus every listed git worktree under the resolved repository root.
- Branch evaluation uses merge state, unique remaining commits, worktree dirtiness, staged or uncommitted work, inactivity age, and local override metadata instead of duration alone.
- Worktree evaluation uses the bound branch state, worktree cleanliness, staged and unstaged changes, recent local file activity, and the same override metadata.
- The local base branch is always protected from automatic deletion even when you run the command from another branch.
- The default override file is local-only runtime state under the git common directory, not a versioned control-plane artifact.
- In `json` mode, the payload includes branch records, worktree records, recommended actions, and any actions applied during the run.
- In `human` mode, the command prints a focused branch and worktree action summary.
- `--apply` removes only clean non-primary worktrees recommended for removal and deletes only branches recommended as safe `delete_branch` targets after reevaluating post-worktree cleanup.

## Related Commands
| Command | Relationship |
|---|---|
| `watchtower-core git` | Parent command group for local git hygiene review. |
| `watchtower-core route preview` | Shows the workflow route for a branch-hygiene or worktree-cleanup request. |
| `watchtower-core release check` | Separate release gate that inspects worktree cleanliness before staging a customer export. |

## Source Surface
- `core/python/src/watchtower_host/cli/git_handlers.py`
- `core/python/src/watchtower_host/cli/git_family.py`
- `core/python/src/watchtower_core/utils/git_hygiene.py`

## Updated At
- `2026-04-04T22:50:00Z`
