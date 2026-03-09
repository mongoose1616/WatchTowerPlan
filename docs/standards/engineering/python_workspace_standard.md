# Python Workspace Standard

## Summary
This standard defines how Python code, tooling, environments, and tests are organized for the core helper and harness layer under `core/python/`.

## Purpose
Keep the Python workspace deterministic, easy to onboard, and isolated from the authored control plane so engineers can work in one standard local environment without scattering Python tooling across `core/`.

## Scope
- Applies to Python package code, tests, tooling, and local environment bootstrap for the core helper and harness layer.
- Covers workspace placement, required files, package layout, environment management, and generated-artifact boundaries.
- Does not define the full behavior of validators, query services, or control-plane artifact families.

## Use When
- Creating or restructuring Python code under `core/`.
- Adding Python dependencies, developer tools, or onboarding commands.
- Reviewing whether a Python-related file belongs in `core/python/` or somewhere else.

## Related Standards and Sources
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)
- [repository_path_index_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/repository_path_index_standard.md)
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)
- [src_layout_reference.md](/home/j/WatchTowerPlan/docs/references/src_layout_reference.md)
- [pyproject_toml_reference.md](/home/j/WatchTowerPlan/docs/references/pyproject_toml_reference.md)
- [uv_reference.md](/home/j/WatchTowerPlan/docs/references/uv_reference.md)
- [pytest_reference.md](/home/j/WatchTowerPlan/docs/references/pytest_reference.md)
- [ruff_reference.md](/home/j/WatchTowerPlan/docs/references/ruff_reference.md)
- [mypy_reference.md](/home/j/WatchTowerPlan/docs/references/mypy_reference.md)

## Guidance
- Keep all Python-specific repository surfaces under `core/python/`.
- Keep authored machine-readable authority under `core/control_plane/`; do not move schemas, registries, contracts, policies, or indexes into the Python workspace.
- Use one canonical Python workspace rooted at `core/python/`.
- Use `uv` as the standard local environment and dependency-management tool.
- Keep the pinned interpreter version in `core/python/.python-version`.
- Keep canonical package and tool configuration in `core/python/pyproject.toml`.
- Keep the locked dependency graph in `core/python/uv.lock`.
- Keep the local virtual environment at `core/python/.venv/`.
- Run Python workspace commands from `core/python/`.
- Prefer `uv run` for tests, linting, typechecking, CLI execution, and package-local Python invocations.
- Treat `core/python/.venv/` as the canonical local environment. Do not create alternate virtual environments for normal repository work.
- Keep Python source code under `core/python/src/` with one package root at `core/python/src/watchtower_core/`.
- Keep tests under `core/python/tests/`.
- Keep thin entrypoints under `core/python/src/watchtower_core/cli/`; do not create parallel top-level CLI source trees outside the package.
- Keep small bootstrap or maintenance helpers under `core/python/tools/` only when the behavior cannot be expressed cleanly through `uv` commands or package entrypoints.
- Ignore local caches, wheels, build outputs, virtual environments, and `*.egg-info` directories. Do not treat them as governed repository artifacts.
- Do not place generated Python artifacts directly under `core/`.
- Prefer package modules for long-lived behavior over ad hoc standalone scripts.
- Keep the first core package surfaces focused on control-plane loading, validation, query, adapters, evidence, and operator-facing CLI or doctor commands.

## Structure or Data Model
### Required workspace surfaces
| Path | Requirement | Notes |
|---|---|---|
| `core/python/AGENTS.md` | Required | Local instruction layer for agents working in the Python workspace. |
| `core/python/README.md` | Required | Human-readable onboarding and workspace orientation. |
| `core/python/.python-version` | Required | Pins the expected Python major and minor version. |
| `core/python/pyproject.toml` | Required | Canonical project metadata, dependencies, and tool configuration. |
| `core/python/uv.lock` | Required | Locked dependency graph for repeatable onboarding. |
| `core/python/.gitignore` | Required | Ignores local envs, caches, and build outputs. |
| `core/python/src/watchtower_core/` | Required | Canonical package root. |
| `core/python/tests/` | Required | Canonical Python test root. |

### Package layout
| Path | Role |
|---|---|
| `core/python/src/watchtower_core/control_plane/` | Loaders, resolvers, and artifact access for governed control-plane surfaces. |
| `core/python/src/watchtower_core/validation/` | Validator execution, schema-backed checks, and validation result modeling. |
| `core/python/src/watchtower_core/query/` | Index-backed retrieval and structured query helpers. |
| `core/python/src/watchtower_core/adapters/` | Parsers and adapters for Markdown front matter, JSON artifacts, and similar inputs. |
| `core/python/src/watchtower_core/evidence/` | Structured result, issue, and evidence helpers. |
| `core/python/src/watchtower_core/cli/` | Thin entrypoints and operator-facing commands. |
| `core/python/src/watchtower_core/utils/` | Narrow shared helpers that do not justify a first-class domain package. |

## Process or Workflow
1. Add or update Python code under `core/python/`.
2. Keep workspace metadata, lockfile, and source layout aligned in the same change set.
3. Update onboarding commands in `core/python/README.md` and any affected command pages when the environment or CLI contract changes.
4. Keep `core/python/AGENTS.md` aligned when the standard Python execution path for agents changes.
5. Validate the workspace with the standard checks before treating the change as complete.
6. Update related design docs, inventories, and path indexes in the same change set when the Python workspace entrypoints change materially.

## Examples
- A new schema loader belongs in `core/python/src/watchtower_core/control_plane/`.
- A front matter validator belongs in `core/python/src/watchtower_core/validation/`.
- A query helper that searches the repository path index belongs in `core/python/src/watchtower_core/query/`.
- A generated wheel file does not belong in `core/` or `core/python/`; it should remain ignored local output.

## Validation
- `core/python/pyproject.toml` should parse and support local lockfile generation.
- `core/python/uv.lock` should stay current with the declared dependency set.
- `core/python/.venv/` should be reproducible from `uv sync --extra dev`.
- Python source should be importable through the canonical package path.
- `uv run pytest`, `uv run ruff check .`, and `uv run mypy src` should be the default validation entrypoints for normal Python workspace work unless a narrower command is more appropriate.
- Reviewers should reject parallel Python source roots, committed caches, committed build outputs, or Python tooling surfaces placed outside `core/python/`.

## Change Control
- Update this standard when the Python workspace root, package layout, or standard environment contract changes.
- Update `core/README.md`, `core/python/README.md`, `core/python/AGENTS.md`, and the repository path index in the same change set when the Python workspace entrypoints change materially.
- Update affected feature designs when the package boundaries for validators, query, or control-plane loading change materially.

## References
- [src_layout_reference.md](/home/j/WatchTowerPlan/docs/references/src_layout_reference.md)
- [pyproject_toml_reference.md](/home/j/WatchTowerPlan/docs/references/pyproject_toml_reference.md)
- [uv_reference.md](/home/j/WatchTowerPlan/docs/references/uv_reference.md)
- [pytest_reference.md](/home/j/WatchTowerPlan/docs/references/pytest_reference.md)
- [ruff_reference.md](/home/j/WatchTowerPlan/docs/references/ruff_reference.md)
- [mypy_reference.md](/home/j/WatchTowerPlan/docs/references/mypy_reference.md)

## Notes
- This standard intentionally keeps the Python workspace as a sibling of `core/control_plane/` rather than nesting the control plane inside Python-specific tooling.
- The workspace may grow additional modules over time, but it should not grow additional package roots unless a later standard explicitly allows that change.

## Last Synced
- `2026-03-09`
