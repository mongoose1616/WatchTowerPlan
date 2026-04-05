---
id: "foundation.repository_scope"
title: "Repository Scope"
summary: "Defines the WatchTowerCore repository charter, the canonical shared-core boundary, and the relationship between reusable core and downstream hosted-pack repositories."
type: "foundation"
status: "active"
tags:
  - "foundation"
  - "scope"
  - "repository_charter"
owner: "repository_maintainer"
updated_at: "2026-04-05T03:05:00Z"
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
  - "downstream_core_copies"
  - "downstream_pack_repositories"
  - "customer_bootstrap_artifacts"
aliases:
  - "repository scope"
  - "repository charter"
  - "current repo boundary"
---

# Repository Scope

This document defines what `WatchTowerCore` owns today. Use it as the authoritative answer when the question is "what belongs in the canonical shared core, in a downstream hosted-pack repository, or in a portable bootstrap or export artifact?" Future product direction still matters, but it should be read through the boundary defined here.

## Audience

- Primary audience: Maintainers, contributors, and agents deciding whether work belongs in canonical shared core, in a downstream hosted-pack repository, or in a portable bootstrap artifact.
- Secondary audience: Product and design stakeholders who need the current repository boundary before reading future WatchTower direction and narrative.
- Not written for: End customers looking for future product value framing.

## Purpose

`WatchTowerCore` is the reusable core and host-composition upstream for the WatchTower repository family. It owns the canonical shared substrate, authored machine-readable control plane, shared workflow-routing model, authored shared foundations, and the portable export or extract contracts that downstream repositories consume.

`WatchTowerCore` is also the canonical authored source for the shared `core/` tree. Downstream WatchTower repositories may consume that shared runtime by refreshing or copying `core/` alone during integration bring-up or by combining shared core with one or more hosted packs. Which packs remain present is a downstream repository decision, not a reusable-core assumption.

This document is authoritative for current repository ownership. It does not replace future product direction. It defines the boundary that future product direction must respect while work remains in this repo.

## This Repository Owns Today

- The shared governed core substrate under `core/control_plane/` and `core/python/src/watchtower_core/`.
- The host-composition layer under `core/python/src/watchtower_host/`, including shared CLI composition and hosted-pack dispatch.
- The canonical authored `core/` source that downstream WatchTower repositories may consume by refresh, engineering extract, or customer-safe export.
- The authored shared foundations under `core/docs/foundations/`.
- The shared external reference corpus under `core/docs/references/` when the reference supports reusable-core behavior, shared standards, or multiple hosted packs.
- Repository-native workflow routing, execution modules, standards, references, templates, and shared rendered surfaces.
- Machine-readable authority for schemas, startup manifests, shared registries, contracts, indexes, supporting fixtures, and retained validation or purge records.
- Export-ready reusable runtime behavior, host composition, shared tests, and portability or refresh contracts behind the shared workspace contract.
- Documentation, promotion, and enablement work required to keep the core coherent, validated, and ready for future consumption by other packs.

## This Repository Does Not Own Yet

- Downstream hosted-pack workspaces under their owning pack roots, including pack-owned machine state, workflows, docs, tracking, and pack-native runtime surfaces.
- Pack-native Python runtimes under `<pack>/python/src/watchtower_<pack>/`.
- Repo-local active-pack choice, downstream pack registry state, or downstream workspace wiring beyond the portable shared-core contract.
- Pack-local operator content and mutable working state that belong in consuming repositories rather than this upstream shared-core workspace.
- Domain-specific workflows, templates, terminology, and operator framing that should live in downstream hosted packs instead of shared core.
- A claim that this repository is already the full operator-facing product rather than the governed reusable substrate behind it.

## Relationship to Future WatchTower Product Work

- [product_direction.md](product_direction.md) defines the intended future WatchTower product shape.
- [customer_story.md](customer_story.md) provides supporting future-state narrative.
- Those documents remain important because they shape planning and design decisions in this repo.
- They are not the authority for present repository ownership. This document is.

## EntryPoint Guidance

- Start here when the question is whether work belongs in canonical shared core or in a downstream hosted-pack repository.
- Start with [README.md](/README.md) when the main need is root routing.
- Start with `watchtower-core validate portability --root <path> --engineering-core --format json` when the main need is engineering shared-core extract readiness.
- Start with `watchtower-core pack export --output-root <path> --overwrite --format json` when the main need is the customer-safe core bootstrap handoff path.
- Start with [README.md](README.md) when the main need is the foundations corpus and the intended read order across these guiding documents.
- Start with [watchtower_core_query_foundations.md](/core/docs/commands/core_python/watchtower_core_query_foundations.md) when the main need is machine-readable lookup of the governing foundation document for one repo surface, citation path, or applied-reference path.

## Boundaries That Must Hold

- Root entrypoints remain routers, not large repository handbooks.
- Shared core stays reusable and donor-neutral instead of becoming the default home for pack-local procedure, terminology, or operator framing.
- Shared core may host cross-pack external references when they support shared functions, shared standards, or multiple hosted packs.
- Pack-owned docs, workflows, standards, references, and machine state belong in downstream repositories. Packs may intentionally duplicate a topic already present in `core/docs/references/**` when the pack-local purpose or touchpoints differ materially.
- Host composition stays in `watchtower_host`, and pack-native orchestration stays in `watchtower_<pack>` packages.
- Shared core policy and docs must not assume that consuming repositories retain the current hosted-pack set or any other donor-specific pack topology.
- Portable customer/bootstrap handoff is an allowlisted source transfer, not a raw repository snapshot. Retained records, test fixtures, and donor-local pack history stay repo-local unless a release contract explicitly selects them.
- Downstream live pack execution state stays under the owning pack roots, not under shared documentation roots or this upstream repository.
- Shared foundations are authored in `core/docs/foundations/`. Any downstream synchronized copy or pack-owned copied or adapted view must remain aligned when the owning repository contract requires it.
- Shared `core/**` edits must land in `WatchTowerCore/core/**` first and then flow downstream through the shared-core refresh path.
- Future product narrative can guide planning, but it must not quietly redefine current repo scope.
- Repo-specific behavior stays explicit instead of leaking into reusable surfaces.

## References
- [engineering_design_principles.md](engineering_design_principles.md)
- [product_direction.md](product_direction.md)

## Updated At
- `2026-04-05T03:05:00Z`
