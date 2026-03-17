# Plan Artifact Index Runtime Foundation Decision Notes

## Summary
- The first artifact-index slice will publish one authoritative pack-wide artifact catalog at `plan/.wt/artifact_index.json`.
- The slice will treat current live plan artifacts and aggregate indexes as the initial indexed population; frozen `docs/planning/**` history remains out of scope under the hard-cutover decision.
- The legacy `challenge_id`, `source_platform`, and `source_event` fields should be removed from the generic artifact-index contract in favor of neutral provenance fields that do not reintroduce old domain leakage.
