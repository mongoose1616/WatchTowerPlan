# `docs/references`

## Description
`This directory contains working references for external standards, frameworks, specifications, and published guidance that inform this repository. Each reference should include verified canonical upstream links, a dense quick-reference section, and an explicit local mapping to current repository surfaces or clearly marked future-adoption areas. Do not place repo-native standards or purely local reference notes in this directory.`

## How To Use This Directory
- Start with the reference file that matches the external topic, not with a broad repo scan.
- Use `watchtower-core query references --query <topic>` when you want the governed reference lookup surface instead of browsing the directory manually.
- Use `watchtower-core query references --repository-status <candidate_future_guidance|supporting_authority|active_support>` when you need only the current maturity slice instead of the full corpus.
- Treat these files as supporting lookup artifacts. Enforceable local policy still belongs in `docs/standards/**` and executable procedure still belongs in `workflows/**`.
- Use the `Current Repository Status` and `Current Touchpoints` sections inside each reference to tell whether the topic is active local support, supporting authority for an existing standard, or only candidate future guidance.
- Treat `Current Touchpoints` as the authoritative list of live repo-local touchpoints. Generic backlinks in `References` are only supporting navigation and should not be read as active local adoption.
- Re-check the canonical upstream links before tightening local policy for version-sensitive topics such as toolchains, security frameworks, and data-contract formats.

## Current High-Signal Areas
- `active_support`: front matter, GitHub collaboration, and the narrow reference topics that directly support live command, design, or collaboration behavior.
- `supporting_authority`: naming and IDs, data-contract formats, schema governance, documentation templates, decision-capture guidance, Python workspace tooling, and agent or workflow authoring.
- `candidate_future_guidance`: supply-chain attestations, telemetry, SQLite-backed state, AI governance, and security assessment frameworks.

## Notes
- Reference files follow the stable `<topic>_reference.md` naming pattern.
- Prefer `watchtower-core query references` when you know the topic but not the exact filename.
- Keep this README focused on orientation. Topic details belong in the individual reference files.

## Files
| Path | Description |
|---|---|
| `docs/references/README.md` | Describes the purpose of the external references directory and the fastest ways to find topic-specific references. |
| `docs/references/AGENTS.md` | Defines directory-specific rules for authored external reference documents. |
| `docs/references/agent_workflow_authoring_reference.md` | Working reference for efficient workflow-module authoring for agents and LLM-oriented tasks. |
| `docs/references/json_schema_2020_12_reference.md` | Working reference for the JSON Schema version used across governed machine-readable artifacts. |
| `docs/references/uv_reference.md` | Working reference for the Python workspace package and environment toolchain. |
| `docs/references/pytest_reference.md` | Working reference for the canonical Python test runner used in the workspace baseline. |
| `docs/references/mypy_reference.md` | Working reference for static typing guidance used by the Python workspace. |
| `docs/references/ruff_reference.md` | Working reference for linting and formatting policy used by the Python workspace. |
