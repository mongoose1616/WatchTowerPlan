---
id: "std.engineering.repository_portability"
title: "Repository Portability and Release Sanitization Standard"
summary: "This standard defines how reusable core and hosted packs must be prepared for donor-neutral copy-out, release artifacts, and customer bootstrap."
type: "standard"
status: "active"
tags:
  - "standard"
  - "engineering"
  - "portability"
  - "release"
  - "domain_pack"
owner: "repository_maintainer"
updated_at: "2026-03-28T23:15:00Z"
audience: "shared"
authority: "authoritative"
---

# Repository Portability and Release Sanitization Standard

## Summary
This standard defines how reusable core and hosted packs must be prepared for donor-neutral copy-out, release artifacts, and customer bootstrap.

## Purpose
Keep downstream adoption and customer handoff safe by defining the difference between portable source-owned surfaces and repo-local donor residue. Shared wiring, pack validation, and customer-safe release scrubbing are related, but they are not the same operation.

## Scope
- Applies to shared `core/` source, hosted pack roots, shared workspace metadata, packaged Python artifacts, engineering repo-to-repo extracts, and customer/bootstrap deliverables.
- Covers engineering shared-core extract, core-only bootstrap, core-plus-selected-pack bootstrap, pack-only bundle handoff, and release sanitization of donor history, test surfaces, and local runtime residue.
- Does not replace the lower-level pack-interface schemas or the host-pack bootstrap command contract.

## Use When
- Preparing `core/` or one or more hosted packs for copy-out into another repository.
- Reviewing whether a repo snapshot, package artifact, or bootstrap bundle is safe to hand to a customer or consuming repository.
- Reviewing whether a shared-core extract is suitable for engineering reuse in another repository before that repository bootstraps its own hosted pack.
- Removing donor-specific hosted-pack wiring, repo-local history, or internal-only validation surfaces before release.

## Related Standards and Sources
- [repository_scope.md](/core/docs/foundations/repository_scope.md): defines the current ownership boundary between shared core, hosted packs, and future consuming repositories.
- [domain_pack_authoring_standard.md](/core/docs/standards/engineering/domain_pack_authoring_standard.md): defines the pack-owned root shape that must remain portable.
- [hosted_pack_integration_standard.md](/core/docs/standards/engineering/hosted_pack_integration_standard.md): defines the minimum shared and pack-owned integration surfaces that portability work must preserve.
- [core_host_pack_python_boundary_standard.md](/core/docs/standards/engineering/core_host_pack_python_boundary_standard.md): constrains the reusable-core, host, and pack-native Python split that must remain donor-neutral.
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md): constrains workspace metadata, editable installs, tests, and generated-artifact boundaries for portable Python delivery.
- [pack_interface_contract_standard.md](/core/docs/standards/data_contracts/pack_interface_contract_standard.md): governs the machine-readable hosted-pack contract that still must validate after any portability scrub.
- [watchtower_core_pack_bootstrap.md](/core/docs/commands/core_python/watchtower_core_pack_bootstrap.md): operational command contract for reconciling the selected hosted-pack set into the shared registry and workspace metadata.
- [watchtower_core_pack_extract_core.md](/core/docs/commands/core_python/watchtower_core_pack_extract_core.md): operational command contract for staging a donor-neutral shared-core engineering extract.
- [watchtower_core_pack_export.md](/core/docs/commands/core_python/watchtower_core_pack_export.md): operational command contract for staging a curated customer/bootstrap export and validating the staged result.
- [customer_release_and_bootstrap_standard.md](/core/docs/standards/operations/customer_release_and_bootstrap_standard.md): operational checklist for sequencing validation, export, and recipient bootstrap guidance.

## Guidance
- Treat portability as an allowlisted source-transfer contract. A raw repository checkout, raw git archive, or default build artifact is not automatically a portable customer deliverable.
- Distinguish the operating modes explicitly:
  - Internal repository state for ongoing engineering work.
  - Engineering shared-core extract for repo-to-repo refresh when the recipient still needs reusable-core tests and shared engineering surfaces.
  - Core-only bootstrap output for a consuming repository that has not selected a hosted pack yet.
  - Core-plus-selected-pack bootstrap output for a consuming repository that intentionally carries one or more hosted packs.
  - Pack-only bundle output for additive handoff into a compatible consuming repository that already has shared core or will receive it separately.
- `watchtower-core pack extract-core --output-root <path> ...` is the preferred donor-side path for engineering repo-to-repo `core/` refresh. It stages shared `core/` plus the minimal portable root shell, strips donor hosted-pack wiring, preserves shared engineering surfaces such as `core/python/tests/**`, and validates the staged result against the engineering shared-core portability contract.
- Core-only bootstrap may retain shared `core/` source and root routing material, but it must not leave shared registry, workspace, or discovery metadata pointing at omitted donor packs.
- Core-plus-selected-pack bootstrap may retain only the selected pack roots plus the shared metadata updated to exactly that pack set.
- Pack-only bundle output may retain only the selected pack roots. It must not include shared `core/`, and the recipient must run `watchtower-core pack bootstrap` after copying the bundle into a compatible core repository.
- `watchtower-core pack bootstrap --replace-hosted-packs --write` reconciles the selected pack set into the shared hosted-pack registry, shared `core/python` workspace metadata, and shared discovery indexes. It does not by itself purge donor records, tests, fixtures, internal assessments, or customer-release artifacts.
- Treat `watchtower-core pack bootstrap --replace-hosted-packs --write --sync-extra dev` as the normal recipient-side follow-on after copying an engineering shared-core extract into place, unless the recipient intentionally defers workspace sync.
- `watchtower-core pack export --output-root <path> ...` is the preferred staged handoff path because it copies only allowlisted source roots, scrubs default customer-release exclusions, reconciles the staged shared pack set when shared core is present, and then validates the staged output.
- Follow the customer release and bootstrap checklist when the goal is a real handoff rather than only a local portability diagnosis. The normal sequence is broad repo validation, explicit schema-definition checks when needed, then a fresh staged export.
- Treat portability validation of an actively used workspace as diagnostic, not as a release substitute. Working repositories can accumulate fresh telemetry, caches, or runtime residue after bootstrap or validation runs; the final customer/bootstrap artifact should come from a fresh `watchtower-core pack export` pass.
- Exclude the following families from customer release and customer bootstrap by default unless the recipient explicitly needs them:
  - Retained governed history under `core/control_plane/records/**`, including migrations, release records, purge history, and validation evidence.
  - Example, demo, and fixture material that exists only to prove schemas, validation, or traceability behavior, including shared acceptance-contract examples, their acceptance-linked traceability joins, and traceability entries that still point at omitted pack or planning surfaces outside the staged roots.
  - Local environments, caches, build outputs, editable-install residue, and other machine-local developer artifacts.
  - Pack-local runtime outputs such as `<pack>/.wt/runtime/**`, telemetry sinks, or other ephemeral machine state.
  - Shared and pack-owned test trees plus pack-owned `testing/` helper modules that exist only for internal validation. Shared reusable-core tests may remain in engineering shared-core extracts, but not in customer-safe bundle exports.
  - Donor project maps, donor repository references, internal comparison or assessment closeout references, and any content that leaks machine-local absolute filesystem paths.
  - Hosted pack roots that are not part of the selected recipient pack set.
- Customer-facing docs, manifests, and registries must use repository-relative paths or neutral placeholders. Filesystem-absolute donor checkout paths are invalid portability input.
- When retained validation evidence is excluded, the paired shared acceptance-contract examples and acceptance-linked traceability entries must be excluded too. Any remaining traceability entries in a repository bundle must point only at shared `core/` or the selected pack roots. Portable bundles may therefore carry an empty `core/control_plane/indexes/traceability/traceability_index.json` when no live portable trace lineage remains.
- Shared core docs and metadata may mention the current internal pack as an example, but they must not make that pack look like a consuming-repository invariant.
- Treat packaged outputs as curated deliverables. Wheels, sdists, starter bundles, and repo-copy flows may all need different inclusion rules; none should silently inherit internal-only test or history surfaces.
- When donor-governance history is intentionally retained in the source repository, document it as internal retained history rather than implying that it belongs in copied repositories or customer bootstrap bundles.

## Structure or Data Model
### Portable handoff modes
| Mode | Allowed Surfaces | Required Scrub |
|---|---|---|
| Internal repository state | Full repository, including retained records and internal validation surfaces | None beyond normal repo hygiene |
| Engineering shared-core extract | Shared `core/` source plus the minimal portable root shell, including reusable-core tests and portable shared examples | Remove donor hosted-pack registry and workspace assumptions, donor-only retained history, donor-only trace lineage, donor pack roots, and stale workspace lockfiles |
| Core-only bootstrap | Shared `core/` source plus root routing docs needed for navigation | Remove hosted-pack registry and workspace assumptions for omitted packs; exclude donor pack roots and internal-only surfaces |
| Core-plus-selected-pack bootstrap | Shared `core/` source plus only the selected pack roots | Reconcile shared registry, workspace, and discovery surfaces to the selected pack set; exclude donor-only history and internal-only surfaces |
| Pack-only bundle | Only the selected pack roots | Exclude shared `core/`, retained history, internal-only surfaces, and omitted pack roots; bootstrap into a compatible core repository after copy |

### Default customer-release exclusions
| Category | Examples |
|---|---|
| Retained history | `core/control_plane/records/**` |
| Test and fixture surfaces | `core/python/tests/**`, `<pack>/python/tests/**`, fixture packs, `watchtower_<pack>.testing` |
| Developer-machine residue | `.venv/`, `__pycache__/`, `.pytest_cache/`, build directories, wheels, editable-install metadata |
| Ephemeral pack machine state | `<pack>/.wt/runtime/**`, telemetry output, transient runtime sinks |
| Donor-only narrative | project repository maps, donor assessments, absolute local checkout paths |
| Omitted hosted packs | any pack root, docs root, workflow root, tracking root, or registry entry outside the selected pack set |

## Operationalization
- `Modes`: `documentation`; `release`; `bootstrap`; `artifact`
- `Operational Surfaces`: `core/docs/foundations/repository_scope.md`; `core/docs/standards/engineering/domain_pack_authoring_standard.md`; `core/docs/standards/engineering/hosted_pack_integration_standard.md`; `core/docs/standards/engineering/python_workspace_standard.md`; `core/docs/commands/core_python/watchtower_core_pack_bootstrap.md`; `core/docs/commands/core_python/watchtower_core_pack_extract_core.md`; `core/docs/commands/core_python/watchtower_core_pack_export.md`; `core/control_plane/registries/pack_registry.json`; `core/python/pyproject.toml`

## Validation
- Reviewers should reject any customer-ready claim built from a raw repository snapshot without an explicit inclusion contract.
- Reviewers should reject shared registry, workspace, or discovery metadata that still points at omitted donor packs.
- Reviewers should reject release bundles that include retained governed history, tests, fixture packs, pack-local runtime outputs, or developer-machine residue unless the release contract explicitly calls for them.
- Reviewers should reject docs, manifests, or registries that leak absolute filesystem paths, donor-only repository names, or internal assessment closeout references into portable output.
- Reviewers should reject package artifacts that expose repo-local tests or pack-owned `testing/` helpers as installed runtime surface by default.
- Reviewers should reject bootstrap guidance that treats shared pack wiring as a substitute for customer-release sanitization.
- Reviewers should reject engineering repo-to-repo guidance that relies on customer-safe bundle export when the recipient still needs reusable-core tests and shared engineering surfaces retained.

## Change Control
- Update this standard when the repository changes the portable export contract, default customer-release exclusions, or the relationship between pack bootstrap and release scrub.
- Update the companion pack-authoring, hosted-pack integration, Python workspace, root README, and bootstrap command docs in the same change set when portability expectations change materially.

## References
- [repository_scope.md](/core/docs/foundations/repository_scope.md)
- [domain_pack_authoring_standard.md](/core/docs/standards/engineering/domain_pack_authoring_standard.md)
- [hosted_pack_integration_standard.md](/core/docs/standards/engineering/hosted_pack_integration_standard.md)
- [python_workspace_standard.md](/core/docs/standards/engineering/python_workspace_standard.md)

## Updated At
- `2026-03-28T23:15:00Z`
