# Initiative Closeout Workflow

## Purpose
Use this workflow to mark one traced initiative as completed, superseded, cancelled, or abandoned while keeping the traceability index and human planning trackers aligned.

## Use When
- A traced initiative has reached a terminal outcome that should be explicit and durable.
- Human planning trackers and the unified traceability index need to agree on the same initiative outcome.
- A task needs a closeout phase that goes beyond commit creation or ordinary handoff review.

## Inputs
- Scoped initiative-closeout brief
- Target `trace_id`
- Intended terminal initiative status
- Closure reason and optional replacement trace
- Current linked task state, validation evidence, and planning surfaces
- Internal standards and canonical references applied

## Workflow
1. Confirm the closeout boundary.
   - Resolve the target `trace_id`.
   - Confirm which PRDs, decisions, designs, plans, tasks, contracts, or evidence surfaces belong to that trace.
2. Check readiness for terminal closeout.
   - Inspect linked task state and any known downstream validation or acceptance gaps.
   - Decide whether any remaining open work blocks closeout or must be explicitly allowed as an exception.
3. Record the initiative outcome.
   - Set the terminal initiative status.
   - Record `closed_at`, `closure_reason`, and `superseded_by_trace_id` when required.
   - Keep initiative outcome separate from artifact lifecycle `status`.
4. Refresh human and machine mirrors.
   - Update the traceability index entry.
   - Refresh the PRD, decision, and design trackers that mirror initiative status.
5. Validate the closeout result.
   - Re-run the narrowest meaningful traceability and schema checks for the touched surfaces.
   - Ensure the closeout state is explicit in both the machine-readable traceability layer and the human-readable planning trackers.

## Data Structure
- Target trace ID
- Intended terminal initiative status
- Closure metadata
- Open-task exception list when present
- Updated traceability surface
- Updated planning trackers

## Outputs
- Updated traceability entry with initiative closeout metadata
- Updated planning trackers that mirror initiative status
- A short record of any allowed open-task or validation exceptions that remained at closeout

## Done When
- The target trace has a terminal initiative status recorded explicitly.
- The traceability index and human planning trackers agree on the current initiative outcome.
- Any remaining open-task or validation exception is explicit rather than implied.
