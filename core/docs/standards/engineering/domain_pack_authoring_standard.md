---
id: "std.engineering.domain_pack_authoring"
title: "Domain Pack Authoring Standard"
summary: "This standard defines how a hosted domain pack should be structured so it integrates cleanly with reusable core and host composition."
type: "standard"
status: "active"
tags:
  - "standard"
  - "engineering"
  - "domain_pack"
owner: "repository_maintainer"
updated_at: "2026-03-22T22:15:00Z"
audience: "shared"
authority: "authoritative"
---

# Domain Pack Authoring Standard

## Summary
This standard defines how a hosted domain pack should be structured so it integrates cleanly with reusable core and host composition.

## Purpose
Keep hosted packs portable, comprehensible, and validator-friendly by standardizing owned roots, Python harness placement, pack-local docs ownership, and externalization expectations.

## Scope
- Applies to first-party root packs such as `<pack>/` and future domain packs.
- Covers pack-owned docs, workflows, tracking, machine state, and Python harnesses.
- Does not replace the lower-level pack-interface contract or the reusable-core Python boundary standard.

## Use When
- Creating a new hosted pack.
- Refactoring an existing pack toward the core-host-pack model.
- Reviewing whether pack-local code or docs belong in the owning pack or reusable core.

## Related Standards and Sources
- [core_host_pack_python_boundary_standard.md](/core/docs/standards/engineering/core_host_pack_python_boundary_standard.md): defines the reusable core, host, and pack split that every hosted pack must honor.
- [hosted_pack_integration_standard.md](/core/docs/standards/engineering/hosted_pack_integration_standard.md): defines the minimum file set and extension rules contributors should satisfy before treating a pack as integrated.
- [pack_interface_contract_standard.md](/core/docs/standards/data_contracts/pack_interface_contract_standard.md): governs the registry, manifest, and typed integration contracts a hosted pack must publish.
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md): constrains where pack-owned Python code and adjacent workspace artifacts belong.
- [domain_pack_authoring_reference.md](/core/docs/references/domain_pack_authoring_reference.md): provides the worked authoring examples and pack-shape comparisons behind this standard.

## Guidance
- A hosted pack owns its own machine root, durable docs root, workflow root, tracking root, and Python package root.
- Start new packs from `watchtower-core pack scaffold` when working inside a hosted repository, or from `core/docs/templates/pack/` when you need to customize the starter before the first render.
- Keep pack-owned Python narrow and domain-specific.
- Put shared helpers back into `watchtower_core` instead of duplicating them to make them pack-specific.
- Keep pack-owned command docs under the owning pack docs root when the command is pack-specific.
- Publish the pack namespace entry page at `<pack>/docs/commands/core_python/watchtower_core_<namespace>.md` so host introspection and pack validation can resolve the command surface deterministically.
- Keep pack-owned workflow modules under the owning pack workflow root.
- Keep `.wt/` reserved for machine state, manifests, registries, policies, and indexes. Do not put Python source or hand-maintained prose there.
- Build pack-native Python around features and domain flows, not mirrored copies of reusable-core package taxonomy.
- Keep pack contract paths repository-relative and portable. Absolute paths and parent traversal in pack manifests or settings are invalid.
- Publish a pack-owned `python/pyproject.toml` and `python/src/watchtower_<pack>/` package so copy-out portability does not depend on repository-root import tricks.
- Publish typed query and sync runtimes through the pack integration descriptor rather than placeholder hooks or ad hoc tuples.
- Publish non-empty query command and sync target inventories so host inspection and pack validation can fail closed on incomplete pack wiring.
- Use `domain_roots` to name optional pack-specific roots such as `reviews`, `assessments`, or `targets`. Only keep legacy `initiatives_root` or `projects_root` fields when a live pack runtime still depends on them.
- A copied-out pack should require packaging, installation, and declared-path updates only. Hidden repo-local Python path tricks are not allowed.
- Authoring guidance, workflow modules, and standards should be sufficient for pack creation or copy-out; reviewers should not need to reverse-engineer implementation code to determine the required pack shape.
- Scaffold commands should create only pack-owned surfaces.
- Shared host wiring should happen through `watchtower-core pack bootstrap`, which must update shared registry and workspace metadata together and validate the resulting pack contract before leaving the repository mutated unless `--no-sync-workspace` explicitly defers validation until the shared workspace is synced.

## Structure or Data Model
### Expected pack root shape
| Surface | Required Role |
|---|---|
| `<pack>/.wt/**` | Pack machine state and manifests |
| `<pack>/docs/**` | Durable pack-local guidance and command docs |
| `<pack>/workflows/**` | Pack-local workflow modules and routing |
| `<pack>/tracking/**` | Human-facing rendered tracking surfaces |
| `<pack>/python/**` | Pack-native Python package root |
| Optional domain roots | Initiative, project, review, or other pack-specific state containers |

### Python authoring checkpoints
| Checkpoint | Expected Shape |
|---|---|
| Command registration | One integration module plus pack-owned registrars |
| Packaging surface | `python/pyproject.toml` plus `python/src/watchtower_<pack>/` |
| Runtime orchestration | Feature-owned services |
| Validation semantics | Pack-owned only when the rules are truly domain-specific |
| Shared helpers | Move into `watchtower_core` |

## Operationalization
- `Modes`: `documentation`; `workflow`; `runtime`
- `Operational Surfaces`: `core/docs/references/domain_pack_authoring_reference.md`; `core/docs/templates/pack/`; `core/python/src/watchtower_host/cli/pack_family.py`; `core/python/src/watchtower_core/pack_integration/`; `core/control_plane/registries/pack_registry.json`

## Validation
- Reviewers should reject pack roots that mirror reusable-core package trees without a real domain need.
- Reviewers should reject pack-local docs or workflows placed under shared core roots when ownership is pack-specific.
- Reviewers should reject copied-out pack stories that still require repository-specific Python import hacks.
- Reviewers should reject pack authoring guidance that omits the minimum manifest, package, and command-doc surfaces needed to create or externalize a hosted pack.
- Reviewers should reject packs that keep their namespace command docs in shared core docs or omit the required namespace entry page from the pack-owned docs root.
- Reviewers should reject scaffold flows that silently mutate shared host composition surfaces before the new pack package is installable.
- Reviewers should reject bootstrap flows that update only `pack_registry.json` or only `core/python/pyproject.toml` without the companion shared workspace change.

## Change Control
- Update this standard when the repository changes the expected hosted-pack root shape, portability contract, or pack-owned Python guidance.
- Update the companion reference, pack-interface standard, workflow modules, and affected pack READMEs or AGENTS files in the same change set when authoring expectations change materially.

## References
- [domain_pack_authoring_reference.md](/core/docs/references/domain_pack_authoring_reference.md)
- [python_plugin_discovery_reference.md](/core/docs/references/python_plugin_discovery_reference.md)

## Notes
- This standard is intentionally written for future packs as well as current first-party root packs.
- The goal is one repeatable pack model, not one-off repo-specific exceptions.

## Updated At
- `2026-03-22T22:15:00Z`
