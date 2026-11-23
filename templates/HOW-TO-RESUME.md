# HOW TO RESUME

Put a copy of this file in the run folder. Fill the brackets when the run starts.

1. Check liveness: is any writer still active (process, lock file, fresh mtime under `[write roots]`)? If yes, stay read-only and wait.
2. Read only on-disk records: `[run]/state.json`, `[run]/logs/`, and the output folders. Do not trust chat history.
3. Build the done/partial map per stage: an item is done only if its output file exists, parses, and is listed in the stage log.
4. Snapshot before relaunch: `cp -r [run] [run].snapshot-<date>`.
5. Relaunch gaps only, using an explicit id list from `shard_coverage_check.py`. Never rerun finished items.
6. Disclose orphaned partials (outputs with no log line) in the run report. Move them to `[run]/orphaned/`; do not merge silently.
7. Check caps: `python3 tools/check_caps.py [run]/state.json`. Exit 3 means stop and ask a human.
8. Name every remaining gap in the final report. Do not pass a run with gaps.

Stage list: [stage 1, stage 2, ...]
Human contact for escalation: [role or channel]
