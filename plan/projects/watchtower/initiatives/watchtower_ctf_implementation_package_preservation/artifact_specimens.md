# WatchTower CTF Artifact Specimens

## Summary

This support surface provides example-filled specimens for the first governed offsec records and the first two registry surfaces engineers will need almost immediately. The goal is to remove avoidable implementation guesswork, not to create a second schema authority. When a final schema or validator disagrees with a specimen wrapper field, follow the schema and keep the specimen updated in the same change set.

## Example Scenario

These specimens use one intentionally small placeholder-friendly challenge root:

- challenge root: `offensive_security/ctf/unknown_platform/unknown_event/warmup_echo/`
- challenge id: `challenge.ctf.unknown_platform.unknown_event.warmup_echo`
- session id: `session.ctf.unknown_platform.unknown_event.warmup_echo.001`

The example keeps `unknown_platform` and `unknown_event` on purpose so the preserved v1 placeholder-segment rule stays visible.

## `challenge_metadata.json` Specimen

Path:

- `offensive_security/ctf/unknown_platform/unknown_event/warmup_echo/.wt_local/challenge_metadata.json`

```json
{
  "challenge_id": "challenge.ctf.unknown_platform.unknown_event.warmup_echo",
  "challenge_slug": "warmup_echo",
  "canonical_path": "offensive_security/ctf/unknown_platform/unknown_event/warmup_echo/",
  "challenge_path": "offensive_security/ctf/unknown_platform/unknown_event/warmup_echo/challenge.md",
  "notes_path": "offensive_security/ctf/unknown_platform/unknown_event/warmup_echo/notes.md",
  "source": {
    "summary": "Warmup Echo starter challenge imported from a local challenge brief.",
    "platform": "unknown_platform",
    "event": "unknown_event",
    "type": "challenge_prompt",
    "ref": "challenge-brief-local"
  },
  "status": "active",
  "created_at_utc": "2026-03-28T00:00:00Z",
  "updated_at_utc": "2026-03-28T00:03:14Z",
  "platform_slug": "unknown_platform",
  "event_slug": "unknown_event",
  "display_title": "Warmup Echo",
  "current_session_id": "session.ctf.unknown_platform.unknown_event.warmup_echo.001",
  "active_blocker_count": 0,
  "unresolved_discrepancy_count": 0,
  "last_activity_at_utc": "2026-03-28T00:03:14Z",
  "rendered_view_path": "offensive_security/tracking/challenge_tracking.md"
}
```

## `notes_metadata.json` Specimen

Path:

- `offensive_security/ctf/unknown_platform/unknown_event/warmup_echo/.wt_local/notes_metadata.json`

```json
{
  "challenge_id": "challenge.ctf.unknown_platform.unknown_event.warmup_echo",
  "notes_path": "offensive_security/ctf/unknown_platform/unknown_event/warmup_echo/notes.md",
  "reconciliation_state": "in_sync",
  "updated_at_utc": "2026-03-28T00:05:02Z",
  "unresolved_blocker_count": 0,
  "unresolved_discrepancy_count": 0,
  "content_checksum": {
    "algorithm": "sha256",
    "value": "4d2b4d984aa4f4de7390cf7f6fb8573fe4b8c6c6d050511ec37ec96d1c5a9b24"
  },
  "last_user_edit_at_utc": "2026-03-28T00:04:11Z",
  "last_agent_edit_at_utc": "2026-03-28T00:05:02Z",
  "last_reconciled_at_utc": "2026-03-28T00:05:02Z",
  "current_session_id": "session.ctf.unknown_platform.unknown_event.warmup_echo.001",
  "last_editor_actor_ref": "actor.repository_maintainer",
  "visible_summary_present": true
}
```

## `environment_context.json` Specimen

Path:

- `offensive_security/ctf/unknown_platform/unknown_event/warmup_echo/.wt_local/environment_context.json`

The preserved package locks the nested `environment_context` shape exactly. The outer wrapper below is representative and should be aligned with the final offsec schema when authored.

```json
{
  "challenge_id": "challenge.ctf.unknown_platform.unknown_event.warmup_echo",
  "session_id": "session.ctf.unknown_platform.unknown_event.warmup_echo.001",
  "updated_at_utc": "2026-03-28T00:01:12Z",
  "environment_context": {
    "summary": "Local Linux shell with normal file-write access and no outbound internet for the challenge workspace.",
    "type": "local",
    "os_family": "linux",
    "shell": "bash",
    "runtime": "python311",
    "execution_location": "workstation",
    "transport": "local_process",
    "constraints": [
      "no_outbound_internet"
    ],
    "capabilities": [
      "bash_available",
      "python_available",
      "artifact_capture_available",
      "checksum_available",
      "can_execute_locally"
    ],
    "user_controls_execution": true,
    "agent_can_execute": true,
    "requires_human_transfer": false
  }
}
```

## `session_state.json` Specimen

Path:

- `offensive_security/ctf/unknown_platform/unknown_event/warmup_echo/.wt_local/session_state.json`

```json
{
  "session_id": "session.ctf.unknown_platform.unknown_event.warmup_echo.001",
  "challenge_id": "challenge.ctf.unknown_platform.unknown_event.warmup_echo",
  "status": "active",
  "requested_mode": "assistant",
  "effective_mode": "assistant",
  "interaction_mode": "guided",
  "environment_context_ref": "offensive_security/ctf/unknown_platform/unknown_event/warmup_echo/.wt_local/environment_context.json",
  "started_at_utc": "2026-03-28T00:00:30Z",
  "last_activity_at_utc": "2026-03-28T00:05:15Z",
  "current_workflow_id": "workflow.offensivesecurity.challenge_intake",
  "current_route_id": "route.offsec.challenge_intake",
  "current_summary": "Challenge root created, initial notes started, and first metadata records written.",
  "recent_command_refs": [
    "event.ctf.unknown_platform.unknown_event.warmup_echo.command_001"
  ],
  "recent_evidence_refs": [
    "artifact.ctf.unknown_platform.unknown_event.warmup_echo.command_output_001"
  ],
  "handoff_ready": false,
  "operator_actor_ref": "actor.repository_maintainer"
}
```

## `event_stream.ndjson` Specimen

Path:

- `offensive_security/ctf/unknown_platform/unknown_event/warmup_echo/.wt_local/event_stream.ndjson`

```json
{"event_id":"event.ctf.unknown_platform.unknown_event.warmup_echo.challenge_created_001","event_type":"challenge_created","timestamp_utc":"2026-03-28T00:00:31Z","challenge_id":"challenge.ctf.unknown_platform.unknown_event.warmup_echo","actor_ref":"actor.repository_maintainer","workflow_id":"workflow.offensivesecurity.challenge_intake","route_id":"route.offsec.challenge_intake","payload":{"summary":"Created challenge root and initialized core machine records."}}
{"event_id":"event.ctf.unknown_platform.unknown_event.warmup_echo.session_started_001","event_type":"session_started","timestamp_utc":"2026-03-28T00:00:32Z","challenge_id":"challenge.ctf.unknown_platform.unknown_event.warmup_echo","session_id":"session.ctf.unknown_platform.unknown_event.warmup_echo.001","requested_mode":"assistant","effective_mode":"assistant","interaction_mode":"guided","payload":{"summary":"Started first guided execution session."}}
{"event_id":"event.ctf.unknown_platform.unknown_event.warmup_echo.command_001","event_type":"command_activity","timestamp_utc":"2026-03-28T00:04:58Z","challenge_id":"challenge.ctf.unknown_platform.unknown_event.warmup_echo","session_id":"session.ctf.unknown_platform.unknown_event.warmup_echo.001","artifact_id":"artifact.ctf.unknown_platform.unknown_event.warmup_echo.command_output_001","artifact_family":"evidence_artifact","payload":{"stage":"executed","execution_context_type":"local","command_summary":"Ran strings against provided sample artifact.","exit_code":0,"related_evidence_refs":["artifact.ctf.unknown_platform.unknown_event.warmup_echo.command_output_001"],"safety_classification":"read_only"}}
```

## `artifact_index.json` Specimen

Path:

- `offensive_security/.wt/indexes/artifact_index.json`

The wrapper shape below follows the live pack artifact-index posture used by `plan`. The important locked contract is the entry field set.

```json
{
  "$schema": "urn:watchtower:schema:interfaces:packs:artifact-index:v1",
  "surface_name": "artifact_index",
  "contract_version": "v1",
  "description": "Cross-family artifact lookup for the offensive-security pack.",
  "updated_at": "2026-03-28T00:05:30Z",
  "artifacts": [
    {
      "artifact_id": "artifact.ctf.unknown_platform.unknown_event.warmup_echo.challenge_metadata",
      "artifact_family": "challenge_metadata",
      "path": "offensive_security/ctf/unknown_platform/unknown_event/warmup_echo/.wt_local/challenge_metadata.json",
      "pack": "pack.offensivesecurity",
      "subdomain": "ctf",
      "challenge_id": "challenge.ctf.unknown_platform.unknown_event.warmup_echo",
      "status": "active",
      "authoritative": true,
      "hidden": true,
      "derived": false,
      "created_at_utc": "2026-03-28T00:00:31Z",
      "updated_at_utc": "2026-03-28T00:03:14Z",
      "title": "Warmup Echo Challenge Metadata",
      "summary": "Machine-governed identity and lifecycle metadata for the Warmup Echo challenge.",
      "source_type": "challenge_prompt",
      "rendered_view_path": "offensive_security/tracking/challenge_tracking.md"
    },
    {
      "artifact_id": "artifact.ctf.unknown_platform.unknown_event.warmup_echo.command_output_001",
      "artifact_family": "evidence_artifact",
      "path": "offensive_security/ctf/unknown_platform/unknown_event/warmup_echo/artifacts/strings_output.txt",
      "pack": "pack.offensivesecurity",
      "subdomain": "ctf",
      "challenge_id": "challenge.ctf.unknown_platform.unknown_event.warmup_echo",
      "session_id": "session.ctf.unknown_platform.unknown_event.warmup_echo.001",
      "status": "active",
      "authoritative": true,
      "hidden": false,
      "derived": false,
      "created_at_utc": "2026-03-28T00:04:58Z",
      "updated_at_utc": "2026-03-28T00:04:58Z",
      "title": "Warmup Echo strings output",
      "summary": "Read-only command output captured during initial intake.",
      "trust_state": "source_attested",
      "verification_status": "inspected",
      "parent_artifact_id": "artifact.ctf.unknown_platform.unknown_event.warmup_echo.challenge_metadata",
      "related_artifact_ids": [
        "artifact.ctf.unknown_platform.unknown_event.warmup_echo.challenge_metadata"
      ]
    }
  ]
}
```

## Minimal `authority_map.json` Specimen

Path:

- `offensive_security/.wt/registries/authority_map.json`

This specimen follows the real shared authority-map schema.

```json
{
  "$schema": "urn:watchtower:schema:artifacts:registries:authority-map:v1",
  "id": "registry.authority_map",
  "title": "Offensive-Security Authority Map",
  "status": "active",
  "entries": [
    {
      "question_id": "authority.offsec.challenge_lookup",
      "domain": "planning",
      "question": "Which challenges exist and what state is each challenge in?",
      "status": "active",
      "artifact_kind": "challenge_index",
      "canonical_path": "offensive_security/.wt/indexes/challenge_index.json",
      "preferred_command": "watchtower-core offsec query challenges",
      "preferred_human_path": "offensive_security/tracking/challenge_tracking.md",
      "status_fields": [
        "status",
        "closeout_outcome"
      ],
      "fallback_paths": [
        "offensive_security/offensivesecurity_overview.md",
        "offensive_security/.wt/indexes/artifact_index.json",
        "offensive_security/ctf/"
      ],
      "aliases": [
        "challenge lookup",
        "challenge state",
        "which challenge am I in"
      ],
      "notes": "Use the challenge index first instead of opening challenge-local state directly."
    }
  ]
}
```

## Minimal `query_family_registry.json` Specimen

Path:

- `offensive_security/.wt/registries/query_family_registry.json`

This registry does not currently have a shared published schema in the donor repo. The specimen below is therefore a pack-local draft shape aligned to the preserved contract rather than a claimed shared-schema artifact.

```jsonc
{
  "$schema": "<pack-owned query-family-registry schema urn>",
  "id": "registry.query_family",
  "title": "Offensive-Security Query Family Registry",
  "status": "active",
  "entries": [
    {
      "family_id": "query_family.challenges",
      "entry_status": "active",
      "exposure_mode": "curated",
      "backing_surface": "offensive_security/.wt/indexes/challenge_index.json",
      "output_contract_ref": "offensive_security/docs/commands/core_python/query_families.md#challenges",
      "command_doc_path": "offensive_security/docs/commands/core_python/watchtower_core_offsec_query_challenges.md",
      "curated_command_name": "challenges",
      "supports_graph_expansion": false,
      "supports_generic_family_query": false
    },
    {
      "family_id": "query_family.artifacts",
      "entry_status": "active",
      "exposure_mode": "curated",
      "backing_surface": "offensive_security/.wt/indexes/artifact_index.json",
      "output_contract_ref": "offensive_security/docs/commands/core_python/query_families.md#artifacts",
      "command_doc_path": "offensive_security/docs/commands/core_python/watchtower_core_offsec_query_artifacts.md",
      "curated_command_name": "artifacts",
      "supports_graph_expansion": true,
      "supports_generic_family_query": true
    }
  ]
}
```

## Cross-Specimen Checks

- Every path is repository-relative and POSIX-style.
- `challenge_id` is stable across challenge-local records, event stream, and index rows.
- `session_state.environment_context_ref` points to the actual challenge-local `environment_context.json`.
- `event_stream` uses compact payloads and keeps raw command output in evidence artifacts rather than inline payload blobs.
- `artifact_index` is rich enough to answer lookup questions without opening raw files first.
- `authority_map` points to implemented commands and real rendered surfaces, not placeholders.
- `query_family_registry` stays aligned with actual command-doc pages and backing surfaces in the same change set.
