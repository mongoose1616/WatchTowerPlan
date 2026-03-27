# WatchTower CTF Starter Surface Blueprint

## Summary

This support surface turns the preserved README / AGENTS posture into copy-ready offsec starter guidance. It adapts the current `plan` and `oversight` root-template behavior without copying either pack wholesale.

Use `starter_registry_exemplars.md` as the machine-registry companion for the registry artifacts that should govern these human surfaces.

## Carry-Forward Rules

- Use the thin root `README.md` pattern from `plan/.wt/templates/roots/README.md` and `/home/j/WatchTowerOversight/oversight/.wt/templates/roots/README.md`.
- Use the narrow local `AGENTS.md` pattern from `plan/.wt/templates/roots/AGENTS.md` and `/home/j/WatchTowerOversight/oversight/.wt/templates/roots/AGENTS.md`.
- Keep `README.md` navigational and machine-aware rather than trying to restate every contract locally.
- Keep `AGENTS.md` subtree-local and behavior-specific; do not restate repository-wide safety or workflow rules wholesale.
- Treat the starter surfaces as governed outputs backed by `template_catalog`, `documentation_family_registry`, and `human_surface_policy_registry`, not as prose-only conventions.
- Keep the first real registry entries materially aligned with `starter_registry_exemplars.md` unless an offsec-specific divergence is explicit and justified.
- Update starter human surfaces, the registries that govern them, and any rendered visibility companions in the same change set when one depends on the other.

## Required Starter Roots

| Root | Required Surfaces | Why This Root Must Exist Early | Donor Pattern To Follow |
|---|---|---|---|
| `offensive_security/` | `README.md`, `AGENTS.md` | main pack navigation, local instruction overlay, and pack identity anchor | `plan/README.md`, `plan/AGENTS.md`, `oversight/README.md`, `oversight/AGENTS.md` |
| `offensive_security/docs/` | `README.md` | durable doc root navigation before docs families expand | `plan/docs/README.md`, `oversight/docs/README.md` |
| `offensive_security/workflows/` | `README.md`, `AGENTS.md`, `ROUTING_TABLE.md` | workflow discovery, local routing rules, and module inventory entrypoint | `plan/workflows/README.md`, `plan/workflows/AGENTS.md` |
| `offensive_security/docs/commands/core_python/` | `README.md` | namespace command docs must have a clear human entrypoint before authority-map lookup depends on them | `core/docs/commands/core_python/README.md` and pack command-doc roots in donor packs |
| `offensive_security/tracking/` | `README.md` | rendered tracking surfaces need one stable human router | `oversight/tracking/README.md` |
| `offensive_security/python/` | `README.md`, `AGENTS.md` | pack-owned Python boundary and local coding constraints need one rooted explanation | `plan/python/README.md`, `plan/python/AGENTS.md`, `oversight/python/README.md`, `oversight/python/AGENTS.md` |

`offensive_security/docs/AGENTS.md` stays optional unless the docs subtree later needs local behavior that materially differs from the pack root rules.

## Minimum Registry Baseline

These machine-readable pack-local surfaces should exist before claiming documentation or human-surface completeness.

| Surface | Purpose | Minimum Phase |
|---|---|---|
| `offensive_security/.wt/registries/template_catalog.json` | governs README, AGENTS, challenge, notes, recap, and rendered-view templates | `phase.2` |
| `offensive_security/.wt/registries/documentation_family_registry.json` | governs pack-owned documentation families and allowed roots | `phase.2` |
| `offensive_security/.wt/registries/human_surface_policy_registry.json` | governs required README, AGENTS, routing, and rendered-visibility roots | `phase.2` |
| `offensive_security/.wt/registries/rendered_surface_registry.json` | governs pack overview and rendered tracking surfaces | `phase.2` then `phase.3` |
| `offensive_security/.wt/registries/authority_map.json` | maps common operator questions to commands, machine paths, and human paths | `phase.2` then `phase.3` |

## Starter README Shape

Use this shape for the initial offsec root README and adapt it narrowly for `docs/`, `workflows/`, `tracking/`, and `python/` roots.

```md
# `offensive_security`

## Start Here
| Need | Open |
|---|---|
| Current pack status and next action | `offensive_security/tracking/<rendered_surface>.md` |
| Durable guidance and standards | `offensive_security/docs/README.md` |
| Workflow procedures and routing | `offensive_security/workflows/README.md` |
| Python runtime boundary | `offensive_security/python/README.md` |

## Workspace Map
| Area | Role | Use It When |
|---|---|---|
| `offensive_security/ctf/` | challenge workspace root | You are running or reviewing challenge-local work. |
| `offensive_security/knowledge/` | reusable knowledge root | You are promoting or retrieving reusable knowledge. |
| `offensive_security/docs/` | durable guidance root | You need standards, references, or command docs. |
| `offensive_security/workflows/` | routed workflow root | You need workflow procedures, routing, or module ownership. |
| `offensive_security/tracking/` | rendered human tracking root | You need current status without reading raw machine JSON. |
| `offensive_security/python/` | pack-owned Python root | You are editing pack-owned runtime code. |

## Notes
- Start from this README, then move to the matching rendered tracking or workflow surface.
- Treat pack-local machine state under `offensive_security/.wt/**` or challenge-local `.wt_local/**` as authority where the pack contract says so.
- Keep this file thin and navigational; deeper rules belong in standards, workflows, registries, or local AGENTS files.
```

## Starter AGENTS Shape

Use this shape for the offsec root `AGENTS.md` and adapt it only where local behavior actually changes.

```md
# AGENTS.md

## Role
- This file applies to `offensive_security/**`.
- Use it for offsec-domain instructions that narrow the repository-wide rules for challenge work, knowledge work, docs, workflows, tracking, and pack-owned Python behavior.

## Scope
- Applies to `offensive_security/**`.
- Inherit the repository root `AGENTS.md` first.
- More-local `AGENTS.md` files add subtree guidance and must not weaken repository-wide safety or evidence rules.

## Routing Or Behavior Differences
- Use the offsec routing table under `offensive_security/workflows/ROUTING_TABLE.md` for pack-owned workflow selection.
- Reuse shared `core/workflows/modules/` behavior where the pack does not own a different domain rule.

## Local Instructions
- Treat `offensive_security/.wt/**` as pack machine state and `.wt_local/**` as challenge-local machine state.
- Keep durable docs in `offensive_security/docs/`, routed procedures in `offensive_security/workflows/`, rendered trackers in `offensive_security/tracking/`, and pack-owned code in `offensive_security/python/`.
- Keep challenge-specific operational notes in challenge roots and reusable knowledge in `offensive_security/knowledge/`.

## Exclusions Or Constraints
- Do not place durable docs inside `.wt/**` or `.wt_local/**`.
- Do not copy donor-pack retained state or caches into the recipient repo.

## Do
- Keep docs, registries, rendered surfaces, and validators aligned in the same change set when one depends on the other.

## Do Not
- Do not duplicate reusable-core logic into the pack when shared core already owns it.
```

## Root-Specific Adjustments

| Root | README Emphasis | AGENTS Delta |
|---|---|---|
| `offensive_security/docs/` | documentation families, command docs, standards, references | no local AGENTS file unless docs behavior diverges from pack root |
| `offensive_security/workflows/` | routing table, modules, roles, workflow inventory | require local AGENTS guidance about workflow ownership and routing-table alignment |
| `offensive_security/docs/commands/core_python/` | namespace command inventory and command-doc entrypoints | no local AGENTS file by default |
| `offensive_security/tracking/` | rendered human trackers and how to read them | no local AGENTS file by default |
| `offensive_security/python/` | package boundary, runtime modules, tests, and pack-owned code ownership | optional local AGENTS file should narrow coding expectations for pack-owned Python only |

## Registry Starter Expectations

- `template_catalog` should start with README and AGENTS roots plus the challenge, notes, and recap templates locked by the preserved contract.
- `documentation_family_registry` should at minimum cover workflow guidance, command docs, standards, references, rendered tracking, and knowledge families once those roots exist.
- `human_surface_policy_registry` should explicitly declare:
  - the required `README.md` and `AGENTS.md` surfaces for `offensive_security/`;
  - the required `README.md`, `AGENTS.md`, `ROUTING_TABLE.md`, and `modules/README.md` surfaces for `offensive_security/workflows/`;
  - the required `README.md` for `offensive_security/docs/`, `offensive_security/docs/commands/core_python/`, and `offensive_security/tracking/`; and
  - the required `README.md` plus optional or required `AGENTS.md` treatment for `offensive_security/python/`.

## Best-Practice Reminders

- Use rendered visibility surfaces as first-class pack outputs rather than ad hoc notes.
- Keep command docs and command-runtime behavior aligned in the same change set.
- Keep route tables and workflow metadata registry entries aligned in the same change set.
- Use the shared-core capability first, then add pack-owned code only when the behavior is genuinely domain-specific.
- Treat this blueprint as the starter posture only; once the pack owns real runtime code and real docs families, update the governing registries rather than letting the starter files drift.
