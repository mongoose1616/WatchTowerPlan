# Reference Pack Precedent Review

## Purpose

This review distills how `/home/j/WatchTowerPlan/plan` and `/home/j/WatchTowerOversight/oversight` already solve comparable hosted-pack problems so the offensive-security pack can reuse proven shapes instead of inventing new ones unnecessarily.

## Confirmed Precedents

| Area | WatchTowerPlan | WatchTowerOversight | Offensive-Security Implication |
|---|---|---|---|
| integration descriptor | `plan/python/src/watchtower_plan/integration.py` exports one `PACK_INTEGRATION` with `command_registration`, `query_runtime`, `sync_targets`, and `validation_provider` | `oversight/python/src/watchtower_oversight/integration.py` uses the same shape | keep the offsec pack on the same four-capability integration seam; do not invent a new runtime entry model |
| routing authority | `plan/workflows/ROUTING_TABLE.md` is the authoritative task-to-workflow routing surface | `oversight/workflows/ROUTING_TABLE.md` is also authoritative | keep `offensive_security/workflows/ROUTING_TABLE.md` as the route authority and keep workflow docs composable |
| workflow metadata | plan still points `workflow_metadata_registry` at shared core because its workflow split is still in progress | oversight publishes a pack-local `workflow_metadata_registry.json` for pack-owned IDs | use the oversight pattern for offsec because all planned workflow IDs are pack-owned |
| validation baseline | plan `validation_suite_registry.json` uses one baseline suite with `pack_contract`, `front_matter`, `document_semantics`, and `artifact` steps | oversight uses the same four-step baseline | offsec should keep the same baseline suite shape first, then layer challenge- or safety-specific suites later instead of inventing a different baseline taxonomy |
| pack control registries | plan pack settings declare `artifact_family_registry`, `documentation_family_registry`, `template_catalog`, `human_surface_policy_registry`, `authority_map`, `rendered_surface_registry`, `promotion_policy_registry`, `relation_type_registry`, `source_type_registry`, and lifecycle/review registries | oversight pack settings declare the same control-plane shape for its smaller domain, including `artifact_family_registry`, `documentation_family_registry`, `template_catalog`, `human_surface_policy_registry`, `authority_map`, and `rendered_surface_registry` | offsec likely needs the same pack-local control registries if its docs, templates, rendered views, and artifact families are meant to be governed rather than prose-only |
| artifact families | plan uses `artifact_family_registry.json` to publish placement roots, status fields, allowed status values, renderability, and derived indexes per family | oversight does the same for review-package families | offsec should likely add a pack-local `artifact_family_registry` rather than burying family placement and status semantics inside scattered schemas |
| templates and doc policies | plan `template_catalog.json` and `human_surface_policy_registry.json` govern required sections, section order, authorship mode, and required README/AGENTS/ROUTING_TABLE surfaces | oversight uses the same pattern and also governs rendered tracking docs | offsec templates should likely be governed through `template_catalog` plus `human_surface_policy_registry`, not only through prose standards |
| rendered visibility | plan renders `plan_overview.md` and tracking views from machine state and records them in `rendered_surface_registry` | oversight renders `oversight_overview.md`, `tracking/review_tracking.md`, and `tracking/template_tracking.md` | offsec should likely define explicit rendered visibility surfaces for challenge, knowledge, blocker, and session visibility rather than leaving rendered views unnamed |
| authority routing | plan `authority_map.json` maps recurring operator questions to canonical machine artifacts, preferred commands, preferred human paths, and fallbacks | oversight uses a smaller `authority_map.json` with the same question-to-surface pattern | offsec should likely define a starter authority map so operators and follow-on agents know the first authoritative surface for status, blockers, knowledge, sessions, routing, and safety questions |
| provenance vocabulary | plan uses `source_type_registry.json` to control provenance classes and allowed families | oversight relies more on standards-context and review-package provenance, but still uses governed machine artifacts and event trails | offsec should likely use a pack-local provenance vocabulary registry instead of loose enum strings in schemas |
| relation vocabulary | plan uses `relation_type_registry.json` to define directional relations, allowed families, and cardinality | oversight is smaller here and does not need a comparable relation vocabulary | offsec knowledge relations should likely follow the plan pattern and use a governed relation registry |
| promotion policy | plan uses `promotion_policy_registry.json` to map source artifact kinds to target families, target roots, required review paths, provenance requirements, and mirror rules | oversight does not promote reusable knowledge the same way | offsec knowledge promotion should likely use a policy registry, not only a status field |
| lifecycle registries | plan uses `lifecycle_stage_registry.json` and `review_status_registry.json` | oversight uses `review_package_status_registry.json` plus `status_transition_rules.json` | offsec challenge/session/knowledge candidate lifecycles should likely use registries and transition policy, not code-only transition logic |
| retention and cleanup | plan uses `retention_policy_registry.json` to distinguish surviving authority from purge-eligible closed packages | oversight separates closeout, archive, cleanup, extract, and delete, and retains deletion ledgers | offsec should explicitly decide whether archived challenges relocate, what survives closeout, and whether any cleanup or deletion is supported in v1 |
| closeout gating | plan closeout helpers reject closeout when required artifacts are missing, open tasks remain, or acceptance issues remain unless explicit override flags are supplied | oversight review-package lifecycle blocks illegal transitions and preserves event history across closeout, archive, cleanup, and delete | offsec closeout should explicitly check required artifacts, blocking discrepancies, and transition policy before mutating state |
| discrepancy and event handling | plan has an `InitiativeDiscrepancyCoordinator` that syncs managed discrepancy records, appends events, and enforces actor-based maintainer approval | oversight uses review-package event streams and status-transition policy for lifecycle auditability | offsec should treat discrepancy management and event streams as first-class pack-owned services with actor-linked audit behavior |
| query pattern | plan query services use one service per command plus typed search param dataclasses over indexes or rendered entries | oversight query services use the same typed search pattern for review-package lookup | offsec should mirror the same one-command/one-service/typed-search-params pattern for `status`, `challenges`, `knowledge`, `sessions`, and `blockers` |
| sync pattern | plan defines a canonical `sync/registry.py` with `SYNC_TARGET_SPECS` and explicit output paths | oversight does the same for its smaller target set | offsec should implement sync targets through one canonical sync registry module rather than ad hoc CLI branching |

## Most Important Implications For Offsec

- `workflow_metadata_registry` should be pack-local from day one because the planned offsec workflow IDs are new and pack-owned.
- The first offsec validation suite should mirror the existing pack baseline shape: `pack_contract`, `front_matter`, `document_semantics`, and `artifact`.
- The current offsec package under-specifies several control registries that both reference packs already use: `artifact_family_registry`, `documentation_family_registry`, `template_catalog`, `human_surface_policy_registry`, `authority_map`, and `rendered_surface_registry`.
- The current offsec package should explicitly define its first authority questions and their canonical lookup surfaces instead of leaving `authority_map` abstract.
- The current offsec package should likely add explicit policy or registry surfaces for lifecycle transitions, provenance source types, typed knowledge relations, and promotion policy.
- The current offsec package should explicitly decide whether `archived` is only a lifecycle flag or also a relocation or cleanup event.
- Offsec closeout should follow the plan and oversight pattern of explicit preconditions plus audited state transition, not a best-effort closeout mutation.

## Areas With Weak Or No Direct Precedent

- local, SSH, VPN, and airgapped environment adapters;
- offensive-security command safety taxonomy and confirmation gates;
- redaction policy for sensitive command capture during active challenge execution;
- challenge-specific evidence versus exploit artifact handling.

These remain genuinely pack-native decisions and should stay explicit in `open_decisions.json` rather than being forced into donor-pack patterns that solve a different problem.
