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
updated_at: "2026-03-19T05:30:00Z"
audience: "shared"
authority: "authoritative"
applies_to:
  - "README.md"
  - "AGENTS.md"
  - "core/docs/foundations/"
  - "plan/docs/foundations/"
  - "core/workflows/"
  - "plan/workflows/"
  - "plan/"
  - "core/"
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

`WatchTowerPlan` is the reusable core and first internal plan-domain workspace for WatchTower. It owns the reusable substrate, machine-readable control plane, split workflow-routing model, authored shared foundations, mirrored plan foundations, and the live plan system that prepare the project for later product implementation.

This document is authoritative for current repository ownership. It does not replace future product direction. It defines the boundary that future product direction must respect while work remains in this repo.

## This Repository Owns Today

- The shared governed core substrate under `core/control_plane/` and `core/python/`.
- The live plan-domain workspace under `plan/`, including `plan/.wt/`, pack-wide initiatives, project-scoped initiatives, and plan-domain workflow surfaces.
- The authored shared foundations under `core/docs/foundations/` and the required mirrored copy under `plan/docs/foundations/`.
- Repository-native workflow routing, execution modules, standards, references, templates, and plan-facing rendered surfaces.
- Machine-readable authority for schemas, startup manifests, registries, contracts, indexes, supporting fixtures, and retained validation or purge records.
- Export-ready reusable runtime behavior plus any still-residual repo-local plan-runtime behavior until the remaining cleanup slices remove it.
- Documentation, promotion, and planning work required to keep the core coherent, validated, and ready for future consumption by other packs.

## This Repository Does Not Own Yet

- A separate operator-facing `WatchTower` product implementation repository.
- External domain-pack runtimes or mounted execution environments beyond the current internal planning-and-implementation pack.
- Pack-local operator content and mutable working state that belong in a future consuming repository rather than this core-and-pack workspace.
- Domain-specific workflows, templates, or terminology that should live in another pack instead of the current planning-and-implementation pack.
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
- Start with [watchtower_core_query_foundations.md](/docs/commands/core_python/watchtower_core_query_foundations.md) when the main need is machine-readable lookup of the governing foundation document for one repo surface, citation path, or applied-reference path.

## Boundaries That Must Hold

- Root entrypoints remain routers, not large repository handbooks.
- Shared core surfaces stay domain-agnostic.
- Live plan execution state stays under `plan/**`, not under documentation roots.
- Shared foundations are authored in `core/docs/foundations/` and mirrored into `plan/docs/foundations/`.
- Future product narrative can guide planning, but it must not quietly redefine current repo scope.
- Repo-specific behavior stays explicit instead of leaking into reusable surfaces.

## References
- [engineering_design_principles.md](engineering_design_principles.md)
- [product_direction.md](product_direction.md)

## Updated At
- `2026-03-19T05:30:00Z`
