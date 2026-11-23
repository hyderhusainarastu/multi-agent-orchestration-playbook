# Resume runbook

For long runs that crash, hit a rate limit, or get closed mid-way. Goal: finish the run without redoing finished work and without hiding what was lost. A fill-in copy is in `templates/HOW-TO-RESUME.md`.

## Steps

1. **Liveness check.** Is a writer still active? Look for a live process, a lock file, or output files whose modification time is still changing. If any writer may be active, stay read-only: observe, do not launch.
2. **Done/partial map from disk only.** For each stage, list items and mark each one:
   - done: the output file exists, parses, and appears in the stage log.
   - partial: a file exists but does not parse, or has no log line.
   - missing: nothing on disk.
   Do not trust chat history or an agent's summary. Write the map to `status/resume-map.json`.
3. **Snapshot before relaunch.** Copy the run folder to a dated snapshot. A relaunch that goes wrong must be undoable.
4. **Gap-only relaunch.** Build an explicit id list of missing and partial items, check it with `tools/shard_coverage_check.py` against the full list, and launch only those. Never rerun done items.
5. **Orphaned partials.** Partial outputs with no log line are orphans. Move them to `orphaned/` and list them in the run report. Do not merge them silently, and do not delete them.
6. **Name gaps instead of passing.** If an item cannot be finished, it stays in the gap list of the final report with the reason. A run with named gaps is honest; a run that reports success over gaps is not.
7. **Loop caps.** Track four counters in `state.json`:
   - rounds (full plan, execute, verify cycles)
   - secondary loops (fix-and-recheck loops inside a round)
   - chain depth (agent spawns agent spawns agent)
   - hops (hand-offs between roles for one item)
   Run `python3 tools/check_caps.py status/state.json` before every relaunch. Exit code 3 means a cap is reached: stop and escalate to a human with the gap list and the logs. Do not raise a cap on your own.

## Atomic promote

Write results to `tmp/<owner>/` first and run the checks there. Promote with a single rename into the final folder only when the checks pass. A crash then leaves either the old result or the new one, never half of each.

## Checkpoints

After each stage, write one status file: stage, items_in, items_out, time, tool and model versions. Keep it small. It is what the next resume reads first.

## Do not

- Relaunch while a writer may be live.
- Edit state by hand to make a check pass.
- Treat an empty agent result as done.
