# Executive Summary

## Objective

Build a planning package that is strong enough for a follow-on Codex agent to implement the first WatchTower offensive-security / CTF hosted pack phase by phase without re-deriving baseline decisions.

## Implementation Judgment

- Current shared `watchtower_core` and `watchtower_host` are strong enough to support the first CTF pack now.
- The practical start point is the verified scaffold baseline from `STEP1_PACK_SCAFFOLD_SPEC_v1.md`, not the idealized slug values shown in `STEP1_FINAL_v3.md`.
- CTF lifecycle, challenge artifacts, knowledge promotion, environment adapters, safety policy, and pack-local semantic validation remain pack-owned work.
- Shared governance surfaces now exist upstream and should be adopted where the pack needs the full typed `PackContext`.
- `workflow_catalog` is a locked post-v1 deferral, not a baseline requirement for the first implementation.

## Non-Negotiable Baseline

| Surface | Value |
|---|---|
| `pack_root` | `offensive_security` |
| `workspace_root` | `offensive_security/` |
| `pack_slug` | `offensivesecurity` |
| `pack_id` | `pack.offensivesecurity` |
| `command_namespace` | `offsec` |
| `domain_roots` | `ctf`, `knowledge` |
| canonical challenge path | `offensive_security/ctf/<platform>/<event>/<challenge>/` |

## Destination

- Donor shared core and source contract: `/home/j/WatchTowerPlan/core`
- Working hosted-pack references: `/home/j/WatchTowerPlan/plan`, `/home/j/WatchTowerOversight/oversight`
- Final destination repository: `/home/j/WatchTower`
- Target repository state as of `2026-03-26`: empty except for `.git`

## Phase Sequence

1. Phase 0: Shared contract adoption
2. Phase 1: Scaffold and integrate the pack
3. Phase 2: Author the pack machine contract
4. Phase 3: Build the CTF runtime
5. Phase 4: Build the domain artifacts
6. Phase 5: Build knowledge, promotion, and retrieval
7. Phase 6: Build environment adapters and safety controls
8. Phase 7: Release and portability proof

## Primary Risks

- Step 1 document history contains superseded topology and identifier assumptions that must not leak into the final package.
- Shared core evolved after `STEP1_FINAL_v3.md`; live repo truth must win when current contract surfaces disagree with the workbook.
- The planning package must keep human-readable docs and JSON indexes synchronized or it becomes misleading immediately.
