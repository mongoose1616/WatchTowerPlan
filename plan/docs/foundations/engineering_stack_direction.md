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
updated_at: "2026-03-22T17:45:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "core/control_plane/"
  - "core/python/"
  - "core/python/src/watchtower_host/"
  - "core/python/src/watchtower_core/pack_integration/"
  - "plan/python/src/watchtower_plan/"
  - "core/control_plane/registries/pack_registry.json"
  - "plan/.wt/manifests/pack_runtime_manifest.json"
  - "core/docs/standards/"
  - "plan/docs/standards/"
aliases:
  - "technology stack"
  - "stack direction"
  - "engineering stack direction"
---

# Engineering Stack Direction

This repository is a governed docs-plus-runtime system that currently owns reusable core, host composition, and the first internal pack. The stack should be read as the current operating baseline for that architecture plus a small set of future candidates. The selection rule is straightforward: prefer local-first, inspectable, deterministic tools that improve LLM and agent effectiveness, support strong validation, and preserve clear source-of-truth boundaries.

## Audience

- Primary audience: Engineers making implementation, tooling, validation, and storage decisions in the repository.
- Secondary audience: Product and design stakeholders who need to understand the practical constraints behind implementation choices.
- Not written for: End customers or buyers who need product value framing rather than internal stack direction.

## Current Shape

Today the repository has a substantial governed documentation corpus, reusable Python runtime, host-composition layer, hosted-pack integration contract, and plan-pack orchestration layer. The docs, workflows, control plane, and Python workspace all matter; none of them should be described as incidental scaffolding anymore.

| Technology | Current Use | Main Surfaces | Human-Relevant Notes |
|---|---|---|---|
| Markdown | Primary human-facing authoring format | `core/docs/**`, `plan/docs/**`, `core/workflows/**`, `plan/workflows/**`, `README.md`, `AGENTS.md` | This remains the dominant human-readable surface. |
| JSON | Primary machine-readable artifact format | `core/control_plane/manifests/**`, `core/control_plane/registries/**`, `core/control_plane/contracts/**`, `core/control_plane/indexes/**`, `core/control_plane/records/**` | Used for canonical control-plane inputs and retained machine-readable records because it is explicit, diff-friendly, and easy to validate. |
| JSON Lines | Local runtime telemetry event format | `<pack>/.wt/runtime/telemetry/**` | Used for append-friendly local command telemetry because it stays inspectable and backend-neutral. |
| JSON Schema Draft 2020-12 | Contract and validation baseline | `core/control_plane/schemas/**` | Defines governed artifact shapes and validation boundaries. |
| YAML front matter | Document metadata layer where governed metadata is useful | Governed docs under `core/docs/**`, `plan/docs/**`, `core/workflows/**`, and `plan/workflows/**` | Used as a small metadata wrapper for routing, indexing, ownership, and lifecycle signals. |
| Python 3.12 | Active runtime, validation, sync, query, and CLI baseline | `core/python/pyproject.toml` and `core/python/uv.lock`, `core/python/src/**`, `core/python/tests/**` | The Python layer is now a real part of the repo's operating model, not just early scaffolding. |
| Hatchling | Python build backend | `core/python/pyproject.toml` | Keeps packaging minimal and standard. |
| pytest | Test runner baseline for Python code | `core/python/pyproject.toml`, `core/python/tests/**` | Standard test surface for the consolidated Python workspace. |

- Durable documentation lives under `core/docs/` and `plan/docs/` according to ownership.
- Routed task behavior lives under `core/workflows/` and `plan/workflows/`.
- Shared implementation assets live under `core/`.
- `watchtower_core`, `watchtower_host`, and `watchtower_<pack>` are the active Python runtime layers in the current architecture.
- `core/control_plane/registries/pack_registry.json`, `plan/.wt/manifests/pack_runtime_manifest.json`, and pack-contract validation are part of the effective operating stack because they define and validate hosted-pack composition.

## Preferred Building Blocks

- Use Markdown for human-facing guidance, standards, templates, and workflow documents.
- Use JSON Schema as the baseline for machine-validated contracts such as manifests, registries, indexes, and compatibility boundaries.
- Use YAML sparingly for front matter and simple human-authored metadata when it improves readability.
- Favor Python for local automation, validators, helper runtime code, and harnesses that improve LLM and agent efficiency when a general-purpose language is needed.
- Treat governed manifests, registries, and pack contracts as the integration contract between host composition and pack-native runtime.
- Keep Python tooling centralized and predictable under `core/python/` with `pyproject.toml`, `uv`, `pytest`, `ruff`, and `mypy`.
- Treat `uv` as the preferred workspace manager and execution path, but keep direct `.venv` execution and helper shells available as practical fallbacks when `uv` is not on `PATH`.
- Use pack-local JSONL runtime telemetry for command timing and error tracing where operator visibility materially improves execution, fault isolation, or performance work.
- Consider Pydantic strict mode for typed runtime validation where schema checks alone are not enough.

## Future Candidate Tools

- Use SQLite only when local durable state, indexing, or retrieval needs a lightweight embedded store.
- Use OPA or Rego only when externally authored rule evaluation materially improves clarity over repository standards plus Python validators.
- Treat OTEL exporters, remote collectors, and cross-process propagation as later additions rather than default baseline requirements.

## Operational Support

- Keep validation local and deterministic wherever possible.
- Prefer support mechanisms that strengthen retrieval, orchestration, validation, and context control for LLM or agent workflows.
- Keep local runtime telemetry active where it materially improves operator or runtime visibility, but make richer observability transports opt-in.
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
- [repository_scope.md](repository_scope.md)
- [engineering_design_principles.md](engineering_design_principles.md)
- [product_direction.md](product_direction.md)
- [format_selection_standard.md](/core/docs/standards/data_contracts/format_selection_standard.md)
- [domain_pack_authoring_reference.md](/core/docs/references/domain_pack_authoring_reference.md)
- [json_schema_2020_12_reference.md](/core/docs/references/json_schema_2020_12_reference.md)
- [uv_reference.md](/core/docs/references/uv_reference.md)
- [pytest_reference.md](/core/docs/references/pytest_reference.md)
- [ruff_reference.md](/core/docs/references/ruff_reference.md)
- [mypy_reference.md](/core/docs/references/mypy_reference.md)
- [ndjson_spec_reference.md](/core/docs/references/ndjson_spec_reference.md)
- [python_logging_reference.md](/core/docs/references/python_logging_reference.md)
- [pydantic_strict_mode_reference.md](/core/docs/references/pydantic_strict_mode_reference.md)
- [opa_rego_reference.md](/core/docs/references/opa_rego_reference.md)
- [opentelemetry_reference.md](/core/docs/references/opentelemetry_reference.md)
- [w3c_trace_context_reference.md](/core/docs/references/w3c_trace_context_reference.md)
- [cyclonedx_1_7_reference.md](/core/docs/references/cyclonedx_1_7_reference.md)
- [sigstore_reference.md](/core/docs/references/sigstore_reference.md)
- [slsa_1_1_reference.md](/core/docs/references/slsa_1_1_reference.md)
- [in_toto_reference.md](/core/docs/references/in_toto_reference.md)

## Updated At
- `2026-03-22T17:45:00Z`
