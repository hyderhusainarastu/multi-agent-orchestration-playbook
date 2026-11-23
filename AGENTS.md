# multi-agent-orchestration-playbook

A playbook of twelve rules for running teams of AI agents, an `AGENTS.md` template, and small helper scripts that guard stage counts, shard coverage and loop caps.

## Using this in your project

- Copy `templates/AGENTS.md` into your repo root and edit the bracketed parts. Read `PLAYBOOK.md` for the reasons.
- Guard each stage: import `tools/guards.py` (or `tools/guards.mjs`) and call `stage_log` then `guard_non_empty` after every stage.
- Check shard coverage: `python3 tools/shard_coverage_check.py --expected ids.txt shard-a.txt shard-b.txt`. Exit 0 ok, 1 gaps/duplicates/extras, 2 usage error.
- Check loop caps before a relaunch: `python3 tools/check_caps.py status/state.json`. Exit 0 ok, 3 cap reached (stop and ask a human), 2 bad input.
- Never hand-count; derive numbers with a script. Never take coordinates, DOIs or quotes from memory.
- Never edit outside your write root. Never approve your own work. Never message a running agent.
- Never add AI attribution trailers to commits or pull requests.
- Chat-only users: paste `PROMPT.md` and follow `docs/single-chat-mode.md`.

## Working on this repo

- Setup: none. Python 3.10+ and Node 20+ with no third-party packages.
- Test: `python3 -m unittest discover -s tests` and `node --test tests/guards.test.mjs` (both offline). `pytest -q` also works if installed.
- Do not write outside the repository. Keep `PLAYBOOK.md` at or under 450 lines, `templates/AGENTS.md` at or under 120, `PROMPT.md` at or under 6000 characters and `PROMPT.short.md` at or under 1400.
- Examples must stay synthetic. Numbers in examples are invented and labelled as such.
- No PROMPT.md exemption: this repo ships one.

<!-- cc-only -->
In Claude Code, the moderator is the main session; define builder, reviewer and verifier as separate sub-agents with distinct write roots.
<!-- /cc-only -->
