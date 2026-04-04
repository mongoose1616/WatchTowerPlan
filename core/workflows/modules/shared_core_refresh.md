# Shared Core Refresh Workflow

## Purpose
Use this workflow to refresh shared `core/` from one WatchTower-style repository into another repository through the engineering shared-core extract path instead of raw copy or customer-safe bundle export.

## Use When
- A request asks to refresh, resync, or reimport `core/` from another repository such as `WatchTowerPlan`.
- A repository needs the current shared core plus donor-pack scrub so a recipient pack can be bootstrapped cleanly afterward.
- A task is specifically about engineering repo-to-repo shared-core reuse rather than customer-safe release handoff.
- The main risk is brittle manual copy, stale donor hosted-pack wiring, or leftover donor-only records and trace lineage after copy.

## Inputs
- Donor repository root and recipient repository root
- Active recipient pack settings path and pack slug
- Current shared portability, bootstrap, and hosted-pack integration standards
- Any known donor-only retained history, shared acceptance examples, or command-doc drift that could block a clean extract
- Any known shared-core tests, docs, or workflow assertions that still name donor-pack validators, workflows, rendered surfaces, or tracking files instead of deriving them from the active pack contract

## Additional Files to Load
- [repository_portability_standard.md](/core/docs/standards/engineering/repository_portability_standard.md): defines the difference between engineering shared-core extract and customer-safe export.
- [hosted_pack_integration_standard.md](/core/docs/standards/engineering/hosted_pack_integration_standard.md): defines the shared hosted-pack registry and workspace contract the recipient must satisfy after copy.
- [watchtower_core_pack_extract_core.md](/core/docs/commands/core_python/watchtower_core_pack_extract_core.md): donor-side command contract for staging the engineering shared-core extract.
- [watchtower_core_pack_bootstrap.md](/core/docs/commands/core_python/watchtower_core_pack_bootstrap.md): recipient-side command contract for reloading the recipient pack after copy.
- [watchtower_core_validate_portability.md](/core/docs/commands/core_python/watchtower_core_validate_portability.md): validator contract for engineering shared-core readiness and customer-safe export checks.

## Workflow
1. Confirm donor and recipient roles.
   - Identify which repository is the shared-core donor and which repository is the recipient.
   - Confirm whether the request allows upstream donor fixes. If the donor shared core is the real source of brittleness, fix the donor shared core first instead of hard-coding recipient-side cleanup.
2. Normalize donor shared-core portability surfaces.
   - Check whether shared docs, shared acceptance examples, shared validation evidence, and shared traceability lineage are truly donor-neutral.
   - Treat shared `core/python/tests/**`, shared command docs, and shared workflow docs as part of the portable engineering contract. When they need pack-aware expectations, derive them from activated `pack_settings.json`, declared surfaces, and merged registries instead of hard-coding donor-pack IDs or donor-pack path names.
   - Scan shared-core tests for direct live-pack-root assumptions such as `REPO_ROOT / "plan"`, raw copies from one donor pack root, or unguarded expectations that only pass when the donor's current hosted pack exists. Move those cases to the owning pack root, replace them with fixture-pack setup, or gate them explicitly before staging the extract.
   - Remove or rewrite donor-specific retained artifacts, donor-only trace lineage, or donor-pack assumptions from shared `core/**` surfaces before staging the extract.
   - Keep the minimal portable root shell needed for governed lookup coherence, but do not treat donor root policy or donor pack roots as part of the reusable shared-core payload.
3. Stage the engineering extract from the donor.
   - Prefer `cd core/python && uv run watchtower-core pack extract-core --output-root <path> --overwrite --format json`.
   - Do not substitute `watchtower-core pack export` for this step; export is the customer-safe release path and intentionally strips engineering surfaces such as shared tests.
   - Treat a failed extract as a donor shared-core problem first, not as a signal to hand-edit the staged output blindly.
4. Apply the extract into the recipient.
   - Prefer `cd core/python && uv run watchtower-core pack apply-core --source-root <extract-root> --write --format json` in the recipient repository instead of a raw copy command.
   - Keep the recipient root shell authoritative unless the task explicitly includes root-shell reconciliation too.
   - The apply step should replace governed shared-core content while preserving recipient-local `.venv`, caches, and similar local scratch surfaces.
   - Treat live recipient hosted-pack registry entries and `core/python` workspace registrations as recipient-local environment state that should be rehydrated after the donor-neutral extract is applied. Do not let donor-specific pack wiring replace those local surfaces during refresh.
   - Ignore stale recipient-local pack registrations that no longer point at live local manifests or workspace roots instead of preserving dead donor residue.
5. Bootstrap the recipient pack into the refreshed shared core.
   - Run `cd core/python && uv run watchtower-core pack bootstrap --pack-settings-path <recipient-pack-settings> --replace-hosted-packs --write --sync-extra dev --format json` unless the recipient intentionally needs a different extra set.
   - `apply-core` may already rehydrate the recipient's live pack registry and workspace metadata, but bootstrap remains the authoritative step for exact shared-pack replacement, shared validation, workspace sync, and pack-local `sync all`.
   - Expect the normal bootstrap path to rebuild both the shared discovery indexes and the recipient pack's declared `sync all` slice when the pack publishes that target.
   - Use `--no-sync-workspace` only when a fixture or staged environment intentionally needs deferred sync, then follow immediately with the explicit `uv sync` command, the recipient `watchtower-core <namespace> sync all --write --format json` pass when declared, and `watchtower-core pack validate`.
6. Validate the refreshed recipient state.
   - Confirm the donor extract already passed engineering-core readiness.
   - Run the recipient validation baseline, targeted pack-contract validation, and any repo-local workspace validation required by the active repository contract.
   - Confirm lingering donor hosted-pack registry entries, workspace sources, stale lockfiles, donor-only records, and donor-only traceability joins are gone.
   - If recipient validation fails because shared-core tests or docs still assert donor-pack validators, donor workflows, or donor tracking surfaces directly, treat that as donor shared-core drift. Fix the donor shared core, restage the extract, and reapply instead of carrying a recipient-only cleanup patch.
   - Treat any shared-core test failure caused by a missing live donor pack root as donor shared-core drift too. Shared-core suites must not require the donor repository's internal pack layout unless the scenario is explicitly pack-owned or explicitly gated.
   - When changing or hardening this workflow itself, rerun the full extract, apply, and bootstrap cycle at least once more and confirm the second pass lands on the same final recipient state apart from expected transient runtime residue.
7. Close the workflow surfaces in the same change.
   - Update command docs, workflow docs, standards, and governed indexes when the shared-core extract or bootstrap contract changed materially.
   - Record whether the fix belonged in the donor shared core, the recipient repository, or both.

## Data Structure
- Donor and recipient role map
- Extract contract and bootstrap contract used
- Donor-side portability blockers and their resolution
- Recipient bootstrap inputs and validation results
- Shared docs, workflow, and governed-artifact surfaces updated in the same change

## Outputs
- A repeatable donor-side engineering shared-core extract flow
- A recipient-side bootstrap sequence that reloads the local hosted pack cleanly after shared-core refresh
- A refresh path that keeps donor-neutral shared core separate from recipient-local hosted-pack environment state
- Updated workflow, command, and standards guidance for future shared-core refresh requests
- Validation evidence or command results showing the refreshed path worked

## Done When
- Shared `core/` can be refreshed from donor to recipient without manual reasoning through donor pack residue each time.
- The donor extract path and recipient bootstrap path are both documented and executable.
- Donor-only hosted-pack wiring, retained artifacts, and donor-only trace lineage no longer survive the refresh.
- Shared-core tests, docs, and workflow references that survive engineering extract stay pack-neutral and derive pack-aware expectations from the active pack contract.
- Future requests can route directly to this workflow instead of improvising from generic pack-integration guidance.
