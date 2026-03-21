# `core/docs/templates/pack`

## Description
`This directory contains the starter templates for creating or externalizing a hosted pack. Use these files together with the generic README, workflow, and routing templates in core/docs/templates/ when scaffolding a new pack root.`

## Files
| Path | Description |
|---|---|
| `core/docs/templates/pack/README.md` | Describes the hosted-pack starter template set and how it fits with the generic repository templates. |
| `core/docs/templates/pack/pack_registry_entry_template.json` | Template snippet for the shared `pack_registry.json` entry that registers one hosted pack with the host runtime. |
| `core/docs/templates/pack/pack_settings_template.json` | Template for the pack-owned `pack_settings.json` load root under `<pack>/.wt/manifests/`. |
| `core/docs/templates/pack/pack_runtime_manifest_template.json` | Template for the pack-owned `pack_runtime_manifest.json` host contract under `<pack>/.wt/manifests/`. |
| `core/docs/templates/pack/pack_schema_catalog_template.json` | Template for the pack-owned schema catalog under `<pack>/.wt/registries/`. |
| `core/docs/templates/pack/pack_validation_suite_registry_template.json` | Template for the pack-owned validation suite registry under `<pack>/.wt/registries/`. |
| `core/docs/templates/pack/pack_validator_registry_template.json` | Template for the pack-owned validator registry under `<pack>/.wt/registries/`. |
| `core/docs/templates/pack/pack_note_schema_template.json` | Template for a minimal pack-local note schema under `<pack>/.wt/schemas/interfaces/packs/`. |
| `core/docs/templates/pack/pack_note_artifact_template.json` | Template for a minimal pack-local note artifact under `<pack>/.wt/work_items/`. |
| `core/docs/templates/pack/pack_python_pyproject_template.toml` | Template for the pack-owned Python package metadata file under `<pack>/python/pyproject.toml`. |
| `core/docs/templates/pack/pack_package_init_template.py` | Template for `<pack>/python/src/watchtower_<pack>/__init__.py`. |
| `core/docs/templates/pack/pack_integration_module_template.py` | Template for `<pack>/python/src/watchtower_<pack>/integration.py` exporting `PACK_INTEGRATION`. |
| `core/docs/templates/pack/pack_namespace_command_reference_template.md` | Template for the pack-owned namespace command page under `<pack>/docs/commands/core_python/`. |

## Notes
`Pair this starter set with core/docs/templates/readme_template.md, core/docs/templates/workflow_template.md, and core/docs/templates/routing_table_template.md when a new pack also needs local README.md files or workflow docs.`
