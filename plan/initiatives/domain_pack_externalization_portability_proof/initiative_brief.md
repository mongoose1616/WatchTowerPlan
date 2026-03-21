# Domain Pack Externalization and Portability Proof

## Summary
Proves that plan and future domain packs can be copied out with only packaging and path updates while reusable core and host integration remain stable.

## Identity
- `initiative_id`: `initiative.domain_pack_externalization_portability_proof`
- `trace_id`: `trace.domain_pack_externalization_portability_proof`
- `scope_type`: `pack_wide`

## Problem
The repository now has a clearer `watchtower_core` / `watchtower_host` / `watchtower_<pack>` split, but the contract is not yet proven portable. `plan` still lives inside the monorepo, and future pack adoption needs a concrete proof that pack-local code, manifests, docs, validation, and packaging can move together without hidden repository coupling.

## Objectives
- Prove the portable pack capsule for `plan/**`, including Python package boundaries, `.wt` machine state, docs, workflows, and manifests.
- Add a stronger second-pack proof path so reusable-core and host integration stay generic when another domain pack is present.
- Validate the copy-out contract directly so missing installation or missing declared pack surfaces fail in expected ways rather than through accidental runtime coupling.
- Publish the operator and developer guidance needed to externalize or add a pack without reading implementation code first.

## Scope
- `plan` pack portability and copy-out assumptions.
- Reusable-core and host validation for pack manifests, owned roots, packaging, and import direction.
- Synthetic second-pack fixtures and WatchTowerOversight-informed comparison checks.
- Pack-authoring standards, references, and workflow guidance where the portability contract needs stronger documentation.

## Non-Goals
- Extracting `plan` into a separate repository in this tranche.
- Rewriting WatchTowerOversight in place.
- Reintroducing direct `watchtower_core -> watchtower_plan` coupling or flat pack-owned root CLI commands.

## Initial Task Set
- `task.domain_pack_externalization_portability_proof.bootstrap_domain_pack_externalization_and_portability_proof`: Bootstrap Domain Pack Externalization and Portability Proof live initiative package.
