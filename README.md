# multi-agent-orchestration-playbook

A short, opinionated playbook for people who run teams of AI agents: twelve rules, an `AGENTS.md` template you can drop into a project, and small tested helper scripts that enforce the rules that can be enforced by code.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## The 12 rules

1. **Moderator only.** The main session plans, routes, reviews and reports. Work goes to sub-agents or scripts.
2. **Tier by task.** Small models for mechanical work, medium for building and review, large for synthesis, judging and final verification. Never run above the tier a task needs.
3. **Plan before you act.** Understand, independent planners, judge, critic, moderator review, execute, adversarial verify, ship. No jumping from scouting to edits.
4. **No self-approval.** The agent that made a thing never signs it off. Reviewer, designer, fixer and verifier are separate roles.
5. **One owner per file.** Every writable path has exactly one owner and one write root. Everything else is read-only.
6. **Freeze contracts.** Stage inputs and outputs are written down and frozen before parallel work starts. Changes go through the owner.
7. **Guard silent drops.** Log item counts into and out of every stage. Throw when input is above zero and output is zero.
8. **Cover shards by list, not by count.** Prove coverage with a set difference over explicit ids: no gaps, no duplicates.
9. **Pilot before scale.** Score candidate methods on a small gold set and negative controls before any full run.
10. **Resume from disk, cap the loops.** Rebuild state from on-disk records, relaunch only the gaps, and stop at hard caps by escalating to a human.
11. **Data by file, numbers by script.** Bulk data moves through files, never through an agent repeating it back. Never hand-count: derive numbers with code.
12. **No facts from model memory.** Coordinates, DOIs, quotes and figures carry a source and a method, or they do not ship.

## Works with

| Surface | How | Status |
|---|---|---|
| Any shell with Python 3 | CLI: `tools/*.py` | tested 2026-11-23, Python 3.14.10 |
| Any shell with Node 20+ | CLI: `tools/guards.mjs` (library) | tested 2026-11-23, Node 24.22.3 |
| Claude Code | `AGENTS.md` imported by `CLAUDE.md` | not tested |
| Codex | reads `AGENTS.md` | not tested |
| Cursor | reads `AGENTS.md` | not tested |
| Gemini CLI | `GEMINI.md` imports `AGENTS.md` | not tested |
| Copilot | `.github/copilot-instructions.md` points to `AGENTS.md` | not tested |
| ChatGPT / Claude.ai / Gemini (chat) | paste `PROMPT.md`; see `docs/single-chat-mode.md` | not tested |

## Quick start

```sh
git clone https://github.com/hyderhusainarastu/multi-agent-orchestration-playbook
cd multi-agent-orchestration-playbook
python3 -m unittest discover -s tests -v   # offline
node --test tests/guards.test.mjs         # offline
```

To adopt the rules in your own project, copy `templates/AGENTS.md` to your repo root and edit the bracketed parts. In a chat window, paste `PROMPT.md` (or `PROMPT.short.md` into a custom-instructions field).

## Example

```sh
$ python3 tools/shard_coverage_check.py --expected examples/ids.txt examples/shard-a.txt examples/shard-b.txt
GAPS (1): item-004
DUPLICATES (1): item-002 (in shard-a.txt, shard-b.txt)
$ echo $?
1
```

## Map of the files

| Path | What it is |
|---|---|
| `PLAYBOOK.md` | The full rules, rules first and rationale second |
| `docs/silent-drop.md` | The silent-drop failure and its guard |
| `docs/pilot-before-scale.md` | Method scouting with a gold set, red team and skeptic |
| `docs/resume-runbook.md` | Liveness, done/partial map, gap-only relaunch, loop caps |
| `docs/single-chat-mode.md` | Running the stages by hand in one chat |
| `docs/framework-mapping.md` | Concepts mapped to common tools and frameworks |
| `templates/` | `AGENTS.md`, ownership table, brief header, defect report, resume note, JSON schemas |
| `tools/` | `guards.py`, `guards.mjs`, `shard_coverage_check.py`, `check_caps.py` |
| `tests/` | `unittest` (also pytest-compatible) and `node --test` suites |
| `PROMPT.md`, `PROMPT.short.md` | Paste-in versions for chat UIs |

## How it differs

LangGraph, CrewAI, the OpenAI Agents SDK and AutoGen are frameworks for building agent graphs. This repo is not a framework: it is a set of working rules plus guard scripts that sit beside whichever tool you use. Spec-style files such as `AGENTS.md` are the delivery format. The closest prior art is the general advice in vendor "building effective agents" guides; this playbook is narrower and more prescriptive about process controls (ownership, counts, caps, resume).

## Limits

- The helper scripts check what you give them. They cannot tell whether a stage's output is correct, only whether it is empty, duplicated or incomplete.
- Rules about tiers and roles are conventions. Nothing here enforces them in a tool.
- The framework table in `docs/framework-mapping.md` is a snapshot dated 2026-11-23. Verify against current docs.
- Only the scripts were run. No agent platform row above was exercised by the author, and no benchmark numbers are claimed.

## Related

- `gated-research-pipeline` - stage gates for research runs
- `deep-research-skill` - research waves with a saturation stop rule
- `hallucinated-citation-checker` - checks citations against sources
- `palimnote-agent-patterns` - the pattern catalog this belongs to

## Keywords

multi-agent, agent orchestration, AGENTS.md, subagents, planner judge critic, silent failure guard, resume long runs, model tiers, LLM workflow, context engineering

---
Part of palimnote-agent-patterns - more at https://github.com/hyderhusainarastu
