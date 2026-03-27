# Authority Map And Lookup Plan

## Purpose

Turn the Step 1 authority decisions and the live shared-core `authority_map` contract into an implementation-ready lookup policy for the offensive-security pack.

## Current Contract Basis

- shared contract:
  - `core/docs/standards/data_contracts/authority_map_standard.md`
  - `core/control_plane/schemas/artifacts/authority_map.schema.json`
- Step 1 basis:
  - `STEP1_FINAL.md` `Q01`, `Q02`, and `Q04` for active versus post-close authority
  - `STEP1_PACK_SCAFFOLD_SPEC_v1.md` for `overview_path`, `tracking_root`, and the initial query inventory
  - `STEP1_FINAL_v3.md` for the current-compatible rule that challenge-specific authority surfaces remain pack-owned

## Planned Artifact

- path: `offensive_security/.wt/registries/authority_map.json`
- schema: `urn:watchtower:schema:artifacts:registries:authority-map:v1`
- root fields:
  - `$schema`
  - `id = registry.authority_map`
  - `title = Offensive-Security Authority Map`
  - `status = active`
  - `entries[]`

## Supporting Canonical Machine Surfaces

| Artifact Kind | Canonical Path | Phase | Notes |
|---|---|---|---|
| `challenge_index` | `offensive_security/.wt/indexes/challenge_index.json` | Phase 3 | authoritative pack-level challenge lookup surface |
| `blocker_index` | `offensive_security/.wt/indexes/blocker_index.json` | Phase 3 | authoritative pack-level blocker and blocking-discrepancy lookup surface |
| `knowledge_index` | `offensive_security/.wt/indexes/knowledge_index.json` | Phase 5 | authoritative promoted and candidate knowledge lookup surface |
| `session_index` | `offensive_security/.wt/indexes/session_index.json` | Phase 3 | authoritative session and flattened environment-context lookup surface |
| `artifact_index` | `offensive_security/.wt/indexes/artifact_index.json` | Phase 2 | broad cross-family artifact catalog and path-resolution surface |
| `route_index` | `core/control_plane/indexes/routes/route_index.json` | shared core | current canonical routed-workflow lookup surface |
| `command_index` | `core/control_plane/indexes/commands/command_index.json` | shared core | current canonical command-discovery surface |
| `safety_confirmation_matrix` | `offensive_security/.wt/policies/safety_confirmation_matrix.json` | Phase 6 | authoritative machine safety and confirmation policy for offsec actions |

## V1 Question Set

| Question ID | Domain | Question | Artifact Kind | Canonical Path | Preferred Command | Preferred Human Path | Fallback Paths |
|---|---|---|---|---|---|---|---|
| `authority.offsec.current_state` | `planning` | What is the current offensive-security pack state and next action? | `challenge_index` | `offensive_security/.wt/indexes/challenge_index.json` | `watchtower-core offsec query status` | `offensive_security/offensivesecurity_overview.md` | `offensive_security/tracking/challenge_tracking.md`, `offensive_security/tracking/blocker_tracking.md`, `offensive_security/.wt/indexes/blocker_index.json` |
| `authority.offsec.challenge_lookup` | `planning` | Which challenges exist and what state is each challenge in? | `challenge_index` | `offensive_security/.wt/indexes/challenge_index.json` | `watchtower-core offsec query challenges` | `offensive_security/tracking/challenge_tracking.md` | `offensive_security/offensivesecurity_overview.md`, `offensive_security/.wt/indexes/artifact_index.json`, `offensive_security/ctf/` |
| `authority.offsec.blocker_state` | `planning` | Which challenges are blocked or have blocking discrepancies? | `blocker_index` | `offensive_security/.wt/indexes/blocker_index.json` | `watchtower-core offsec query blockers` | `offensive_security/tracking/blocker_tracking.md` | `offensive_security/.wt/indexes/challenge_index.json`, `offensive_security/.wt/indexes/artifact_index.json`, `offensive_security/ctf/` |
| `authority.offsec.knowledge_lookup` | `planning` | Which promoted or candidate knowledge artifacts exist and where do they live? | `knowledge_index` | `offensive_security/.wt/indexes/knowledge_index.json` | `watchtower-core offsec query knowledge` | `offensive_security/tracking/knowledge_tracking.md` | `offensive_security/knowledge/`, `offensive_security/.wt/indexes/artifact_index.json`, `offensive_security/offensivesecurity_overview.md` |
| `authority.offsec.session_environment_context` | `planning` | What is the current or recent session state and environment context for challenge work? | `session_index` | `offensive_security/.wt/indexes/session_index.json` | `watchtower-core offsec query sessions` | `offensive_security/tracking/session_tracking.md` | `offensive_security/.wt/indexes/challenge_index.json`, `offensive_security/ctf/`, `offensive_security/workflows/modules/environment_context.md` |
| `authority.governance.workflow_routing` | `governance` | Which routed workflow stack applies to this request? | `route_index` | `core/control_plane/indexes/routes/route_index.json` | `watchtower-core route preview` | `offensive_security/workflows/ROUTING_TABLE.md` | `core/workflows/ROUTING_TABLE.md`, `core/control_plane/indexes/workflows/workflow_index.json` |
| `authority.governance.command_lookup` | `governance` | Which command surface should I use and where is it documented? | `command_index` | `core/control_plane/indexes/commands/command_index.json` | `watchtower-core query commands` | `offensive_security/docs/commands/core_python/README.md` | `offensive_security/docs/commands/core_python/watchtower_core_offsec.md`, `core/docs/commands/core_python/README.md`, `core/control_plane/indexes/repository_paths/repository_path_index.json` |
| `authority.offsec.safety_posture` | `governance` | What safety posture, confirmation gates, and execution limits apply before action? | `safety_confirmation_matrix` | `offensive_security/.wt/policies/safety_confirmation_matrix.json` | `watchtower-core offsec query status` | `offensive_security/docs/standards/operations/operator_modes_and_safety_standard.md` | `offensive_security/.wt/indexes/session_index.json`, `offensive_security/workflows/modules/environment_context.md`, `offensive_security/workflows/modules/ctf_execution.md` |

## Locked V1 Rules

- keep the authority map question-driven rather than inventory-driven;
- prefer one canonical machine surface per recurring question;
- treat `watchtower-core offsec query status` as the main operator-context command once it exposes the locked current-state, environment, and safety-posture fields;
- use rendered overview and tracking docs as faster human fallbacks, not as primary authority;
- do not introduce a pack-specific `query authority` command in v1 unless the host query surface later proves it is worth the extra command family;
- keep command and workflow routing discovery delegated to the shared command and route indexes where those already exist upstream.

## Validation Rules

- every `canonical_path` and `fallback_path` must be repository-relative;
- every `preferred_command` must be a real supported command surface in the same implementation slice;
- `authority.offsec.safety_posture` may use `watchtower-core offsec query status` only if that command exposes the locked `effective_mode`, `interaction_mode`, `environment_type`, `safety_posture_summary`, `confirmation_summary`, `refusal_summary`, and `policy_refs` fields defined in `04_contracts/query_sync_rendered_views_docs_plan.md`;
- the authority map must not duplicate the path index or command index without adding question-specific precedence value;
- the authority map must land in the same slice as the first real challenge, blocker, knowledge, and session indexes so the entries do not point at placeholder artifacts.
