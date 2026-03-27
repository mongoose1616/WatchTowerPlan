# Schemas, Registries, Ledgers, And Validation Plan

## Schema Rollout

| Rollout Stage | Required Schemas |
|---|---|
| scaffold baseline | starter note schema only, kept temporarily |
| before first real challenge flow | `ctf_challenge_metadata`, `ctf_notes_metadata`, `ctf_event_stream`, `ctf_artifact_index`, `ctf_evidence_artifact`, `ctf_closeout_record`, `ctf_extraction_output`, `ctf_environment_context`, `ctf_session_state`, `ctf_discrepancy_record` |
| before knowledge promotion | `knowledge_tactic`, `knowledge_playbook`, `knowledge_tool_profile`, `knowledge_protocol`, `knowledge_reference`, `knowledge_command_pattern` |

## Registry And Governance Surface Plan

| Surface | Owner | Notes |
|---|---|---|
| `schema_catalog` | pack | authoritative pack schema catalog |
| `validator_registry` | pack | pack-local validators only |
| `validation_suite_registry` | pack | start with one baseline suite that mirrors existing packs: `pack_contract`, `front_matter`, `document_semantics`, `artifact`; add later suites only after the baseline exists |
| `workflow_metadata_registry` | pack | replace scaffold starter entry immediately |
| `artifact_family_registry` | pack | both reference packs use this to publish placement, status field, renderability, and derived-index relationships by artifact family |
| `documentation_family_registry` | pack | declare pack-owned documentation families and their governed roots |
| `template_catalog` | pack | machine-readable template contract for required sections, section order, authorship mode, and LLM/operator guidance |
| `human_surface_policy_registry` | pack | govern required README, AGENTS, ROUTING_TABLE, and rendered-visibility surfaces by root |
| `authority_map` | pack | make human versus machine source-of-truth routing explicit instead of leaving it implicit in prose |
| `rendered_surface_registry` | pack | record derived rendered surfaces and their authoritative machine or markdown sources |
| `event_type_registry` | pack | govern allowed event names, required top-level fields, and allowed payload fields for `event_stream` |
| `discrepancy_type_registry` | pack | govern discrepancy classes and their default severity or review implications |
| `severity_registry` | pack | govern discrepancy severity values separately from discrepancy workflow state |
| `discrepancy_resolution_registry` | pack | govern allowed discrepancy resolution methods and exception-bearing outcomes |
| `governance_limit_registry` | pack | govern enforceable discrepancy-imposed limits such as closeout or promotion ineligibility |
| `source_type_registry` | pack | controlled provenance vocabulary for challenge observations, tool output, external references, and derived inference |
| `trust_state_registry` | pack | controlled trust vocabulary distinct from verification activity |
| `verification_status_registry` | pack | controlled verification-activity vocabulary distinct from trust posture |
| `relation_type_registry` | pack | controlled relation vocabulary for reusable knowledge and challenge artifact links |
| `review_status_registry` | pack | controlled review-progress vocabulary kept separate from lifecycle `status` |
| `promotion_policy_registry` | pack | map source artifact kinds to knowledge target families, required review path, provenance requirements, and update rules |
| `term_registry` | pack | machine-readable vocabulary surface with deprecation and replacement fields for offensive-security terminology |
| `status_transition_rules` | pack policy | explicit machine-readable transition policy with locked starter entries for `challenge_state`, `session_state`, `knowledge_state`, `closeout_record`, and `extraction_output` |
| `retention_policy_registry` | pack policy if cleanup or deletion is supported | add only if v1 supports archive relocation, cleanup pruning, or deletion beyond a logical `archived` lifecycle state |
| `governance_surface_map` | shared core, declared in pack settings | adopt once full pack context is needed |
| `path_pattern_registry` | shared core plus pack-local path rules if needed | use shared root rules and add pack-specific challenge/workspace patterns |
| `status_registry` | shared core | reuse global status vocabulary, add family-specific transition rules separately |
| `actor_registry` | shared core | available for later actor-ref validation and audit linkage |

## Ledger Plan

Pack-owned authoritative ledgers or streams should include:

- challenge event stream
- command I/O capture
- mode and autonomy transitions
- blocker/discrepancy records
- closeout record
- extraction output
- environment context
- session state
- airgapped transfer and provenance notes

## Validation Expansion

Scaffold baseline:

- pack contract validation
- governed front matter validation
- governed document-semantics validation
- governed artifact validation

First real expansion:

- challenge metadata validation
- notes metadata validation
- event stream validation
- artifact index validation
- evidence artifact validation
- closeout record validation
- extraction output validation
- environment context validation
- session state validation
- discrepancy validation
- knowledge-family validation as each family lands

## Locked Payload Contract Defaults

- keep one baseline validation suite named `suite.offensivesecurity.validation_baseline` with `pack_contract`, `front_matter`, `document_semantics`, `artifact`, `graph_index`, `authority_map`, `query_contracts`, and `lifecycle_policy` step kinds; add later suites only when a real offsec-specific gate needs separate execution;
- use the locked current-compatible registry posture from `04_contracts/control_plane_registry_contracts_plan.md` for root fields, entry lists, and rendered JSON-to-markdown companion behavior;
- use `04_contracts/artifact_payload_contracts_plan.md` as the field-level contract source for `ctf_closeout_record`, `ctf_evidence_artifact`, `ctf_extraction_output`, the shared reusable-knowledge envelope, and the family-specific knowledge payloads;
- raw evidence captures live under `artifacts/`, while the authoritative governed evidence inventory and provenance records live under `.wt_local/evidence/artifacts.json`;
- every governed JSON artifact family inherits the shared payload primitives: `contract_version`, pack-relative POSIX paths, UTC whole-second timestamps, and structured checksums;
- candidate reusable knowledge is created directly in its target family with `status: candidate` and promoted in place to `status: accepted`.

## Locked State And Runtime Contract Defaults

- use `04_contracts/state_and_index_contracts_plan.md` as the field-level contract source for `ctf_event_stream`, `ctf_artifact_index`, `ctf_environment_context`, and `ctf_discrepancy_record`;
- use `04_contracts/state_and_index_contracts_plan.md` as the field-level contract source for `ctf_challenge_metadata`, `ctf_notes_metadata`, `ctf_session_state`, and the row contracts behind `challenge_index`, `blocker_index`, `session_index`, and `knowledge_index`;
- use `04_contracts/routing_and_runtime_contracts_plan.md` as the current-compatible contract source for workflow metadata, route index, route preview, and generic query-helper composition;
- use `04_contracts/artifact_payload_contracts_plan.md` as the current-compatible contract source for the nested `source` object plus `source.type`, `trust_state`, and `verification_status` vocabularies;
- treat discrepancy severity, discrepancy workflow status, and discrepancy-imposed governance limits as separate governed concepts;
- treat the live shared-core `workflow_metadata_registry` schema and live `watchtower-core route preview` payload as the current contract unless shared core changes upstream.

## Semantic Validation Rules

- use pack-owned document-semantics validation for offensive-security docs and challenge artifacts;
- reuse shared command, workflow, standards, and link semantics helpers where they already exist;
- allow required front matter to be populated at the next workflow opportunity rather than assuming immediate synchronous authoring at intake;
- keep pack-local validators thin and domain-specific.

## Reference-Pack Precedent

- `plan` and `oversight` both treat the baseline suite as one explicit validation baseline with standard step kinds rather than separate domain-named suites from day one;
- `plan` extends beyond the starter baseline with pack-local registries for provenance, relations, promotion policy, and lifecycle vocabularies;
- `oversight` proves that pack-local lifecycle transition policy can live as a separate governed policy surface instead of staying hidden in service code.
