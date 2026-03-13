# Initiative Closeout Workflow

## Purpose
Use this workflow to mark one traced initiative as completed, superseded, cancelled, or abandoned while keeping the traceability index, initiative coordination view, and mirrored family trackers aligned.

## Use When
- A traced initiative has reached a terminal outcome that should be explicit and durable.
- The initiative view, family trackers, and unified traceability index need to agree on the same initiative outcome.
- A task needs a closeout phase that goes beyond commit creation or ordinary handoff review.

## Inputs
- Scoped initiative-closeout brief
- Target `trace_id`
- Intended terminal initiative status
- Closure reason and optional replacement trace
- Current linked task state, validation evidence, and planning surfaces
- Internal standards and canonical references applied

## Additional Files to Load
- [initiative_closeout_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_closeout_standard.md): defines the allowable initiative end states and the mirrored surfaces that must stay aligned.
- [traceability_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/traceability_standard.md): requires closeout to preserve explicit trace links rather than relying on prose-only state.
- [initiative_tracking_standard.md](/home/j/WatchTowerPlan/docs/standards/governance/initiative_tracking_standard.md): defines the derived initiative surfaces that must stay aligned with the terminal closeout state.
- [watchtower_core_closeout_initiative.md](/home/j/WatchTowerPlan/docs/commands/core_python/watchtower_core_closeout_initiative.md): documents the command surface that performs the closeout mutation and derived-surface rebuild.

## Workflow
1. Confirm the closeout boundary.
   - Resolve the target `trace_id`.
   - Confirm which PRDs, decisions, designs, plans, tasks, contracts, or evidence surfaces belong to that trace.
2. Check readiness for terminal closeout.
   - Inspect linked task state and any known downstream validation or acceptance gaps.
   - Run or review `watchtower-core validate acceptance --trace-id <trace_id>` when the trace publishes acceptance or evidence surfaces.
   - Decide whether any remaining open work blocks closeout or must be explicitly allowed as an exception.
   - Use an explicit acceptance-exception override only when the validation gap is intentional and should remain visible at closeout.
3. Record the initiative outcome.
   - Set the terminal initiative status.
   - Record `closed_at`, `closure_reason`, and `superseded_by_trace_id` when required.
   - Keep initiative outcome separate from artifact lifecycle `status`.
4. Refresh human and machine mirrors.
   - Update the traceability index entry.
   - Refresh the initiative index and initiative tracker that project current initiative status.
   - Refresh the PRD, decision, and design trackers that mirror initiative status.
5. Validate the closeout result.
   - Re-run the narrowest meaningful traceability and schema checks for the touched surfaces.
   - Ensure the closeout state is explicit in the machine-readable traceability layer, the initiative view, and the mirrored family trackers.

## Data Structure
- Target trace ID
- Intended terminal initiative status
- Closure metadata
- Open-task exception list when present
- Updated traceability surface
- Updated initiative coordination surfaces
- Updated family trackers

## Outputs
- Updated traceability entry with initiative closeout metadata
- Updated initiative index and initiative tracker that mirror the terminal initiative state
- Updated PRD, decision, and design trackers that mirror initiative status
- A short record of any allowed open-task or validation exceptions that remained at closeout

## Done When
- The target trace has a terminal initiative status recorded explicitly.
- The traceability index, initiative view, and mirrored family trackers agree on the current initiative outcome.
- Any remaining open-task or acceptance-validation exception is explicit rather than implied.
