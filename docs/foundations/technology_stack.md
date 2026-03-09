---
id: "foundation.technology_stack"
title: "Technology Stack"
summary: "Defines the current technology-direction baseline and selection rules for the repository."
type: "foundation"
status: "active"
tags:
  - "foundation"
  - "technology_stack"
owner: "repository_maintainer"
updated_at: "2026-03-09T23:02:08Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/control_plane/"
  - "core/python/"
  - "docs/standards/"
aliases:
  - "stack direction"
---

# Technology Stack

This repository is still defining the product more than implementing it, so the stack should be read as a working direction rather than a frozen inventory. The selection rule is straightforward: prefer local-first, inspectable, deterministic tools that improve LLM/agent effectiveness, support strong validation, and preserve clear source-of-truth boundaries.

## Current Shape

Today the repository is documentation-first. Most of the surface area is Markdown guidance, workflow modules, templates, and standards. That is intentional: the operating model, contracts, and governance rules should be clear before the implementation footprint grows. The repository should bias toward artifacts that are readable by a human reviewer and directly usable by an LLM or agent.

| Technology | Current Use | Main Surfaces | Human-Relevant Notes |
|---|---|---|---|
| Markdown | Primary human-facing authoring format | `docs/**`, `workflows/**`, `README.md`, `AGENTS.md` | This is the dominant repository surface today. Most governance, routing, and product intent lives here. |
| JSON | Primary machine-readable artifact format | `core/control_plane/registries/**`, `core/control_plane/indexes/**`, `core/control_plane/examples/**` | Used for canonical control-plane artifacts and examples because it is explicit, diff-friendly, and easy to validate. |
| JSON Schema Draft 2020-12 | Contract and validation baseline | `core/control_plane/schemas/**` | The repo already uses published schemas to define governed artifact shapes and validation boundaries. |
| YAML front matter | Document metadata layer where governed metadata is useful | Mostly `docs/references/**` and any governed docs that adopt front matter | Used as a small metadata wrapper for routing, indexing, ownership, and lifecycle signals rather than as a primary document format. |
| Python 3.12 | Early helper-runtime and validator baseline | `core/python/.python-version`, `core/python/src/**`, `core/python/tests/**` | Present as a scaffolded implementation layer. The runtime direction is clear, but most repository value is still in docs and control-plane artifacts. |
| Hatchling | Python build backend | `core/python/pyproject.toml` | Keeps packaging minimal and standard. Relevant mainly when the Python helper layer grows beyond the current scaffold. |
| pytest | Test runner baseline for Python code | `core/python/pyproject.toml`, `core/python/tests/**` | Configured as the standard test surface for the consolidated Python workspace. |

- Durable documentation lives under `docs/`.
- Routed task behavior lives under `workflows/`.
- Shared implementation assets are expected to live under `core/` as they appear.

## Preferred Building Blocks

When implementation expands, the stack should stay small and boring. The repository already points toward a practical set of tools and formats that fit the governance model. The priority is not code for its own sake; the priority is enabling the LLM or agent to work faster, more safely, and with better context.

- Use Markdown for human-facing guidance, standards, templates, and workflow documents.
- Use JSON Schema as the baseline for machine-validated contracts such as manifests, registries, indexes, and compatibility boundaries.
- Use YAML sparingly for front matter and simple human-authored metadata when it improves readability.
- Favor Python for local automation, validators, helper runtime code, and harnesses that improve LLM/agent efficiency when a general-purpose language is needed.
- Keep Python tooling centralized and predictable under `core/python/` with `pyproject.toml`, `uv`, `pytest`, `ruff`, and `mypy`.
- Consider Pydantic strict mode for typed runtime validation where schema checks alone are not enough.
- Use SQLite only when local durable state, indexing, or retrieval needs a lightweight embedded store.
- Use OPA/Rego only when policy logic benefits from being explicit, testable, and separate from application code.

## Operational Support

The stack should also support evidence, validation, and future observability without turning the repo into an overbuilt platform.

- Keep validation local and deterministic wherever possible.
- Prefer support mechanisms that strengthen retrieval, orchestration, validation, and context control for LLM or agent workflows.
- Add structured logging and trace semantics only when they materially improve operator or runtime visibility.
- Treat SBOM, attestation, signing, and provenance formats such as CycloneDX, in-toto, Sigstore, and SLSA as release-evidence tools, not default complexity.
- Choose formats and tools that keep generated artifacts reviewable and storage rules explicit.

## Selection Rules

Any new technology should earn its way in. The stack is there to support the product model, not to create a second product made of tooling decisions.

- Prefer the simplest tool that preserves determinism, portability, and governance.
- Avoid hosted or opaque dependencies when a local repo-native option is good enough.
- Keep human-readable surfaces easy to review and machine-facing surfaces easy to validate and consume by agents.
- Treat Python and other code as enabling infrastructure for LLM/agent workflows, not as the primary value by themselves.
- Do not add domain-specific assumptions to shared core choices unless they are truly cross-domain.
- Reject tools that blur authority boundaries or make failure modes harder to inspect.

## References
- [design_philosophy.md](/home/j/WatchTowerPlan/docs/foundations/design_philosophy.md)
- [product.md](/home/j/WatchTowerPlan/docs/foundations/product.md)
- [format_selection_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/format_selection_standard.md)

## Updated At
- `2026-03-09T23:02:08Z`
