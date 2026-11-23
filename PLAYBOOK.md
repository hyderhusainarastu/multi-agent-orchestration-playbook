# Playbook

Rules first, rationale second. Each rule is short on purpose. Where a rule has code, it lives in `tools/`.

Contents: 1 Moderator loop, 2 Tier routing, 3 Order of work, 4 Roles, 5 Ownership, 6 Frozen contracts, 7 Logs, status, tmp, 8 Never verify by revert, 9 Shard coverage, 10 Nulls, checkpoints, promote, 11 Retry cap, 12 No mid-run messages, 13 Data by file, 14 Numbers by script, 15 Facts need sources.

## 1. Moderator-only main loop

**Rule.** The main session does five things: scout, plan, route, review, report. It does not build, fix or bulk-read.

- The moderator writes briefs and reads results. Substantive work goes to sub-agents or scripts.
- The moderator keeps its own context small: it reads counts, paths and defect lists, not raw output.
- Parallelize everything that is independent. Serialize only where one stage needs another's output.

**Why.** A main session that also builds fills its context with detail, loses the plan, and starts approving its own work. Keeping it thin keeps it honest.

<!-- cc-only -->
In Claude Code the moderator is the main conversation and sub-agents are defined in `.claude/agents/`. A workflow script can fan out stages; the moderator reviews its summary, not its transcript.
<!-- /cc-only -->

## 2. Tier routing

**Rule.** Route every task to the smallest tier that can do it. Never run above the tier the task needs.

| Tier | Use for | Do not use for |
|---|---|---|
| small | mechanical work: census, checksums, renames, metadata pushes, format conversion | judgement, synthesis |
| medium | harvesting, building, auditing, review, test writing | final sign-off on a hard call |
| large | synthesis across sources, judging plans, final adversarial verification | bulk or repetitive work |

Example model families per tier, as of 2026-11-23. These are family names only; check each vendor's current lineup before use.

| Vendor | small | medium | large |
|---|---|---|---|
| OpenAI | GPT mini / nano class | GPT standard class | GPT flagship / reasoning class |
| Anthropic | Haiku family | Sonnet family | Opus family |
| Google | Gemini Flash-Lite / Flash | Gemini Flash / Pro | Gemini Pro with extended thinking |
| Local open-weight | roughly 3B to 8B (Llama, Qwen, Mistral small, Gemma) | roughly 14B to 32B | 70B and up, or a hosted large model |

**Record exact model IDs and versions in the run log** (in `logs/`, not in docs or `AGENTS.md`). Families change names and behaviour; the log is what makes a run reproducible. A run log line looks like: `stage=verify tier=large model=<exact id and version> date=<date>`.

**Why.** Cost and speed fall sharply by tier, and a small model is often more reliable on a mechanical task than a large one that "improves" it.

## 3. Order of work

**Rule.** Follow this order and never skip ahead.

1. **Understand.** Audit and harvest what exists. Measure, do not guess.
2. **Independent planners.** Two or three planners, each blind to the others.
3. **Judge.** Compares plans against the goal and picks or merges one.
4. **Critic.** Attacks the chosen plan; lists likely failures.
5. **Moderator review.** A human or the main session accepts, edits or rejects.
6. **Execute.** Builders work inside their write roots.
7. **Adversarial verify.** An agent that did not build tries to break the result.
8. **Ship.** Only after verification, and only on instruction.

**Why.** Independent plans expose assumptions. Plans written after seeing another plan converge and share its blind spots. Skipping from understanding to execution is the most common source of rework.

## 4. Role separation

**Rule.** The agent that made a thing never approves it.

| Role | Does | Never |
|---|---|---|
| Builder | makes the artifact inside its write root | reviews or ships its own work |
| Reviewer | reads and writes defect reports | edits the artifact |
| Designer | sets structure, interfaces and contracts | builds the full artifact |
| Fixer | applies the smallest fix for each defect | judges whether the fix is enough |
| Verifier | attacks the result, runs the checks | knows how it was built |

A defect report uses one line: `owner - file:line - what - fix` (`templates/defect-report.md`). After a fix, the reviewer re-checks. The same model family can play several roles, but never on the same artifact.

**Why.** A model reviewing its own output shares its blind spots. A fresh context with no memory of the build is the cheapest independent check there is.

## 5. Write roots and single-owner files

**Rule.** Every writable path has exactly one owner and lives under one write root. All other paths are read-only.

Example table (full template: `templates/ownership-table.md`):

| Path | Owner | Write root | Everyone else |
|---|---|---|---|
| `work/stage-a/` | builder A | `work/stage-a/` | read-only |
| `work/stage-b/` | builder B | `work/stage-b/` | read-only |
| `contracts/` | moderator | `contracts/` | read-only |
| `reports/` | verifier | `reports/` | read-only |

- Put the write root in the first lines of the brief. Name what is off limits, not just what is allowed.
- A change needed outside your write root becomes a defect report to the owner.
- Two writers never share a file. Parallel agents each get their own folder or worktree.
- If a project belongs to someone else or is live (being edited by another session), it is read-only for every agent.

**Why.** Merge conflicts between agents are silent and hard to diagnose. Ownership makes every file's history one agent long.

## 6. Frozen stage contracts

**Rule.** Before parallel work starts, write each stage's contract and freeze it.

A contract lists: inputs (paths, shape), outputs (paths, shape), invariants, the counts that must reconcile, and the owner. Once frozen, only the moderator changes it, through a dated change note. Builders code to the contract; reviewers check against it.

- Freeze identifiers and file formats first. Late changes to those cost the most.
- A builder who finds the contract wrong stops and files a defect against the contract. It does not work around it.

**Why.** Stages built in parallel against a moving interface fail only at integration, which is the most expensive place to learn it.

## 7. Logs, status and tmp

**Rule.** Keep three kinds of file in three places and never mix them.

| Kind | Meaning | Rule |
|---|---|---|
| `logs/` | evidence of what happened | append only; never rewritten |
| `status/` | current truth | small files, overwritten, owned by one writer |
| `tmp/` | scratch | per-owner subfolders; deletable; never cited |

If a claim in a report cannot be traced to `logs/` or a source, it does not ship.

**Why.** When logs and status are the same file, a resume cannot tell what happened from what is claimed now.

## 8. Never verify by revert

**Rule.** Do not confirm that a fix works by undoing it and watching the problem return.

Rationale (anonymised): in one project a reviewer tried to prove a fix mattered by reverting it in the working tree. The revert silently overwrote unrelated edits another agent had made to the same files, and the fix itself was lost in the confusion. The check "proved" nothing and cost an afternoon of reconstruction.

Instead:

- Write a failing test or check before the fix, and show it passes after.
- If you must compare, work on a copy or a separate worktree, never the live tree.
- Verify on a snapshot (`cp -r`), then discard the snapshot.

## 9. Shard coverage by explicit lists

**Rule.** Coverage is proved with a set difference over explicit ids, not by comparing counts.

Two shards of 50 and 50 "cover" 100 items only if no item is in both and none is missing; a count of 100 hides one duplicate plus one gap.

```sh
python3 tools/shard_coverage_check.py --expected ids.txt shard-a.txt shard-b.txt
```

It prints gaps, duplicates and extras and exits 1 on any. Run it after sharding and again after the shards finish (against the ids actually written). Exit 0 is required to proceed.

## 10. Nulls, checkpoints and atomic promote

**Rule.** A null or empty agent result is a failure. Work is checkpointed and promoted atomically.

- Treat `null`, `""`, `[]` and a missing file as failed unless the contract says empty is valid.
- After every stage, write a checkpoint into `status/`: stage, items_in, items_out, tool and model versions.
- Write outputs to `tmp/<owner>/`, check them there, and promote with one rename into the final path. A crash leaves the old result or the new one, never a mix.
- Guard each stage with `guard_non_empty` (see `docs/silent-drop.md`).

## 11. Retry cap, then a failure brief

**Rule.** Retry a failed task at most twice. Then stop and write a failure brief.

A failure brief has: what was tried, the exact error or output, what was ruled out, and the smallest question that would unblock it. It goes to the moderator or a human. Loops carry hard caps (rounds, secondary loops, chain depth, hops) in `state.json`; `tools/check_caps.py` exits 3 at a cap, and a cap means escalate to a human, not raise the cap. Details: `docs/resume-runbook.md`.

**Why.** An agent that keeps retrying burns budget and often drifts into a different task than the one assigned.

## 12. Never message agents mid-run

**Rule.** Do not send follow-up messages to an agent that is running. Wait for its output file.

If the brief was wrong, let the run end (or stop it), fix the brief, and relaunch. Mid-run messages create results that no brief explains and no log reproduces.

## 13. Bulk data by file, never by agent echo

**Rule.** Data moves between stages as files. An agent never repeats a large payload in its reply.

- The brief names an input file and an output file. The reply reports counts and paths only.
- A stage that must pass 500 records writes 500 records to disk; the next stage reads the file and counts it.
- Anything an agent re-types can be shortened, reordered or "fixed" without notice. That is how silent drops start.

## 14. Never hand-count

**Rule.** Derive every number with a script, and say which script and which input.

Counts, totals, percentages, coverage figures and "N of M" statements in reports must come from code that anyone can rerun. If the number cannot be recomputed from files on disk, it does not go in the report. Write the command next to the number.

## 15. Facts need a source and a method

**Rule.** Never take a fact from model memory. Coordinates, DOIs, quotes, dates, statistics and names each carry a source and a method.

- Source: where it came from (file, URL, document, page).
- Method: how it was obtained (read from the source, computed by script, measured).
- A model may propose a candidate fact. A check against the source turns it into a fact.
- Unverified items stay labelled `unverified` and are never mixed into verified tables.
- For locations: record the coordinate system and the source of each coordinate. Never let a model supply coordinates from memory.

**Why.** Models state wrong DOIs, invented quotes and plausible coordinates with the same confidence as right ones.

## Quick checklist for a new run

1. Write the contract and ownership table; freeze them.
2. Pick tiers per stage; plan to log exact model IDs.
3. Independent plans, judge, critic, review.
4. Pilot any new method on a gold set and negative controls (`docs/pilot-before-scale.md`).
5. Execute with guards on every stage.
6. Check shard coverage; check caps.
7. Verify with a fresh agent. Fix. Re-verify with a fresh agent.
8. Report with counts from scripts, gaps named.
9. Ship only on instruction.
