---
id: "std.engineering.deterministic_sync_cache"
title: "Deterministic Sync Cache Standard"
summary: "This standard defines when deterministic sync and index rebuild surfaces may persist incremental cache metadata and where that runtime state must live."
type: "standard"
status: "active"
tags:
  - "standard"
  - "engineering"
  - "sync_cache"
  - "performance"
owner: "repository_maintainer"
updated_at: "2026-04-04T22:45:00Z"
audience: "shared"
authority: "authoritative"
---

# Deterministic Sync Cache Standard

## Summary
This standard defines when deterministic sync and index rebuild surfaces may persist incremental cache metadata and where that runtime state must live.

## Purpose
Improve repeated sync performance without blurring the line between authored authority, canonical derived artifacts, and mutable runtime residue.

## Scope
- Applies to reusable-core and pack-owned deterministic sync services that build canonical documents or indexes from repo-local inputs.
- Covers cache eligibility, required input declaration, cache-root placement, export behavior, and validation expectations.
- Does not define non-deterministic caches, external dependency caches, or arbitrary application memoization.

## Use When
- Adding or refactoring a sync service under `watchtower_core.sync` or `watchtower_<pack>.sync`.
- Reviewing whether a rebuild surface may reuse canonical outputs on warm runs.
- Deciding where mutable sync cache state belongs and how exports should treat it.

## Related Standards and Sources
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md): defines the shared Python workspace and the fallback local cache boundary under `core/python/`.
- [hosted_pack_integration_standard.md](/core/docs/standards/engineering/hosted_pack_integration_standard.md): defines the pack-owned runtime roots that the preferred sync cache location must use.
- [runtime_telemetry_standard.md](/core/docs/standards/engineering/runtime_telemetry_standard.md): constrains the pack-local runtime-state posture that sync cache manifests must follow.
- [repository_portability_standard.md](/core/docs/standards/engineering/repository_portability_standard.md): requires portable staging and customer-facing bundles to exclude mutable runtime cache residue.
- [domain_pack_authoring_reference.md](/core/docs/references/domain_pack_authoring_reference.md): gives the pack-authoring checklist that should operationalize this cache contract for pack-owned sync services.
- [uv_reference.md](/core/docs/references/uv_reference.md): explains the workspace execution model used to run sync commands and timing checks.

## Guidance
- Only deterministic sync services may use the shared sync cache contract.
- A cache-aware document sync service must declare its repo-relative tracked inputs through `sync_cache_inputs()`.
- Declare tracked inputs broadly enough to cover every authored file, directory, registry, workflow surface, or code path that can change the canonical output.
- Prefer reusable helpers such as `module_relative_path(...)`, `ordered_sync_cache_paths(...)`, and `discover_pack_sync_cache_paths(...)` instead of hand-rolled path normalization.
- Treat the canonical derived artifact as the reusable cached document source. A warm-cache hit is valid only when the declared input fingerprint matches and the canonical output bytes still match the recorded output hash.
- A cached document must still validate against the current schema store before reuse. Invalid or schema-drifted cached hits must degrade to a cache miss and rebuild.
- Keep `build_document()` deterministic and side-effect free. Any write-time side effects that must still happen on cache hits belong in `write_document(...)`.
- Preferred cache root: `<active-pack>/.wt/runtime/sync_cache/` when the active or default pack exposes a pack-local machine root.
- Fallback cache root: `core/python/.cache/watchtower/sync_cache/` only when no usable pack-local machine root is active.
- Never persist sync cache manifests under `core/control_plane/` or any other authored machine-authority root.
- Treat sync cache manifests as disposable runtime residue. They may be deleted at any time and must never be treated as a source of truth.
- Pack-owned deterministic sync services should implement the same cache-input contract instead of inventing pack-specific cache formats.
- Portable export, shared-core extract, and staged bootstrap flows must not emit runtime sync cache state into staged artifacts. Those flows should disable cache persistence and scrub any fallback cache roots before validation or handoff.

## Operationalization
- `Modes`: `sync`; `validation`; `documentation`
- `Operational Surfaces`: `core/python/src/watchtower_core/sync/cache.py`; `core/python/src/watchtower_core/sync/harness.py`; `core/python/src/watchtower_core/cli/sync_runtime_helpers.py`; `core/python/src/watchtower_core/pack_integration/bootstrap.py`; `core/python/src/watchtower_core/pack_integration/export.py`; `core/python/.gitignore`; `core/python/src/watchtower_core/sync/README.md`

## Validation
- Reviewers should reject cache-aware sync services that do not declare `sync_cache_inputs()` or that under-declare materially relevant inputs.
- Reviewers should reject sync cache roots under `core/control_plane/` or other authored authority trees.
- Reviewers should reject cache-aware rebuild paths that reuse cached documents without current schema validation.
- Reviewers should reject cache-aware services whose `build_document()` depends on write-time side effects or mutable runtime state that is not part of the declared inputs.
- Reviewers should reject export or portability flows that leave `runtime/sync_cache/` or `core/python/.cache/watchtower/sync_cache/` residue in staged deliverables.
- Repeated sync timing checks should demonstrate a warm-run speedup on unchanged inputs before a substantially more expensive cache design is kept.

## Change Control
- Update this standard when the shared cache root policy, cache-hit validity rules, or cache-input declaration contract changes materially.
- Update shared sync docs, pack-authoring guidance, Python workspace guidance, ignore rules, and affected sync command docs in the same change set when this contract changes materially.

## References
- [domain_pack_authoring_reference.md](/core/docs/references/domain_pack_authoring_reference.md)
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md)
- [hosted_pack_integration_standard.md](/core/docs/standards/engineering/hosted_pack_integration_standard.md)
- [repository_portability_standard.md](/core/docs/standards/engineering/repository_portability_standard.md)
- [runtime_telemetry_standard.md](/core/docs/standards/engineering/runtime_telemetry_standard.md)

## Updated At
- `2026-04-04T22:45:00Z`
