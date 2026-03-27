# Phase 2: Author The Pack Machine Contract

## Purpose

Define the offensive-security pack’s schemas, registries, suites, validators, path rules, and governed surfaces so the pack has a stable machine contract before deeper runtime work begins.

## In-Scope Surfaces

- pack-local schemas
- schema catalog, validator registry, validation suite registry
- workflow metadata registry
- adoption of shared governance surfaces from core
- pack-local ledgers, records, and governed path patterns

## Exact Planned Files, Schemas, Registries, Ledgers, Workflows, Validators, And Command Surfaces

- schemas:
  - `ctf_challenge_metadata`
  - `ctf_notes_metadata`
  - `ctf_event_stream`
  - `ctf_artifact_index`
  - `ctf_graph_index`
  - `ctf_evidence_artifact`
  - `ctf_closeout_record`
  - `ctf_extraction_output`
  - `ctf_environment_context`
  - `ctf_session_state`
  - `ctf_discrepancy_record`
- pack registries:
  - `offensive_security/.wt/registries/schema_catalog.json`
  - `offensive_security/.wt/registries/validator_registry.json`
  - `offensive_security/.wt/registries/validation_suite_registry.json`
  - `offensive_security/.wt/registries/workflow_metadata_registry.json`
  - `offensive_security/.wt/registries/artifact_family_registry.json`
  - `offensive_security/.wt/registries/documentation_family_registry.json`
  - `offensive_security/.wt/registries/template_catalog.json`
  - `offensive_security/.wt/registries/human_surface_policy_registry.json`
  - `offensive_security/.wt/registries/authority_map.json`
  - `offensive_security/.wt/registries/rendered_surface_registry.json`
  - `offensive_security/.wt/registries/query_family_registry.json`
  - `offensive_security/.wt/registries/event_type_registry.json`
  - `offensive_security/.wt/registries/discrepancy_type_registry.json`
  - `offensive_security/.wt/registries/severity_registry.json`
  - `offensive_security/.wt/registries/discrepancy_resolution_registry.json`
  - `offensive_security/.wt/registries/governance_limit_registry.json`
  - `offensive_security/.wt/registries/source_type_registry.json`
  - `offensive_security/.wt/registries/trust_state_registry.json`
  - `offensive_security/.wt/registries/verification_status_registry.json`
  - `offensive_security/.wt/registries/relation_type_registry.json`
  - `offensive_security/.wt/registries/review_status_registry.json`
  - `offensive_security/.wt/registries/promotion_policy_registry.json`
  - `offensive_security/.wt/registries/term_registry.json`
- pack policies:
  - `offensive_security/.wt/policies/status_transition_rules.json`
- shared surfaces to declare in pack settings once full pack context is needed:
  - `governance_surface_map`
  - `path_pattern_registry`
  - `status_registry`
  - `actor_registry`

## Dependencies

- Phase 0 identity and live-contract baselines
- Phase 1 scaffolded machine root
- current typed shared schemas for pack settings and governance surfaces

## Upstream Assumptions

- full `PackContext` loading is the right boundary for pack-governed surface access
- shared status and actor registries are generic enough for initial pack adoption

## Validation And Acceptance Criteria

- all required schema families are assigned concrete paths
- all governed artifact families inherit the shared payload primitives from `04_contracts/artifact_payload_contracts_plan.md`
- `event_stream`, `artifact_index`, `environment_context`, `challenge_metadata`, `notes_metadata`, `session_state`, and `discrepancy` field contracts are locked by `04_contracts/state_and_index_contracts_plan.md`
- the first machine-record slice lands `challenge_metadata`, `notes_metadata`, `event_stream`, `artifact_index`, `graph_index`, `session_state`, and `environment_context` together as one coherent substrate
- `source.type`, `trust_state`, and `verification_status` vocabularies are locked by `04_contracts/artifact_payload_contracts_plan.md`
- template, documentation-family, and human-surface-policy registry entry shapes are locked by `04_contracts/control_plane_registry_contracts_plan.md`
- rendered-surface registry entry shape is locked by `04_contracts/rendered_surface_contracts_plan.md`
- lifecycle policy artifact shape is locked by `04_contracts/lifecycle_and_safety_policy_contracts_plan.md`
- the validation suite expansion path replaces starter note validation with real CTF artifact validation
- the baseline validation suite covers `pack_contract`, `front_matter`, `document_semantics`, `artifact`, `graph_index`, `authority_map`, `query_contracts`, and `lifecycle_policy`
- the package distinguishes shared governance surfaces from pack-local registries cleanly
- conflict or deferred-extension items are separated from baseline requirements

## Risks And Unresolved Questions

- actor bootstrap and strict actor-ref validation may still be deferred if not needed on day one
- any future retention-policy registry should remain deferred unless v1 expands beyond logical archive plus frozen local state

## Exit Criteria

- the package provides a complete schema/registry/validation plan for the first real challenge flow
