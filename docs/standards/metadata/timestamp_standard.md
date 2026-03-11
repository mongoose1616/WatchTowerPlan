---
id: "std.metadata.timestamp"
title: "Timestamp Standard"
summary: "This standard defines the canonical timestamp field names and UTC timestamp format used by governed documents and machine-readable artifacts in this repository."
type: "standard"
status: "active"
tags:
  - "standard"
  - "metadata"
  - "timestamp"
owner: "repository_maintainer"
updated_at: "2026-03-11T06:00:00Z"
audience: "shared"
authority: "authoritative"
---

# Timestamp Standard

## Summary
This standard defines the canonical timestamp field names and UTC timestamp format used by governed documents and machine-readable artifacts in this repository.

## Purpose
Keep time-bearing metadata predictable enough for validation, indexing, traceability, and generated output without letting each artifact family invent its own timestamp shape or timezone policy.

## Scope
- Applies to governed timestamp fields in document front matter, document metadata sections, control-plane artifacts, and generated machine-readable outputs.
- Covers canonical field names, UTC formatting rules, and when different timestamp fields should be used.
- Does not define business-specific calendar-date fields such as `effective_date` when a document family intentionally tracks a date without a time of day.

## Use When
- Adding or renaming a timestamp field in a governed document or machine-readable artifact.
- Defining validation rules for front matter or control-plane artifact timestamps.
- Reviewing whether a timestamp field is ambiguous, inconsistent, or using the wrong timezone or field name.

## Related Standards and Sources
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md): companion standard that constrains this standard's boundary, validation, or change-control expectations.
- [rfc_3339_timestamp_reference.md](/home/j/WatchTowerPlan/docs/references/rfc_3339_timestamp_reference.md): local reference surface for the external or canonical guidance this standard depends on.
- [rfc_9557_timestamp_extensions_reference.md](/home/j/WatchTowerPlan/docs/references/rfc_9557_timestamp_extensions_reference.md): local reference surface for the external or canonical guidance this standard depends on.

## Guidance
- Use UTC for governed mutable timestamps across repository docs, control-plane artifacts, and generated outputs.
- Serialize governed timestamps as RFC 3339 date-time strings with a trailing `Z`.
- Use the repository baseline form `YYYY-MM-DDTHH:MM:SSZ`.
- Do not store governed mutable timestamps as local time, offset timestamps such as `-05:00`, or naive timestamps with no timezone.
- Do not use a generic field such as `date`, `updated`, `last_updated`, or `last_synced` when one of the canonical timestamp fields fits.
- Use `updated_at` for the last meaningful content update of a durable document or artifact.
- Use `recorded_at` for evidence or event-style records that capture when a result or observation was recorded.
- Use `generated_at` only when an artifact needs a distinct generation or build timestamp in addition to `updated_at` or `recorded_at`.
- Use a scoped `*_at` field such as `github_synced_at` only when a narrower integration-specific timestamp meaning is required and none of the canonical generic fields fit.
- Prefer one canonical timestamp field per meaning. Do not store duplicate synonymous timestamp fields in the same artifact.
- Reuse the shared UTC timestamp schema fragment under `core/control_plane/schemas/common/` instead of open-coding separate timestamp regexes in each schema.
- Reserve date-only fields for true calendar semantics such as an effective date or review date, and standardize those separately when they become governed.

## Structure or Data Model
| Field | Use | Notes |
|---|---|---|
| `updated_at` | Durable document or artifact metadata | Use for the last meaningful content change. |
| `recorded_at` | Evidence or event-style records | Use when the timestamp captures when a result or observation was recorded. |
| `generated_at` | Generated artifact build metadata | Use only when generation time is distinct from content update or evidence-record time. |
| `github_synced_at` | Integration-specific sync metadata | Use only for the last successful GitHub sync of a local task record. |

## Examples
- Front matter on a governed reference document should use `updated_at: "2026-03-09T05:23:35Z"`.
- A PRD, decision index, or traceability index entry should carry `updated_at` in the same UTC form.
- A validation-evidence artifact should use `recorded_at` rather than `updated_at` when the timestamp describes when the evidence was captured.
- A future generated export could carry both `updated_at` and `generated_at` if those two meanings differ materially.

## Operationalization
- `Modes`: `schema`
- `Operational Surfaces`: `core/control_plane/schemas/common/`

## Validation
- Governed timestamp fields should validate as RFC 3339 date-time strings in UTC with a trailing `Z`.
- Reviewers should reject alternate mutable timestamp field names when a canonical field already exists for the same meaning.
- Reviewers should reject local-time or offset timestamps for governed mutable metadata unless a narrower standard explicitly allows them.
- Shared schema fragments and live examples should stay aligned with this standard when timestamp rules change.

## Change Control
- Update this standard when the repository changes its canonical timestamp field set or timestamp serialization policy.
- Update affected schemas, templates, live artifacts, and companion standards in the same change set when timestamp rules change materially.
- Record any future exception for non-UTC or richer timestamp encoding in a narrower artifact-family standard rather than weakening this baseline.

## References
- [front_matter_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/front_matter_standard.md)
- [naming_and_ids_standard.md](/home/j/WatchTowerPlan/docs/standards/metadata/naming_and_ids_standard.md)
- [schema_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/schema_standard.md)
- [validation_evidence_standard.md](/home/j/WatchTowerPlan/docs/standards/data_contracts/validation_evidence_standard.md)
- [rfc_3339_timestamp_reference.md](/home/j/WatchTowerPlan/docs/references/rfc_3339_timestamp_reference.md)
- [rfc_9557_timestamp_extensions_reference.md](/home/j/WatchTowerPlan/docs/references/rfc_9557_timestamp_extensions_reference.md)

## Notes
- This repository uses a narrower subset of RFC 3339 than the full standard: UTC only, trailing `Z`, and whole-second precision.
- `generated_at` is approved as a reserved field name even if it is not yet widely used.

## Updated At
- `2026-03-11T06:00:00Z`
