---
id: "foundation.repository_scope"
title: "Repository Scope"
summary: "Defines the current repository charter, ownership boundary, and the relationship between WatchTowerPlan and future WatchTower product implementation."
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

This document defines what `WatchTowerPlan` owns today. Use it as the authoritative answer when the question is "what belongs in this repository right now?" Future product direction still matters, but it should be read through the boundary defined here.

## Audience

- Primary audience: Maintainers, contributors, and agents deciding whether work belongs in `WatchTowerPlan` or in a future consuming product repository.
- Secondary audience: Product and design stakeholders who need the current repository boundary before reading future WatchTower direction and narrative.
- Not written for: End customers looking for future product value framing.

## Purpose

`WatchTowerPlan` is the reusable core, host-composition home, and first internal plan-domain pack for WatchTower. It owns the reusable substrate, machine-readable control plane, split workflow-routing model, authored shared foundations, mirrored plan foundations, and the live plan system that prepare the project for later product implementation.

`WatchTowerPlan` is also the canonical authored source for the shared `core/` tree. One supported operating mode for the broader WatchTower series is for a downstream repository to consume that shared runtime by copying `core/` alone during integration bring-up or by copying `core/` together with one or more hosted packs. Which packs are present remains a repo-local decision for the consuming repository, not a reusable-core assumption.

This document is authoritative for current repository ownership. It does not replace future product direction. It defines the boundary that future product direction must respect while work remains in this repo.

## This Repository Owns Today

- The shared governed core substrate under `core/control_plane/` and `core/python/src/watchtower_core/`.
- The host-composition layer under `core/python/src/watchtower_host/`, including shared CLI composition and hosted-pack dispatch.
- The canonical authored `core/` source that downstream WatchTower repositories may consume by copying shared core alone or together with selected hosted packs.
- The live plan-domain workspace under `plan/`, including `plan/.wt/`, pack-wide initiatives, project-scoped initiatives, and plan-domain workflow surfaces.
- The first internal hosted-pack runtime under `plan/python/src/watchtower_plan/`, installed through the shared workspace contract.
- The authored shared foundations under `core/docs/foundations/` and the required plan-owned copied/adapted view under `plan/docs/foundations/`.
- The shared external reference corpus under `core/docs/references/` when the reference supports reusable-core behavior, shared standards, or multiple hosted packs.
- Repository-native workflow routing, execution modules, standards, references, templates, and plan-facing rendered surfaces.
- Machine-readable authority for schemas, startup manifests, registries, contracts, indexes, supporting fixtures, and retained validation or purge records.
- Export-ready reusable runtime behavior, host composition, and the first internal pack runtime behind the shared workspace contract.
- Documentation, promotion, and planning work required to keep the core coherent, validated, and ready for future consumption by other packs.

## This Repository Does Not Own Yet

- A separate operator-facing `WatchTower` product implementation repository.
- External operator-facing hosted-pack runtimes or mounted execution environments beyond the current internal pack and current portability proofs.
- Pack-local operator content and mutable working state that belong in a future consuming repository rather than this core-plus-host-plus-pack workspace.
- Domain-specific workflows, templates, or terminology that should live in another pack instead of the current internal plan-domain pack.
- A claim that the current repository is already the full product rather than the governed substrate and first internal pack behind it.

## Relationship to Future WatchTower Product Work

- [product_direction.md](product_direction.md) defines the intended future WatchTower product shape.
- [customer_story.md](customer_story.md) provides supporting future-state narrative.
- Those documents remain important because they shape planning and design decisions in this repo.
- They are not the authority for present repository ownership. This document is.

## EntryPoint Guidance

- Start here when the question is whether work belongs in `WatchTowerPlan`.
- Start with [README.md](/README.md) when the main need is root routing.
- Start with [plan_overview.md](/plan/plan_overview.md) when the main need is current live work state, overall repository coherence, or the next active plan-domain action.
- Start with [README.md](README.md) when the main need is the foundations corpus and the intended read order across these guiding documents.
- Start with [watchtower_core_query_foundations.md](/core/docs/commands/core_python/watchtower_core_query_foundations.md) when the main need is machine-readable lookup of the governing foundation document for one repo surface, citation path, or applied-reference path.

## Boundaries That Must Hold

- Root entrypoints remain routers, not large repository handbooks.
- Shared core stays reusable and donor-neutral instead of becoming the default home for pack-local procedure, terminology, or operator framing.
- Shared core may host cross-pack external references when they support shared functions, shared standards, or multiple hosted packs.
- Pack-owned docs, workflows, standards, and references own pack-applied operator framing, pack-local touchpoints, and domain-native mappings. Packs may intentionally duplicate a topic already present in `core/docs/references/**` when the pack-local purpose or touchpoints differ materially.
- Host composition stays in `watchtower_host`, and pack-native orchestration stays in `watchtower_<pack>` packages.
- Shared core policy and docs must not assume that consuming repositories retain the current internal `plan/` pack or any other donor-specific pack set.
- Portable customer/bootstrap handoff is an allowlisted source transfer, not a raw repository snapshot. Retained records, test fixtures, and donor-local plan history stay repo-local unless a release contract explicitly selects them.
- Live plan execution state stays under `plan/**`, not under documentation roots.
- Shared foundations are authored in `core/docs/foundations/` and copied into `plan/docs/foundations/`, where plan-local wording may be adapted as needed.
- `WatchTowerPlan/core/` remains the canonical authored shared-core source. When a downstream working repository edits `core/**`, the same change must be reconciled back into `WatchTowerPlan/core/**` in the same workstream, and any foundations change must also refresh `WatchTowerPlan/plan/docs/foundations/**` plus the plan-specific wording there before the work is considered complete.
- Future product narrative can guide planning, but it must not quietly redefine current repo scope.
- Repo-specific behavior stays explicit instead of leaking into reusable surfaces.

## References
- [engineering_design_principles.md](engineering_design_principles.md)
- [product_direction.md](product_direction.md)

## Updated At
- `2026-03-29T00:45:00Z`
