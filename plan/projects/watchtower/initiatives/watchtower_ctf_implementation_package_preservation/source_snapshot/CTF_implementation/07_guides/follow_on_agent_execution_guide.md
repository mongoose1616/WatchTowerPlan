# Follow-On Agent Execution Guide

## How To Use This Package

1. read `README.md`, `00_context/step1_line_by_line_deconfliction_audit.md`, `08_tracking/implementation_gap_audit.md`, `00_context/reference_pack_precedent_review.md`, `04_contracts/artifact_payload_contracts_plan.md`, `04_contracts/state_and_index_contracts_plan.md`, `04_contracts/routing_and_runtime_contracts_plan.md`, `04_contracts/control_plane_registry_contracts_plan.md`, `04_contracts/rendered_surface_contracts_plan.md`, `04_contracts/lifecycle_and_safety_policy_contracts_plan.md`, `04_contracts/knowledge_governance_and_retrieval_plan.md`, `04_contracts/environment_and_safety_execution_plan.md`, `04_contracts/authority_map_and_lookup_plan.md`, `04_contracts/retention_and_cleanup_policy_plan.md`, and the `00_context/` baseline docs first;
2. implement phases in order unless a phase doc explicitly marks an item as parallel-safe;
3. use the contract docs in `04_contracts/` when writing manifests, schemas, validators, query/sync runtimes, and bootstrap logic;
4. use `03_workflows/` when authoring workflow docs, routing, and metadata;
5. keep `indexes/` updated in the same change set as the docs they describe.

## Required Discipline

- do not reintroduce retired `domain_packs/**` topology or `/docs/**` authority assumptions;
- keep the current-compatible scaffold identity until upstream slug handling is fixed;
- record any new live-contract delta before changing a phase or contract doc;
- prefer shared-core reuse over pack-local duplication when generic helpers already exist.

## Success Condition

The implementation is complete only when the real pack matches the package’s phase docs, contract docs, and JSON indexes without hidden interpretation steps.
