# Workflow Topology And Roles

## Workflow Model

The first offensive-security pack should use the current shared routing model:

- authored workflow modules and roles under the pack workflow root;
- a pack-owned `workflow_metadata_registry`;
- a pack-owned `ROUTING_TABLE.md`;
- shared workflow/route indexes and route preview from core.

## Internal Versus User-Facing Workflow Split

| Workflow Class | Planned Surfaces | Notes |
|---|---|---|
| user-facing | `challenge_intake`, `environment_context`, `ctf_execution`, `blocker_recovery`, `knowledge_capture`, `challenge_closeout` | operator-facing challenge flow |
| specialized governed lanes | `safety_review`, `discrepancy_reconciliation`, closeout extraction, validation, sync/rebuild shaping | safety review and discrepancy reconciliation are standalone routed modules that may also be composed as overlays from other workflows |
| roles | `ctf_operator`, `ctf_reviewer`, `ctf_safety_reviewer`, `ctf_discrepancy_reviewer`, `ctf_knowledge_reviewer` | roles compose modules and carry review/execution posture |

## Required Role Semantics

- `ctf_operator` is the main execution persona across intake, environment assessment, execution, blocker handling, and closeout.
- `ctf_reviewer` is the review lens for extraction quality, closeout completeness, and reusable-knowledge generalization.
- `ctf_safety_reviewer` owns escalation and admissibility review for higher-risk execution paths.
- `ctf_discrepancy_reviewer` owns discrepancy resolution, exception handling, and governance-limit release.
- `ctf_knowledge_reviewer` owns candidate quality, provenance sufficiency, and acceptance or rejection for reusable knowledge.
- role docs must include explicit `Composes Modules` sections that stay aligned with workflow metadata and route/index surfaces.

## Companion Shared Modules

Pack routes may compose shared workflow modules when needed, especially:

- `core.md`
- `task_scope_definition.md`
- `current_state_inspection.md`
- `internal_context_review.md`
- `external_guidance_research.md`
- `task_handoff_review.md`

Use shared modules for generic scoping, context gathering, and handoff. Keep CTF domain logic in pack-owned workflow docs.
