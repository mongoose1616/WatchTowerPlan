# Deferred Review Register

## How To Use This File

- `implementation_gap_audit.md` is the full human-readable decision register.
- `indexes/open_decisions.json` is the machine-readable companion.
- All decisions in the package are now locked. This file tracks the subset whose locked default is an intentional post-v1 deferral rather than a v1 implementation requirement.

## Implementation State

- No phase-gated implementation decisions remain open. The package defaults are now locked across Phases 0 through 7.

## Locked Post-V1 Deferrals

- `decision.workflow_catalog`: defer richer `workflow_catalog` beyond the routing-table plus workflow-metadata baseline, with the later target adding titles, summaries, inputs, outputs, owner, version, workflow-surface links, composition/dependency metadata, and a generated human explorer over a machine-primary catalog
- `decision.actor_bootstrap_day_one`: reuse shared `actor_registry` and defer explicit actor bootstrap unless strict actor-ref validation is needed immediately
- `decision.public_rebuild_cli`: keep public operator guidance aligned to `sync`
- `decision.pentest_pack_split`: start with one `offensive_security` hosted pack and revisit future pack-splitting later
- `decision.saved_query_views`: defer saved query views beyond v1; when added, ship pack-owned defaults first, user-local customization later, and keep user-local views outside the governed pack root
- `decision.provenance_review_impact_surface`: defer richer provenance/trust review workflows beyond v1; when added, prefer provenance-triggered re-review, downstream impact analysis, and a reviewer-facing affected-downstream view while still flagging accepted artifacts for review rather than auto-invalidating them

## Current Package Defaults

- the first implementation stays on one hosted pack rooted at `offensive_security/` with `ctf` and `knowledge` domain roots;
- routing/runtime shared-core contracts are locked in `04_contracts/routing_and_runtime_contracts_plan.md`;
- the routing-table versus workflow-metadata split is locked, and offsec does not add pack-specific aliases for shared route/workflow query surfaces in v1;
- control-plane registry entry contracts are locked in `04_contracts/control_plane_registry_contracts_plan.md`;
- the v1 control-plane registry inventory and current-compatible registry root posture are locked in `04_contracts/control_plane_registry_contracts_plan.md` and `04_contracts/schemas_registries_ledgers_validation_plan.md`;
- the v1 path, placeholder, collision, and typed-id rules are locked in `04_contracts/path_and_id_generation_plan.md`;
- the v1 authority map is locked in `04_contracts/authority_map_and_lookup_plan.md`;
- `notes.md` stays on one canonical template with append-preserving reconciliation, while `challenge.md` stays source-faithful with delayed front-matter population allowed;
- the v1 document template minimums are locked in `06_standards/documentation_and_templates_standard.md`;
- challenge/session lifecycle subsets now align to the live shared `status_registry`, with solve and unresolved semantics carried in closeout outcome rather than pack-only status values;
- the v1 retention and cleanup rule is locked in `04_contracts/retention_and_cleanup_policy_plan.md`;
- the v1 closeout gate is locked in `04_contracts/retention_and_cleanup_policy_plan.md`, including solved-only `solution/`, recap requirements by outcome, discrepancy admissibility gates, and required validation;
- artifact payload primitives plus the field-level closeout, evidence, extraction, and knowledge-family contracts are locked in `04_contracts/artifact_payload_contracts_plan.md`;
- command capture and redaction are locked in `06_standards/evidence_provenance_and_audit_standard.md`, with compact routine surfaces and artifact-backed handling for raw or sensitive output;
- state/index/discrepancy contracts are locked in `04_contracts/state_and_index_contracts_plan.md`;
- challenge metadata, notes metadata, session state, and the four pack index row contracts are locked in `04_contracts/state_and_index_contracts_plan.md`;
- nested `source`, `source.type`, `trust_state`, and `verification_status` are locked in `04_contracts/artifact_payload_contracts_plan.md`;
- the shared offsec query-output baseline plus the minimal sync namespace and target-output split are locked in `04_contracts/query_sync_rendered_views_docs_plan.md`;
- rendered-surface registry shape and starter visibility recommendations are locked in `04_contracts/rendered_surface_contracts_plan.md`;
- lifecycle and safety policy artifact shapes are locked in `04_contracts/lifecycle_and_safety_policy_contracts_plan.md`;
- the baseline validation suite layout is locked in `04_contracts/schemas_registries_ledgers_validation_plan.md`;
- discrepancy governance now uses separate `status`, `severity`, `forces_needs_review`, and `governance_limits` concepts rather than a special `policy_block` severity;
- extraction is on-demand plus automatic at closeout, with no periodic active-phase extraction by default;
- vocabulary governance uses one canonical glossary standard, one pack-facing glossary surface, and one machine `term_registry`;
- reusable-knowledge lifecycle and review-state baselines are locked in `06_standards/knowledge_taxonomy_and_promotion_standard.md`;
- relation typing, promotion policy, deterministic retrieval, source clarification, and reusable-knowledge external-reference rules are locked in `04_contracts/knowledge_governance_and_retrieval_plan.md`;
- session state distinguishes requested mode from effective mode, and full-auto observability uses planned-command previews plus concise post-step summaries;
- the shared adapter protocol, safety confirmation triggers, airgapped transfer manifest, and actor-ref requirement are locked in `04_contracts/environment_and_safety_execution_plan.md`;
- shared `actor_registry` is available, but actor bootstrap remains optional for v1;
- public operator guidance stays centered on `sync`.
