# Multi-agent operating rules

Drop this file at the repository root and edit the bracketed parts. Every other instruction file (CLAUDE.md, GEMINI.md, copilot instructions) should only point here.

## Roles and routing

- The main session is the **moderator**. It plans, routes work, reviews results and reports. It does not do bulk work itself.
- Route by task tier, never above what the task needs:
  - small: mechanical work (counting files, checksums, metadata updates).
  - medium: building, harvesting, auditing, review.
  - large: synthesis, judging, final adversarial verification.
- Record the exact model name and version used for each run in the run log.

## Order of work

1. Understand (audit, read, measure).
2. Independent planners write plans without seeing each other.
3. A judge compares them; a critic attacks the chosen plan.
4. The moderator reviews the plan.
5. Execute.
6. Adversarial verify by an agent that did not build.
7. Ship.

Never go from scouting straight to edits.

## Ownership

- Each writable path has one owner and one write root: [list in `ownership-table.md`]. Everything else is read-only.
- No self-approval. Reviewer, designer, fixer and verifier are separate roles.
- Stage contracts in [`contracts/`] are frozen before parallel work starts. Change them only through the moderator.
- Keep logs (evidence), status (current truth) and tmp (scratch) in separate folders. Never cite tmp.

## Guards

- Every stage logs `items_in` and `items_out`. Throw when in > 0 and out == 0.
- Prove shard coverage with an explicit id list and a set difference, not with counts.
- Bulk data moves by file. Agents reply with counts and paths, never with the data.
- Never hand-count. Derive every number with a script and say which one.
- Never take coordinates, DOIs, quotes or figures from model memory. Each carries a source and a method.
- Treat an empty or null agent result as a failure, not as "nothing found".
- Never verify a fix by reverting it.

## Loops and failures

- Retry a failed task at most [2] times, then write a failure brief and stop.
- Caps: rounds [3], secondary loops [2], chain depth [3], hops [6]. At a cap, escalate to a human.
- Do not message an agent mid-run. Wait for its output file.
- Resume from on-disk records only (see `HOW-TO-RESUME.md`). Relaunch gaps, not finished work.
- While another writer may be active, stay read-only.

## Pilot before scale

- Score any new method on a small gold set (recall) and negative controls (false positives) before a full run.
- An independent skeptic gives the verdict. Scale only on "scale".

## Git and attribution

- Commit with the repo-local identity [name / no-reply email].
- No AI attribution trailers in commits, pull requests or READMEs.
- Never push without an explicit instruction. Never commit secrets or local absolute paths.

## Done means

- Tests pass offline: `[test command]`.
- Counts in and out reconcile for every stage.
- Gaps are named, not hidden.
