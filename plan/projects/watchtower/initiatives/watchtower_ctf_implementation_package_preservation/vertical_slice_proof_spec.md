# WatchTower CTF Vertical Slice Proof Spec

## Summary

This support surface defines the first real Phase 3 proof path. Its purpose is to prevent a vague "runtime started" claim. The first runtime proof is not complete until one real challenge root is created through the real offsec seam, the first machine-record bundle exists, and real query outputs prove the slice end to end.

## Proof Boundary

This is the smallest acceptable Phase 3 runtime proof:

`challenge_intake -> challenge_metadata + notes_metadata + event_stream + artifact_index + challenge_index + offsec query challenges + offsec query artifacts`

The broader first machine-record substrate still lands together:

- `challenge_metadata`
- `notes_metadata`
- `event_stream`
- `artifact_index`
- `graph_index`
- `session_state`
- `environment_context`

But the first proof claim is narrower than the full Phase 3 scope. It proves the pack can create real governed records, refresh the first derived lookup surfaces, and answer the first two high-value pack queries.

## Preconditions

- Phase 1 scaffold and bootstrap are complete and no starter workflow metadata remains trusted.
- Phase 2 schemas, registries, policies, and validators exist for the machine-record bundle used in this slice.
- `ROUTING_TABLE.md`, workflow docs, workflow metadata, and command-doc entrypoints exist for the offsec runtime seam.
- The slice runs on the actual `offensive_security/` pack root in `/home/j/WatchTower`, not through helper-only tests detached from the real pack layout.

## Mandatory Surface Set

| Surface | Expected Path | Why It Must Exist |
|---|---|---|
| challenge root | `offensive_security/ctf/<platform>/<event>/<challenge>/` | proves the slice is pack-root real rather than temporary scratch output |
| challenge metadata | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/challenge_metadata.json` | authoritative challenge identity, path, and lifecycle metadata |
| notes metadata | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/notes_metadata.json` | authoritative reconciliation companion for `notes.md` |
| event stream | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/event_stream.ndjson` | append-only audit trail for the first runtime actions |
| session state | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/session_state.json` | proves requested versus effective mode and current session projection exist |
| environment context | `offensive_security/ctf/<platform>/<event>/<challenge>/.wt_local/environment_context.json` | proves environment type and context are governed, not inferred from narrative |
| artifact index | `offensive_security/.wt/indexes/artifact_index.json` | required for broad artifact lookup and path resolution |
| challenge index | `offensive_security/.wt/indexes/challenge_index.json` | required for `offsec query challenges` |
| command docs | `offensive_security/docs/commands/core_python/` | proves the namespace surfaces are documented before use claims are made |
| workflow docs | `offensive_security/workflows/` | proves `challenge_intake` is governed and routable rather than implicit |

## Required Workflow And Query Behavior

The slice must prove these behaviors in order:

1. A real offsec runtime entrypoint routes or invokes `challenge_intake` on the actual pack root.
2. The challenge root is created or normalized without ad hoc path logic outside the pack contract.
3. `challenge_metadata.json`, `notes_metadata.json`, and `event_stream.ndjson` are written with real governed content.
4. The pack refreshes the derived lookup surfaces needed for the slice, at minimum `artifact_index.json` and `challenge_index.json`.
5. `watchtower-core offsec query challenges --format json` returns the created challenge through the real pack query surface.
6. `watchtower-core offsec query artifacts --format json` returns the relevant artifact or artifacts for that challenge through the real pack query surface.

If the shared-core sync surface keeps the expected namespace pattern, the slice should also prove a real offsec sync target invocation for `challenge-index` or `all`. Confirm the exact command spelling against the generated command docs at implementation time instead of inventing a pack-local alias.

## Required Validation Proof

The slice is not complete without validation proof tied to the real pack settings:

- `uv run watchtower-core pack validate --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
- `uv run watchtower-core validate all --pack-settings-path offensive_security/.wt/manifests/pack_settings.json --format json`
- artifact validation for the newly created governed records when separate targeted validators exist
- command-doc and workflow-doc integrity checks once the first offsec command docs and workflow docs are authored

## Minimum Evidence To Capture

- the exact challenge root used for the proof;
- the produced machine-record paths listed above;
- validation output proving the slice ran against real validators;
- query output showing the challenge in `offsec query challenges`;
- query output showing the relevant artifact rows in `offsec query artifacts`;
- one short note stating whether sync was proven through a dedicated target, `all`, or both; and
- any discrepancy opened during the slice, with explicit note that the slice is not considered clean until the discrepancy is resolved or intentionally carried.

## Failure Conditions

Do not count the slice as passed if any of the following is true:

- the proof uses helper-only fixtures without creating a real offsec challenge root;
- the challenge exists but query surfaces read from placeholders or stale static files;
- event, notes, or challenge metadata are created but not validated;
- query commands exist only in docs or only in tests, but not in the real namespace runtime;
- artifact lookup works only by direct file reads rather than through `artifact_index.json`; or
- the slice omits session or environment context even though the first machine-record bundle is supposed to land together.

## Exit Signal

Phase 3 may claim its first concrete proof only when the slice above passes end to end on the real pack root with real validators, real query output, and no hidden manual repair step between record creation and query visibility.
