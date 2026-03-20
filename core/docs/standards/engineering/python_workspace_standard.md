---
id: "std.engineering.python_workspace"
title: "Python Workspace Standard"
summary: "This standard defines how Python code, tooling, environments, and tests are organized across the shared `core/python/` workspace and the approved plan-owned package root under `plan/python/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "engineering"
  - "python_workspace"
owner: "repository_maintainer"
updated_at: "2026-03-20T09:26:00Z"
audience: "shared"
authority: "authoritative"
---

# Python Workspace Standard

## Summary
This standard defines how Python code, tooling, environments, and tests are organized across the shared `core/python/` workspace and the approved plan-owned package root under `plan/python/`.

## Purpose
Keep the Python workspace deterministic, easy to onboard, and isolated from the authored control plane so engineers can work in one standard local environment without scattering Python tooling across `core/` and `plan/`.

## Scope
- Applies to Python package code, tests, tooling, and local environment bootstrap for the shared core helper and harness layer plus the approved plan-owned package root.
- Covers workspace placement, required files, package layout, environment management, and generated-artifact boundaries.
- Does not define the full behavior of validators, query services, or control-plane artifact families.

## Use When
- Creating or restructuring Python code under `core/`.
- Adding Python dependencies, developer tools, or onboarding commands.
- Reviewing whether a Python-related file belongs in `core/python/`, `plan/python/`, or somewhere else.

## Related Standards and Sources
- [format_selection_standard.md](/core/docs/standards/data_contracts/format_selection_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [schema_standard.md](/core/docs/standards/data_contracts/schema_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [repository_path_index_standard.md](/core/docs/standards/data_contracts/repository_path_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md): defines the Python module-boundary, naming, typing, docstring, and consolidation rules that fit within this workspace layout.
- [naming_and_ids_standard.md](/core/docs/standards/metadata/naming_and_ids_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [src_layout_reference.md](/core/docs/references/src_layout_reference.md): local reference surface for the external or canonical guidance this standard depends on.
- [pyproject_toml_reference.md](/core/docs/references/pyproject_toml_reference.md): local reference surface for the external or canonical guidance this standard depends on.
- [uv_reference.md](/core/docs/references/uv_reference.md): local reference surface for the external or canonical guidance this standard depends on.
- [pytest_reference.md](/core/docs/references/pytest_reference.md): local reference surface for the external or canonical guidance this standard depends on.
- [ruff_reference.md](/core/docs/references/ruff_reference.md): local reference surface for the external or canonical guidance this standard depends on.
- [mypy_reference.md](/core/docs/references/mypy_reference.md): local reference surface for the external or canonical guidance this standard depends on.

## Guidance
- Keep shared Python tooling, tests, and the local virtual environment under `core/python/`.
- Keep authored machine-readable authority under `core/control_plane/`; do not move schemas, registries, contracts, manifests, or indexes into the Python workspace.
- Use one canonical shared Python workspace rooted at `core/python/`, with the approved plan-owned package source boundary rooted at `plan/python/`.
- Use `uv` as the standard local environment and dependency-management tool.
- Keep the supported interpreter range in `core/python/pyproject.toml` and keep the locked dependency graph in `core/python/uv.lock`.
- Keep canonical package and tool configuration in `core/python/pyproject.toml`.
- Keep the locked dependency graph in `core/python/uv.lock`.
- Keep the local virtual environment at `core/python/.venv/`.
- Run Python workspace commands from `core/python/`.
- Prefer `uv run` for tests, linting, typechecking, CLI execution, and package-local Python invocations.
- Treat `uv run ...` as the default human and agent execution path. Manual virtual-environment activation is optional and mainly for interactive shell work.
- Treat `core/python/.venv/` as the canonical local environment. Do not create alternate virtual environments for normal repository work.
- When a command is intended for both human operators and agent or automation use, prefer one explicit `--format` option with values such as `human` and `json` instead of separate bespoke `--human` and `--json` flags.
- Keep reusable-core Python source under `core/python/src/watchtower_core/` and plan-domain Python source under `plan/python/src/watchtower_plan/`.
- Install the plan-owned package through the shared `core/python` workspace contract; do not rely on repo-local `sys.path` mutation to import `watchtower_plan`.
- Keep tests under `core/python/tests/`.
- Keep the fast default suite under `core/python/tests/unit/` and repository-aware orchestration coverage under `core/python/tests/integration/`.
- Keep thin entrypoints under `core/python/src/watchtower_core/cli/`; do not create parallel top-level CLI source trees outside the package.
- Keep small bootstrap or maintenance helpers under `core/python/tools/` only when the behavior cannot be expressed cleanly through `uv` commands or package entrypoints.
- Small helper shells under `core/python/tools/` may exist to improve human onboarding or interactive use, but they must not replace the documented `uv run` contract.
- Ignore local caches, wheels, build outputs, virtual environments, and `*.egg-info` directories. Do not treat them as governed repository artifacts.
- Do not place generated Python artifacts directly under `core/`.
- Prefer package modules for long-lived behavior over ad hoc standalone scripts.
- Keep the first core package surfaces focused on control-plane loading, validation, explicit boundary-layer guardrails, repo-local orchestration, adapters, evidence, and operator-facing CLI or doctor commands.
- Keep deterministic derived-artifact refresh and materialization logic in the dedicated repo-local sync surfaces instead of scattering it across ad hoc scripts.
- Keep `watchtower_plan` explicitly plan-owned. New generic helpers should land in `control_plane/`, `query/`, `sync/`, `rebuild/`, `routing/`, `workflow_execution/`, `evidence/`, `documentation/`, or `utils/` instead of growing broad catch-all repo-local modules inside either Python boundary.
- Use [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md) for Python naming, boundary, docstring, typing, and consolidation rules instead of re-encoding those choices in workspace-only guidance.

## Structure or Data Model
### Required workspace surfaces
| Path | Requirement | Notes |
|---|---|---|
| `core/python/AGENTS.md` | Required | Local instruction layer for agents working in the Python workspace. |
| `core/python/README.md` | Required | Human-readable onboarding and workspace orientation. |
| `core/python/pyproject.toml` and `core/python/uv.lock` | Required | Define the supported interpreter range and the locked dependency set. |
| `core/python/pyproject.toml` | Required | Canonical project metadata, dependencies, and tool configuration. |
| `core/python/uv.lock` | Required | Locked dependency graph for repeatable onboarding. |
| `core/python/.gitignore` | Required | Ignores local envs, caches, and build outputs. |
| `core/python/src/watchtower_core/` | Required | Canonical package root. |
| `plan/python/src/watchtower_plan/` | Required for plan-domain Python | Approved plan-owned package root, installed through the shared workspace as a local editable dependency. |
| `core/python/tests/` | Required | Canonical Python test root. |

### Package layout
| Path | Role |
|---|---|
| `core/python/src/watchtower_core/control_plane/` | Loaders, resolvers, and artifact access for governed control-plane surfaces. |
| `core/python/src/watchtower_core/documentation/` | Repo-shared governed-document semantics, front-matter path normalization, and standard/reference helper logic. |
| `core/python/src/watchtower_core/validation/` | Validator execution, schema-backed checks, and validation result modeling. |
| `core/python/src/watchtower_core/query/` | Export-safe generic query services over governed command, workflow, route, surface, and artifact-family metadata; authoritative live planning query logic still lives under `plan/python/src/watchtower_plan/query/`. |
| `core/python/src/watchtower_core/adapters/` | Parsers and adapters for Markdown front matter, JSON artifacts, and similar inputs. |
| `core/python/src/watchtower_core/evidence/` | Structured result, issue, and evidence helpers. |
| `core/python/src/watchtower_core/sync/` | Export-safe generic sync harness plus repo-shared command, route, and repository-path rebuild services; plan-domain sync target logic still lives under `plan/python/src/watchtower_plan/sync/`. |
| `core/python/src/watchtower_core/rebuild/` | Export-safe rebuild harness plus registry-backed rendered-view building and markdown reconciliation. |
| `core/python/src/watchtower_core/routing/` | Export-safe route-selection runtime over governed route and workflow indexes. |
| `core/python/src/watchtower_core/workflow_execution/` | Export-safe workflow execution harness over routed workflow selection and workflow metadata. |
| `core/python/src/watchtower_core/integrations/` | External-system integration clients and adapters. |
| `core/python/src/watchtower_core/closeout/` | Fail-closed compatibility guard; plan-domain closeout services live under `plan/python/src/watchtower_plan/closeout/`. |
| `plan/python/src/watchtower_plan/closeout/` | Plan-domain closeout orchestration for retained traces, initiative packages, and guarded purge flows. |
| `plan/python/src/watchtower_plan/` | Approved WatchTowerPlan-specific planning, query, sync, validation, and document-orchestration behavior that belongs on the plan-owned side of the core-versus-domain split. |
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
- A reusable-core query helper that searches governed command, workflow, authority, route, or artifact-family metadata belongs in `core/python/src/watchtower_core/query/`.
- A repo-local query helper that searches live planning indexes or initiative packages belongs in `plan/python/src/watchtower_plan/query/`.
- A reusable route-selection engine belongs in `core/python/src/watchtower_core/routing/`.
- A reusable rebuild helper for derived surfaces belongs in `core/python/src/watchtower_core/rebuild/`.
- A generated wheel file does not belong in `core/` or `core/python/`; it should remain ignored local output.

## Operationalization
- `Modes`: `sync`; `query`; `artifact`; `documentation`
- `Operational Surfaces`: `plan/python/src/watchtower_plan/`; `plan/python/src/watchtower_plan/sync/`; `plan/python/src/watchtower_plan/query/`; `core/python/src/watchtower_core/documentation/`; `core/python/src/watchtower_core/query/`; `core/python/src/watchtower_core/sync/`; `core/python/src/watchtower_core/rebuild/`; `core/python/src/watchtower_core/routing/`; `core/python/src/watchtower_core/workflow_execution/`; `core/control_plane/`; `core/README.md`

## Validation
- `core/python/pyproject.toml` should parse and support local lockfile generation.
- `core/python/uv.lock` should stay current with the declared dependency set.
- `core/python/.venv/` should be reproducible from `uv sync --extra dev`.
- Python source should be importable through the canonical package path.
- Reusable-core packages should remain clean under the stricter `mypy` override declared in `core/python/pyproject.toml`, including `adapters/`, `validation/`, `control_plane/`, `query/`, `sync/`, `rebuild/`, `routing/`, `workflow_execution/`, `evidence/`, and `utils/`.
- `uv run pytest -q`, `uv run ruff check .`, and `uv run mypy src` should be the default narrow validation entrypoints for normal Python workspace work unless a narrower command is more appropriate.
- `./.venv/bin/python -m pytest tests/unit tests/integration -q` should be the explicit broad Python test pass before closeout when repository-aware integration behavior changed.
- `core/python/README.md` should explain one-time setup, daily `uv run` usage, and when manual activation or helper shells are appropriate.
- Reviewers should reject unapproved parallel Python source roots, committed caches, committed build outputs, or Python tooling surfaces placed outside `core/python/` and the approved `plan/python/` boundary.

## Change Control
- Update this standard when the Python workspace root, package layout, or standard environment contract changes.
- Update `core/README.md`, `core/python/README.md`, `core/python/AGENTS.md`, [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md), and the repository path index in the same change set when the Python workspace entrypoints change materially.
- Update affected design records when the package boundaries for validators, query, sync, rebuild, routing, workflow execution, or control-plane loading change materially.

## References
- [src_layout_reference.md](/core/docs/references/src_layout_reference.md)
- [pyproject_toml_reference.md](/core/docs/references/pyproject_toml_reference.md)
- [uv_reference.md](/core/docs/references/uv_reference.md)
- [pytest_reference.md](/core/docs/references/pytest_reference.md)
- [ruff_reference.md](/core/docs/references/ruff_reference.md)
- [mypy_reference.md](/core/docs/references/mypy_reference.md)
- [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md)

## Notes
- This standard intentionally keeps the shared Python workspace as a sibling of `core/control_plane/` rather than nesting the control plane inside Python-specific tooling.
- The repository now has two approved Python package roots: reusable core under `core/python/src/watchtower_core/` and plan-domain code under `plan/python/src/watchtower_plan/`.

## Updated At
- `2026-03-20T09:26:00Z`
