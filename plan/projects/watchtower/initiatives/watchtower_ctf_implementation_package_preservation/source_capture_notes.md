# Source Capture Notes

## Capture Summary

- `source_root`: `/home/j/mvp_reference/CTF_implementation`
- `initiative_root`: `/home/j/WatchTowerPlan/plan/projects/watchtower/initiatives/watchtower_ctf_implementation_package_preservation`
- `capture_timestamp_utc`: `2026-03-27T05:25:10Z`
- `source_file_count`: `62`
- `stored_file_count`: `62`
- `transformed_mirror_root`: `source_snapshot/CTF_implementation/`

## Mirror Policy

- every non-JSON source file is copied byte-for-byte to `source_snapshot/CTF_implementation/<same-relative-path>`
- every source `*.json` file is copied byte-for-byte to `source_snapshot/CTF_implementation/<same-relative-path>.raw`
- the transformed mirror is frozen after capture; later corrections must happen in canonical initiative docs or through an explicit recapture pass rather than by editing mirrored files in place
- raw source `*.json` files are intentionally not stored under the initiative root because initiative artifact validation scans recursive JSON paths and raw donor indexes would be misclassified as governed plan artifacts

## Section Counts

| Section | File Count |
|---|---|
| `00_context` | `10` |
| `01_capability_map` | `3` |
| `02_phases` | `8` |
| `03_workflows` | `3` |
| `04_contracts` | `15` |
| `05_research` | `2` |
| `06_standards` | `4` |
| `07_guides` | `3` |
| `08_tracking` | `5` |
| `README.md` | `1` |
| `indexes` | `8` |

## Validation Inputs

- `source_original_inventory.txt` is the sorted source-relative file list
- `source_stored_inventory.txt` is the sorted stored-relative file list after the `.json.raw` transform
- `source_sha256.tsv` stores `sha256`, `original_relative_path`, and `stored_relative_path` columns for every mirrored file
- `source_coverage_matrix.md` accounts for every source file and names the canonical initiative surface that absorbs or references it
- restored JSON files can be reconstructed losslessly by stripping the trailing `.raw` suffix from mirrored JSON paths
