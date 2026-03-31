# `core/docs/standards/engineering`

## Description
`This directory contains engineering standards that govern code, automation, tooling, testing, style, and project layout for this repository. Use it for normative engineering rules that should shape repository implementation and contributor behavior.`

## Files
| Path | Description |
|---|---|
| `core/docs/standards/engineering/README.md` | Describes the purpose of the engineering standards directory and indexes the standards stored here. |
| `core/docs/standards/engineering/cli_help_text_standard.md` | Defines the minimum detail, examples, and usability expectations for repository CLI help text. |
| `core/docs/standards/engineering/core_host_pack_python_boundary_standard.md` | Defines the required split between reusable core, host composition, and pack-native Python ownership. |
| `core/docs/standards/engineering/domain_pack_authoring_standard.md` | Defines the pack-owned root shape and authoring rules for hosted packs. |
| `core/docs/standards/engineering/engineering_best_practices_standard.md` | Defines repository-specific engineering best practices for implementation, validation, and synchronized human or machine updates. |
| `core/docs/standards/engineering/git_commit_standard.md` | Defines the repository-standard Git commit message policy for human and assistant contributors. |
| `core/docs/standards/engineering/git_workflow_standard.md` | Defines repository-standard local git workflow behavior including branch naming, lifecycle, and sync expectations. |
| `core/docs/standards/engineering/hosted_pack_integration_standard.md` | Defines the minimum shared and pack-owned surfaces a hosted pack must satisfy before integration. |
| `core/docs/standards/engineering/performance_benchmarking_standard.md` | Defines the deliberate fail-closed benchmarking contract for reusable-core performance measurement and retained benchmark evidence. |
| `core/docs/standards/engineering/runtime_telemetry_standard.md` | Defines the baseline local runtime telemetry contract for command timing, error tracing, and pack-local telemetry sinks. |
| `core/docs/standards/engineering/python_code_design_standard.md` | Defines the authoritative Python code design philosophy, naming rules, and consolidation rules for `core/python/`. |
| `core/docs/standards/engineering/python_workspace_standard.md` | Defines the standard Python workspace layout, environment, and onboarding contract under core/python. |
| `core/docs/standards/engineering/repository_portability_standard.md` | Defines how shared core and hosted packs must be scrubbed for donor-neutral bootstrap and customer-safe release. |
