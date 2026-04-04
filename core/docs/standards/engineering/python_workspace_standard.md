---
id: "std.engineering.python_workspace"
title: "Python Workspace Standard"
summary: "This standard defines how Python code, tooling, environments, and tests are organized across reusable core, host composition, and approved pack-owned package roots."
type: "standard"
status: "active"
tags:
  - "standard"
  - "engineering"
  - "python_workspace"
owner: "repository_maintainer"
updated_at: "2026-04-04T21:20:00Z"
audience: "shared"
authority: "authoritative"
---

# Python Workspace Standard

## Summary
This standard defines how Python code, tooling, environments, and tests are organized across reusable core, host composition, and approved pack-owned package roots.

## Purpose
Keep the Python workspace deterministic, easy to onboard, and isolated from the authored control plane so engineers can work in one standard local environment without scattering Python tooling across shared core and pack roots.

## Scope
- Applies to Python package code, tests, tooling, and local environment bootstrap for the shared core helper and harness layer plus approved pack-owned package roots in this repository.
- Covers workspace placement, required files, package layout, environment management, and generated-artifact boundaries.
- Does not define the full behavior of validators, query services, or control-plane artifact families.

## Use When
- Creating or restructuring Python code under `core/`.
- Adding Python dependencies, developer tools, or onboarding commands.
- Reviewing whether a Python-related file belongs in `core/python/`, an owning pack's `python/` root, or somewhere else.

## Related Standards and Sources
- [format_selection_standard.md](/core/docs/standards/data_contracts/format_selection_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [schema_standard.md](/core/docs/standards/data_contracts/schema_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [repository_path_index_standard.md](/core/docs/standards/data_contracts/repository_path_index_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md): defines the Python module-boundary, naming, typing, docstring, and consolidation rules that fit within this workspace layout.
- [repository_portability_standard.md](/core/docs/standards/engineering/repository_portability_standard.md): defines the donor-neutral bootstrap and customer-release scrub expectations that packaged Python artifacts must satisfy.
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
- Use one canonical shared Python workspace rooted at `core/python/`, with pack-owned package source boundaries rooted under their owning pack directories such as `<pack-root>/python/`.
- Use `uv` as the standard local environment and dependency-management tool.
- Keep the supported interpreter range in `core/python/pyproject.toml` and keep the locked dependency graph in `core/python/uv.lock`.
- Keep canonical package and tool configuration in `core/python/pyproject.toml`.
- Keep the locked dependency graph in `core/python/uv.lock`.
- Keep the local virtual environment at `core/python/.venv/`.
- Run Python workspace commands from `core/python/`.
- Prefer `uv run` for tests, linting, typechecking, CLI execution, and package-local Python invocations.
- Treat `uv run ...` as the default human and agent execution path. Manual virtual-environment activation is optional and mainly for interactive shell work.
- Treat `core/python/.venv/` as the canonical local environment. Do not create alternate virtual environments for normal repository work.
- For agent or automation execution, use the documented workspace entrypoint directly: prefer `uv run ...`; when a direct interpreter or tool binary is required after the workspace is synced, use `./.venv/bin/python` or `./.venv/bin/<tool>` from `core/python/`.
- Do not probe generic aliases such as `python`, `python3`, `pip`, or bare tool names before the documented workspace entrypoints, and do not treat their absence as a workflow issue when the documented workspace entrypoints exist.
- When a command is intended for both human operators and agent or automation use, prefer one explicit `--format` option with values such as `human` and `json` instead of separate bespoke `--human` and `--json` flags.
- Keep reusable-core Python source under `core/python/src/watchtower_core/`, host composition under `core/python/src/watchtower_host/`, and pack-domain Python source under the owning pack root such as `<pack-root>/python/src/watchtower_<pack>/`.
- Install pack-owned packages through the shared `core/python` workspace contract; do not rely on repo-local `sys.path` mutation to import `watchtower_<pack>` or other hosted pack packages.
- Treat downstream repositories that copy `core/` as a supported operating mode. Shared workspace docs may use the current internal pack as an example in this repository, but the hosted-pack dependency set and local editable source paths remain repo-local configuration that must match the packs actually present in the consuming repository.
- Treat copied-core portability as a source-level workflow. Do not copy donor `core/python/.venv`, environment-specific editable-install metadata, caches, or pack `.wt/runtime/**` outputs into the consuming repository.
- During copied-core bring-up, host composition may load a selected pack integration directly from the declared pack-owned `<python_root>/src` path when workspace registration is not present yet. That bootstrap path is bounded runtime compatibility only; it does not replace the requirement to persist shared `core/python/pyproject.toml` registration once the pack is integrated.
- Keep shared pack-neutral tests under `core/python/tests/`.
- Keep the fast default shared suite under `core/python/tests/unit/` and shared repository-aware orchestration coverage under `core/python/tests/integration/`.
- Keep pack-owned tests under the owning pack root such as `<pack-root>/python/tests/`.
- Do not keep tests that import `watchtower_<pack>` directly under `core/python/tests/`; those belong under the owning pack root.
- Treat repo snapshots, sdists, and wheels as separate deliverables. Customer-facing portable artifacts should exclude committed tests, fixture packs, build residue, and pack-owned `testing/` helper modules unless the recipient explicitly needs internal validation surfaces.
- Pack-owned `watchtower_<pack>.testing` modules are internal validation helpers by default, not portable runtime API surface.
- When shared-core tests need pack context, use synthetic fixture packs or typed loader/runtime seams instead of direct imports of a live hosted pack package.
- Treat effective pack activation as the first step for any pack-aware test seam. Tests that only need runtime manifest, owned roots, import resolution, or command-namespace behavior should activate the effective pack settings first and should not require a full `PackContext` unless they actually consume pack-governed surfaces.
- When a shared-core test asserts pack-local validators, authorities, rendered surfaces, workflow metadata, or other control-plane entries, derive the expected records from activated `pack_settings.json`, declared surfaces, and merged registries instead of naming the current donor repository's concrete pack IDs or tracking files.
- Do not let the live current-repository pack workspace become an accidental shared-core test dependency. If a test only passes because the active hosted-pack workspace exists, either move it under the owning pack root or replace that dependency with synthetic fixture-pack setup.
- Do not treat `plan/`, `oversight/`, or any other concrete pack root as a shared-core invariant. Portable shared tests must keep passing when another repository bootstraps a different active pack that satisfies the same contract families.
- Do not reach into one live pack root from shared-core tests through expressions such as `REPO_ROOT / "plan"` or direct copies from that root unless the test is explicitly gated for that pack-owned scenario. Shared-core tests should prove portable behavior through synthetic fixtures, typed loader seams, or active-pack-derived metadata before depending on a concrete live pack root.
- Keep shared CLI entrypoint composition under `core/python/src/watchtower_host/cli/`; pack-owned namespace registration belongs in the owning pack package.
- Keep small bootstrap or maintenance helpers under `core/python/tools/` only when the behavior cannot be expressed cleanly through `uv` commands or package entrypoints.
- A repo-local setup helper such as `./tools/setup_dev_env.sh` may automate `uv python install`, `uv sync --extra dev`, and a `watchtower-core doctor` smoke check for first-run onboarding or agent bootstrap, but it must preserve `uv run ...` as the normal daily execution contract.
- Small helper shells under `core/python/tools/` may exist to improve human onboarding or interactive use, but they must not replace the documented `uv run` contract.
- Ignore local caches, wheels, build outputs, virtual environments, and `*.egg-info` directories. Do not treat them as governed repository artifacts.
- Keep pack-local deterministic sync cache manifests under `<pack>/.wt/runtime/sync_cache/` when an active or default pack machine root is available.
- Use `core/python/.cache/watchtower/sync_cache/` only as the reusable-core fallback when no pack-local machine root is available.
- Treat `core/python/.cache/watchtower/` as disposable local runtime residue, not authored machine authority.
- Do not place generated Python artifacts directly under `core/`.
- Prefer package modules for long-lived behavior over ad hoc standalone scripts.
- Keep the first core package surfaces focused on control-plane loading, validation, explicit boundary-layer guardrails, repo-local orchestration, adapters, evidence, and operator-facing CLI or doctor commands.
- Keep deterministic derived-artifact refresh and materialization logic in the dedicated repo-local sync surfaces instead of scattering it across ad hoc scripts.
- Keep pack-owned packages such as `watchtower_<pack>` explicitly pack-owned. New generic helpers should land in `control_plane/`, `query/`, `sync/`, `rebuild/`, `routing/`, `workflow_execution/`, `evidence/`, `documentation/`, or `utils/` instead of growing broad catch-all pack-local modules inside either Python boundary.
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
| `core/python/src/watchtower_core/` | Required | Canonical reusable-core package root. |
| `core/python/src/watchtower_host/` | Required for host composition | Canonical host-owned CLI and pack-composition package root. |
| `<pack-root>/python/src/watchtower_<pack>/` | Required for each hosted pack Python surface | Pack-owned package root, installed through the shared workspace as a local editable dependency. |
| `core/python/tests/` | Required | Canonical shared pack-neutral Python test root. |
| `<pack-root>/python/tests/` | Required when the pack owns Python behavior | Pack-owned test root for direct `watchtower_<pack>` coverage. |

### Package layout
| Path | Role |
|---|---|
| `core/python/src/watchtower_core/control_plane/` | Loaders, resolvers, and artifact access for governed control-plane surfaces. |
| `core/python/src/watchtower_core/documentation/` | Repo-shared governed-document semantics, front-matter path normalization, and standard/reference helper logic. |
| `core/python/src/watchtower_core/validation/` | Validator execution, schema-backed checks, and validation result modeling. |
| `core/python/src/watchtower_core/query/` | Export-safe generic query services over governed command, workflow, route, surface, and artifact-family metadata; pack-local lifecycle or coordination query logic still lives under the owning pack path. |
| `core/python/src/watchtower_core/adapters/` | Parsers and adapters for Markdown front matter, JSON artifacts, and similar inputs. |
| `core/python/src/watchtower_core/evidence/` | Structured result, issue, and evidence helpers. |
| `core/python/src/watchtower_core/sync/` | Export-safe generic sync harness plus repo-shared command, route, and repository-path rebuild services; pack-local sync target logic still lives under the owning pack path. |
| `core/python/src/watchtower_core/rebuild/` | Export-safe rebuild harness plus registry-backed rendered-view building and markdown reconciliation. |
| `core/python/src/watchtower_core/routing/` | Export-safe route-selection runtime over governed route and workflow indexes. |
| `core/python/src/watchtower_core/workflow_execution/` | Export-safe workflow execution harness over routed workflow selection and workflow metadata. |
| `core/python/src/watchtower_core/integrations/` | External-system integration clients and adapters. |
| `core/python/src/watchtower_core/closeout/` | Fail-closed compatibility guard; pack-owned closeout services live under the owning pack root. |
| `core/python/src/watchtower_host/cli/` | Host-owned parser construction, command registration, and dispatch composition. |
| `<pack-root>/python/src/watchtower_<pack>/closeout/` | Pack-owned closeout orchestration for retained traces, initiative packages, and guarded purge flows. |
| `<pack-root>/python/src/watchtower_<pack>/` | Pack-owned planning, query, sync, validation, and document-orchestration behavior that belongs on the pack-owned side of the core-versus-domain split. |
| `<pack-root>/python/src/watchtower_<pack>/cli/` | Pack-owned namespace registration and pack-specific CLI wiring. |
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
- A pack-local query helper that searches a pack workspace or initiative-package state belongs in the owning pack package.
- A reusable route-selection engine belongs in `core/python/src/watchtower_core/routing/`.
- A reusable rebuild helper for derived surfaces belongs in `core/python/src/watchtower_core/rebuild/`.
- A generated wheel file does not belong in `core/` or `core/python/`; it should remain ignored local output.

## Operationalization
- `Modes`: `sync`; `query`; `artifact`; `documentation`
- `Operational Surfaces`: `core/python/`; `core/python/src/watchtower_core/documentation/`; `core/python/src/watchtower_core/query/`; `core/python/src/watchtower_core/sync/`; `core/python/src/watchtower_core/rebuild/`; `core/python/src/watchtower_core/routing/`; `core/python/src/watchtower_core/workflow_execution/`; `core/python/src/watchtower_host/`; `core/control_plane/`; `core/README.md`

## Validation
- `core/python/pyproject.toml` should parse and support local lockfile generation.
- `core/python/uv.lock` should stay current with the declared dependency set.
- `core/python/.venv/` should be reproducible from `uv sync --extra dev`.
- Python source should be importable through the canonical package path.
- Reusable-core packages should remain clean under the stricter `mypy` override declared in `core/python/pyproject.toml`, including `adapters/`, `validation/`, `control_plane/`, `query/`, `sync/`, `rebuild/`, `routing/`, `workflow_execution/`, `evidence/`, and `utils/`.
- `uv run pytest -q`, `uv run ruff check .`, and `uv run mypy src` should be the default narrow validation entrypoints for normal shared Python workspace work unless a narrower command is more appropriate.
- `./tools/verify.sh <fast|all> --fail-fast` should be the preferred wrapper when a remediation or refactor loop needs pytest-driven validation to stop on the first failure.
- `./.venv/bin/python -m pytest tests/unit tests/integration -q` should be the explicit broad shared-core Python test pass before closeout when repository-aware integration behavior changed.
- `./.venv/bin/python -m pytest ../../<pack-root>/python/tests -q` should be the pack-owned Python test pass when a change touches one hosted pack directly.
- `core/python/README.md` should explain one-command bootstrap via `./tools/setup_dev_env.sh`, daily `uv run` usage, and when manual activation or helper shells are appropriate.
- Reviewers should reject agent-facing Python guidance or task procedures that start by probing `python`, `python3`, `pip`, or bare tool names instead of using the documented workspace entrypoints.
- Reviewers should reject shared-workspace guidance or metadata changes that make the donor repository's hosted-pack set look like a reusable-core invariant instead of current-repository configuration.
- Reviewers should reject unapproved parallel Python source roots, committed caches, committed build outputs, or Python tooling surfaces placed outside `core/python/` and approved pack-owned boundaries.
- Reviewers should reject sync cache manifests written under `core/control_plane/` or other authored authority roots instead of pack-local runtime space or the shared Python fallback cache root.
- Reviewers should reject package artifacts that install repo-local tests or pack-owned `testing/` helpers as default runtime surface for customer delivery.
- Reviewers should reject shared-core tests or workspace guidance that hard-code donor-pack validator IDs, workflow IDs, rendered surfaces, or tracking filenames where the assertion should be resolved from the active pack contract.

## Change Control
- Update this standard when the Python workspace root, package layout, or standard environment contract changes.
- Update `core/README.md`, `core/python/README.md`, `core/python/AGENTS.md`, [python_code_design_standard.md](/core/docs/standards/engineering/python_code_design_standard.md), [deterministic_sync_cache_standard.md](/core/docs/standards/engineering/deterministic_sync_cache_standard.md), and the repository path index in the same change set when the Python workspace entrypoints or runtime cache contract change materially.
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
- The repository currently has three Python layers: reusable core under `core/python/src/watchtower_core/`, host composition under `core/python/src/watchtower_host/`, and pack-domain code plus direct pack tests under pack-owned roots such as `<pack-root>/python/src/watchtower_<pack>/` and `<pack-root>/python/tests/`.

## Updated At
- `2026-04-04T21:20:00Z`
