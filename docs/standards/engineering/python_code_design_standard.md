---
id: "std.engineering.python_code_design"
title: "Python Code Design Standard"
summary: "This standard defines the local design philosophy, naming rules, and consolidation rules for Python code under `core/python/`."
type: "standard"
status: "active"
tags:
  - "standard"
  - "engineering"
  - "python_code_design"
owner: "repository_maintainer"
updated_at: "2026-03-18T06:44:55Z"
audience: "shared"
authority: "authoritative"
---

# Python Code Design Standard

## Summary
This standard defines the local design philosophy, naming rules, and consolidation rules for Python code under `core/python/`.

## Purpose
Keep the Python workspace coherent, explicit, and easy to maintain by giving contributors one authoritative rule set for module shape, naming, typing, documentation, testing, and reusable-core extraction.

## Scope
- Applies to Python package code under `core/python/src/watchtower_core/`, workspace tests under `core/python/tests/`, and the package-facing docs that describe those code boundaries.
- Covers module responsibilities, boundary placement, naming, typing posture, docstrings, tests, and how to reduce sprawl or duplication.
- Does not redefine workspace bootstrap, dependency management, or repository-wide git process rules that already belong to narrower or broader standards.

## Use When
- Adding or refactoring Python modules under `core/python/src/watchtower_core/`.
- Reviewing whether a new helper belongs in `control_plane/`, a reusable-core runtime package, `repo_ops/`, or `cli/`.
- Choosing names for modules, classes, services, helpers, results, or tests.
- Consolidating duplicate code or shrinking transitional surfaces such as `repo_ops/`.

## Related Standards and Sources
- [python_workspace_standard.md](/docs/standards/engineering/python_workspace_standard.md): defines the workspace, package-root, and toolchain constraints that this code-design standard must fit within.
- [engineering_best_practices_standard.md](/docs/standards/engineering/engineering_best_practices_standard.md): defines the broader repository engineering checkpoints that this Python-specific standard refines.
- [naming_and_ids_standard.md](/docs/standards/metadata/naming_and_ids_standard.md): governs stable artifact naming and keeps code-local naming advice from drifting into governed-ID policy.
- [engineering_design_principles.md](/docs/foundations/engineering_design_principles.md): defines the repository-wide design philosophy that this Python standard operationalizes for code structure.
- [pep8_reference.md](/docs/references/pep8_reference.md): provides the upstream readability baseline for module, class, function, constant, import, and comment style.
- [pep257_reference.md](/docs/references/pep257_reference.md): provides the upstream baseline for concise docstrings on public or non-obvious Python surfaces.
- [src_layout_reference.md](/docs/references/src_layout_reference.md): reinforces the package-boundary and import-discipline expectations of the `src/` layout used here.
- [pyproject_toml_reference.md](/docs/references/pyproject_toml_reference.md): supports the one-file tool-configuration and package-metadata assumptions this standard relies on.
- [ruff_reference.md](/docs/references/ruff_reference.md): supports the lint and import-order rules that keep local style predictable.
- [mypy_reference.md](/docs/references/mypy_reference.md): supports the typed-boundary and gradual-strictness expectations defined here.
- [pytest_reference.md](/docs/references/pytest_reference.md): supports the testing posture for observable behavior and focused fixtures.

## Guidance
- Prefer explicitness over cleverness. Code should be easy to read in one pass without hidden control flow, magical defaults, or broad implicit repository scans.
- Prefer extraction to a reusable-core package before growing `repo_ops/`. If logic is not specific to this repository's live planning corpus or repo-local artifact layout, move it out of `repo_ops/`.
- Keep modules narrow and named after one primary responsibility. Split files before they become mixed-purpose collections of query logic, parsing, rendering, validation, and orchestration.
- Keep package boundaries explicit:
  - `control_plane/` owns reusable loaders, registries, policies, resolvers, and typed governed-artifact models.
  - `query/`, `sync/`, `rebuild/`, `routing/`, `workflow_execution/`, `evidence/`, `closeout/`, and `utils/` own reusable runtime seams.
  - `repo_ops/` owns only residual repository-local orchestration that still depends on this repository's live planning or governed layout.
  - `cli/` owns argument parsing, command wiring, and output shaping, not business logic.
- Prefer one canonical implementation for each behavior. Delete compatibility shims, dead wrappers, and parallel helpers once callers migrate.
- Consolidate duplicated control flow behind a shared helper only when the repetition is structural and the new helper has a clear boundary. Do not create generic abstractions that are broader than the duplicated behavior.
- Prefer pure or read-oriented helpers for parsing, filtering, shaping, or summarizing data. Keep filesystem writes, sync operations, closeout steps, and other side effects in explicit orchestration layers.
- Keep interfaces argument-driven. Pass explicit dependencies, paths, IDs, filters, and write options instead of relying on hidden globals or embedded task-specific constants.
- Use standard Python naming:
  - Modules, functions, variables, and tests use `snake_case`.
  - Classes use `CapWords`.
  - Module-level constants use `UPPER_SNAKE_CASE`.
  - Predicate functions and boolean fields should read as booleans, such as `is_ready`, `has_drift`, or `should_write`.
- Use role-bearing type names only when the role is real:
  - `*Service` for a scoped orchestration or lifecycle owner.
  - `*Helper` for a narrow stateless policy, registry, lookup, or transformation surface.
  - `*Result`, `*Issue`, `*Request`, `*Descriptor`, or `*Record` for explicit data shapes.
  - Avoid vague names such as `helpers`, `utils`, `misc`, `manager`, or `common` unless the module truly centralizes one repeated pattern and no narrower name fits.
- Keep public module, class, and non-obvious callable docstrings concise and behavior-focused. Do not document trivial private helpers by default, and do not let docstrings drift behind the implementation.
- Keep comments rare and useful. Explain intent, invariants, or non-obvious constraints, not line-by-line mechanics.
- Type reusable and cross-module boundaries first. Public functions, services, and typed records should make inputs and outputs explicit.
- Keep `Any` at the edges where untyped libraries, JSON payloads, or dynamic external data make it unavoidable. Convert into narrower local shapes quickly instead of letting `Any` spread.
- Prefer typed records or small data classes over loose dict conventions for internal multi-field data when the shape is stable and not already governed by a schema-backed artifact contract.
- Keep imports grouped as standard library, third-party, and local package imports. Avoid wildcard imports and avoid import-time side effects beyond constant or lightweight registry initialization.
- Write tests around observable behavior. Use unit tests for narrow helpers and integration tests for repo-local orchestration, loader behavior, or multi-surface sync flows.
- Keep fixtures local and explicit. Prefer a small helper or fixture near the tests that need it over a broad hidden fixture tree.

## Structure or Data Model
### Python boundary checkpoints
| Checkpoint | Preferred Shape | Notes |
|---|---|---|
| Boundary placement | reusable-core first, `repo_ops/` only when repo-local state truly matters | New generic helpers should not land in transitional namespaces. |
| Module size | one primary responsibility | Split files before they become mixed-purpose grab bags. |
| Interface style | explicit arguments and typed return values | Hidden globals and embedded task constants increase maintenance cost. |
| Naming | role-bearing, specific, and boring | Names should describe responsibility, not implementation history. |
| Documentation | concise docstrings for public or non-obvious behavior | Use comments only for intent or constraints. |
| Tests | targeted unit coverage plus boundary integration coverage | Match the validation scope to the change. |

## Operationalization
- `Modes`: `documentation`; `artifact`; `workflow`
- `Operational Surfaces`: `core/python/src/watchtower_core/`; `core/python/tests/`; `core/python/AGENTS.md`; `core/python/README.md`; `docs/standards/engineering/python_workspace_standard.md`; `docs/standards/engineering/engineering_best_practices_standard.md`

## Validation
- `core/python/pyproject.toml` should continue to reflect the style and typing posture this standard assumes, including `ruff`, `mypy`, and `pytest` configuration.
- `core/python/pyproject.toml` should keep reusable-core packages such as `adapters`, `validation`, `control_plane`, `query`, `sync`, `rebuild`, `routing`, `workflow_execution`, `evidence`, and `utils` under a stricter `mypy` override than transitional repo-local orchestration until `repo_ops/` and CLI surfaces are brought up to the same bar.
- `core/python/pyproject.toml` should keep `ruff` configured to catch unnecessary comprehension churn in addition to import, upgrade, bugbear, and core readability issues.
- Reviewers should reject new mixed-purpose modules, vague role-free names, or duplicate implementations that could be consolidated cleanly.
- Reviewers should reject new generic behavior placed in `repo_ops/` when a reusable-core package boundary fits.
- Reviewers should reject CLI handlers that own business logic instead of delegating to package services.
- The narrowest meaningful `uv run pytest ...`, `uv run ruff check ...`, and `uv run mypy ...` commands should be run for touched Python surfaces.

## Change Control
- Update this standard when the repository's Python boundary taxonomy, naming rules, docstring posture, or consolidation rules change materially.
- Update `core/python/AGENTS.md`, `core/python/README.md`, and the workspace or best-practices standards in the same change set when this standard changes contributor-facing expectations.
- Update affected reference docs when their repository touchpoints change from candidate guidance to active supporting authority for this Python code policy.

## References
- [python_workspace_standard.md](/docs/standards/engineering/python_workspace_standard.md)
- [engineering_best_practices_standard.md](/docs/standards/engineering/engineering_best_practices_standard.md)
- [naming_and_ids_standard.md](/docs/standards/metadata/naming_and_ids_standard.md)
- [engineering_design_principles.md](/docs/foundations/engineering_design_principles.md)
- [pep8_reference.md](/docs/references/pep8_reference.md)
- [pep257_reference.md](/docs/references/pep257_reference.md)
- [src_layout_reference.md](/docs/references/src_layout_reference.md)
- [pyproject_toml_reference.md](/docs/references/pyproject_toml_reference.md)
- [ruff_reference.md](/docs/references/ruff_reference.md)
- [mypy_reference.md](/docs/references/mypy_reference.md)
- [pytest_reference.md](/docs/references/pytest_reference.md)

## Notes
- This standard intentionally favors boring, explicit code over framework-heavy or pattern-heavy abstractions.
- The goal is maintainable consolidation, not abstraction for its own sake.
- When a helper is extracted from `repo_ops/`, that is usually a sign that this standard is working as intended.

## Updated At
- `2026-03-18T06:44:55Z`
