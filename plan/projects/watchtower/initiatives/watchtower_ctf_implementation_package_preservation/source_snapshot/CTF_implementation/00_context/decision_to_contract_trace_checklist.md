# Decision To Contract Trace Checklist

## Purpose

This checklist verifies that the answered decision-workshop questions were propagated into canonical package docs and indexes rather than left only in conversational history.

Verification date:

- `2026-03-26`

Verification rule:

- `verified` means the answer is present in the canonical contract, standard, phase, workflow, or machine-index surfaces that govern implementation;
- this checklist is a trace aid, not a second authority surface.

## Identity, Lifecycle, And Closeout

- `Q01`: fixed canonical challenge root with `unknown_platform` and `unknown_event` placeholders. Verified in `04_contracts/path_and_id_generation_plan.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.
- `Q02`: placeholder-created roots are corrected later through governed rename or migration rather than staying permanently canonical. Verified in `04_contracts/path_and_id_generation_plan.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.
- `Q03`: `challenge_id = challenge.<platform_slug>.<event_slug>.<challenge_slug>`. Verified in `04_contracts/path_and_id_generation_plan.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.
- `Q04`: `knowledge_id = knowledge.<family>.<context_slug>.<knowledge_slug>` when the family naturally nests; otherwise `knowledge.<family>.<knowledge_slug>`. Verified in `04_contracts/path_and_id_generation_plan.md` and `indexes/open_decisions.json`.
- `Q05`: governed rename rewrites known machine refs, rendered links, and internal doc links atomically. Verified in `04_contracts/path_and_id_generation_plan.md`.
- `Q06`: slug collisions use numeric suffixes mirrored into ids. Verified in `04_contracts/path_and_id_generation_plan.md` and `indexes/open_decisions.json`.
- `Q07`: auto-rename still applies after downstream refs exist, through one governed migration. Verified in `04_contracts/path_and_id_generation_plan.md`.
- `Q08`: challenge status subset is `active`, `blocked`, `needs_review`, `in_review`, `completed`, `closed`. Verified in `04_contracts/state_and_index_contracts_plan.md` and `indexes/open_decisions.json`.
- `Q09`: session status subset is `active`, `blocked`, `needs_review`, `in_review`, `completed`, `closed`, `cancelled`. Verified in `04_contracts/state_and_index_contracts_plan.md` and `indexes/open_decisions.json`.
- `Q10`: closeout outcomes are `solved`, `blocked_closeout`, `unresolved`, and `closed_without_attempt`. Verified in `04_contracts/artifact_payload_contracts_plan.md` and `04_contracts/retention_and_cleanup_policy_plan.md`.
- `Q11`: closeout gate requires `challenge.md`, `notes.md`, `closeout_record`, extraction output, passing closeout validation, no active `no_closeout` discrepancy, solved-only `solution/`, and recap for attempted-work outcomes. Verified in `04_contracts/retention_and_cleanup_policy_plan.md`, `02_phases/phase_4_domain_artifacts.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.

## Notes, Evidence, And Redaction

- `Q12`: one canonical `notes.md` structure with optional sections and mode-aware overlays. Verified in `06_standards/documentation_and_templates_standard.md` and `02_phases/phase_4_domain_artifacts.md`.
- `Q13`: `notes.md` edits are append-preserving during active work. Verified in `06_standards/documentation_and_templates_standard.md` and `02_phases/phase_4_domain_artifacts.md`.
- `Q14a`: redact only clearly player-owned material from routine machine-visible surfaces. Verified in `06_standards/evidence_provenance_and_audit_standard.md`, `02_phases/phase_4_domain_artifacts.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.
- `Q15`: raw captures stay under `artifacts/`. Verified in `04_contracts/artifact_payload_contracts_plan.md`, `04_contracts/retention_and_cleanup_policy_plan.md`, and `06_standards/evidence_provenance_and_audit_standard.md`.
- `Q15a`: governed evidence metadata lives in `.wt_local/evidence/artifacts.json` with `entries[]`. Verified in `04_contracts/artifact_payload_contracts_plan.md`, `04_contracts/retention_and_cleanup_policy_plan.md`, `04_contracts/schemas_registries_ledgers_validation_plan.md`, `02_phases/phase_4_domain_artifacts.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.
- `Q16`: evidence entries are current-state rows keyed by `artifact_id` and updated in place. Verified in `04_contracts/artifact_payload_contracts_plan.md`.
- `Q16a`: use `created_at_utc`, `updated_at_utc`, and event-stream mirroring instead of a per-entry change log. Verified in `04_contracts/artifact_payload_contracts_plan.md`.
- `Q17`: event stream remains `.wt_local/event_stream.ndjson`. Verified in `04_contracts/state_and_index_contracts_plan.md` and `02_phases/phase_4_domain_artifacts.md`.
- `Q18`: discrepancy workflow is `open -> in_review -> resolved | dismissed`. Verified in `04_contracts/state_and_index_contracts_plan.md`.

## Knowledge Governance And Retrieval

- `Q19`: candidate knowledge is created directly in target family paths and promoted in place to `accepted`. Verified in `04_contracts/artifact_payload_contracts_plan.md` and `06_standards/knowledge_taxonomy_and_promotion_standard.md`.
- `Q20`: reusable knowledge families are `tactics`, `playbooks`, `tools`, `protocols`, `references`, and `commands`. Verified in `04_contracts/artifact_payload_contracts_plan.md` and `06_standards/knowledge_taxonomy_and_promotion_standard.md`.
- `Q21`: `playbooks` stay nested under `tactics`. Verified in `04_contracts/artifact_payload_contracts_plan.md` and `06_standards/knowledge_taxonomy_and_promotion_standard.md`.
- `Q22`: starter relation vocabulary includes `imported_via_transfer`. Verified in `04_contracts/knowledge_governance_and_retrieval_plan.md`, `06_standards/knowledge_taxonomy_and_promotion_standard.md`, and `indexes/open_decisions.json`.
- `Q22a`: keep `imported_via_transfer` as a first-class relation type. Verified in the same surfaces.
- `Q23`: promotion remains review-heavy with auto-promotion off by default. Verified in `04_contracts/knowledge_governance_and_retrieval_plan.md` and `indexes/open_decisions.json`.
- `Q24`: retrieval ranking uses scope match, exact tool or protocol match, reusability, freshness, evidence quality, breadth, teacher-mode explanation boost, then deterministic `knowledge_id` tie-break. Verified in `04_contracts/knowledge_governance_and_retrieval_plan.md`, `06_standards/knowledge_taxonomy_and_promotion_standard.md`, `02_phases/phase_5_knowledge_promotion_and_retrieval.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.
- `Q25a`: ask material clarification questions in `assistant`, `teacher`, and `note_taker`, but stay provisional in `full_auto`. Verified in `04_contracts/knowledge_governance_and_retrieval_plan.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.
- `Q26`: external references require `url` and `reference_kind`, recommend `label`, and may add `is_primary` and `quality_notes`. Verified in `04_contracts/knowledge_governance_and_retrieval_plan.md`.

## Environment, Safety, And Actors

- `Q27`: adapters are `local`, `vpn_reachable`, `ssh`, and `airgapped`. Verified in `04_contracts/environment_and_safety_execution_plan.md`, `06_standards/operator_modes_and_safety_standard.md`, and `02_phases/phase_6_environment_adapters_and_safety.md`.
- `Q28`: shared adapter methods are `describe_context`, `check_capability`, `execute_command`, `capture_artifact`, `stage_transfer`, and `record_provenance`. Verified in `04_contracts/environment_and_safety_execution_plan.md`, `06_standards/operator_modes_and_safety_standard.md`, and `indexes/open_decisions.json`.
- `Q29`: confirmation is required for mode changes, credential use, privilege escalation, remote state changes, long-running automation, external transfer, and destructive cleanup. Verified in `04_contracts/environment_and_safety_execution_plan.md`, `06_standards/operator_modes_and_safety_standard.md`, and `indexes/open_decisions.json`.
- `Q30`: `full_auto` refusal posture remains destructive-unattended refusal plus scope, context, provenance, and stale-state guards. Verified in `04_contracts/environment_and_safety_execution_plan.md` and `indexes/open_decisions.json`.
- `Q31`: actor refs are mandatory for approvals, confirmations, promotion approvals, closeout approvals or finalization, delegated or remote execution, airgapped transfer, and destructive or retention actions. Verified in `04_contracts/environment_and_safety_execution_plan.md`, `06_standards/operator_modes_and_safety_standard.md`, and `indexes/open_decisions.json`.
- `Q32`: airgapped transfers require structured manifests, checksum when practical, quarantine or lower trust until verified, and mandatory re-paste on malformed structured output. Verified in `04_contracts/environment_and_safety_execution_plan.md`, `02_phases/phase_6_environment_adapters_and_safety.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.
- `Q33`: `status` query exposes safety-posture fields. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md` and `04_contracts/authority_map_and_lookup_plan.md`.

## Query, Generic Retrieval, And Graph

- `Q34`: everything useful for operator or LLM retrieval should be queryable. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md` and `indexes/open_decisions.json`.
- `Q35`: use a two-tier query model with derived outputs by default and stable raw governed records where useful. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md`.
- `Q36`: use curated first-class query commands plus generic family-query fallback. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md`.
- `Q37`: curated v1 query families include `status`, `challenges`, `knowledge`, `sessions`, `blockers`, `artifacts`, `events`, and `environment`, with later workshop answers extending the curated set to `discrepancies`, `closeout`, `commands`, and `references`. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md` and `02_phases/phase_3_ctf_runtime.md`.
- `Q38`: generic family-query fallback may expose stable derived indexes and stable raw governed records. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md`.
- `Q39`: expose a public graph query surface for operators and LLMs or agents. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md`, `04_contracts/state_and_index_contracts_plan.md`, and `02_phases/phase_3_ctf_runtime.md`.
- `Q40`: graph traversal spans all typed relational artifact families. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md` and `04_contracts/state_and_index_contracts_plan.md`.
- `Q41a`: graph output supports `human`, `json`, and `both`. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md` and `04_contracts/state_and_index_contracts_plan.md`.
- `Q42`: graph traversal controls support `from`, `depth`, `direction`, `relation`, `family`, `limit`, `format`, `status`, `review-status`, `trust-state`, and `verification-status`. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md` and `04_contracts/state_and_index_contracts_plan.md`.
- `Q43`: graph traversal defaults to both directions. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md` and `04_contracts/state_and_index_contracts_plan.md`.
- `Q44`: graph roots may be any typed artifact id from relational families. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md` and `04_contracts/state_and_index_contracts_plan.md`.
- `Q45`: graph edges are typed, directed, and may carry evidence or provenance refs. Verified in `04_contracts/state_and_index_contracts_plan.md`.
- `Q46a`: use a separate derived `graph_index`. Verified in `04_contracts/state_and_index_contracts_plan.md`, `04_contracts/query_sync_rendered_views_docs_plan.md`, `02_phases/phase_2_pack_machine_contract.md`, and `02_phases/phase_3_ctf_runtime.md`.
- `Q47`: `graph_index` includes nodes, edges, adjacency, and traversal metadata. Verified in `04_contracts/state_and_index_contracts_plan.md`.
- `Q48`: graph node rows include ids, family, kind, summary, canonical path, review or trust posture, and context refs. Verified in `04_contracts/state_and_index_contracts_plan.md`.
- `Q49`: graph edge rows are denormalized beyond bare triples. Verified in `04_contracts/state_and_index_contracts_plan.md`.
- `Q50`: `graph-index` is a dedicated sync target and is also included in `all`. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md` and `02_phases/phase_3_ctf_runtime.md`.

## Validation, Workflow Modules, Roles, And Modes

- `Q51`: validation baseline includes `pack_contract`, `front_matter`, `document_semantics`, `artifact`, `graph_index`, `authority_map`, `query_contracts`, and `lifecycle_policy`. Verified in `04_contracts/schemas_registries_ledgers_validation_plan.md`, `02_phases/phase_2_pack_machine_contract.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.
- `Q52`: workflow modules include `challenge_intake`, `environment_context`, `ctf_execution`, `blocker_recovery`, `knowledge_capture`, `challenge_closeout`, `safety_review`, and `discrepancy_reconciliation`. Verified in `03_workflows/workflow_inventory.md`, `03_workflows/routing_and_metadata_plan.md`, `03_workflows/workflow_topology_and_roles.md`, `02_phases/phase_3_ctf_runtime.md`, `README.md`, and `04_contracts/scaffold_and_bootstrap_baseline.md`.
- `Q53`: workflow roles include `ctf_operator`, `ctf_reviewer`, `ctf_safety_reviewer`, `ctf_discrepancy_reviewer`, and `ctf_knowledge_reviewer`. Verified in `03_workflows/workflow_inventory.md`, `03_workflows/workflow_topology_and_roles.md`, and `02_phases/phase_3_ctf_runtime.md`.
- `Q54`: operating modes remain session-state fields rather than workflow roles. Verified in `06_standards/operator_modes_and_safety_standard.md` and `04_contracts/state_and_index_contracts_plan.md`.
- `Q55`: operating mode vocabulary is `note_taker`, `assistant`, `teacher`, and `full_auto`. Verified in `06_standards/operator_modes_and_safety_standard.md` and `02_phases/phase_6_environment_adapters_and_safety.md`.
- `Q56`: interaction-mode overlays are `shared_workspace`, `guided_user_execution`, `delegated_agent_execution`, `airgapped_exchange`, `observer_review`, `async_handoff`, and `pairing`. Verified in `04_contracts/environment_and_safety_execution_plan.md`, `06_standards/operator_modes_and_safety_standard.md`, and `02_phases/phase_6_environment_adapters_and_safety.md`.
- `Q57`: command-doc structure includes a directory `README.md`, per-command pages, a query-family overview page, and a graph-query guide. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md`, `04_contracts/scaffold_and_bootstrap_baseline.md`, `02_phases/phase_3_ctf_runtime.md`, and `README.md`.
- `Q58`: `ROUTING_TABLE.md` and `workflow_metadata_registry.json` are co-equal authorities. Verified in `04_contracts/routing_and_runtime_contracts_plan.md`, `03_workflows/routing_and_metadata_plan.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.
- `Q59`: disagreement between those routing surfaces fails validation immediately. Verified in `04_contracts/routing_and_runtime_contracts_plan.md`.
- `Q60`: `safety_review` and `discrepancy_reconciliation` are standalone routed modules that may also act as overlays. Verified in `03_workflows/workflow_inventory.md`, `03_workflows/workflow_topology_and_roles.md`, `03_workflows/routing_and_metadata_plan.md`, and `02_phases/phase_3_ctf_runtime.md`.

## Evidence Model, Discrepancy Vocabularies, And Event Vocabulary

- `Q61`: evidence metadata uses one shared envelope plus `artifact_kind`-specific payloads. Verified in `04_contracts/artifact_payload_contracts_plan.md`.
- `Q62`: starter evidence kinds are `command_output`, `file_capture`, `screenshot`, `network_capture`, `manual_note`, `clipboard_capture`, and `transfer_bundle`. Verified in `04_contracts/artifact_payload_contracts_plan.md`.
- `Q62a`: scripts and executables stay under `file_capture` with payload roles such as `generated_script`, `generated_binary`, and `downloaded_binary`. Verified in `04_contracts/artifact_payload_contracts_plan.md` and `06_standards/evidence_provenance_and_audit_standard.md`.
- `Q63`: discrepancy severities are `informational`, `low`, `medium`, `high`, and `critical`. Verified in `04_contracts/state_and_index_contracts_plan.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.
- `Q64`: discrepancy resolutions are `resolved`, `dismissed`, and `exceptioned`. Verified in `04_contracts/state_and_index_contracts_plan.md` and `indexes/open_decisions.json`.
- `Q65`: governance limits are `read_only_only`, `no_remote_execution`, `no_closeout`, `review_required`, `no_promotion`, `no_full_auto`, and `no_transfer`. Verified in `04_contracts/state_and_index_contracts_plan.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.
- `Q66`: starter event vocabulary includes lifecycle, command, transfer, discrepancy, sync, rebuild, validation, and workflow-route events. Verified in `04_contracts/state_and_index_contracts_plan.md`.
- `Q67`: command execution events are modeled through one command activity family rather than only a single flat `command_executed` event. Verified in `04_contracts/state_and_index_contracts_plan.md`.
- `Q68a`: use `command_activity` with payload `stage` and `execution_context_type`. Verified in `04_contracts/state_and_index_contracts_plan.md` and `04_contracts/artifact_payload_contracts_plan.md`.
- `Q69`: workflow events include `workflow_started`, `workflow_completed`, `workflow_routed`, `workflow_handoff`, and `workflow_escalated`. Verified in `04_contracts/state_and_index_contracts_plan.md`.
- `Q70`: validation and sync events include started and completed events for validation, sync, and rebuild. Verified in `04_contracts/state_and_index_contracts_plan.md`.

## Rich Index Rows And Curated Query Extensions

- `Q71`: `challenge_index` is a rich row, not a minimal row. Verified in `04_contracts/state_and_index_contracts_plan.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.
- `Q72`: `blocker_index` is a rich row, not a minimal row. Verified in the same surfaces.
- `Q73`: `session_index` is a rich row, not a minimal row. Verified in the same surfaces.
- `Q74`: `knowledge_index` is a rich row, not a minimal row. Verified in the same surfaces.
- `Q75`: `artifacts` is a curated first-class query command. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md` and `02_phases/phase_3_ctf_runtime.md`.
- `Q76`: `events` is a curated first-class query command. Verified in the same surfaces.
- `Q77`: `environment` is a curated first-class query command. Verified in the same surfaces.
- `Q78`: `discrepancies` is a curated first-class query command. Verified in the same surfaces.
- `Q79`: `closeout` is a curated query surface that groups closeout records with extraction outputs. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md`.
- `Q80`: `commands` is a curated filtered view over `knowledge`. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md` and `02_phases/phase_3_ctf_runtime.md`.
- `Q81`: `references` is a curated filtered view over `knowledge`. Verified in the same surfaces.
- `Q82`: query docs include a general query overview, a graph guide, and generic family-query fallback explanation. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md`.
- `Q83`: route and workflow discovery stays on shared-core surfaces; no offsec-local aliases. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md` and `04_contracts/routing_and_runtime_contracts_plan.md`.
- `Q84`: use a pack-local `query_family_registry` and generate query docs from it. Verified in `04_contracts/query_sync_rendered_views_docs_plan.md`, `04_contracts/control_plane_registry_contracts_plan.md`, `02_phases/phase_2_pack_machine_contract.md`, and `02_phases/phase_3_ctf_runtime.md`.

## Propagation And Canonicalization Rules

- `Q85`: incorporated decisions should not keep a permanent standalone workshop log. The temporary 2026-03-27 workshop log was used only to capture still-unincorporated answers, then removed after normalization, verification, and validation.
- `Q86`: the canonical record of each finalized answer still lives in the directly affected contract, standard, workflow, phase, or index surfaces; the temporary workshop log was never authoritative and was removed once normalization completed.
- `Q87`: apply workshop changes deepest-contracts-first and then propagate outward. Verified by the normalization sequence across `04_contracts/`, then `03_workflows/`, then `02_phases/`, then `indexes/`, `README.md`, and `08_tracking/implementation_gap_audit.md`.
- `Q88`: normalize the answered decisions into the package now instead of deferring. Verified by the present state of the canonical docs and indexes and by removal of the temporary workshop note.

## Active Workshop 2026-03-27 Normalization

- `Q89-Q129`, `Q151`, `Q153`, `Q154`, and `Q157`: query human-output, graph-human-output, relation-expansion, sorting, and `status`-as-context decisions are normalized into `04_contracts/query_sync_rendered_views_docs_plan.md`, `04_contracts/authority_map_and_lookup_plan.md`, `02_phases/phase_3_ctf_runtime.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.
- `Q160`, `Q161`, `Q170-Q188`: knowledge, commands, and references retrieval-presentation decisions are normalized into `04_contracts/query_sync_rendered_views_docs_plan.md`, `04_contracts/knowledge_governance_and_retrieval_plan.md`, `02_phases/phase_3_ctf_runtime.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.
- `Q131-Q146`, `Q152`, `Q155`, `Q158`, `Q162`, `Q165`, and `Q168`: runtime-rollout and first-slice sequencing decisions are normalized into `02_phases/phase_1_scaffold_and_integrate.md`, `02_phases/phase_2_pack_machine_contract.md`, `02_phases/phase_3_ctf_runtime.md`, `README.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.
- `Q147-Q150`, `Q156`, `Q159`, `Q163`, `Q166`, and `Q169`: post-v1 roadmap decisions are normalized into `08_tracking/deferred_review_register.md`, `08_tracking/implementation_gap_audit.md`, and `indexes/open_decisions.json`.

## Residual Note

- `00_context/step1_traceability_matrix.md` still contains source-wording references such as "teaching mode" because that file traces original Step 1 questions verbatim. Those source-question phrases are not package policy defaults.
