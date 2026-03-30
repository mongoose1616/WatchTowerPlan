---
id: "foundation.repository_scope"
title: "Repository Scope"
summary: "Defines the shared-core repository charter, ownership boundary, and the relationship between reusable core and hosted-pack workspaces."
type: "foundation"
status: "active"
tags:
  - "foundation"
  - "scope"
  - "repository_charter"
owner: "repository_maintainer"
updated_at: "2026-03-29T00:45:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "README.md"
  - "AGENTS.md"
  - "core/docs/foundations/"
  - "core/workflows/"
  - "core/"
  - "core/python/src/watchtower_core/"
  - "core/python/src/watchtower_host/"
  - "foundations_mirror"
  - "pack_owned_workflows"
  - "live_pack_workspace"
  - "first_internal_pack_python"
aliases:
  - "repository scope"
  - "repository charter"
  - "current repo boundary"
---

# Repository Scope

This document defines what the current core-authoring repository owns today. Use it as the authoritative answer when the question is "what belongs in shared core, in the active hosted pack, or in a downstream consuming repository?" Future product direction still matters, but it should be read through the boundary defined here.

## Audience

- Primary audience: Maintainers, contributors, and agents deciding whether work belongs in shared core, in the active hosted pack, or in a downstream consuming product repository.
- Secondary audience: Product and design stakeholders who need the current repository boundary before reading future WatchTower direction and narrative.
- Not written for: End customers looking for future product value framing.

## Purpose

The current core-authoring repository is the reusable core and host-composition home for WatchTower. It owns the reusable substrate, machine-readable control plane, split workflow-routing model, authored shared foundations, and the currently hosted pack workspaces that prepare the project for later product implementation.

The current core-authoring repository is also the canonical authored source for the shared `core/` tree. One supported operating mode for the broader WatchTower series is for a downstream repository to consume that shared runtime by copying `core/` alone during integration bring-up or by copying `core/` together with one or more hosted packs. Which packs are present remains a repo-local decision for the consuming repository, not a reusable-core assumption.

This document is authoritative for current repository ownership. It does not replace future product direction. It defines the boundary that future product direction must respect while work remains in this repo.

## This Repository Owns Today

- The shared governed core substrate under `core/control_plane/` and `core/python/src/watchtower_core/`.
- The host-composition layer under `core/python/src/watchtower_host/`, including shared CLI composition and hosted-pack dispatch.
- The canonical authored `core/` source that downstream WatchTower repositories may consume by copying shared core alone or together with selected hosted packs.
- The currently hosted pack workspaces under their owning pack roots, including pack-owned machine state, workflows, docs, tracking, and pack-native runtime surfaces.
- The pack-native Python runtimes installed through the shared workspace contract under `<pack>/python/src/watchtower_<pack>/`.
- The authored shared foundations under `core/docs/foundations/` plus any pack-owned copied/adapted foundations view or promoted guidance surfaces required by the active pack contract.
- The shared external reference corpus under `core/docs/references/` when the reference supports reusable-core behavior, shared standards, or multiple hosted packs.
- Repository-native workflow routing, execution modules, standards, references, templates, and shared rendered surfaces.
- Machine-readable authority for schemas, startup manifests, shared registries, contracts, indexes, supporting fixtures, and retained validation or purge records.
- Export-ready reusable runtime behavior, host composition, and the currently hosted pack runtimes behind the shared workspace contract.
- Documentation, promotion, and enablement work required to keep the core coherent, validated, and ready for future consumption by other packs.

## This Repository Does Not Own Yet

- A separate operator-facing `WatchTower` product implementation repository.
- External operator-facing hosted-pack runtimes or mounted execution environments beyond the currently hosted pack set and current portability proofs.
- Pack-local operator content and mutable working state that belong in a future consuming repository rather than this shared-core-plus-current-pack workspace.
- Domain-specific workflows, templates, or terminology that should live in another hosted pack instead of the current pack set.
- A claim that the current repository is already the full product rather than the governed substrate and current hosted-pack set behind it.

## Relationship to Future WatchTower Product Work

- [product_direction.md](product_direction.md) defines the intended future WatchTower product shape.
- [customer_story.md](customer_story.md) provides supporting future-state narrative.
- Those documents remain important because they shape planning and design decisions in this repo.
- They are not the authority for present repository ownership. This document is.

## EntryPoint Guidance

- Start here when the question is whether work belongs in shared core or in an owning pack.
- Start with [README.md](/README.md) when the main need is root routing.
- Start with `watchtower-core pack describe --format json` when the main need is the active pack identity, runtime manifest, or pack-owned roots.
- Start with [README.md](README.md) when the main need is the foundations corpus and the intended read order across these guiding documents.
- Start with [watchtower_core_query_foundations.md](/core/docs/commands/core_python/watchtower_core_query_foundations.md) when the main need is machine-readable lookup of the governing foundation document for one repo surface, citation path, or applied-reference path.

## Boundaries That Must Hold

- Root entrypoints remain routers, not large repository handbooks.
- Shared core stays reusable and donor-neutral instead of becoming the default home for pack-local procedure, terminology, or operator framing.
- Shared core may host cross-pack external references when they support shared functions, shared standards, or multiple hosted packs.
- Pack-owned docs, workflows, standards, and references own pack-applied operator framing, pack-local touchpoints, and domain-native mappings. Packs may intentionally duplicate a topic already present in `core/docs/references/**` when the pack-local purpose or touchpoints differ materially.
- Host composition stays in `watchtower_host`, and pack-native orchestration stays in `watchtower_<pack>` packages.
- Shared core policy and docs must not assume that consuming repositories retain the current hosted-pack set or any other donor-specific pack topology.
- Portable customer/bootstrap handoff is an allowlisted source transfer, not a raw repository snapshot. Retained records, test fixtures, and donor-local pack history stay repo-local unless a release contract explicitly selects them.
- Live pack execution state stays under the owning pack roots, not under shared documentation roots.
- Shared foundations are authored in `core/docs/foundations/`. Any pack-owned copied/adapted view or promoted projection must remain aligned when the owning pack contract requires it.
- The canonical authored shared-core source remains responsible for reconciling downstream `core/**` edits back into that source in the same workstream.
- Future product narrative can guide planning, but it must not quietly redefine current repo scope.
- Repo-specific behavior stays explicit instead of leaking into reusable surfaces.

## References
- [engineering_design_principles.md](engineering_design_principles.md)
- [product_direction.md](product_direction.md)

## Updated At
- `2026-03-29T00:45:00Z`
