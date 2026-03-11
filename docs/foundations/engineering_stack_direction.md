---
id: "foundation.engineering_stack_direction"
title: "Engineering Stack Direction"
summary: "Defines the current technology-direction baseline and selection rules for the repository."
type: "foundation"
status: "active"
tags:
  - "foundation"
  - "technology_stack"
owner: "repository_maintainer"
updated_at: "2026-03-11T01:34:31Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/control_plane/"
  - "core/python/"
  - "docs/standards/"
aliases:
  - "technology stack"
  - "stack direction"
  - "engineering stack direction"
---

# Engineering Stack Direction

This repository is still closer to governed-core and planning infrastructure than to a finished product implementation, so the stack should be read as a current working baseline plus a small set of future candidates. The selection rule is straightforward: prefer local-first, inspectable, deterministic tools that improve LLM and agent effectiveness, support strong validation, and preserve clear source-of-truth boundaries.

## Audience

- Primary audience: Engineers making implementation, tooling, validation, and storage decisions in the repository.
- Secondary audience: Product and design stakeholders who need to understand the practical constraints behind implementation choices.
- Not written for: End customers or buyers who need product value framing rather than internal stack direction.

## Current Shape

Today the repository is still documentation-heavy, but it also has a substantive Python runtime and control-plane maintenance layer. The docs, workflows, control plane, and Python workspace all matter; none of them should be described as incidental scaffolding anymore.

| Technology | Current Use | Main Surfaces | Human-Relevant Notes |
|---|---|---|---|
| Markdown | Primary human-facing authoring format | `docs/**`, `workflows/**`, `README.md`, `AGENTS.md` | This remains the dominant human-readable surface. |
| JSON | Primary machine-readable artifact format | `core/control_plane/registries/**`, `core/control_plane/indexes/**`, `core/control_plane/examples/**` | Used for canonical control-plane artifacts and examples because it is explicit, diff-friendly, and easy to validate. |
| JSON Schema Draft 2020-12 | Contract and validation baseline | `core/control_plane/schemas/**` | Defines governed artifact shapes and validation boundaries. |
| YAML front matter | Document metadata layer where governed metadata is useful | Governed docs under `docs/**` | Used as a small metadata wrapper for routing, indexing, ownership, and lifecycle signals. |
| Python 3.12 | Active runtime, validation, sync, query, and CLI baseline | `core/python/.python-version`, `core/python/src/**`, `core/python/tests/**` | The Python layer is now a real part of the repo's operating model, not just early scaffolding. |
| Hatchling | Python build backend | `core/python/pyproject.toml` | Keeps packaging minimal and standard. |
| pytest | Test runner baseline for Python code | `core/python/pyproject.toml`, `core/python/tests/**` | Standard test surface for the consolidated Python workspace. |

- Durable documentation lives under `docs/`.
- Routed task behavior lives under `workflows/`.
- Shared implementation assets live under `core/`.

## Preferred Building Blocks

- Use Markdown for human-facing guidance, standards, templates, and workflow documents.
- Use JSON Schema as the baseline for machine-validated contracts such as manifests, registries, indexes, and compatibility boundaries.
- Use YAML sparingly for front matter and simple human-authored metadata when it improves readability.
- Favor Python for local automation, validators, helper runtime code, and harnesses that improve LLM and agent efficiency when a general-purpose language is needed.
- Keep Python tooling centralized and predictable under `core/python/` with `pyproject.toml`, `uv`, `pytest`, `ruff`, and `mypy`.
- Treat `uv` as the preferred workspace manager and execution path, but keep direct `.venv` execution and helper shells available as practical fallbacks when `uv` is not on `PATH`.
- Consider Pydantic strict mode for typed runtime validation where schema checks alone are not enough.

## Future Candidate Tools

- Use SQLite only when local durable state, indexing, or retrieval needs a lightweight embedded store.
- Use OPA or Rego only when policy logic benefits from being explicit, testable, and separate from application code.
- Treat richer observability or provenance tooling as opt-in later additions, not default baseline requirements.

## Operational Support

- Keep validation local and deterministic wherever possible.
- Prefer support mechanisms that strengthen retrieval, orchestration, validation, and context control for LLM or agent workflows.
- Add structured logging and trace semantics only when they materially improve operator or runtime visibility.
- Treat SBOM, attestation, signing, and provenance formats such as CycloneDX, in-toto, Sigstore, and SLSA as release-evidence tools, not default complexity.
- Choose formats and tools that keep generated artifacts reviewable and storage rules explicit.

## Selection Rules

- Prefer the simplest tool that preserves determinism, portability, and governance.
- Avoid hosted or opaque dependencies when a local repo-native option is good enough.
- Keep human-readable surfaces easy to review and machine-facing surfaces easy to validate and consume by agents.
- Treat Python and other code as enabling infrastructure for LLM and agent workflows, not as the primary value by themselves.
- Do not add domain-specific assumptions to shared core choices unless they are truly cross-domain.
- Reject tools that blur authority boundaries or make failure modes harder to inspect.

## References
- [repository_scope.md](/home/j/WatchTowerPlan/docs/foundations/repository_scope.md)
- [engineering_design_principles.md](/home/j/WatchTowerPlan/docs/foundations/engineering_design_principles.md)
- [product_direction.md](/home/j/WatchTowerPlan/docs/foundations/product_direction.md)
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)

## Updated At
- `2026-03-11T01:34:31Z`
