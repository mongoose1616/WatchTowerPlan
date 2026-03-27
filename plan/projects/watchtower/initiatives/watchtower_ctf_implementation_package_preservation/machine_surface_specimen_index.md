# WatchTower CTF Machine Surface Specimen Index

## Summary

This support surface lists the first expected offsec `.wt/` and `.wt_local/` machine artifacts, when they first matter, and which support docs already show specimen shapes for them. Use it during Phase 2 and Phase 3 to avoid losing track of which surfaces are authoritative, derived, or rendered.

## Challenge-Local Authoritative Surfaces

| Surface | Canonical Path | First Phase | Authority Class | Specimen / Contract Anchor |
|---|---|---|---|---|
| challenge metadata | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/challenge_metadata.json` | `phase.2` then proven in `phase.3` | authoritative | `artifact_specimens.md`, `implementation_slice.md` |
| notes metadata | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/notes_metadata.json` | `phase.2` then proven in `phase.3` | authoritative companion | `artifact_specimens.md`, `implementation_slice.md` |
| event stream | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/event_stream.ndjson` | `phase.2` then proven in `phase.3` | authoritative append-only audit | `artifact_specimens.md`, `implementation_slice.md` |
| session state | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/session_state.json` | `phase.2` then proven in `phase.3` | authoritative current session projection | `artifact_specimens.md`, `implementation_slice.md` |
| environment context | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/environment_context.json` | `phase.2` then proven in `phase.3` | authoritative execution-context record | `artifact_specimens.md`, `implementation_slice.md` |
| evidence inventory | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/evidence/artifacts.json` | `phase.4` | authoritative evidence metadata collection | `phase_output_manifest.md`, `implementation_slice.md` |
| discrepancy record | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/discrepancies/<discrepancy_id>.json` | `phase.4` | authoritative discrepancy state | `implementation_slice.md` |
| closeout record | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/closeout_record.json` | `phase.4` | authoritative closeout outcome | `implementation_slice.md`, `promotion_extraction_map.md` |
| extraction output | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/extractions/<extraction_id>.json` | `phase.4` then consumed in `phase.5` | authoritative extraction history | `promotion_extraction_map.md`, `implementation_slice.md` |

## Pack-Level Authoritative Registries And Policies

| Surface | Canonical Path | First Phase | Authority Class | Specimen / Contract Anchor |
|---|---|---|---|---|
| template catalog | `offensive_security/.wt/registries/template_catalog.json` | `phase.2` | authoritative registry | `starter_registry_exemplars.md` |
| documentation family registry | `offensive_security/.wt/registries/documentation_family_registry.json` | `phase.2` | authoritative registry | `starter_registry_exemplars.md` |
| human surface policy registry | `offensive_security/.wt/registries/human_surface_policy_registry.json` | `phase.2` | authoritative registry | `starter_registry_exemplars.md` |
| authority map | `offensive_security/.wt/registries/authority_map.json` | `phase.2` then used in `phase.3` | authoritative registry | `starter_registry_exemplars.md`, `artifact_specimens.md` |
| query family registry | `offensive_security/.wt/registries/query_family_registry.json` | `phase.2` then used in `phase.3` | authoritative registry | `artifact_specimens.md`, `implementation_slice.md` |
| rendered surface registry | `offensive_security/.wt/registries/rendered_surface_registry.json` | `phase.2` then used in `phase.3` | authoritative registry | `starter_registry_exemplars.md` |
| event type registry | `offensive_security/.wt/registries/event_type_registry.json` | `phase.2` | authoritative registry | `implementation_slice.md` |
| promotion policy registry | `offensive_security/.wt/registries/promotion_policy_registry.json` | `phase.5` | authoritative registry | `promotion_extraction_map.md`, `implementation_slice.md` |
| relation type registry | `offensive_security/.wt/registries/relation_type_registry.json` | `phase.5` | authoritative registry | `promotion_extraction_map.md`, `implementation_slice.md` |
| safety confirmation matrix | `offensive_security/.wt/policies/safety_confirmation_matrix.json` | `phase.6` | authoritative policy | `implementation_slice.md`, `phase_test_matrix.md` |

## Pack-Level Derived Indexes And Rendered Surfaces

| Surface | Canonical Path | First Phase | Authority Class | Specimen / Contract Anchor |
|---|---|---|---|---|
| artifact index | `offensive_security/.wt/indexes/artifact_index.json` | `phase.2` then proven in `phase.3` | derived authoritative lookup | `artifact_specimens.md`, `implementation_slice.md` |
| challenge index | `offensive_security/.wt/indexes/challenge_index.json` | `phase.3` | derived authoritative lookup | `artifact_specimens.md`, `vertical_slice_proof_spec.md` |
| session index | `offensive_security/.wt/indexes/session_index.json` | `phase.3` | derived authoritative lookup | `implementation_slice.md` |
| blocker index | `offensive_security/.wt/indexes/blocker_index.json` | `phase.3` or `phase.4` | derived authoritative lookup | `implementation_slice.md` |
| graph index | `offensive_security/.wt/indexes/graph_index.json` | `phase.2` then query-visible in `phase.3` or later | derived traversal index | `vertical_slice_proof_spec.md`, `implementation_slice.md` |
| knowledge index | `offensive_security/.wt/indexes/knowledge_index.json` | `phase.5` | derived authoritative lookup | `promotion_extraction_map.md`, `implementation_slice.md` |
| overview surface | `offensive_security/offensivesecurity_overview.md` | `phase.3` | rendered | `starter_registry_exemplars.md`, `implementation_slice.md` |
| challenge tracking | `offensive_security/tracking/challenge_tracking.md` | `phase.3` | rendered | `starter_registry_exemplars.md`, `implementation_slice.md` |

## Working Rule

- If a surface is listed as authoritative, its governed record or registry is the source of truth and rendered or indexed companions must follow it.
- If a surface is listed as derived, the implementation must define how it is rebuilt and validated before operators rely on it.
- If a surface is listed as rendered, it should remain a human aid backed by authoritative machine state instead of becoming a hand-maintained second source of truth.
